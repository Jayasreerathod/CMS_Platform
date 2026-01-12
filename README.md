##LessonCMS — Full Stack Content Management Platform

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
            │ Auth (RBAC: Admin / Editor / Viewer)             │
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
# source venv/bin/activate  # on macOS/Linux
pip install -r requirements.txt

## Run Database Migration 
#if using SQLite(local)
python -m app.database

#if using Alembic migration 
alembic upgrade head

## Seed Data
python seed_data.py

This creates:
Programs: Python Basics, Advanced React
Lessons under each program

## Test users:
admin@cms.com / admin123
editor@cms.com / editor123
viewer@cms.com / viewer123

## Run Backend Server 
uvicorn app.main:app --reload

## Deployed URLs 
    
 **Frontend (Vercel)**    | 🔗 [https://cms-platform-phi.vercel.app](https://cms-platform-phi.vercel.app)                       
 **Backend API (Render)** | 🔗 [https://cms-platform-backend.onrender.com](https://cms-platform-backend.onrender.com)            **Docs**                 | 🔗 [https://cms-platform-backend.onrender.com/docs](https://cms-platform-backend.onrender.com/docs) 


## Demo Flow

1️ Login as Editor

    Go to frontend login

    Use admin@cms.com / admin123

2️ Create or Edit a Lesson/Program

    Navigate to CMS Dashboard

    Add a new lesson, set it to draft

3️ Publish the Program

4️ Worker Executes

    Background worker marks lessons as “published” after scheduled time

5️ Verify

    Revisit Public Catalog

    Published lessons now visible to everyone