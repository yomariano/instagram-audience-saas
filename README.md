# Instagram Audience Analysis SaaS

A comprehensive platform for analyzing Instagram account demographics through AI-powered profile analysis.

## 🎯 Features

- **Instagram Scraping**: Automated extraction of posts and comments using Apify
- **AI Demographics**: Gender, age, and account type classification using Google Gemini Flash
- **Real-time Analytics**: Dashboard with demographic breakdowns and engagement metrics
- **Scalable Architecture**: Queue-based processing with Redis and FastAPI
- **Easy Deployment**: Ready for Coolify deployment on Hetzner VPS

## 🏗️ Architecture

```
User Input → Apify Scraper → AI Analysis (Gemini) → PostgreSQL → FastAPI → Dashboard
```

### Key Components

- **Backend**: FastAPI with async job processing
- **Database**: PostgreSQL for data storage
- **Queue**: Redis with RQ for job management
- **AI**: Google Gemini Flash for image analysis
- **Scraper**: Apify actor for Instagram data collection

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Apify account
- Google Cloud account (Gemini API)

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-username/instagram-audience-saas.git
cd instagram-audience-saas

# Setup backend
cd backend
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Edit .env with your API keys

# Start services
cd ../infra
docker-compose up -d

# Run API
cd ../backend
uvicorn app.main:app --reload
```

### Environment Variables

```env
DATABASE_URL=postgresql://user:pass@localhost/instagram_analysis
REDIS_URL=redis://localhost:6379
APIFY_TOKEN=your_apify_token
GEMINI_API_KEY=your_gemini_key
SECRET_KEY=your_jwt_secret
```

## 📖 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Apify Actor Setup](apify/README.md)

## 🛠️ API Usage

```bash
# Add Instagram account for analysis
curl -X POST http://localhost:8000/api/v1/accounts \
  -H "Content-Type: application/json" \
  -d '{"username": "target_username"}'

# Get demographics
curl http://localhost:8000/api/v1/accounts/target_username/demographics
```

## 📊 Data Pipeline

1. **Input**: Instagram username
2. **Scraping**: Apify actor extracts posts and comments
3. **Processing**: Comments and profile pictures collected
4. **Analysis**: Gemini Flash analyzes profile images
5. **Storage**: Results saved to PostgreSQL
6. **Output**: Demographic insights via API

## 🔄 Deployment

### Coolify (Recommended)

```bash
# Deploy to Coolify
git push origin main
# Configure in Coolify dashboard
# Set environment variables
# Deploy services
```

### Docker Compose

```bash
cd infra
docker-compose up -d
```

## 📈 Scaling

- **Horizontal**: Add more worker containers
- **Vertical**: Increase CPU/memory resources
- **Database**: Read replicas for analytics
- **Cache**: Redis for frequent queries

## 🔒 Security

- JWT authentication for API access
- Environment variables for sensitive data
- Rate limiting on all endpoints
- GDPR compliance for profile data

## 🧪 Testing

```bash
cd backend
pytest tests/
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📞 Support

- Documentation: `/docs`
- Issues: GitHub Issues
- Email: support@yourdomain.com

---

Built with ❤️ for Instagram audience analysis