from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time
import os
import redis
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DevOps Demo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["endpoint"])

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/appdb")


def get_redis():
    try:
        r = redis.from_url(REDIS_URL, socket_connect_timeout=2)
        r.ping()
        return r
    except Exception:
        return None


def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=2)
        return conn
    except Exception:
        return None


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(duration)
    return response


@app.get("/")
def root():
    return {"message": "DevOps Demo API", "version": "1.0.0", "status": "running"}


@app.get("/health")
def health():
    checks = {
        "api": "healthy",
        "redis": "healthy" if get_redis() else "unhealthy",
        "database": "healthy" if get_db() else "unhealthy",
    }
    overall = "healthy" if all(v == "healthy" for v in checks.values()) else "degraded"
    return {"status": overall, "checks": checks}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/items")
def list_items():
    r = get_redis()
    if r:
        cached = r.get("items")
        if cached:
            logger.info("Cache hit for items")
            import json
            return {"source": "cache", "items": json.loads(cached)}

    items = [
        {"id": 1, "name": "Item Alpha", "status": "active"},
        {"id": 2, "name": "Item Beta", "status": "active"},
        {"id": 3, "name": "Item Gamma", "status": "inactive"},
    ]

    if r:
        import json
        r.setex("items", 60, json.dumps(items))

    return {"source": "db", "items": items}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 1 or item_id > 3:
        raise HTTPException(status_code=404, detail="Item not found")
    items = {1: "Alpha", 2: "Beta", 3: "Gamma"}
    return {"id": item_id, "name": items[item_id], "status": "active"}
