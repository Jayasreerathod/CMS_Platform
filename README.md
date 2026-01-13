## LessonCMS — Full Stack Content Management Platform

A full-stack CMS for managing lessons and publishing them to a public catalog.
Built with FastAPI + PostgreSQL + SQLAlchemy + React (Vite) + Tailwind.
Deployed using Render (backend) and Vercel (frontend).

## Architecture Overview

            ┌──────────────────────────────────────────────────┐
            │                     FRONTEND                     │
            │ React + Vite + Tailwind                          │
            │ Deployed on Vercel                               │
            │ Calls REST API via Axios                         │
            └───────────────▲──────────────────────────────────┘
                            │ HTTPS (CORS enabled)
            ┌───────────────┴──────────────────────────────────┐
            │                    BACKEND                       │
            │ FastAPI + SQLAlchemy + Alembic                   │
            │ Auth (RBAC: Admin / Editor )             │
            │ CRUD for Programs / Lessons                      │
            │ Scheduled publishing via Background Worker       │
            │ Deployed on Render                               │
            └───────────────▲──────────────────────────────────┘
                            │ SQLAlchemy ORM
            ┌───────────────┴──────────────────────────────────┐
            │                   DATABASE                       │
            │ PostgreSQL (Render Datastore)                    │
            │ Tables: users, programs, lessons, schedules      │
            │ Constraints, indexes, timestamps, relations      │
            └──────────────────────────────────────────────────┘

##  Local Setup

###  Clone the Repository
git clone https://github.com/Jayasreerathod/CMS_Platform.git
cd CMS_Platform

## Backend Setup 
cd backend
python -m venv venv

venv\Scripts\activate     # on Windows
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
npm run dev

## Configure .env in the frontend
VITE_API_BASE_URL=https://cms-platform-backend.onrender.com

## Deployed URLs 
    
 **Frontend (Vercel)**    | 🔗 [https://cms-platform-phi.vercel.app](https://cms-platform-phi.vercel.app)                       
 **Backend API (Render)** | 🔗 [https://cms-platform-backend.onrender.com](https://cms-platform-backend.onrender.com)            **Docs**                 | 🔗 [https://cms-platform-backend.onrender.com/docs](https://cms-platform-backend.onrender.com/docs) 


## Demo Flow

1. Authenticate via Backend (Recommended First Step)
    Go to  https://cms-platform-backend.onrender.com/docs
    Under POST /auth/login, test credentials:
    admin@cms.com / admin123
    editor@cms.com / editor123
    Confirm you receive a valid token and role in the response.
    Once verified, proceed to frontend login.

2 Login as Editor or Admin
    Go to frontend login page
    Use admin@cms.com / admin123
    or editor@cms.com / editor123

3 Create or Edit a Lesson/Program
    Navigate to CMS Dashboard
    Add a new Program and Lessons

4 Schedule or Publish the Program
    Editors can schedule lessons for future publishing
    Admins can publish 
    
5 Worker Executes
    A background worker checks for scheduled lessons
    Once time is reached → lessons auto-publish

6 Verify
    Revisit Public Catalog
    Published lessons now visible to everyone