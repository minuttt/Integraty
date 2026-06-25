from integraty.models.base import Base, engine, get_db
from integraty.models.user import User
from integraty.models.organization import Organization
from integraty.models.session import Session, SessionParticipant
from integraty.models.monitoring import Screenshot, DetectionEvent, WindowEvent


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


__all__ = [
    'Base',
    'engine',
    'get_db',
    'User',
    'Organization',
    'Session',
    'SessionParticipant',
    'Screenshot',
    'DetectionEvent',
    'WindowEvent',
    'create_tables',
]
