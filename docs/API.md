# Instagram Audience Analysis API

Base URL: `https://api.yourdomain.com/api/v1`

## Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Account Management

#### Add Instagram Account
```http
POST /accounts
Content-Type: application/json

{
    "username": "target_instagram_username"
}
```

**Response:**
```json
{
    "message": "Analysis started for @target_username",
    "job_id": "uuid-job-id"
}
```

#### Get Account Analysis
```http
GET /accounts/{username}/analysis
```

**Response:**
```json
{
    "username": "target_username",
    "total_comments": 150,
    "demographics": {
        "gender_split": {"male": 45, "female": 55},
        "age_distribution": {"18-24": 30, "25-34": 40, "35+": 30}
    },
    "status": "completed"
}
```

#### Get Demographics Breakdown
```http
GET /accounts/{username}/demographics
```

**Response:**
```json
{
    "gender_split": {
        "male": 45,
        "female": 55
    },
    "age_distribution": {
        "18-24": 30,
        "25-34": 40,
        "35-44": 20,
        "45+": 10
    },
    "account_types": {
        "private": 60,
        "public": 40
    },
    "engagement_metrics": {
        "avg_comments_per_post": 25.5,
        "top_commenters": [
            {"username": "user1", "comment_count": 5},
            {"username": "user2", "comment_count": 4}
        ]
    }
}
```

### Job Management

#### Get Job Status
```http
GET /jobs/{job_id}/status
```

**Response:**
```json
{
    "id": "job-id",
    "status": "completed",
    "progress": {
        "total_posts": 10,
        "processed_posts": 10,
        "total_comments": 150,
        "analyzed_comments": 150
    },
    "started_at": "2024-01-01T00:00:00Z",
    "completed_at": "2024-01-01T00:05:00Z"
}
```

### Analytics

#### Get Account Insights
```http
GET /accounts/{username}/insights
```

**Response:**
```json
{
    "summary": {
        "total_engagement": 1250,
        "unique_commenters": 89,
        "avg_engagement_rate": 5.2
    },
    "demographics": {
        "gender_distribution": {"male": 45, "female": 55},
        "age_ranges": {"18-24": 30, "25-34": 40, "35+": 30},
        "account_privacy": {"private": 60, "public": 40}
    },
    "trends": {
        "engagement_by_time": [
            {"hour": 9, "comments": 15},
            {"hour": 12, "comments": 25},
            {"hour": 18, "comments": 35}
        ],
        "top_engaging_demographics": [
            {"group": "female_25-34", "engagement_rate": 8.5},
            {"group": "male_18-24", "engagement_rate": 6.2}
        ]
    }
}
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

**Error Response Format:**
```json
{
    "error": "Error message",
    "code": "ERROR_CODE",
    "details": "Additional error details"
}
```

## Rate Limits

- 100 requests per minute per user
- 10 account analysis requests per hour
- 1000 demographic queries per day

## Webhooks

Configure webhooks to receive notifications when analysis completes:

```http
POST /webhooks
Content-Type: application/json

{
    "url": "https://your-app.com/webhook",
    "events": ["analysis.completed", "scraping.failed"]
}
```