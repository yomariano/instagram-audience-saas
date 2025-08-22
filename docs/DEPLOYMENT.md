# Deployment Guide - Hetzner VPS + Coolify

## Prerequisites

- Hetzner VPS (minimum 2 vCPU, 4GB RAM)
- Domain name configured
- Coolify installed on VPS
- Apify account with API token
- Google Cloud account with Gemini API access

## Environment Setup

### 1. VPS Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Coolify Installation

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

### 3. Repository Setup

```bash
# Clone repository
git clone https://github.com/your-username/instagram-audience-saas.git
cd instagram-audience-saas
```

## Environment Variables

Create `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://postgres:secure_password@postgres:5432/instagram_analysis
POSTGRES_PASSWORD=secure_password

# Redis
REDIS_URL=redis://redis:6379

# API Keys
APIFY_TOKEN=your_apify_token_here
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_jwt_key_here

# Application
ENVIRONMENT=production
DEBUG=false
```

## Coolify Deployment

### 1. Create New Project

1. Access Coolify dashboard
2. Create new project: "Instagram Analysis"
3. Connect your Git repository

### 2. Configure Services

#### API Service
- **Name**: instagram-analysis-api
- **Type**: Application
- **Port**: 8000
- **Domain**: api.yourdomain.com
- **Environment**: Load from `.env`
- **Health Check**: `/health`

#### Worker Service
- **Name**: instagram-analysis-worker
- **Type**: Worker
- **Command**: `python -m rq worker --url $REDIS_URL`
- **Environment**: Load from `.env`

#### Database Service
- **Name**: postgres
- **Type**: Database
- **Image**: postgres:15
- **Volume**: `/var/lib/postgresql/data`

#### Cache Service
- **Name**: redis
- **Type**: Cache
- **Image**: redis:7-alpine
- **Volume**: `/data`

### 3. Deploy

1. Commit changes to Git
2. Trigger deployment in Coolify
3. Monitor logs for successful startup

## Database Setup

```bash
# Run migrations (if using Alembic)
docker exec -it api_container alembic upgrade head

# Or create tables manually
docker exec -it api_container python -c "
from app.db import engine
from app.models import user, instagram, analysis
user.Base.metadata.create_all(bind=engine)
instagram.Base.metadata.create_all(bind=engine)
analysis.Base.metadata.create_all(bind=engine)
"
```

## Apify Actor Deployment

### 1. Install Apify CLI

```bash
npm install -g apify-cli
apify login
```

### 2. Deploy Actor

```bash
cd apify/actors
apify push
```

### 3. Update Configuration

Update `backend/app/services/scraper.py` with your actor ID:
```python
actor_id = "your-deployed-actor-id"
```

## Monitoring & Maintenance

### 1. Log Monitoring

```bash
# API logs
docker logs -f api_container

# Worker logs
docker logs -f worker_container

# Database logs
docker logs -f postgres_container
```

### 2. Backup Setup

```bash
# Database backup script
#!/bin/bash
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR
docker exec postgres_container pg_dump -U postgres instagram_analysis > $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql

# Add to crontab for daily backups
0 2 * * * /path/to/backup_script.sh
```

### 3. SSL Certificate

Coolify automatically handles SSL certificates via Let's Encrypt.

### 4. Scaling

#### Horizontal Scaling
- Add more worker containers in Coolify
- Configure load balancer for API instances

#### Vertical Scaling
- Upgrade VPS resources in Hetzner console
- Restart services to use new resources

## Security Checklist

- [ ] Firewall configured (ports 80, 443, 22 only)
- [ ] SSH key-based authentication
- [ ] Database passwords strong and unique
- [ ] API rate limiting enabled
- [ ] CORS properly configured
- [ ] Environment variables secured
- [ ] Regular security updates scheduled

## Troubleshooting

### Common Issues

1. **Worker not processing jobs**
   - Check Redis connection
   - Verify queue name consistency
   - Check worker logs for errors

2. **Scraping failures**
   - Verify Apify token validity
   - Check actor deployment status
   - Monitor Instagram rate limits

3. **Database connection errors**
   - Verify DATABASE_URL format
   - Check PostgreSQL service status
   - Ensure database exists

4. **Gemini API errors**
   - Verify API key validity
   - Check quota limits
   - Monitor API usage

### Performance Optimization

1. **Database**
   - Add indexes on frequently queried columns
   - Enable connection pooling
   - Consider read replicas for analytics

2. **Caching**
   - Implement Redis caching for frequent queries
   - Cache analysis results
   - Use CDN for static assets

3. **Queue Optimization**
   - Tune worker count based on CPU cores
   - Implement job prioritization
   - Monitor queue length