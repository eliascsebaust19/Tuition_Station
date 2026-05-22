# Complete Implementation Code Package

## Overview
Deliver a production-ready location-based tuition marketplace application with all backend services, frontend interfaces, database initialization, and deployment configuration. The application must be runnable immediately after setup with `python run.py` and accessible at http://localhost:5000.

## Problem Statement
The epic defines the feature set and architecture, but lacks a complete, integrated codebase. Developers need a fully implemented package with all layers (backend models, routes, decorators, config), frontend assets (templates, CSS, JavaScript), database seeding, and documentation to launch the platform.

## Solution
Implement all components as a cohesive package: Flask backend with SQLite persistence, Jinja2 templates with responsive CSS, client-side JavaScript for interactivity, database seeding with realistic sample data, and comprehensive setup documentation.

## Project Structure
```
tuition-marketplace/
├── run.py                          # Entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── README.md                       # Setup and usage instructions
├── app/
│   ├── __init__.py                # Flask app factory
│   ├── config.py                  # Configuration (dev, test, prod)
│   ├── models.py                  # SQLAlchemy models (User, Tutor, Student, Request)
│   ├── decorators.py              # Auth decorators (login_required, role_required)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                # Registration, login, logout
│   │   ├── student.py             # Student dashboard, search, send requests
│   │   ├── teacher.py             # Teacher profile, availability, request management
│   │   ├── admin.py               # Admin user management, statistics
│   │   └── main.py                # Landing page, featured tutors
│   ├── templates/
│   │   ├── base.html              # Base layout (nav, footer, flash messages)
│   │   ├── index.html             # Landing page
│   │   ├── auth/
│   │   │   ├── register.html      # Registration form
│   │   │   └── login.html         # Login form
│   │   ├── student/
│   │   │   ├── dashboard.html     # Student dashboard with search
│   │   │   ├── search_results.html # Tutor search results
│   │   │   └── my_requests.html   # Student's sent requests
│   │   ├── teacher/
│   │   │   ├── dashboard.html     # Teacher dashboard
│   │   │   ├── profile.html       # Teacher profile edit
│   │   │   ├── availability.html  # Availability management
│   │   │   └── requests.html      # Incoming student requests
│   │   └── admin/
│   │       ├── dashboard.html     # Admin dashboard
│   │       └── users.html         # User management table
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css          # Global styles, responsive design
│   │   │   ├── cards.css          # Card component styles
│   │   │   ├── forms.css          # Form styling
│   │   │   └── responsive.css     # Mobile breakpoints
│   │   └── js/
│   │       ├── main.js            # Global utilities, event handlers
│   │       ├── search.js          # Search filtering and AJAX
│   │       ├── forms.js           # Form validation and submission
│   │       └── modal.js           # Modal interactions
│   └── utils/
│       ├── __init__.py
│       └── seed.py                # Database seeding script
└── instance/
    └── tuition_marketplace.db     # SQLite database (created on first run)
```

## Backend Implementation

### Models (app/models.py)
Define SQLAlchemy ORM models with relationships and constraints:

**User** (Base for all users)
- id (Integer, Primary Key)
- username (String, Unique, Not Null)
- email (String, Unique, Not Null)
- password_hash (String, Not Null)
- role (String, Not Null) — "student", "teacher", or "admin"
- created_at (DateTime, Default: now)
- updated_at (DateTime, Default: now, OnUpdate: now)
- Relationships: One-to-One with Student or Tutor (polymorphic or separate tables)

**Student** (Extends User)
- user_id (Integer, Foreign Key → User.id, Primary Key)
- location (String, Not Null) — e.g., "Downtown, City"
- budget_min (Integer) — Minimum budget in currency units
- budget_max (Integer) — Maximum budget in currency units
- subjects_interested (String) — Comma-separated or JSON array
- Relationships: One-to-Many with TuitionRequest (as requester)

**Tutor** (Extends User)
- user_id (Integer, Foreign Key → User.id, Primary Key)
- location (String, Not Null)
- subjects_offered (String) — Comma-separated or JSON array
- hourly_rate (Integer, Not Null)
- bio (Text)
- availability_status (String) — "available", "unavailable", "on_break"
- Relationships: One-to-Many with Availability, One-to-Many with TuitionRequest (as receiver)

