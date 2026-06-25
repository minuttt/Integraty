from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from integraty.core.session_manager import SessionStatus

router = APIRouter()


def get_session_manager(request: Request):
    """Get session manager from app state"""
    return request.app.state.session_manager


# Request/Response Models
class SessionCreate(BaseModel):
    user_id: str
    session_name: str
    session_type: str = "exam"
    screenshot_interval: int = 30
    screenshot_quality: int = 85
    enable_ocr: bool = True
    enable_window_monitoring: bool = True


class SessionResponse(BaseModel):
    session_id: str
    user_id: str
    status: str
    start_time: Optional[datetime] = None
    stats: dict


@router.post("/", response_model=SessionResponse)
async def create_session(request: Request, session_data: SessionCreate):
    """Create a new monitoring session"""
    session_manager = get_session_manager(request)

    try:
        # Create session config
        config = {
            "session_name": session_data.session_name,
            "session_type": session_data.session_type,
            "screenshot_interval": session_data.screenshot_interval,
            "screenshot_quality": session_data.screenshot_quality,
            "enable_ocr": session_data.enable_ocr,
            "enable_window_monitoring": session_data.enable_window_monitoring,
        }

        # Create session
        session = session_manager.create_session(
            user_id=session_data.user_id,
            config=config,
        )

        return SessionResponse(
            session_id=session.session_id,
            user_id=session.user_id,
            status=session.status,
            start_time=session.start_time,
            stats=session.get_stats(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/start")
async def start_session(request: Request, session_id: str, background_tasks: BackgroundTasks):
    """Start a monitoring session"""
    session_manager = get_session_manager(request)
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        background_tasks.add_task(session.start)

        return {
            "session_id": session_id,
            "status": "starting",
            "message": "Session is starting",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{session_id}/pause")
async def pause_session(request: Request, session_id: str):
    """Pause a monitoring session"""
    session_manager = get_session_manager(request)
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        await session.pause()

        return {
            "session_id": session_id,
            "status": session.status,
            "message": "Session paused",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{session_id}/resume")
async def resume_session(request: Request, session_id: str):
    """Resume a paused session"""
    session_manager = get_session_manager(request)
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        await session.resume()

        return {
            "session_id": session_id,
            "status": session.status,
            "message": "Session resumed",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{session_id}/complete")
async def complete_session(request: Request, session_id: str):
    """Complete a monitoring session"""
    session_manager = get_session_manager(request)
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        await session.complete()

        return {
            "session_id": session_id,
            "status": session.status,
            "stats": session.get_stats(),
            "message": "Session completed",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(request: Request, session_id: str):
    """Get session details"""
    session_manager = get_session_manager(request)
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionResponse(
        session_id=session.session_id,
        user_id=session.user_id,
        status=session.status,
        start_time=session.start_time,
        stats=session.get_stats(),
    )


@router.get("/", response_model=List[SessionResponse])
async def list_sessions(request: Request, status: Optional[str] = None):
    """List all sessions"""
    session_manager = get_session_manager(request)
    sessions = session_manager.sessions.values()

    if status:
        sessions = [s for s in sessions if s.status == status]

    return [
        SessionResponse(
            session_id=s.session_id,
            user_id=s.user_id,
            status=s.status,
            start_time=s.start_time,
            stats=s.get_stats(),
        )
        for s in sessions
    ]


@router.delete("/{session_id}")
async def delete_session(request: Request, session_id: str):
    """Delete a session"""
    session_manager = get_session_manager(request)
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Stop session if active
    if session.status == SessionStatus.ACTIVE:
        await session.complete()

    session_manager.remove_session(session_id)

    return {"message": "Session deleted", "session_id": session_id}
