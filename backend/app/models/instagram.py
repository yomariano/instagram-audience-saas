from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class InstagramAccount(Base):
    __tablename__ = "instagram_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    last_scraped = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="tracked_accounts")
    posts = relationship("InstagramPost", back_populates="account")

class InstagramPost(Base):
    __tablename__ = "instagram_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, unique=True, index=True)
    account_id = Column(Integer, ForeignKey("instagram_accounts.id"))
    caption = Column(Text)
    likes_count = Column(Integer)
    comments_count = Column(Integer)
    posted_at = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    account = relationship("InstagramAccount", back_populates="posts")
    comments = relationship("InstagramComment", back_populates="post")

class InstagramComment(Base):
    __tablename__ = "instagram_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(String, unique=True, index=True)
    post_id = Column(Integer, ForeignKey("instagram_posts.id"))
    commenter_username = Column(String)
    commenter_profile_pic = Column(String)
    text = Column(Text)
    likes_count = Column(Integer)
    posted_at = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("InstagramPost", back_populates="comments")
    analysis = relationship("CommenterAnalysis", back_populates="comment", uselist=False)