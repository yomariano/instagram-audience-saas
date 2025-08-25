from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.config import settings

app = FastAPI(
    title="Instagram Audience Analysis API",
    description="API for analyzing Instagram account demographics",
    version="1.0.0"
)

# Configure CORS to allow frontend access
import os
cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",") if os.getenv("CORS_ALLOWED_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,  # Set to False when using wildcard origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

# Custom exception handler to ensure CORS headers on errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    
    # Add CORS headers to error responses
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

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