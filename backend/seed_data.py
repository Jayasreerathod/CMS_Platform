from datetime import datetime, timedelta, UTC
from app.database import SessionLocal, engine, Base
from app.models_program import Program, Term, Lesson, StatusEnum, ContentTypeEnum

# Recreate database schema
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

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
    poster_assets_by_language={
        "en": {
            "portrait": "https://cdn.demo/assets/python_poster_portrait_en.jpg",
            "landscape": "https://cdn.demo/assets/python_poster_landscape_en.jpg",
        },
        "hi": {
            "portrait": "https://cdn.demo/assets/python_poster_portrait_hi.jpg",
            "landscape": "https://cdn.demo/assets/python_poster_landscape_hi.jpg",
        },
    },
)

program_react = Program(
    title="Advanced React",
    description="Deep dive into React components, hooks, and performance.",
    language_primary="en",
    languages_available=["en"],
    status=StatusEnum.draft,
    poster_assets_by_language={
        "en": {
            "portrait": "https://cdn.demo/assets/react_poster_portrait_en.jpg",
            "landscape": "https://cdn.demo/assets/react_poster_landscape_en.jpg",
        }
    },
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
        thumbnail_assets_by_language={
            "en": {
                "portrait": "https://cdn.demo/thumbnails/python_intro_portrait_en.jpg",
                "landscape": "https://cdn.demo/thumbnails/python_intro_landscape_en.jpg",
            }
        },
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
        thumbnail_assets_by_language={
            "en": {
                "portrait": "https://cdn.demo/thumbnails/python_datatypes_portrait_en.jpg",
                "landscape": "https://cdn.demo/thumbnails/python_datatypes_landscape_en.jpg",
            }
        },
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
        status=StatusEnum.draft,
        thumbnail_assets_by_language={
            "en": {
                "portrait": "https://cdn.demo/thumbnails/python_controlflow_portrait_en.jpg",
                "landscape": "https://cdn.demo/thumbnails/python_controlflow_landscape_en.jpg",
            }
        },
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
        thumbnail_assets_by_language={
            "en": {
                "portrait": "https://cdn.demo/thumbnails/react_hooks_portrait_en.jpg",
                "landscape": "https://cdn.demo/thumbnails/react_hooks_landscape_en.jpg",
            }
        },
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
        thumbnail_assets_by_language={
            "en": {
                "portrait": "https://cdn.demo/thumbnails/react_optimize_portrait_en.jpg",
                "landscape": "https://cdn.demo/thumbnails/react_optimize_landscape_en.jpg",
            }
        },
    ),
]

db.add_all(lessons)
db.commit()

# -------------------------------------------------------------------
#  SUMMARY
# -------------------------------------------------------------------
print(" Seed data created successfully!")
print(f"Programs: {[p.title for p in db.query(Program).all()]}")
print(f"Lessons in Python Basics: {[l.title for l in db.query(Lesson).filter_by(program_id=program_python.id).all()]}")
print(" One scheduled lesson will auto-publish in 2 minutes.")

db.close()
