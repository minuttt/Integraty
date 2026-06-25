from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from integraty.config import settings
from integraty.core.session_manager import SessionManager
from integraty.api.v1 import router as api_router
from integraty.models import create_tables

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://.*\.vercel\.app",  # Allow all Vercel domains
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global session manager
session_manager = SessionManager(data_dir=settings.DATA_DIR)

# Store in app state for access in endpoints
app.state.session_manager = session_manager


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Data directory: {settings.DATA_DIR}")
    print(f"Environment: {settings.APP_ENV}")

    # Create database tables
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("Shutting down...")
    await session_manager.stop_all_sessions()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    active_sessions = len(session_manager.get_active_sessions())

    return {
        "status": "healthy",
        "active_sessions": active_sessions,
        "features": {
            "screen_capture": True,
            "window_monitoring": True,
            "ocr": settings.OCR_ENABLED,
            "browser_monitoring": settings.ENABLE_BROWSER_MONITORING,
        },
    }


# Include API routes
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "integraty.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
