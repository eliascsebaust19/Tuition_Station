# Tuition Marketplace System - Technical Specification

## Project Overview
An offline tuition marketplace connecting home tutors with students based on location, subject, and budget. Built with Python Flask (Backend) and a modern HTML/CSS/JS frontend.

## 1. Backend Architecture (Flask)
- **Framework:** Flask
- **Database:** SQLite (SQLAlchemy ORM)
- **Authentication:** Flask-Login with password hashing (Werkzeug)
- **Routing:**
    - `/`: Landing Page
    - `/login`, `/register`: Authentication
    - `/student/dashboard`: Student panel
    - `/student/search`: Search results with filters
    - `/teacher/dashboard`: Teacher panel
    - `/teacher/profile/edit`: Profile management
    - `/admin`: Basic admin panel

## 2. Database Models
- **User:** `id, email, password, role (student/teacher), created_at`
- **TeacherProfile:** `id, user_id, full_name, subjects (comma-separated), location, hourly_rate, bio, availability (bool), rating`
- **TuitionRequest:** `id, student_id, teacher_id, subject, status (pending/accepted/rejected), message, timestamp`
- **Review:** `id, student_id, teacher_id, rating, comment`

## 3. UI/UX Style Guide
- **Theme:** Professional, trustworthy, modern startup aesthetic.
- **Color Palette:** Trust Blue (#2563eb), Success Green (#10b981), Neutral Grays for typography.
- **Components:** Card-based layouts, sidebar navigation for dashboards, sticky headers.
- **Frameworks:** Tailwind CSS (via CDN) for rapid styling and responsiveness, FontAwesome for icons.

## 4. Folder Structure
```text
/tuition_marketplace
│
├── app.py              # Main Flask application & routes
├── models.py           # Database schemas
├── forms.py            # Flask-WTF forms
├── /static
│   ├── /css
│   ├── /js
│   └── /img
└── /templates
    ├── base.html       # Shared layout
    ├── index.html      # Landing page
    ├── login.html
    ├── register.html
    ├── /student
    │   ├── dashboard.html
    │   └── search.html
    └── /teacher
        ├── dashboard.html
        └── profile.html
```

## 5. Sample Data Strategy
- Populate 5-10 teacher profiles across different subjects (Math, Science, English).
- Sample locations: "Downtown", "Uptown", "North Suburbs".
