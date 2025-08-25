from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db import get_db
import uuid
# from app.services.analyzer import get_analysis_results
from typing import List

router = APIRouter()

@router.post("/accounts")
async def add_instagram_account(
    account: dict
):
    """Add an Instagram account for analysis"""
    try:
        username = account.get("username")
        if not username:
            raise HTTPException(status_code=400, detail="Username is required")
        
        # Generate job ID and mock the scraping job for now
        job_id = str(uuid.uuid4())
        print(f"Mock scraping job created for user: {username}, job_id: {job_id}")
        
        return {"message": f"Analysis started for @{username}", "job_id": job_id}
    except Exception as e:
        # Log the actual error for debugging
        print(f"Error in add_instagram_account: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/accounts/{username}/analysis")
async def get_account_analysis(
    username: str
):
    """Get analysis results for an Instagram account"""
    # Mock results for now
    return {
        "username": username,
        "status": "completed", 
        "followers_count": 1250,
        "posts_analyzed": 10,
        "engagement_rate": 3.2,
        "last_updated": "2024-08-25T10:00:00Z"
    }

@router.get("/accounts/{username}/demographics")
async def get_demographics(
    username: str
):
    """Get demographic breakdown for account followers"""
    # Implementation for demographic analysis
    return {
        "gender_split": {"male": 45, "female": 55},
        "age_distribution": {"18-24": 30, "25-34": 40, "35+": 30},
        "account_types": {"private": 60, "public": 40}
    }