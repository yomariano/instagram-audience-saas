from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import settings

app = FastAPI(
    title="Instagram Audience Analysis API",
    description="API for analyzing Instagram account demographics",
    version="1.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=False,  # Set to False when using wildcard
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

@app.options("/health")
async def health_options():
    return {"status": "ok"}

@app.options("/api/v1/{path:path}")
async def api_options(path: str):
    return {"status": "ok"}