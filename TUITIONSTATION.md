🎓 TuitionStation Project Documentation

Location-Based Offline Tuition Marketplace

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [Database Schema](#4-database-schema)
5. [Frontend — HTML, CSS, JS](#5-frontend--html-css-js)
6. [Backend — Python Flask](#6-backend--python-flask)
7. [Features Breakdown](#7-features-breakdown)
   - [Student Dashboard](#71-student-dashboard)
   - [Teacher Dashboard](#72-teacher-dashboard)
   - [Admin Dashboard](#73-admin-dashboard)
8. [Google Authentication](#8-google-authentication)
9. [Email Notification System](#9-email-notification-system)
10. [Public Landing Page (/landing)](#10-public-landing-page-landing)
11. [Available Routes](#11-available-routes)
12. [Setup & Installation](#12-setup--installation)
13. [Test Credentials](#13-test-credentials)
14. [Design System](#14-design-system)
15. [Update History](#15-update-history)
16. [Roadmap / Next Steps](#16-roadmap--next-steps)

---

## 1. Project Overview

**TuitionStation** is a full-stack web application that connects students with nearby home tutors. Students can search tutors by subject, location, and budget. Teachers can manage their profile, set availability, and accept/reject student requests. An admin panel provides full system oversight.

### 🎯 Problem Statement
- Students struggle to find qualified home tutors locally — they rely on word-of-mouth or expensive centers.
- Teachers have no centralized platform to connect with students seeking their expertise.

### ✅ Solution
A location-based marketplace that makes tutor discovery efficient and builds direct connections between students and teachers — with real-time notifications, Google login, and a professional admin panel.

---

## 2. Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.8+, Flask 2.3.3 |
| **Database** | Firebase Firestore (NoSQL) |
| **Authentication** | Firebase Auth (Email/Password + Google OAuth) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Design System** | Custom "Tuition Station" (Glassmorphism + Editorial) |
| **Icons** | Font Awesome 6+ |
| **Storage** | Firebase Storage (profile pictures, CVs) |
| **Email** | Flask-Mail / SMTP (Gmail) |
| **Session** | Flask-Login |
| **Environment** | python-dotenv |

---

## 3. Project Structure

```
tuition_system/
├── run.py                      # App entry point
├── app.py                      # Flask app factory
├── config.py                   # Config (env, mail, firebase)
├── firebase_config.py          # Firebase SDK init
├── firebase_db.py              # Firestore CRUD operations
├── requirements.txt            # Python dependencies
├── seed.py                     # DB seeding script
├── .env.example                # Environment variable template
├── schema.sql                  # DB schema reference (MySQL)
├── README.md                   # Project readme
├── TUITIONSTATION.md           # This documentation file
├── TODO.md                     # Implementation tracking
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Login, Register, Google OAuth, /landing
│   ├── student.py              # Student routes
│   ├── teacher.py              # Teacher routes
│   ├── admin.py                # Admin routes
│   └── todo.py                 # ToDo tracking
│
├── templates/
│   ├── base.html               # Base layout (nav, footer)
│   ├── index.html              # Landing page
│   ├── login.html
│   ├── register.html
│   ├── developer.html
│   ├── student/
│   │   ├── dashboard.html
│   │   ├── search.html
│   │   ├── teacher_profile.html
│   │   ├── messages.html
│   │   └── edit_profile.html
│   ├── teacher/
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   └── messages.html
│   └── admin/
│       ├── dashboard.html
│       ├── users.html
│       ├── requests.html
│       └── messages.html
│
├── static/
│   ├── css/
│   │   ├── atelier.css         # Tuition Station design system
│   │   └── style.css           # Legacy/global styles
│   ├── js/
│   │   └── main.js             # Vanilla JS (search, auth, UI)
│   ├── Assets/
│   │   └── Image/              # Static images
│   └── uploads/                # User-uploaded files
│
└── instance/
    └── tuition.db              # SQLite fallback (if used)
```

---

## 4. Database Schema

All data is stored in **Firebase Firestore** using the following collections:

### 🔹 `users` Collection
```
users/{uid}
├── uid: string
├── name: string
├── email: string
├── role: "student" | "teacher" | "admin"
├── is_active: boolean
├── created_at: timestamp
├── profile_picture: string (URL)
└── phone: string
```

### 🔹 `teachers` Collection
```
teachers/{uid}
├── uid: string
├── name: string
├── email: string
├── subjects: [string]
├── location: string
├── fee_per_hour: number
├── bio: string
├── availability: "available" | "busy"
├── is_approved: boolean
├── rating: number
├── review_count: number
├── profile_picture: string (URL)
├── cv_url: string (URL)
└── created_at: timestamp
```

### 🔹 `requests` Collection
```
requests/{id}
├── student_id: string
├── teacher_id: string
├── subject: string
├── message: string
├── status: "pending" | "accepted" | "rejected"
└── created_at: timestamp
```

### 🔹 `messages` Collection
```
messages/{id}
├── sender_id: string
├── receiver_id: string
├── content: string
├── is_read: boolean
└── created_at: timestamp
```

### 🔹 `reviews` Collection
```
reviews/{id}
├── student_id: string
├── teacher_id: string
├── rating: number (1–5)
├── comment: string
└── created_at: timestamp
```

---

## 5. Frontend — HTML, CSS, JS

### HTML (Jinja2 Templates)

All pages extend `base.html` using Flask's Jinja2 templating:

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{% block title %}TuitionStation{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/atelier.css') }}"/>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
</head>
<body>
  <nav class="ts-nav">
    <a class="ts-logo" href="{{ url_for('auth.landing') }}">
      <span>Tuition</span><strong>Station</strong>
    </a>
    {% if current_user.is_authenticated %}
      <a href="{{ url_for('auth.logout') }}">Logout</a>
    {% else %}
      <a href="{{ url_for('auth.login') }}">Login</a>
      <a href="{{ url_for('auth.register') }}">Register</a>
    {% endif %}
  </nav>

  <main>{% block content %}{% endblock %}</main>

  <footer class="ts-footer">
    <p>&copy; 2024 TuitionStation. All rights reserved.</p>
  </footer>

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

---

### CSS — Tuition Station Design System (`atelier.css`)

```css
/* ── Root Variables ─────────────────────────────── */
:root {
  --ts-primary:      #004ac6;   /* Deep Blue */
  --ts-secondary:    #006c49;   /* Growth Green */
  --ts-surface:      #faf8ff;   /* Soft White */
  --ts-bg:           #faf8ff;
  --ts-text:         #1a1a2e;
  --ts-muted:        #6b7280;
  --ts-border:       #e5e7eb;
  --ts-glass:        rgba(255, 255, 255, 0.72);
  --ts-shadow:       0 4px 24px rgba(0, 74, 198, 0.10);
  --ts-radius:       12px;
  --ts-radius-lg:    20px;
  --ts-font:         'Inter', 'Segoe UI', system-ui, sans-serif;
}

/* ── Global Reset ───────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--ts-font);
  background: var(--ts-bg);
  color: var(--ts-text);
  line-height: 1.6;
}

/* ── Navigation ─────────────────────────────────── */
.ts-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: var(--ts-glass);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 0 var(--ts-border);
}
.ts-logo span { color: var(--ts-primary); font-weight: 400; }
.ts-logo strong { color: var(--ts-secondary); font-weight: 800; }

/* ── Cards ──────────────────────────────────────── */
.ts-card {
  background: var(--ts-glass);
  border-radius: var(--ts-radius-lg);
  box-shadow: var(--ts-shadow);
  backdrop-filter: blur(8px);
  padding: 1.5rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.ts-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0, 74, 198, 0.16);
}

/* ── Buttons ─────────────────────────────────────── */
.ts-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.4rem;
  border-radius: var(--ts-radius);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
  text-decoration: none;
}
.ts-btn-primary {
  background: var(--ts-primary);
  color: #fff;
}
.ts-btn-primary:hover { background: #003aa0; transform: translateY(-1px); }
.ts-btn-secondary {
  background: transparent;
  color: var(--ts-primary);
  border: 2px solid var(--ts-primary);
}
.ts-btn-secondary:hover { background: var(--ts-primary); color: #fff; }

/* ── Form Inputs ─────────────────────────────────── */
.ts-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1.5px solid var(--ts-border);
  border-radius: var(--ts-radius);
  font-size: 0.95rem;
  background: #fff;
  transition: border-color 0.2s ease;
  outline: none;
}
.ts-input:focus { border-color: var(--ts-primary); }

/* ── Hero Section ───────────────────────────────── */
.ts-hero {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #f0f4ff 0%, #e8f5f0 100%);
}
.ts-hero h1 {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 800;
  color: var(--ts-text);
  margin-bottom: 1rem;
  line-height: 1.2;
}
.ts-hero p {
  font-size: 1.15rem;
  color: var(--ts-muted);
  max-width: 520px;
  margin-bottom: 2rem;
}

/* ── Grid ────────────────────────────────────────── */
.ts-grid { display: grid; gap: 1.5rem; }
.ts-grid-3 { grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }
.ts-grid-2 { grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); }

/* ── Badge / Status ──────────────────────────────── */
.ts-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.03em;
}
.ts-badge-green  { background: #d1fae5; color: #065f46; }
.ts-badge-blue   { background: #dbeafe; color: #1e40af; }
.ts-badge-red    { background: #fee2e2; color: #991b1b; }
.ts-badge-yellow { background: #fef3c7; color: #92400e; }

/* ── Star Rating ─────────────────────────────────── */
.ts-stars { color: #f59e0b; font-size: 0.9rem; }

/* ── Responsive ──────────────────────────────────── */
@media (max-width: 768px) {
  .ts-nav { flex-wrap: wrap; gap: 0.5rem; }
  .ts-hero h1 { font-size: 2rem; }
  .ts-grid-3, .ts-grid-2 { grid-template-columns: 1fr; }
}
```

---

### JavaScript (`main.js`)

```javascript
// ── Live Search Filter ────────────────────────────
function initSearch() {
  const input = document.getElementById('searchInput');
  if (!input) return;
  input.addEventListener('input', function () {
    const query = this.value.toLowerCase();
    document.querySelectorAll('.teacher-card').forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(query) ? '' : 'none';
    });
  });
}

// ── Flash Message Auto-Dismiss ────────────────────
function initFlashMessages() {
  setTimeout(() => {
    document.querySelectorAll('.ts-alert').forEach(el => {
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 300);
    });
  }, 4000);
}

// ── Profile Picture Preview ───────────────────────
function initImagePreview() {
  const fileInput = document.getElementById('profile_picture');
  if (!fileInput) return;
  fileInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = e => {
      const preview = document.getElementById('imagePreview');
      if (preview) preview.src = e.target.result;
    };
    reader.readAsDataURL(file);
  });
}

// ── Google Sign-In Button Loader ──────────────────
function initGoogleAuth() {
  const btn = document.getElementById('googleSignInBtn');
  if (!btn) return;
  btn.addEventListener('click', function () {
    this.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Signing in...';
    this.disabled = true;
  });
}

// ── Availability Toggle ───────────────────────────
function initAvailabilityToggle() {
  const toggle = document.getElementById('availabilityToggle');
  if (!toggle) return;
  toggle.addEventListener('change', function () {
    const status = this.checked ? 'available' : 'busy';
    fetch('/teacher/availability', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    }).then(res => res.json())
      .then(data => {
        const label = document.getElementById('availabilityLabel');
        if (label) label.textContent = data.status === 'available' ? 'Available' : 'Busy';
      });
  });
}

// ── Init All ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initSearch();
  initFlashMessages();
  initImagePreview();
  initGoogleAuth();
  initAvailabilityToggle();
});
```

---

## 6. Backend — Python Flask

### App Factory (`app.py`)

```python
from flask import Flask
from flask_login import LoginManager
from config import Config
from firebase_config import init_firebase

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_firebase()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.teacher import teacher_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
```

### Configuration (`config.py`)

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # Firebase
    FIREBASE_API_KEY             = os.getenv('FIREBASE_API_KEY')
    FIREBASE_AUTH_DOMAIN         = os.getenv('FIREBASE_AUTH_DOMAIN')
    FIREBASE_PROJECT_ID          = os.getenv('FIREBASE_PROJECT_ID')
    FIREBASE_STORAGE_BUCKET      = os.getenv('FIREBASE_STORAGE_BUCKET')
    FIREBASE_MESSAGING_SENDER_ID = os.getenv('FIREBASE_MESSAGING_SENDER_ID')
    FIREBASE_APP_ID              = os.getenv('FIREBASE_APP_ID')
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    # Flask-Mail (Gmail SMTP)
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
```

### Auth Routes (`routes/auth.py`)

```python
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from firebase_db import get_user_by_email, create_user
from utils.email_utils import send_welcome_email
import firebase_admin.auth as fb_auth

auth_bp = Blueprint('auth', __name__)

# ── Landing (Always Public) ───────────────────────
@auth_bp.route('/landing')
def landing():
    from firebase_db import get_all_teachers
    teachers = get_all_teachers(limit=6)
    return render_template('index.html', teachers=teachers)

# ── Home (Redirect Based on Role) ────────────────
@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        role = current_user.role
        if role == 'student':
            return redirect(url_for('student.dashboard'))
        elif role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        elif role == 'admin':
            return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.landing'))

# ── Login ─────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        try:
            user = fb_auth.get_user_by_email(email)
            db_user = get_user_by_email(email)
            if db_user and db_user.get('is_active', True):
                login_user(db_user)
                flash('Welcome back!', 'success')
                return redirect(url_for('auth.index'))
            else:
                flash('Account is blocked. Contact admin.', 'danger')
        except Exception:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

# ── Register ──────────────────────────────────────
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form.get('name')
        email    = request.form.get('email')
        password = request.form.get('password')
        role     = request.form.get('role', 'student')
        try:
            fb_user = fb_auth.create_user(email=email, password=password,
                                          display_name=name)
            create_user(uid=fb_user.uid, name=name, email=email, role=role)
            send_welcome_email(email, name)
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
    return render_template('register.html')

# ── Google OAuth ──────────────────────────────────
@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    id_token = request.json.get('idToken')
    try:
        decoded = fb_auth.verify_id_token(id_token)
        uid   = decoded['uid']
        email = decoded.get('email')
        name  = decoded.get('name', 'User')
        db_user = get_user_by_email(email)
        if not db_user:
            create_user(uid=uid, name=name, email=email, role='student')
            send_welcome_email(email, name)
            db_user = get_user_by_email(email)
        login_user(db_user)
        return {'status': 'ok', 'redirect': url_for('auth.index')}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400

# ── Logout ────────────────────────────────────────
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.landing'))
```

---

## 7. Features Breakdown

### 7.1 Student Dashboard

**Route:** `/student/dashboard`

**Features:**
- View active tuition requests with status badges (Pending / Accepted / Rejected)
- Quick search bar to find tutors by subject or location
- Saved/favorite teacher list
- Unread message count indicator
- Recent activity timeline

**Code snippet (`routes/student.py`):**
```python
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from firebase_db import get_requests_by_student, get_messages_for_user

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard():
    requests = get_requests_by_student(current_user.uid)
    unread   = get_messages_for_user(current_user.uid, unread_only=True)
    return render_template('student/dashboard.html',
                           requests=requests,
                           unread_count=len(unread))
```

**Student Features:**
- 🔍 Search tutors by subject, location, and max hourly fee
- 🎛️ Multi-filter with AND logic
- 👤 View full teacher profile (ratings, bio, CV download)
- 📩 Send tuition request with custom message
- 💬 In-app messaging with teachers
- ⭐ Rate and review teachers (1–5 stars)
- 🔖 Save favorite tutors

---

### 7.2 Teacher Dashboard

**Route:** `/teacher/dashboard`

**Features:**
- Profile completion progress bar
- Toggle availability status (Available / Busy)
- Incoming request list with Accept / Reject actions
- Student messages inbox
- Rating overview with recent reviews

**Code snippet (`routes/teacher.py`):**
```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from firebase_db import (get_teacher_profile, get_requests_for_teacher,
                          update_request_status, update_teacher_availability)
from utils.email_utils import send_request_status_email

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    profile  = get_teacher_profile(current_user.uid)
    requests = get_requests_for_teacher(current_user.uid)
    return render_template('teacher/dashboard.html',
                           profile=profile, requests=requests)

@teacher_bp.route('/request/<request_id>/<action>')
@login_required
def handle_request(request_id, action):
    if action not in ('accept', 'reject'):
        flash('Invalid action.', 'danger')
        return redirect(url_for('teacher.dashboard'))
    update_request_status(request_id, action)
    # Send email notification to student
    req = get_request_by_id(request_id)
    send_request_status_email(req['student_email'], action)
    flash(f'Request {action}ed successfully.', 'success')
    return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/availability', methods=['POST'])
@login_required
def set_availability():
    from flask import jsonify
    status = request.json.get('status', 'available')
    update_teacher_availability(current_user.uid, status)
    return jsonify({'status': status})
```

**Teacher Features:**
- 📝 Create/edit professional profile (subjects, fee, location, bio)
- 🖼️ Upload profile picture (Firebase Storage)
- 📄 Upload CV / resume (Firebase Storage)
- ✅ Accept or ❌ Reject student requests
- 🟢 Set availability status (Available / Busy)
- 💬 View and reply to student messages
- ⭐ View all reviews from students

---

### 7.3 Admin Dashboard

**Route:** `/admin/dashboard`

**Features:**
- System statistics: total users, teachers, students, requests
- User management: activate, block, or delete users
- Teacher approval workflow
- All requests overview
- All messages overview

**Code snippet (`routes/admin.py`):**
```python
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from firebase_db import (get_all_users, toggle_user_status, delete_user,
                          approve_teacher, get_all_requests, get_all_messages,
                          get_stats)

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = get_stats()
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
@admin_required
def users():
    all_users = get_all_users()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/user/<uid>/toggle')
@admin_required
def toggle_user(uid):
    toggle_user_status(uid)
    flash('User status updated.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/teacher/<uid>/approve')
@admin_required
def approve(uid):
    approve_teacher(uid)
    flash('Teacher profile approved.', 'success')
    return redirect(url_for('admin.users'))
```

**Admin Features:**
- 📊 Dashboard statistics card grid
- 👥 View and manage all users (filter by role)
- 🔒 Activate / Block users
- 🗑️ Delete users
- ✅ Approve teacher profiles before they appear in search
- 📋 Monitor all tuition requests
- 💬 Monitor all messages

---

## 8. Google Authentication

### Overview
Google OAuth is implemented via **Firebase Authentication** on the frontend using the Firebase JS SDK, and verified on the backend using **Firebase Admin SDK**.

### Frontend (`login.html` + `main.js`)

```html
<!-- Add Firebase SDK in base.html <head> -->
<script src="https://www.gstatic.com/firebasejs/10.0.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.0.0/firebase-auth-compat.js"></script>

<script>
  const firebaseConfig = {
    apiKey:            "{{ config.FIREBASE_API_KEY }}",
    authDomain:        "{{ config.FIREBASE_AUTH_DOMAIN }}",
    projectId:         "{{ config.FIREBASE_PROJECT_ID }}",
    storageBucket:     "{{ config.FIREBASE_STORAGE_BUCKET }}",
    messagingSenderId: "{{ config.FIREBASE_MESSAGING_SENDER_ID }}",
    appId:             "{{ config.FIREBASE_APP_ID }}"
  };
  firebase.initializeApp(firebaseConfig);
</script>
```

```javascript
// Google Sign-In
document.getElementById('googleSignInBtn').addEventListener('click', async () => {
  const provider = new firebase.auth.GoogleAuthProvider();
  try {
    const result = await firebase.auth().signInWithPopup(provider);
    const idToken = await result.user.getIdToken();

    // Send token to Flask backend
    const res = await fetch('/google-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idToken })
    });
    const data = await res.json();
    if (data.status === 'ok') window.location.href = data.redirect;
    else alert('Login failed: ' + data.message);
  } catch (err) {
    console.error('Google sign-in error:', err);
  }
});
```

### Backend Verification (`routes/auth.py`)

```python
import firebase_admin.auth as fb_auth

@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    id_token = request.json.get('idToken')
    try:
        decoded = fb_auth.verify_id_token(id_token)
        uid   = decoded['uid']
        email = decoded.get('email')
        name  = decoded.get('name', 'User')
        # Auto-register if first time
        db_user = get_user_by_email(email)
        if not db_user:
            create_user(uid=uid, name=name, email=email, role='student')
            send_welcome_email(email, name)
            db_user = get_user_by_email(email)
        login_user(db_user)
        return {'status': 'ok', 'redirect': url_for('auth.index')}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400
```

### `.env` Keys Required
```env
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/serviceAccountKey.json
```

---

## 9. Email Notification System

Email notifications are sent using **Flask-Mail** via Gmail SMTP.

### Setup (`utils/email_utils.py`)

```python
from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_welcome_email(to_email: str, name: str):
    """Sent after successful registration (email or Google)."""
    msg = Message(
        subject='Welcome to TuitionStation! 🎓',
        recipients=[to_email],
        html=f"""
        <div style="font-family: Arial, sans-serif; max-width: 520px; margin: auto;">
          <h2 style="color: #004ac6;">Welcome, {name}!</h2>
          <p>Your account on <strong>TuitionStation</strong> has been created successfully.</p>
          <p>Start exploring tutors or set up your teacher profile today.</p>
          <a href="https://yourdomain.com" style="
            display:inline-block; padding:10px 24px;
            background:#004ac6; color:#fff;
            border-radius:8px; text-decoration:none;
            font-weight:600; margin-top:12px;">
            Go to Dashboard
          </a>
          <hr style="margin-top:24px; border:none; border-top:1px solid #e5e7eb;"/>
          <small style="color:#6b7280;">TuitionStation — Connecting Students & Teachers</small>
        </div>
        """
    )
    mail.send(msg)

def send_request_status_email(to_email: str, action: str):
    """Sent to student when teacher accepts or rejects their request."""
    status_text = "accepted ✅" if action == 'accept' else "rejected ❌"
    color       = "#006c49" if action == 'accept' else "#dc2626"
    msg = Message(
        subject=f'Your Tuition Request has been {status_text}',
        recipients=[to_email],
        html=f"""
        <div style="font-family: Arial, sans-serif; max-width: 520px; margin: auto;">
          <h2 style="color: {color};">Request {status_text.capitalize()}</h2>
          <p>Your tuition request has been <strong>{status_text}</strong> by the teacher.</p>
          <a href="https://yourdomain.com/student/dashboard" style="
            display:inline-block; padding:10px 24px;
            background:{color}; color:#fff;
            border-radius:8px; text-decoration:none;
            font-weight:600; margin-top:12px;">
            View Dashboard
          </a>
        </div>
        """
    )
    mail.send(msg)

def send_new_message_email(to_email: str, sender_name: str):
    """Sent when a new message is received."""
    msg = Message(
        subject=f'New message from {sender_name} on TuitionStation',
        recipients=[to_email],
        html=f"""
        <div style="font-family: Arial, sans-serif; max-width: 520px; margin: auto;">
          <h2 style="color: #004ac6;">You have a new message 💬</h2>
          <p><strong>{sender_name}</strong> sent you a message on TuitionStation.</p>
          <a href="https://yourdomain.com/student/messages" style="
            display:inline-block; padding:10px 24px;
            background:#004ac6; color:#fff;
            border-radius:8px; text-decoration:none;
            font-weight:600; margin-top:12px;">
            Read Message
          </a>
        </div>
        """
    )
    mail.send(msg)
```

### `.env` Keys Required
```env
MAIL_USERNAME=yourapp@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

> ⚠️ Use a **Gmail App Password**, not your regular Gmail password. Enable 2FA → App Passwords in your Google Account.

### Triggered Events

| Event | Recipient | Email |
|---|---|---|
| New registration | New user | Welcome email |
| Google sign-in (first time) | New user | Welcome email |
| Request accepted | Student | Request accepted |
| Request rejected | Student | Request rejected |
| New message received | Recipient | New message alert |

---

## 10. Public Landing Page (/landing)

Added as a separate always-public route so even logged-in users can preview the landing page.

```python
# routes/auth.py
@auth_bp.route('/landing')
def landing():
    from firebase_db import get_all_teachers
    teachers = get_all_teachers(limit=6)
    return render_template('index.html', teachers=teachers)
```

**Sections:**
1. **Hero** — headline, subtext, CTA buttons (Student / Teacher signup)
2. **Search Bar** — search by subject + location (no login required)
3. **Featured Tutors** — grid of top-rated teacher cards
4. **How It Works** — 3-step visual guide
5. **Footer** — links and branding

---

## 11. Available Routes

### Public Routes
| Route | Method | Description |
|---|---|---|
| `/` | GET | Home (redirects by role) |
| `/landing` | GET | Public landing page preview |
| `/login` | GET/POST | Login page |
| `/register` | GET/POST | Registration page |
| `/google-login` | POST | Google OAuth endpoint |
| `/logout` | GET | Logout user |

### Student Routes (Login Required)
| Route | Method | Description |
|---|---|---|
| `/student/dashboard` | GET | Student dashboard |
| `/student/search` | GET | Search tutors |
| `/student/teacher/<id>` | GET | View teacher profile |
| `/student/request/<id>` | POST | Send tuition request |
| `/student/review/<id>` | POST | Add review |
| `/student/messages` | GET | View messages |
| `/student/send_message/<id>` | POST | Send message to teacher |
| `/student/profile/edit` | GET/POST | Edit student profile |

### Teacher Routes (Login Required)
| Route | Method | Description |
|---|---|---|
| `/teacher/dashboard` | GET | Teacher dashboard |
| `/teacher/profile` | GET/POST | Manage profile |
| `/teacher/upload-picture` | POST | Upload profile picture |
| `/teacher/upload-cv` | POST | Upload CV |
| `/teacher/request/<id>/<action>` | GET | Accept/reject request |
| `/teacher/availability` | POST | Toggle availability |
| `/teacher/messages` | GET | View messages |
| `/teacher/reply_message/<id>` | POST | Reply to student |

### Admin Routes (Admin Role Required)
| Route | Method | Description |
|---|---|---|
| `/admin/dashboard` | GET | Admin dashboard |
| `/admin/users` | GET | Manage all users |
| `/admin/user/<id>/toggle` | GET | Activate/block user |
| `/admin/user/<id>/delete` | GET | Delete user |
| `/admin/teacher/<id>/approve` | GET | Approve teacher |
| `/admin/requests` | GET | View all requests |
| `/admin/messages` | GET | View all messages |

---

## 12. Setup & Installation

### Prerequisites
- Python 3.8+
- pip
- Firebase project (Firestore + Auth + Storage enabled)
- Gmail account (for email notifications)
- Node.js (optional, for frontend tooling)

### Step-by-Step

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/tuition_system.git
cd tuition_system

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
copy .env.example .env
# Edit .env with your Firebase + Gmail credentials

# 5. Seed sample data (optional)
python seed.py

# 6. Run the app
python run.py
# → http://localhost:5000
```

### Reset Database
```bash
python seed.py --reset
```

---

## 13. Test Credentials

| Role | Email | Password | Purpose |
|---|---|---|---|
| Admin | admin@tuition.com | admin123 | Full system access |
| Student | rahim@student.com | password123 | Search tutors, send requests |
| Student | karim@student.com | password123 | Alternative student account |
| Teacher | ahmed@tutor.com | password123 | Manage profile, handle requests |
| Teacher | sarah@tutor.com | password123 | Alternative teacher account |

---

## 14. Design System

**"Tuition Station"** — Premium editorial design language.

| Principle | Description |
|---|---|
| Editorial Sophistication | Intentional asymmetry, high-contrast typography |
| No-Line Design | Boundaries via tonal surface layers, not borders |
| Glassmorphism | Blurred, translucent card surfaces |
| Ambient Shadows | Soft layered depth, not hard drop shadows |

### Color Palette
| Token | Value | Usage |
|---|---|---|
| `--ts-primary` | `#004ac6` | CTAs, links, active states |
| `--ts-secondary` | `#006c49` | Success, growth, accept |
| `--ts-surface` | `#faf8ff` | Page backgrounds |
| `--ts-text` | `#1a1a2e` | Body text |
| `--ts-muted` | `#6b7280` | Secondary text |

---

## 15. Update History

| Version | Date | Changes |
|---|---|---|
| v1.0 | Initial | Base Flask + Firebase setup, student & teacher auth |
| v1.1 | — | Student search with multi-filter |
| v1.2 | — | Teacher profile + file uploads (Firebase Storage) |
| v1.3 | — | In-app messaging system |
| v1.4 | — | Review & rating system |
| v1.5 | — | Admin dashboard with user management |
| v1.6 | — | Google OAuth (Firebase + backend token verify) |
| v1.7 | — | Email notification system (Flask-Mail) |
| v1.8 | — | `/landing` public route — always accessible regardless of login state |
| v1.9 | — | Nav logo updated to point to `auth.landing` in base.html & index.html |

---

## 16. Roadmap / Next Steps

- [ ] **Payment Integration** — bKash / Stripe for booking fee collection
- [ ] **Advanced Matching** — AI-based tutor recommendation by subject & location
- [ ] **Mobile App** — React Native or Flutter client
- [ ] **Real-time Chat** — Firebase Realtime DB or Socket.IO
- [ ] **Video Sessions** — WebRTC or Jitsi integration
- [ ] **SMS Notifications** — Twilio or BD SMS gateway
- [ ] **Multi-language** — Bangla (বাংলা) + English support
- [ ] **Production Deployment** — Railway / Render / VPS with Gunicorn + Nginx

---

## 📄 License

MIT License © 2024 TuitionStation

---

**Built with ❤️ for connecting students and teachers across Bangladesh**
