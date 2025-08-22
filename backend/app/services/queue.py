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
    job_id = str(uuid.uuid4())
    
    job_data = {
        "id": job_id,
        "type": job_type,
        "data": data,
        "status": "pending"
    }
    
    if job_type == "scrape_instagram":
        from app.worker.worker import scrape_instagram_task
        queue.enqueue(scrape_instagram_task, job_data)
    elif job_type == "analyze_profiles":
        from app.worker.worker import analyze_profiles_task
        queue.enqueue(analyze_profiles_task, job_data)
    
    return job_id

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