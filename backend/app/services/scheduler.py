import schedule
import time
import asyncio
from app.services.scraper import ApifyScraper
from app.services.analyzer import analyze_commenter_batch
from app.db import SessionLocal
from sqlalchemy.orm import Session

class SchedulerService:
    def __init__(self):
        self.scraper = ApifyScraper()
    
    def setup_scheduled_jobs(self):
        """Setup recurring jobs"""
        # Schedule daily scraping for active accounts
        schedule.every().day.at("02:00").do(self.daily_scraping_job)
        
        # Schedule weekly analysis reports
        schedule.every().week.do(self.weekly_analysis_job)
        
        # Schedule cleanup of old data
        schedule.every().month.do(self.cleanup_old_data)
    
    async def daily_scraping_job(self):
        """Daily job to scrape active Instagram accounts"""
        db = SessionLocal()
        try:
            # Get active accounts from database
            active_accounts = []  # Query from DB
            
            for account in active_accounts:
                await self.scraper.scrape_instagram_account(account["username"])
                
        except Exception as e:
            print(f"Daily scraping job failed: {e}")
        finally:
            db.close()
    
    async def weekly_analysis_job(self):
        """Weekly job to generate analysis reports"""
        db = SessionLocal()
        try:
            # Generate weekly reports for all users
            pass
        except Exception as e:
            print(f"Weekly analysis job failed: {e}")
        finally:
            db.close()
    
    def cleanup_old_data(self):
        """Clean up old scraping data"""
        db = SessionLocal()
        try:
            # Delete data older than 30 days
            pass
        except Exception as e:
            print(f"Cleanup job failed: {e}")
        finally:
            db.close()
    
    def run_scheduler(self):
        """Run the scheduler"""
        self.setup_scheduled_jobs()
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute