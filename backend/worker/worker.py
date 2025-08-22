import asyncio
from app.services.scraper import ApifyScraper
from app.services.analyzer import analyze_commenter_batch
from app.db import SessionLocal
from app.models.analysis import AnalysisJob

async def scrape_instagram_task(job_data: dict):
    """Worker task to scrape Instagram account"""
    username = job_data["data"]["username"]
    job_id = job_data["id"]
    
    db = SessionLocal()
    
    try:
        # Update job status
        job = AnalysisJob(
            job_id=job_id,
            account_username=username,
            job_type="scraping",
            status="running"
        )
        db.add(job)
        db.commit()
        
        # Start scraping
        scraper = ApifyScraper()
        run_id = await scraper.scrape_instagram_account(username)
        
        # Wait for completion and get results
        await asyncio.sleep(30)  # Wait for scraping to complete
        results = await scraper.get_scraping_results(run_id)
        
        # Process results and save to database
        # ... implementation to save posts and comments
        
        # Update job status
        job.status = "completed"
        job.total_posts = len(results.get("posts", []))
        job.total_comments = sum(len(post.get("comments", [])) for post in results.get("posts", []))
        db.commit()
        
        # Queue analysis job
        from app.services.queue import add_job
        add_job("analyze_profiles", {"username": username, "scrape_job_id": job_id})
        
        return {"status": "completed", "job_id": job_id}
        
    except Exception as e:
        # Update job with error
        job.status = "failed"
        job.error_message = str(e)
        db.commit()
        raise e
    finally:
        db.close()

async def analyze_profiles_task(job_data: dict):
    """Worker task to analyze commenter profiles"""
    username = job_data["data"]["username"]
    job_id = job_data["id"]
    
    db = SessionLocal()
    
    try:
        # Get commenters from recent scraping
        # ... query database for commenters
        
        commenters = []  # List of commenters from database
        
        # Analyze in batches
        batch_size = 10
        for i in range(0, len(commenters), batch_size):
            batch = commenters[i:i+batch_size]
            results = await analyze_commenter_batch(batch)
            
            # Save analysis results to database
            # ... implementation to save analysis results
        
        return {"status": "completed", "analyzed_count": len(commenters)}
        
    except Exception as e:
        print(f"Analysis task failed: {e}")
        raise e
    finally:
        db.close()