# Docker Setup for Instagram Audience Analysis

This guide covers running the Instagram Audience Analysis SaaS using Docker and Docker Compose for both development and production.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- Git

## Quick Start

1. **Clone and setup environment**:
```bash
git clone https://github.com/yomariano/instagram-audience-saas.git
cd instagram-audience-saas
cp .env.example .env
```

2. **Configure environment variables**:
Edit `.env` with your API keys:
```bash
APIFY_TOKEN=your_apify_token_here
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your-super-secret-jwt-key
```

3. **Start all services**:
```bash
docker-compose up -d
```

4. **Access the application**:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Services

### Backend API (`api`)
- **Port**: 8000
- **Health Check**: http://localhost:8000/health
- **Features**: FastAPI with auto-reload in development
- **Dependencies**: PostgreSQL, Redis

### Frontend (`frontend`)
- **Port**: 3000 (mapped from container port 80)
- **Technology**: Static HTML/JS with Nginx
- **Features**: Modern UI with Tailwind CSS, Chart.js

### Database (`postgres`)
- **Port**: 5432
- **Database**: `instagram_analysis`
- **User**: `postgres`
- **Password**: `password123` (change in production!)

### Cache (`redis`)
- **Port**: 6379
- **Features**: Persistent storage with AOF

### Worker (`worker`)
- **Purpose**: Background job processing
- **Queue**: Redis Queue (RQ)
- **Jobs**: Instagram scraping, AI analysis

### Nginx Proxy (`nginx`)
- **Port**: 80
- **Features**: Load balancing, SSL termination (in production)
- **Endpoints**: 
  - `app.localhost` → Frontend
  - `api.localhost` → Backend API

## Development Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api
docker-compose logs -f frontend
docker-compose logs -f worker

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Access database
docker-compose exec postgres psql -U postgres -d instagram_analysis

# Access Redis
docker-compose exec redis redis-cli

# Run backend shell
docker-compose exec api python -c "from app.db import engine; print('DB Connected!')"
```

## Production Deployment

For production deployment on Coolify or other platforms:

1. **Backend**: Use the optimized Dockerfile with multi-stage build
2. **Frontend**: Static files served by Nginx
3. **Database**: Use managed PostgreSQL service
4. **Cache**: Use managed Redis service

### Environment Variables for Production

```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
APIFY_TOKEN=your_production_apify_token
GEMINI_API_KEY=your_production_gemini_key
SECRET_KEY=super-secure-secret-key
ENVIRONMENT=production
DEBUG=false
```

## Security Features

- ✅ Non-root user in containers
- ✅ Multi-stage builds for smaller images
- ✅ Health checks for all services
- ✅ CORS configuration for frontend
- ✅ Environment variable isolation
- ✅ Network isolation between services

## Monitoring

### Health Checks
- API: `curl http://localhost:8000/health`
- Frontend: `curl http://localhost:3000/`
- Database: `docker-compose exec postgres pg_isready`

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api

# Follow new logs
docker-compose logs -f --tail=50 api
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in `docker-compose.yml`
2. **Database connection**: Check PostgreSQL is healthy
3. **CORS errors**: Verify frontend domain in backend CORS settings
4. **API keys**: Ensure valid Apify and Gemini API keys

### Reset Everything
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build -d
```

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │────│    Nginx    │────│   Backend   │
│  (Port 3000)│    │  (Port 80)  │    │  (Port 8000)│
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                         ┌─────────────────────┼─────────────────────┐
                         │                     │                     │
                   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
                   │ PostgreSQL  │    │    Redis    │    │   Worker    │
                   │ (Port 5432) │    │ (Port 6379) │    │ Background  │
                   └─────────────┘    └─────────────┘    └─────────────┘
```

Built with ❤️ for Instagram audience analysis