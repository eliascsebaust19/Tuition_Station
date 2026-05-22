# Project Entry Point, Database Seeding, and Documentation

## Overview
Create the application entry point (`run.py`), database seeding script (`seed.py`), environment configuration template (`.env.example`), and comprehensive README documentation to enable developers to launch the Flask application and populate it with realistic test data in minutes.

## Problem Statement
Developers cannot currently start the application or test it with realistic data. Without clear setup instructions, entry points, and sample data, onboarding is blocked and manual testing requires tedious data creation.

## Solution
Provide a complete bootstrap package: a simple Flask entry point, an automated seeding script with sample students/teachers/requests, environment configuration guidance, and step-by-step documentation covering installation, configuration, running the app, and testing with provided credentials.

---

## Functional Requirements

### run.py - Flask Application Entry Point
- **Purpose**: Single command to start the Flask development server
- **Behavior**:
  - Import Flask app from `app/__init__.py` (or appropriate app factory location)
  - Load environment variables from `.env` file using `python-dotenv`
  - Initialize database (create tables if they don't exist)
  - Start Flask development server on `localhost:5000` with debug mode enabled
  - Display startup message with app URL and available routes
- **Execution**: `python run.py` from project root
- **Output**: Flask server running, accessible at `http://localhost:5000`

### seed.py - Database Seeding Script
- **Purpose**: Populate SQLite database with realistic sample data for testing
- **Data to Create**:
  - **5 Student accounts** with:
    - Name, email, password (hashed), location, budget range, subjects of interest
    - Example: "Alice Chen, alice@example.com, location: Downtown, budget: $20-30/hr, subjects: Math, Physics"
  - **5 Teacher accounts** with:
    - Name, email, password (hashed), location, hourly rate, subjects offered, bio
    - Example: "Bob Smith, bob@example.com, location: Downtown, rate: $25/hr, subjects: Math, Chemistry, bio: 10 years experience"
  - **8-10 Tuition Requests** with:
    - Student-to-teacher requests in various states (pending, accepted, rejected)
    - Mix of recent and older requests
    - Example: "Alice requests Bob for Math tutoring, pending since 2 days ago"
- **Behavior**:
  - Clear existing data (optional flag: `--reset` to drop and recreate tables)
  - Create sample users with deterministic test credentials (e.g., `student1@test.com / password123`)
  - Create requests linking students to teachers
  - Print summary of created data (e.g., "Created 5 students, 5 teachers, 10 requests")
- **Execution**: `python seed.py` or `python seed.py --reset` from project root
- **Idempotency**: Safe to run multiple times; either skips existing data or resets on `--reset` flag

### .env.example - Environment Configuration Template
- **Purpose**: Guide developers on required environment variables
- **Content**:
  ```
  FLASK_ENV=development
  FLASK_APP=app
  SECRET_KEY=your-secret-key-here-change-in-production
  DATABASE_URL=sqlite:///tuition_marketplace.db
  DEBUG=True
  ```
- **Usage**: Copy to `.env` and customize for local development
- **Note**: `.env` is in `.gitignore`; `.env.example` is committed to repo

### README.md - Comprehensive Documentation
- **Sections**:
  1. **Project Overview** (1-2 sentences): What the app does, who it's for
  2. **Quick Start** (5 steps):
     - Clone repo
     - Create virtual environment
     - Install dependencies (`pip install -r requirements.txt`)
     - Run seeding script (`python seed.py`)
     - Start app (`python run.py`)
  3. **Setup Instructions** (detailed):
     - Python version requirement (3.8+)
     - Virtual environment creation
     - Dependency installation
     - Environment configuration (copy `.env.example` to `.env`)
  4. **Running the Application**:
     - Command: `python run.py`
     - Access: `http://localhost:5000`
     - Debug mode enabled by default
  5. **Test Credentials** (table format):
| Role    | Email             | Password    | Purpose                             |
| ------- | ----------------- | ----------- | ----------------------------------- |
| Student | student1@test.com | password123 | Search tutors, send requests        |
| Student | student2@test.com | password123 | Alternative student account         |
| Teacher | teacher1@test.com | password123 | Manage profile, respond to requests |
| Teacher | teacher2@test.com | password123 | Alternative teacher account         |
| Admin   | admin@test.com    | password123 | User management (if applicable)     |
  6. **Database Seeding**:
     - Purpose: Populate with sample data
     - Command: `python seed.py`
     - Reset: `python seed.py --reset`
     - Sample data includes: 5 students, 5 teachers, 10 requests in various states
  7. **Project Structure** (tree view):
     ```
     tuition-marketplace/
     ├── app/
     │   ├── __init__.py
     │   ├── models.py
     │   ├── routes/
     │   └── templates/
     ├── run.py
     ├── seed.py
     ├── .env.example
     ├── requirements.txt
     ├── README.md
     └── .gitignore
     ```
  8. **Available Routes** (table or list):
     - Landing page: `/`
     - Register: `/register`
     - Login: `/login`
     - Student dashboard: `/student/dashboard`
     - Teacher dashboard: `/teacher/dashboard`
     - Admin panel: `/admin` (if applicable)
  9. **Troubleshooting**:
     - "Port 5000 already in use" → Change `FLASK_ENV` or kill process
     - "Database locked" → Delete `.db` file and re-seed
     - "Module not found" → Ensure virtual environment is activated
  10. **Next Steps**:
      - Modify test credentials in `seed.py` for custom testing
      - Explore routes and features using test accounts
      - Refer to API documentation (if available) for integration details

---

## Technical Requirements

- **run.py**:
  - Use Flask app factory pattern (import from `app/__init__.py`)
  - Load `.env` using `python-dotenv` (add to `requirements.txt`)
  - Initialize database before starting server
  - Use `if __name__ == '__main__':` guard
  - Set `debug=True` for development

- **seed.py**:
  - Import models from `app.models`
  - Use database session for transactions
  - Hash passwords using werkzeug.security or equivalent
  - Support `--reset` flag via `argparse`
  - Commit changes to database
  - Print clear status messages

- **Dependencies** (add to `requirements.txt`):
  - `python-dotenv` (for `.env` loading)
  - Existing: Flask, SQLAlchemy, werkzeug (for password hashing)

- **File Locations**:
  - `run.py` → Project root
  - `seed.py` → Project root
  - `.env.example` → Project root
  - `README.md` → Project root

---

## Data Model Reference
Sample data structure (for seed.py implementation):

**Student**:
- id, name, email, password_hash, location, budget_min, budget_max, subjects_interested, created_at

**Teacher**:
- id, name, email, password_hash, location, hourly_rate, subjects_offered, bio, created_at

**TuitionRequest**:
- id, student_id, teacher_id, subject, status (pending/accepted/rejected), created_at, updated_at

---

## Acceptance Criteria
- [ ] Given a developer clones the repo, When they run `python run.py`, Then Flask server starts on `localhost:5000` without errors
- [ ] Given a developer runs `python seed.py`, When the script completes, Then database contains 5 students, 5 teachers, and 10 requests with deterministic test credentials
- [ ] Given a developer copies `.env.example` to `.env`, When they modify values, Then Flask app respects the custom configuration
- [ ] Given a developer reads README.md, When they follow Quick Start section, Then they can launch the app and log in with provided test credentials within 5 minutes
- [ ] Given a developer logs in with `student1@test.com / password123`, When they access the student dashboard, Then they see tutors and can send requests
- [ ] Given a developer logs in with `teacher1@test.com / password123`, When they access the teacher dashboard, Then they see incoming requests from students
- [ ] Given a developer runs `python seed.py --reset`, When the script completes, Then database is cleared and repopulated with fresh sample data
- [ ] Given a developer encounters an issue, When they check README Troubleshooting section, Then they find guidance for common problems (port conflicts, database locks, missing modules)