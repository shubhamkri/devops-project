FROM nginx:1.27-alpine AS production

COPY index.html /usr/share/nginx/html/index.html
COPY ../nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s \
    CMD wget -qO- http://localhost/health || exit 1
