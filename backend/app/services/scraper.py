import requests
import asyncio
from app.config import settings
from app.services.queue import add_job

class ApifyScraper:
    def __init__(self):
        self.api_token = settings.apify_token
        self.base_url = "https://api.apify.com/v2"
    
    async def scrape_instagram_account(self, username: str):
        """Scrape Instagram account posts and comments using Apify"""
        actor_id = "your-instagram-actor-id"
        
        run_input = {
            "username": username,
            "maxPosts": 10,
            "includeComments": True,
            "maxCommentsPerPost": 50
        }
        
        headers = {"Authorization": f"Bearer {self.api_token}"}
        
        # Start actor run
        response = requests.post(
            f"{self.base_url}/acts/{actor_id}/runs",
            json={"input": run_input},
            headers=headers
        )
        
        if response.status_code == 201:
            run_id = response.json()["data"]["id"]
            return run_id
        else:
            raise Exception(f"Failed to start scraping: {response.text}")
    
    async def get_scraping_results(self, run_id: str):
        """Get results from completed Apify run"""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        
        response = requests.get(
            f"{self.base_url}/actor-runs/{run_id}/dataset/items",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get results: {response.text}")

def start_scraping_job(username: str):
    """Add scraping job to queue"""
    job_id = add_job("scrape_instagram", {"username": username})
    return job_id

async def scrape_with_playwright(username: str):
    """Fallback scraper using Playwright"""
    # Implementation for Playwright-based scraping
    pass