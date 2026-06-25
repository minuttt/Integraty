from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from integraty.models.base import Base, generate_uuid


class PlanType(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    plan = Column(Enum(PlanType), default=PlanType.FREE, nullable=False)

    # Limits based on plan
    max_students = Column(Integer, default=10)  # Free: 10, Pro: unlimited
    max_sessions_per_month = Column(Integer, default=5)  # Free: 5, Pro: unlimited
    data_retention_days = Column(Integer, default=7)  # Free: 7, Pro: 90, Enterprise: custom

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="organization")
    sessions = relationship("Session", back_populates="organization")

    def __repr__(self):
        return f"<Organization {self.name}>"
