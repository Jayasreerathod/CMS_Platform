## LessonCMS — Full Stack Content Management Platform

A full-stack Lesson Content Management System (LessonCMS) built using FastAPI, React (Vite), and PostgreSQL.
It allows admins to manage educational programs, terms, and lessons — with automatic publishing handled in the background.

## Architecture Overview

            ┌──────────────────────────────────────────────────────────────┐
            │                        FRONTEND (Vercel)                     │
            │──────────────────────────────────────────────────────────────│
            │ • React + Vite + Tailwind CSS                                │
            │ • Axios calls backend REST APIs                              │
            │ • Displays Programs, Lessons & Publish Actions (CMS UI)      │
            │ • Deployed on: https://cms-platform-phi.vercel.app/catalog   |
            └──────────────▲───────────────────────────────────────────────┘
                           │ HTTPS (CORS enabled via FastAPI Middleware)
                           │
            ┌──────────────┴──────────────────────────────────────────────-┐
            │                        BACKEND (Render)                      │
            │──────────────────────────────────────────────────────────────│
            │ • FastAPI + SQLAlchemy ORM                                   │
            │ • REST API Endpoints: Auth, CMS, Catalog                     │
            │ • Role-based Access Control (Admin / Editor)                 │
            │ • Seed script auto-runs at startup if DB empty               │
            │ • Background Worker runs every 60s for scheduled publishing  │
            │ • Deployed on: https://cms-platform-backend.onrender.com     │
            └──────────────▲───────────────────────────────────────────────┘
                           │ SQLAlchemy ORM + psycopg2 (DB Driver)
                           │
            ┌──────────────┴──────────────────────────────────────────────┐
            │                    DATABASE (PostgreSQL - Render)           │
            │─────────────────────────────────────────────────────────────│
            │ • Hosted in Render Datastore                                │
            │ • Tables: programs, terms, lessons, users, assets           │
            │ • Seed data auto-created (Python Basics, Advanced React)    │
            │ • Constraints, enums & timestamps for all relations         │
            └─────────────────────────────────────────────────────────────┘


## Tech Stack
# Backend
FastAPI (Python)
SQLAlchemy ORM
PostgreSQL (hosted on Render)
Gunicorn + Uvicorn (production server)
Background worker for scheduled lesson publishing

# Frontend
React (Vite)
Axios for API communication
Hosted on Vercel

##  Local Setup
###  Clone the Repository
git clone https://github.com/Jayasreerathod/CMS_Platform.git
cd CMS_Platform

## Backend Setup 
cd backend
python -m venv venv
venv\Scripts\activate     # on Windows

## Install Dependencies
pip install -r requirements.txt

## Run Database Migration 
#if using SQLite(local)
python -m app.database

#if using Alembic migration 
alembic upgrade head

## Seed Data
python seed_data.py

This creates:
2 Programs: Python Basics, Advanced React
6 Lessons under the programs
One lesson scheduled to publish automatically (worker demo)
Multi-language and assets examples included

## Database Seeding
( To add initial demo programs and lessons:)

set DATABASE_URL=postgresql://<user>:<password>@<host>/<db_name>
python seed_data.py

## Test users:
admin@cms.com / admin123
editor@cms.com / editor123

### Before Frontend Login
Before logging in from the frontend, first confirm backend authentication works correctly:

Open backend docs:
 https://cms-platform-backend.onrender.com/docs

Expand POST /auth/login

Test login with the above credentials
Once you receive a valid token and role, proceed to login through the frontend

## Run Backend Locally 
uvicorn app.main:app --reload

Local API will run on:
http://127.0.0.1:8000
Docs available at: http://127.0.0.1:8000/docs

## Frontend Setup (Optional Local Run)
cd frontend
npm install
npm run preview

## Configure .env in the frontend
VITE_API_BASE_URL=https://cms-platform-backend.onrender.com

## Deployed URLs 
    
 **Frontend (Vercel)**    | 🔗 [https://cms-platform-phi.vercel.app](https://cms-platform-phi.vercel.app)                       
 **Backend API (Render)** | 🔗 [https://cms-platform-backend.onrender.com](https://cms-platform-backend.onrender.com)           
 **Docs**                 | 🔗 [https://cms-platform-backend.onrender.com/docs](https://cms-platform-backend.onrender.com/docs)
                          | 🔗 [https://cms-platform-backend.onrender.com/redoc](https://cms-platform-backend.onrender.com/redoc)


## Demo Flow

1 Login as Editor or Admin
    Go to frontend login page
    Use the demo credentials:
        Admin : admin@cms.com / admin123
        Editor: editor@cms.com / editor123
2  Create or Edit a Lesson/Program
    Navigate to CMS Dashboard
    Add a new Program and its associated Lessons
3 Schedule or Publish the Program
    Editors can schedule lessons for future publishing
    Admins can immediately publish programs using the Publish button
    When published, the status changes to published and appears in the public catalog   
4 Background Worker Executes Automatically
    A background worker runs every 60 seconds on the backend
    Once the scheduled time is reached →
    The lesson and its parent program are automatically published
5 Verify
    Revisit Public Catalog(frontend)
    You’ll now see all published lessons and programs available to all users
    Scheduled lessons appear automatically once their time is reached
