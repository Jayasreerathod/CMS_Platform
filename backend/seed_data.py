from app.database import SessionLocal, engine, Base
from app.models_program import Program, Lesson, StatusEnum
from datetime import datetime, timedelta

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
db = SessionLocal()

program1 = Program(
    title="Python Basics",
    description="Learn Python programming from scratch.",
    status=StatusEnum.published,
    published_at=datetime.utcnow(),
)
program2 = Program(
    title="Advanced React",
    description="Deep dive into React components, hooks, and state management.",
    status=StatusEnum.scheduled,
    published_at=datetime.utcnow() + timedelta(minutes=2),
)
program3 = Program(
    title="Python Avanzado",
    description="Aprende Python avanzado en español.",
    status=StatusEnum.draft,
    language_primary="es"
)

db.add_all([program1, program2, program3])
db.commit()

lessons = [
    Lesson(
        title="Introduction to Python",
        program_id=program1.id,
        lesson_number=1,
        status=StatusEnum.published,
        published_at=datetime.utcnow(),
    ),
    Lesson(
        title="Data Types and Variables",
        program_id=program1.id,
        lesson_number=2,
        status=StatusEnum.published,
        published_at=datetime.utcnow(),
    ),
    Lesson(
        title="Control Flow",
        program_id=program1.id,
        lesson_number=3,
        status=StatusEnum.draft,
    ),
    Lesson(
        title="React Hooks",
        program_id=program2.id,
        lesson_number=1,
        status=StatusEnum.scheduled,
        published_at=datetime.utcnow() + timedelta(minutes=2),
    ),
    Lesson(
        title="React Components",
        program_id=program2.id,
        lesson_number=2,
        status=StatusEnum.draft,
    ),
    Lesson(
        title="Avanzado: Funciones",
        program_id=program3.id,
        lesson_number=1,
        status=StatusEnum.draft,
    ),
]

db.add_all(lessons)
db.commit()

print(" Seed data created successfully!")
print(f"Programs: {[p.title for p in db.query(Program).all()]}")
db.close()
