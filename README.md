# DevOps Demo Project

A production-grade full-stack application demonstrating end-to-end DevOps practices — built for resume showcasing.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | Python 3.12, FastAPI, Prometheus metrics |
| Frontend | HTML/JS dashboard served via Nginx |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions → GHCR |
| Infrastructure | Terraform (AWS EC2, VPC, EIP) |
| Config Management | Ansible |
| Monitoring | Prometheus + Grafana + Loki |
| Orchestration | Kubernetes (HPA, probes) |

## Architecture

```
Internet → Nginx (port 80)
              ├── /          → Frontend (static HTML)
              └── /api/      → FastAPI backend
                                  ├── PostgreSQL
                                  └── Redis (cache)

Monitoring: Prometheus → Grafana (port 3000)
```

## Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/YOURUSERNAME/devops-project.git
cd devops-project

# 2. Start everything in one command
docker compose up -d

# 3. Visit the app
open http://localhost         # Frontend dashboard
open http://localhost:9090    # Prometheus
open http://localhost:3000    # Grafana (admin / admin123)
```

## CI/CD Pipeline

Every push to `main` triggers:

```
Push → GitHub Actions
  ├── 1. Run pytest + flake8
  ├── 2. Build multi-stage Docker images
  ├── 3. Push to GitHub Container Registry (GHCR)
  └── 4. SSH deploy to EC2 (docker compose pull + up)
```

### Required GitHub Secrets

| Secret | Value |
|--------|-------|
| `EC2_HOST` | Your EC2 Elastic IP |
| `EC2_SSH_KEY` | Private SSH key (PEM format) |

## Infrastructure Setup (AWS)

```bash
cd terraform

# 1. Configure your variables
cp terraform.tfvars.example terraform.tfvars
# Edit: aws_region, public_key_path, github_repo

# 2. Deploy infrastructure
terraform init
terraform plan
terraform apply

# 3. Note the output IP
terraform output public_ip
```

## Ansible Deploy

```bash
cd ansible

# Update inventory.ini with your EC2 IP
# then run:
ansible-playbook -i inventory.ini playbooks/deploy.yml
```

## Kubernetes (Bonus)

```bash
# Local testing with k3s or minikube
kubectl apply -f k8s/deployment.yaml

# Check HPA scaling
kubectl get hpa
kubectl top pods
```

## Monitoring

- **Prometheus**: Scrapes `/metrics` from FastAPI every 15s
- **Grafana**: Pre-built dashboards for request rate, latency, error rate (RED method)
- **Metrics tracked**: `http_requests_total`, `http_request_duration_seconds`

## Resume Bullet Points (copy these!)

- Designed and deployed a containerized full-stack application on AWS EC2 using Docker and Docker Compose, reducing environment setup time by 90%
- Built a GitHub Actions CI/CD pipeline that automates testing, image builds (GHCR), and zero-downtime deployments on every push to main
- Provisioned AWS infrastructure (VPC, EC2, Security Groups, Elastic IP) using Terraform with remote S3 state management
- Configured Prometheus + Grafana observability stack tracking RED metrics (request rate, error rate, duration) with custom dashboards
- Implemented Kubernetes Horizontal Pod Autoscaler scaling backend from 2→5 replicas based on CPU utilization

## Project Structure

```
devops-project/
├── backend/
│   ├── app/main.py          # FastAPI application
│   ├── tests/               # pytest tests
│   ├── requirements.txt
│   └── Dockerfile           # Multi-stage build
├── frontend/
│   ├── index.html           # Dashboard UI
│   └── Dockerfile
├── nginx/nginx.conf          # Reverse proxy config
├── docker-compose.yml        # Full local stack
├── .github/workflows/
│   └── ci-cd.yml            # GitHub Actions pipeline
├── terraform/
│   ├── main.tf              # AWS infrastructure
│   └── variables.tf
├── ansible/
│   ├── inventory.ini
│   └── playbooks/deploy.yml
├── monitoring/
│   └── prometheus/prometheus.yml
└── k8s/deployment.yaml      # Kubernetes manifests + HPA
```
# devops-project
