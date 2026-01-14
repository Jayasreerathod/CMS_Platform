from datetime import datetime, timedelta, UTC
from app.database import SessionLocal, engine, Base
from app.models_program import (
    Program,
    Term,
    Lesson,
    ProgramAsset,
    LessonAsset,
    StatusEnum,
    ContentTypeEnum,
    AssetVariantEnum,
    AssetTypeEnum,
)

# --- Ensure tables exist (don’t drop existing data) ---
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Skip seeding if data already exists ---
if db.query(Program).first():
    print(" Database already has programs — skipping seed.")
    db.close()
    exit()

print("🌱 Seeding new data into Render database...")

# -------------------------------------------------------------------
#  PROGRAMS
# -------------------------------------------------------------------
program_python = Program(
    title="Python Basics",
    description="Learn Python programming from scratch.",
    language_primary="en",
    languages_available=["en", "hi"],
    status=StatusEnum.published,
    published_at=datetime.now(UTC),
)

program_react = Program(
    title="Advanced React",
    description="Deep dive into React components, hooks, and performance.",
    language_primary="en",
    languages_available=["en"],
    status=StatusEnum.published,
    published_at=datetime.now(UTC),
)

db.add_all([program_python, program_react])
db.commit()

# -------------------------------------------------------------------
#  TERMS
# -------------------------------------------------------------------
term1 = Term(program_id=program_python.id, term_number=1, title="Fundamentals")
term2 = Term(program_id=program_react.id, term_number=1, title="Hooks & Optimization")
db.add_all([term1, term2])
db.commit()

# -------------------------------------------------------------------
#  LESSONS
# -------------------------------------------------------------------
lessons = [
    Lesson(
        program_id=program_python.id,
        term_id=term1.id,
        lesson_number=1,
        title="Intro to Python",
        content_type=ContentTypeEnum.video,
        duration_ms=300000,
        content_language_primary="en",
        content_languages_available=["en", "hi"],
        content_urls_by_language={
            "en": "https://cdn.demo/python_intro_en.mp4",
            "hi": "https://cdn.demo/python_intro_hi.mp4",
        },
        status=StatusEnum.published,
        published_at=datetime.now(UTC),
    ),
    Lesson(
        program_id=program_python.id,
        term_id=term1.id,
        lesson_number=2,
        title="Data Types and Variables",
        content_type=ContentTypeEnum.video,
        duration_ms=450000,
        content_language_primary="en",
        content_languages_available=["en"],
        content_urls_by_language={"en": "https://cdn.demo/python_datatypes_en.mp4"},
        status=StatusEnum.published,
        published_at=datetime.now(UTC),
    ),
    Lesson(
        program_id=program_python.id,
        term_id=term1.id,
        lesson_number=3,
        title="Control Flow",
        content_type=ContentTypeEnum.article,
        content_language_primary="en",
        content_languages_available=["en"],
        content_urls_by_language={"en": "https://cdn.demo/python_controlflow.html"},
        status=StatusEnum.published,
        published_at=datetime.now(UTC),
    ),
    Lesson(
        program_id=program_react.id,
        term_id=term2.id,
        lesson_number=1,
        title="React Hooks Deep Dive",
        content_type=ContentTypeEnum.video,
        content_language_primary="en",
        content_languages_available=["en"],
        content_urls_by_language={"en": "https://cdn.demo/react_hooks.mp4"},
        status=StatusEnum.published,
        published_at=datetime.now(UTC),
    ),
    Lesson(
        program_id=program_react.id,
        term_id=term2.id,
        lesson_number=2,
        title="Optimizing React Apps",
        content_type=ContentTypeEnum.video,
        content_language_primary="en",
        content_languages_available=["en"],
        content_urls_by_language={"en": "https://cdn.demo/react_optimize.mp4"},
        status=StatusEnum.scheduled,
        publish_at=datetime.now(UTC) + timedelta(minutes=2),
    ),
]

db.add_all(lessons)
db.commit()

# -------------------------------------------------------------------
#  ASSETS
# -------------------------------------------------------------------
assets = [
    # Posters for Programs
    ProgramAsset(
        program_id=program_python.id,
        language="en",
        variant=AssetVariantEnum.portrait,
        asset_type=AssetTypeEnum.poster,
        url="https://cdn.demo/assets/python_poster_portrait_en.jpg",
    ),
    ProgramAsset(
        program_id=program_python.id,
        language="en",
        variant=AssetVariantEnum.landscape,
        asset_type=AssetTypeEnum.poster,
        url="https://cdn.demo/assets/python_poster_landscape_en.jpg",
    ),
    ProgramAsset(
        program_id=program_react.id,
        language="en",
        variant=AssetVariantEnum.portrait,
        asset_type=AssetTypeEnum.poster,
        url="https://cdn.demo/assets/react_poster_portrait_en.jpg",
    ),
    ProgramAsset(
        program_id=program_react.id,
        language="en",
        variant=AssetVariantEnum.landscape,
        asset_type=AssetTypeEnum.poster,
        url="https://cdn.demo/assets/react_poster_landscape_en.jpg",
    ),
]

# Thumbnails for Lessons
for lesson in lessons:
    assets.extend([
        LessonAsset(
            lesson_id=lesson.id,
            language=lesson.content_language_primary,
            variant=AssetVariantEnum.portrait,
            asset_type=AssetTypeEnum.thumbnail,
            url=f"https://cdn.demo/thumbnails/{lesson.title.replace(' ', '_')}_portrait.jpg",
        ),
        LessonAsset(
            lesson_id=lesson.id,
            language=lesson.content_language_primary,
            variant=AssetVariantEnum.landscape,
            asset_type=AssetTypeEnum.thumbnail,
            url=f"https://cdn.demo/thumbnails/{lesson.title.replace(' ', '_')}_landscape.jpg",
        ),
    ])

db.add_all(assets)
db.commit()

print(" Seed data created successfully!")
print(f"Programs: {[p.title for p in db.query(Program).all()]}")
print("Lessons added and published successfully!")

db.close()
