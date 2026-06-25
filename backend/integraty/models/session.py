from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import random
import string

from integraty.models.base import Base, generate_uuid


class SessionStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ParticipantStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    ABSENT = "absent"


def generate_session_code():
    """Generate unique 6-digit session code"""
    return ''.join(random.choices(string.digits, k=6))


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="sessions")

    name = Column(String(255), nullable=False)
    session_code = Column(String(6), unique=True, default=generate_session_code, index=True)
    session_type = Column(String(50), default="exam")  # exam, interview, certification, etc.

    scheduled_start = Column(DateTime, nullable=False)
    scheduled_end = Column(DateTime, nullable=False)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)

    status = Column(Enum(SessionStatus), default=SessionStatus.PENDING, nullable=False)

    # Configuration
    config = Column(JSON, nullable=False)  # screenshot_interval, enable_ocr, etc.

    # Metadata
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="sessions_created", foreign_keys=[created_by])

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    participants = relationship("SessionParticipant", back_populates="session", cascade="all, delete-orphan")
    screenshots = relationship("Screenshot", back_populates="session", cascade="all, delete-orphan")
    detection_events = relationship("DetectionEvent", back_populates="session", cascade="all, delete-orphan")
    window_events = relationship("WindowEvent", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session {self.name} ({self.session_code})>"


class SessionParticipant(Base):
    __tablename__ = "session_participants"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    session = relationship("Session", back_populates="participants")

    student_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    student = relationship("User", back_populates="session_participants")

    status = Column(Enum(ParticipantStatus), default=ParticipantStatus.PENDING, nullable=False)

    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)

    # Integrity assessment
    integrity_score = Column(Float, nullable=True)  # 0.0 - 1.0
    detection_count = Column(Integer, default=0)
    screenshot_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<SessionParticipant {self.student_id} in {self.session_id}>"
