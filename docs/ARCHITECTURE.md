# Instagram Audience Analysis - Architecture

## Overview

This application analyzes Instagram account demographics by scraping comments and using AI to classify commenter profiles.

## High-Level Flow

```
User inputs IG accounts → Scraper (Apify) → Comments + commenter data
    → Vision Model (Gemini Flash) → Gender + age + profile-type classification
    → Database (Postgres) → API for frontend dashboard
```

## Components

### 1. Data Scraper (Apify)
- **Purpose**: Scrapes posts + comments from target Instagram accounts
- **Technology**: Apify Actor with Puppeteer
- **Output**: Commenter username, profile pic URL, comment text, engagement data
- **Location**: `apify/actors/instagram_scraper.js`

### 2. AI Processing Layer
- **Purpose**: Classifies profile pictures for demographic insights
- **Technology**: Google Gemini Flash API
- **Classifications**: Gender, age range, account type (private/public)
- **Location**: `backend/app/services/analyzer.py`

### 3. Database (PostgreSQL)
- **Purpose**: Stores tracked accounts, posts, comments, and analysis results
- **Schema**: Users, Instagram accounts, posts, comments, analysis results
- **Location**: `backend/app/models/`

### 4. API Backend (FastAPI)
- **Purpose**: RESTful API for frontend integration
- **Endpoints**: Account management, analysis retrieval, demographics
- **Location**: `backend/app/api/routes.py`

### 5. Queue System (Redis + RQ)
- **Purpose**: Async processing of scraping and analysis jobs
- **Components**: Job queue, worker processes, scheduler
- **Location**: `backend/app/services/queue.py`

## Data Flow

1. **User adds Instagram account** → API creates scraping job
2. **Worker picks up job** → Calls Apify actor to scrape account
3. **Apify returns data** → Comments and commenter info saved to DB
4. **Analysis job queued** → Worker processes commenter profile pics
5. **Gemini analyzes images** → Demographics saved to DB
6. **Frontend requests data** → API aggregates and returns insights

## Deployment Architecture

### Development
- Docker Compose with local PostgreSQL and Redis
- FastAPI with hot reload
- Separate worker and scheduler containers

### Production (Coolify + Hetzner)
- Container orchestration via Coolify
- Managed PostgreSQL and Redis
- Load-balanced API instances
- Separate worker containers for scaling
- Cron jobs for scheduled tasks

## Security Considerations

- API authentication with JWT tokens
- Rate limiting on endpoints
- Environment variables for sensitive data
- No direct Instagram credentials stored
- GDPR compliance for profile data

## Scaling Considerations

- Horizontal scaling of worker processes
- Database read replicas for analytics
- CDN for profile image caching
- Queue partitioning by account size
- Analysis result caching