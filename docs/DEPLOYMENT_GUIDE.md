# CivicResolve Deployment Guide

## Production Deployment with Docker

### 1. Server Requirements
- Ubuntu 22.04 LTS
- 4GB RAM minimum
- 2 CPU cores
- 20GB storage
- Docker + Docker Compose installed

### 2. Deploy

```bash
# Clone repository
git clone https://github.com/Hari-kr262/SIH-25031.git
cd SIH-25031

# Configure environment
cp .env.example .env
nano .env  # Set production values

# Start services
docker-compose up -d --build

# Verify
docker-compose ps
docker-compose logs app
```

### 3. Environment Configuration

Critical settings for production:
```env
APP_ENV=production
DEBUG=False
SECRET_KEY=<generate-with-openssl-rand-hex-32>
JWT_SECRET_KEY=<generate-with-openssl-rand-hex-32>
DATABASE_URL=postgresql://user:STRONG_PASSWORD@postgres:5432/civicresolve_db
```

### 4. Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        proxy_pass http://localhost:8080;
    }
}
```

### 5. SSL with Let's Encrypt

```bash
certbot --nginx -d your-domain.com
```

### 6. Database Backup

```bash
# Daily backup cron
0 3 * * * docker exec postgres pg_dump -U civicresolve civicresolve_db > /backup/$(date +%Y%m%d).sql
```

### 7. Monitoring

- Health check: `GET /api/v1/super-admin/health`
- Docker stats: `docker stats`
- Logs: `docker-compose logs -f`
