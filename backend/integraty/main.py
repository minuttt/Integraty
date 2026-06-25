from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from integraty.config import settings
from integraty.core.session_manager import SessionManager

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global session manager
session_manager = SessionManager(data_dir=settings.DATA_DIR)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Data directory: {settings.DATA_DIR}")
    print(f"Environment: {settings.APP_ENV}")


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


# API routes
from integraty.api.v1 import router as api_router

app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "integraty.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
