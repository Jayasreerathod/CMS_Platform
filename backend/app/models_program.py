from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class StatusEnum(str, enum.Enum):
    draft = "draft"
    scheduled = "scheduled"
    published = "published"


class Program(Base):
    __tablename__ = "programs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    language_primary = Column(String, default="en")
    status = Column(Enum(StatusEnum), default=StatusEnum.draft)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lessons = relationship("Lesson", back_populates="program", cascade="all, delete")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    program_id = Column(String, ForeignKey("programs.id"), nullable=False)
    title = Column(String, nullable=False)
    lesson_number = Column(Integer, nullable=True)
    content_type = Column(String, default="video")
    duration_ms = Column(Integer, default=0)
    is_paid = Column(Boolean, default=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.draft)
    publish_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    program = relationship("Program", back_populates="lessons")
