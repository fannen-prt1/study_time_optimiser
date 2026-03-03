"""
Main FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.database.connection import engine, Base
from app.middleware.error_handler import add_error_handlers

# Import models to register them with Base
from app.models import (
    User, Subject, StudySession, Goal, Deadline,
    Achievement, StudyStreak, PomodoroSession,
    DailyWellness, RefreshToken, AIPrediction
)

# Import API routers
from app.api.v1 import auth, sessions, subjects, goals, deadlines, wellness, users, analytics, ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events for the application
    """
    # Startup: Create database tables
    print("🚀 Starting Study Time Optimizer API...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    yield
    
    # Shutdown: Cleanup
    print("👋 Shutting down Study Time Optimizer API...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered study time tracking and optimization platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom error handlers
add_error_handlers(app)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "Study Time Optimizer API",
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to Study Time Optimizer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Include API routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth")
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(subjects.router, prefix=settings.API_V1_PREFIX)
app.include_router(sessions.router, prefix=settings.API_V1_PREFIX)
app.include_router(goals.router, prefix=settings.API_V1_PREFIX)
app.include_router(deadlines.router, prefix=settings.API_V1_PREFIX)
app.include_router(wellness.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)
app.include_router(ai.router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.BACKEND_PORT,
        reload=settings.ENVIRONMENT == "development",
    )
