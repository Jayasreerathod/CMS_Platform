import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Enum,
    DateTime,
    ForeignKey,
    Boolean,
    JSON,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base, DATABASE_URL
import enum
import uuid

def gen_uuid():
    return str(uuid.uuid4())

# ---------- Compatibility Helper ----------
def ArrayType(item_type=String):
    """Uses ARRAY for PostgreSQL, JSON fallback for SQLite."""
    if DATABASE_URL.startswith("sqlite"):
        return JSON
    return ARRAY(item_type)

# ---------- Asset Enums ----------
class AssetVariantEnum(str, enum.Enum):
    portrait = "portrait"
    landscape = "landscape"
    square = "square"
    banner = "banner"


class AssetTypeEnum(str, enum.Enum):
    poster = "poster"
    thumbnail = "thumbnail"
    subtitle = "subtitle"

# ---------- Enum ----------
class StatusEnum(str, enum.Enum):
    draft = "draft"
    scheduled = "scheduled"
    published = "published"
    archived = "archived"


class ContentTypeEnum(str, enum.Enum):
    video = "video"
    article = "article"


# ---------- Program ----------
class Program(Base):
    __tablename__ = "programs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    language_primary = Column(String, nullable=False, default="en")

    # Multi-language support
    languages_available = Column(ArrayType(String), default=["en"])

    # Status tracking
    status = Column(Enum(StatusEnum), default=StatusEnum.draft)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    poster_assets_by_language = Column(JSON, default={})
    # Relationships
    lessons = relationship("Lesson", back_populates="program", cascade="all, delete-orphan")
    terms = relationship("Term", back_populates="program", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Program(title={self.title}, status={self.status})>"


# ---------- Term ----------
class Term(Base):
    __tablename__ = "terms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    program_id = Column(String, ForeignKey("programs.id"), nullable=False)
    term_number = Column(Integer, nullable=False)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    program = relationship("Program", back_populates="terms")
    lessons = relationship("Lesson", back_populates="term", cascade="all, delete-orphan")

    __table_args__ = (
        # Unique constraint per program term
        {"sqlite_autoincrement": True},
    )


# ---------- Lesson ----------
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    program_id = Column(String, ForeignKey("programs.id"), nullable=False)
    term_id = Column(String, ForeignKey("terms.id"), nullable=True)

    lesson_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)

    content_type = Column(Enum(ContentTypeEnum), default=ContentTypeEnum.video)
    duration_ms = Column(Integer, nullable=True)
    is_paid = Column(Boolean, default=False)

    # Multi-language content
    content_language_primary = Column(String, nullable=False, default="en")
    content_languages_available = Column(ArrayType(String), default=["en"])
    content_urls_by_language = Column(JSON, default={})
    subtitle_languages = Column(ArrayType(String), default=[])
    subtitle_urls_by_language = Column(JSON, default={})

    # Media assets
    assets = Column(JSON, default={})  # e.g. { "en": { "portrait": "url", "landscape": "url" } }

    # Publishing workflow
    status = Column(Enum(StatusEnum), default=StatusEnum.draft)
    publish_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    thumbnail_assets_by_language = Column(JSON, nullable=True, default={})
    # Relationships
    program = relationship("Program", back_populates="lessons")
    term = relationship("Term", back_populates="lessons")

    def __repr__(self):
        return f"<Lesson(title={self.title}, status={self.status})>"
    
 # ---------- ProgramAsset ----------
class ProgramAsset(Base):
    __tablename__ = "program_assets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    program_id = Column(String, ForeignKey("programs.id"), nullable=False)
    language = Column(String, nullable=False)
    variant = Column(Enum(AssetVariantEnum), nullable=False)
    asset_type = Column(Enum(AssetTypeEnum), nullable=False)
    url = Column(String, nullable=False)

    program = relationship("Program")

# ---------- LessonAsset ----------
class LessonAsset(Base):
    __tablename__ = "lesson_assets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lesson_id = Column(String, ForeignKey("lessons.id"), nullable=False)
    language = Column(String, nullable=False)
    variant = Column(Enum(AssetVariantEnum), nullable=False)
    asset_type = Column(Enum(AssetTypeEnum), nullable=False)
    url = Column(String, nullable=False)

    lesson = relationship("Lesson")


