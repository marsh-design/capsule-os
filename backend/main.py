"""
CapsuleOS Backend API
FastAPI application for capsule wardrobe planning and purchase decision assistance
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import os
from dotenv import load_dotenv

from app.routers import capsule, analyze, closet
from app.database import init_db

load_dotenv()

app = FastAPI(
    title="CapsuleOS API",
    description="Quarterly capsule wardrobe planner and purchase decision assistant",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(capsule.router, prefix="/api", tags=["capsule"])
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(closet.router, prefix="/api/closet", tags=["closet"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "CapsuleOS API is running"}


@app.get("/api/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
