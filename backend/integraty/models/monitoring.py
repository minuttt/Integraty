from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from integraty.models.base import Base, generate_uuid


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    session = relationship("Session", back_populates="screenshots")

    student_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    student = relationship("User", back_populates="screenshots")

    timestamp = Column(DateTime, nullable=False, index=True)
    sequence_number = Column(Integer, nullable=False)

    # File storage
    file_url = Column(String(500), nullable=False)  # S3 URL or local path
    thumbnail_url = Column(String(500), nullable=True)
    sha256_hash = Column(String(64), nullable=False)

    # Image properties
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    file_size = Column(Integer, nullable=False)  # bytes

    # OCR results
    ocr_text = Column(Text, nullable=True)
    ocr_confidence = Column(Float, nullable=True)
    ocr_processed = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    detection_events = relationship("DetectionEvent", back_populates="screenshot")

    def __repr__(self):
        return f"<Screenshot {self.id} at {self.timestamp}>"


class DetectionEvent(Base):
    __tablename__ = "detection_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    session = relationship("Session", back_populates="detection_events")

    student_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    student = relationship("User", back_populates="detection_events")

    screenshot_id = Column(String(36), ForeignKey("screenshots.id"), nullable=True)
    screenshot = relationship("Screenshot", back_populates="detection_events")

    timestamp = Column(DateTime, nullable=False, index=True)

    # Detection details
    tool_name = Column(String(100), nullable=False)
    tool_type = Column(String(50), nullable=False)  # chatbot, code_assistant, etc.
    detection_method = Column(String(50), nullable=False)  # domain_match, keyword_match, etc.

    confidence_score = Column(Float, nullable=False)  # 0.0 - 1.0
    confidence_level = Column(String(20), nullable=False)  # low, medium, high, very_high

    # Evidence
    evidence = Column(JSON, nullable=False)  # matched_values, context, etc.

    # Review
    reviewed = Column(DateTime, nullable=True)
    review_verdict = Column(String(50), nullable=True)  # confirmed, false_positive, uncertain
    review_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DetectionEvent {self.tool_name} at {self.timestamp}>"


class WindowEvent(Base):
    __tablename__ = "window_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    session = relationship("Session", back_populates="window_events")

    student_id = Column(String(36), ForeignKey("users.id"), nullable=False)

    timestamp = Column(DateTime, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Window details
    process_name = Column(String(255), nullable=False)
    window_title = Column(String(500), nullable=True)
    process_id = Column(Integer, nullable=True)

    # Classification
    is_browser = Column(Integer, default=0)  # SQLite doesn't have proper boolean
    is_ide = Column(Integer, default=0)
    category = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<WindowEvent {self.process_name} at {self.timestamp}>"
