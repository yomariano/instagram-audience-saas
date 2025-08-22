from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class CommenterAnalysis(Base):
    __tablename__ = "commenter_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("instagram_comments.id"))
    
    # Analysis results
    gender = Column(String)  # male, female, unknown
    age_range = Column(String)  # 18-24, 25-34, 35-44, 45+, unknown
    account_type = Column(String)  # private, public
    confidence_score = Column(Float)
    
    # Metadata
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String, default="gemini-1.5-flash")
    
    # Relationships
    comment = relationship("InstagramComment", back_populates="analysis")

class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    account_username = Column(String)
    job_type = Column(String)  # scraping, analysis
    status = Column(String)  # pending, running, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(String)
    
    # Job metadata
    total_posts = Column(Integer)
    total_comments = Column(Integer)
    processed_comments = Column(Integer, default=0)