**Availability** (Tutor's availability slots)
- id (Integer, Primary Key)
- tutor_id (Integer, Foreign Key → Tutor.user_id, Not Null)
- day_of_week (String, Not Null) — "Monday", "Tuesday", etc.
- start_time (Time, Not Null) — e.g., "09:00"
- end_time (Time, Not Null) — e.g., "17:00"
- is_available (Boolean, Default: True)
- Relationships: Many-to-One with Tutor

**TuitionRequest** (Student request to tutor)
- id (Integer, Primary Key)
- student_id (Integer, Foreign Key → Student.user_id, Not Null)
- tutor_id (Integer, Foreign Key → Tutor.user_id, Not Null)
- subject (String, Not Null)
- message (Text)
- status (String, Not Null) — "pending", "accepted", "rejected", "completed"
- created_at (DateTime, Default: now)
- responded_at (DateTime, Nullable)
- Relationships: Many-to-One with Student, Many-to-One with Tutor

### Routes (app/routes/)

**auth.py** — Authentication
- `GET /register` → Render registration form
- `POST /register` → Create user (student or teacher), hash password, redirect to login
- `GET /login` → Render login form
- `POST /login` → Authenticate, set session, redirect to role-specific dashboard
- `GET /logout` → Clear session, redirect to home

**main.py** — Landing page
- `GET /` → Render landing page with hero, search bar, featured tutors (top 6 by rating or newest)

**student.py** — Student features
- `GET /student/dashboard` → Render student dashboard (requires login, role: student)
- `POST /student/search` → Search tutors by subject, location, budget (AJAX or form submission)
- `GET /student/search-results` → Render search results with tutor cards
- `POST /student/send-request` → Create TuitionRequest, redirect to confirmation
- `GET /student/my-requests` → List student's sent requests with status

**teacher.py** — Teacher features
- `GET /teacher/dashboard` → Render teacher dashboard (requires login, role: teacher)
- `GET /teacher/profile` → Render profile edit form
- `POST /teacher/profile` → Update tutor profile (subjects, rate, bio, location)
- `GET /teacher/availability` → Render availability management form
- `POST /teacher/availability` → Add/update availability slots
- `GET /teacher/requests` → List incoming TuitionRequests with status
- `POST /teacher/requests/<request_id>/accept` → Update request status to "accepted"
- `POST /teacher/requests/<request_id>/reject` → Update request status to "rejected"

**admin.py** — Admin features
- `GET /admin/dashboard` → Render admin dashboard with statistics (requires role: admin)
- `GET /admin/users` → List all users with role, created_at, actions
- `POST /admin/users/<user_id>/delete` → Soft delete or mark inactive
- `POST /admin/users/<user_id>/role` → Change user role

### Decorators (app/decorators.py)
- `@login_required` — Redirect to login if not authenticated
- `@role_required(role)` — Redirect to home if user role doesn't match (e.g., `@role_required('teacher')`)

### Config (app/config.py)
- `SQLALCHEMY_DATABASE_URI` — SQLite path (instance/tuition_marketplace.db)
- `SECRET_KEY` — Session secret (from .env)
- `DEBUG` — From .env (True for dev, False for prod)
- `SQLALCHEMY_TRACK_MODIFICATIONS` — False

### App Factory (app/__init__.py)
- Initialize Flask app
- Configure SQLAlchemy
- Register blueprints (auth, main, student, teacher, admin)
- Set up error handlers (404, 500)

## Frontend Implementation

### Base Template (app/templates/base.html)
- Navigation bar with logo, links (Home, Search, Dashboard, Logout), responsive hamburger menu
- Flash message container for alerts
- Main content block
- Footer with copyright, links

### Landing Page (app/templates/index.html)
- Hero section: headline, subheading, call-to-action buttons (Find Tutors, Become a Tutor)
- Search bar: subject dropdown, location input, budget range, search button
- Featured tutors section: 6 tutor cards (name, subjects, location, rate, "View Profile" button)
- How it works section: 3-step visual guide
- Call-to-action footer

### Authentication Templates
- **register.html**: Form with username, email, password, confirm password, role radio buttons (Student/Teacher), submit button, link to login
- **login.html**: Form with email, password, remember me checkbox, submit button, link to register

### Student Templates
- **dashboard.html**: Search form (subject, location, budget), recent searches, saved tutors (if implemented)
- **search_results.html**: Tutor cards in grid layout (name, subjects, location, rate, reviews count, "Send Request" button)
- **my_requests.html**: Table of sent requests (tutor name, subject, status, date sent, actions)

### Teacher Templates
- **dashboard.html**: Quick stats (profile completeness, pending requests, accepted requests), action buttons (Edit Profile, Manage Availability, View Requests)
- **profile.html**: Form with subjects offered, hourly rate, bio, location, availability status, save button
- **availability.html**: Day-of-week selector, time range inputs (start/end), add/remove slots, save button
- **requests.html**: Table of incoming requests (student name, subject, message, status, accept/reject buttons)

### Admin Templates
- **dashboard.html**: Statistics cards (total users, total students, total tutors, total requests), recent activity log
- **users.html**: Table with columns (ID, Username, Email, Role, Created, Actions), delete/role-change buttons

### CSS (app/static/css/)
- **style.css**: Global styles, typography, color scheme, spacing, button styles
- **cards.css**: Card component (shadow, hover effect, padding, responsive grid)
- **forms.css**: Form inputs, labels, validation states, error messages
- **responsive.css**: Mobile breakpoints (320px, 768px, 1024px), stacked layouts, touch-friendly buttons

### JavaScript (app/static/js/)
- **main.js**: Utility functions, event delegation, flash message auto-dismiss
- **search.js**: Search form submission, filter logic, AJAX calls for live filtering
- **forms.js**: Client-side validation (email, password strength), form submission handlers
- **modal.js**: Modal open/close, confirmation dialogs for delete/reject actions

## Database Seeding (app/utils/seed.py)
Create a seeding script that:
1. Drops existing tables (dev only)
2. Creates all tables
3. Inserts sample data:
   - 3 admin users
   - 10 student users with locations, budgets, interests
   - 10 tutor users with subjects, rates, bios, locations
   - 20 availability slots (2-3 per tutor)
   - 15 tuition requests (mix of pending, accepted, rejected)
4. Commits to database

Run via: `python -c "from app.utils.seed import seed_db; seed_db()"`

## Entry Point (run.py)
```python
import os
from app import create_app, db
from app.utils.seed import seed_db

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Optionally seed on first run
        if not os.path.exists('instance/tuition_marketplace.db'):
            seed_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## Dependencies (requirements.txt)
```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
Werkzeug==2.3.0
python-dotenv==1.0.0
```

## Environment Template (.env.example)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///instance/tuition_marketplace.db
DEBUG=True
```

## Documentation (README.md)
1. **Project Overview**: One-liner, value proposition, key features
2. **Tech Stack**: Flask, SQLite, Jinja2, CSS, JavaScript
3. **Setup Instructions**:
   - Clone repository
   - Create virtual environment: `python -m venv venv`
   - Activate: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
   - Install dependencies: `pip install -r requirements.txt`
   - Copy `.env.example` to `.env` and update SECRET_KEY
   - Run: `python run.py`
   - Access: http://localhost:5000
4. **Project Structure**: Directory tree with descriptions
5. **Database Schema**: Entity relationships (User, Student, Tutor, Availability, TuitionRequest)
6. **API Routes**: Table of all endpoints, methods, parameters, responses
7. **Testing**: Instructions for manual testing key flows
8. **Troubleshooting**: Common issues and solutions

## Acceptance Criteria
- [ ] Given the repository is cloned, When `python run.py` is executed, Then the Flask server starts on http://localhost:5000 without errors
- [ ] Given the server is running, When http://localhost:5000 is accessed in a browser, Then the landing page loads with hero section, search bar, and featured tutors
- [ ] Given a new user visits the site, When they click "Register", Then they can create a student or teacher account and are redirected to login
- [ ] Given a user logs in as a student, When they access /student/dashboard, Then they see the search form and can filter tutors by subject, location, and budget
- [ ] Given a student searches for tutors, When results are displayed, Then each tutor card shows name, subjects, location, hourly rate, and a "Send Request" button
- [ ] Given a student clicks "Send Request", When the form is submitted, Then a TuitionRequest is created with status "pending" and the student receives confirmation
- [ ] Given a user logs in as a teacher, When they access /teacher/dashboard, Then they see their profile, availability, and incoming requests
- [ ] Given a teacher edits their profile, When the form is submitted, Then their subjects, rate, bio, and location are updated in the database
- [ ] Given a teacher manages availability, When they add a time slot, Then it is saved and displayed in their availability list
- [ ] Given a teacher receives a student request, When they click "Accept" or "Reject", Then the request status updates and the student is notified (via dashboard)
- [ ] Given a user logs in as an admin, When they access /admin/dashboard, Then they see user statistics and a list of all users
- [ ] Given an admin views the users list, When they click "Delete" on a user, Then that user is marked inactive or removed
- [ ] Given the database is empty on first run, When `python run.py` is executed, Then the database is initialized with sample data (tutors, students, requests)
- [ ] Given the application is running, When the database file is checked, Then all tables (User, Student, Tutor, Availability, TuitionRequest) exist with correct schema
- [ ] Given a user is logged in, When they click "Logout", Then the session is cleared and they are redirected to the home page
- [ ] Given the application is running, When CSS and JavaScript files are loaded, Then the UI is responsive on mobile (320px), tablet (768px), and desktop (1024px+)
- [ ] Given a form is submitted with invalid data, When validation fails, Then an error message is displayed and the form is not submitted
- [ ] Given the .env.example file exists, When a developer copies it to .env, Then the application can be configured without modifying source code
- [ ] Given requirements.txt is present, When `pip install -r requirements.txt` is run, Then all dependencies are installed and the application can start