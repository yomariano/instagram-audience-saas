from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import settings

app = FastAPI(
    title="Instagram Audience Analysis API",
    description="API for analyzing Instagram account demographics",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://instagram-app.teabag.online",
        "http://instagram-app.teabag.online", 
        "http://localhost:3000",
        "http://localhost:8080",
        "https://localhost:3000",
        "*"  # Allow all origins in development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Instagram Audience Analysis API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}