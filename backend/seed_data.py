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

# --- Ensure tables exist ---
Base.metadata.create_all(bind=engine)

db = SessionLocal()

print(" Checking existing programs in database...")

# -------------------------------------------------------------------
#  Insert only if specific demo programs are missing
# -------------------------------------------------------------------
existing_titles = {p.title for p in db.query(Program).all()}

programs_to_add = []

if "Python Basics" not in existing_titles:
    programs_to_add.append(
        Program(
            title="Python Basics",
            description="Learn Python programming from scratch.",
            language_primary="en",
            languages_available=["en", "hi"],
            status=StatusEnum.published,
            published_at=datetime.now(UTC),
        )
    )

if "Advanced React" not in existing_titles:
    programs_to_add.append(
        Program(
            title="Advanced React",
            description="Deep dive into React components, hooks, and performance.",
            language_primary="en",
            languages_available=["en"],
            status=StatusEnum.published,
            published_at=datetime.now(UTC),
        )
    )

if programs_to_add:
    db.add_all(programs_to_add)
    db.commit()
    print(f" Added {len(programs_to_add)} missing demo programs.")
else:
    print(" All demo programs already exist, skipping program insert.")

# Fetch programs again
program_python = db.query(Program).filter_by(title="Python Basics").first()
program_react = db.query(Program).filter_by(title="Advanced React").first()

# -------------------------------------------------------------------
#  TERMS
# -------------------------------------------------------------------
if program_python:
    term1 = (
        db.query(Term)
        .filter_by(program_id=program_python.id, term_number=1)
        .first()
        or Term(program_id=program_python.id, term_number=1, title="Fundamentals")
    )
    db.add(term1)

if program_react:
    term2 = (
        db.query(Term)
        .filter_by(program_id=program_react.id, term_number=1)
        .first()
        or Term(program_id=program_react.id, term_number=1, title="Hooks & Optimization")
    )
    db.add(term2)

db.commit()

# -------------------------------------------------------------------
#  LESSONS
# -------------------------------------------------------------------
lessons_to_add = []

if program_python and not db.query(Lesson).filter_by(program_id=program_python.id).first():
    lessons_to_add.extend([
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
    ])

if program_react and not db.query(Lesson).filter_by(program_id=program_react.id).first():
    lessons_to_add.extend([
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
    ])

if lessons_to_add:
    db.add_all(lessons_to_add)
    db.commit()
    print(f" Added {len(lessons_to_add)} lessons.")
else:
    print(" Lessons already exist for demo programs, skipping.")

# -------------------------------------------------------------------
#  ASSETS
# -------------------------------------------------------------------
assets = []
for program in [program_python, program_react]:
    if program:
        assets += [
            ProgramAsset(
                program_id=program.id,
                language="en",
                variant=AssetVariantEnum.portrait,
                asset_type=AssetTypeEnum.poster,
                url=f"https://cdn.demo/assets/{program.title.replace(' ', '_').lower()}_poster_portrait_en.jpg",
            ),
            ProgramAsset(
                program_id=program.id,
                language="en",
                variant=AssetVariantEnum.landscape,
                asset_type=AssetTypeEnum.poster,
                url=f"https://cdn.demo/assets/{program.title.replace(' ', '_').lower()}_poster_landscape_en.jpg",
            ),
        ]

if lessons_to_add:
    for lesson in lessons_to_add:
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

if assets:
    db.add_all(assets)
    db.commit()
    print(f" Added {len(assets)} assets.")
else:
    print(" Assets already exist, skipping.")

print("\n Seed completed successfully!")
print(f"Programs now in DB: {[p.title for p in db.query(Program).all()]}")
db.close()

def main():
    """Allows other scripts (like main.py) to call the seeder directly."""
    # Just re-run this same file’s logic
    from seed_data import (
        Base, engine, SessionLocal, Program, Term, Lesson, ProgramAsset, LessonAsset,
        StatusEnum, ContentTypeEnum, AssetVariantEnum, AssetTypeEnum
    )
    # Nothing else needed — Python will just re-import and execute above logic


if __name__ == "__main__":
    main()
