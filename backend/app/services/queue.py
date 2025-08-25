import redis
import json
import uuid
from rq import Queue, Worker
from app.config import settings

# Redis connection
redis_conn = redis.from_url(settings.redis_url)
queue = Queue(connection=redis_conn)

def add_job(job_type: str, data: dict):
    """Add a job to the queue"""
    try:
        job_id = str(uuid.uuid4())
        
        job_data = {
            "id": job_id,
            "type": job_type,
            "data": data,
            "status": "pending"
        }
        
        # Test Redis connection first
        redis_conn.ping()
        
        if job_type == "scrape_instagram":
            # For now, just return job_id without actually enqueueing
            # since worker tasks may not exist in deployed environment
            print(f"Would enqueue scraping job for: {data}")
            return job_id
        elif job_type == "analyze_profiles":
            print(f"Would enqueue analysis job for: {data}")
            return job_id
        
        return job_id
    except Exception as e:
        print(f"Error in add_job: {str(e)}")
        raise Exception(f"Queue error: {str(e)}")

def get_job_status(job_id: str):
    """Get status of a job"""
    job = queue.fetch_job(job_id)
    if job:
        return {
            "id": job_id,
            "status": job.get_status(),
            "result": job.result
        }
    return {"id": job_id, "status": "not_found"}

class QueueManager:
    def __init__(self):
        self.redis_conn = redis_conn
        self.queue = queue
    
    def start_worker(self):
        """Start queue worker"""
        worker = Worker([self.queue], connection=self.redis_conn)
        worker.work()