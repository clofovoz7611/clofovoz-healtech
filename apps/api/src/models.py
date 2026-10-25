import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifier = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class VoiceSession(Base):
    __tablename__ = "voice_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    audio_url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

class AcousticBiomarker(Base):
    __tablename__ = "acoustic_biomarkers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("voice_sessions.id"), nullable=False)
    f0_mean_hz = Column(Float, nullable=False)
    jitter_percent = Column(Float, nullable=False)
    shimmer_percent = Column(Float, nullable=False)
    hnr_db = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)