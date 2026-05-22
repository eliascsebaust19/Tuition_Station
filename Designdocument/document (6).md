# Complete Implementation Code Package - All Backend & Frontend Files

## Overview
Deliver a fully functional, production-ready codebase for the location-based offline tuition marketplace. This requirement consolidates all backend (Flask, SQLite, authentication, routes, utilities), frontend (HTML templates, CSS design system, JavaScript), and configuration files into a single, executable package that runs with `python run.py`.

## Problem Statement
The marketplace requires a complete, integrated implementation that brings together all individual components (authentication, search, requests, admin) into a cohesive, deployable application. Without a unified codebase package, developers must manually integrate separate pieces, risking inconsistencies, missing dependencies, and incomplete functionality.

## Solution
Create a comprehensive code package with clear folder structure, all required files, proper dependency management, and a working entry point. The package includes backend models and routes, frontend templates and styling, database initialization, and sample data seeding—everything needed to launch the application immediately.

---

## Project Structure

```
tuition-marketplace/
├── app/
│   ├── __init__.py                 # App factory
│   ├── models.py                   # SQLAlchemy models (User, Tutor, Request, etc.)
│   ├── auth.py                     # Authentication routes (register, login, logout)
│   ├── student.py                  # Student routes (search, send requests)
│   ├── teacher.py                  # Teacher routes (profile, availability, requests)
│   ├── admin.py                    # Admin routes (user management, statistics)
│   ├── decorators.py               # Auth decorators (login_required, role_required)
│   ├── errors.py                   # Error handlers (404, 500, etc.)
│   ├── utils.py                    # Utility functions (distance calc, validation)
│   └── templates/
│       ├── base.html               # Base template with nav, footer
│       ├── index.html              # Landing page
│       ├── register.html           # Registration form
│       ├── login.html              # Login form
│       ├── student_dashboard.html  # Student search & requests
│       ├── teacher_dashboard.html  # Teacher profile & requests
│       ├── admin_dashboard.html    # Admin user management
│       └── components/
│           ├── tutor_card.html     # Reusable tutor card
│           ├── request_card.html   # Reusable request card
│           └── navbar.html         # Navigation component
├── static/
│   ├── css/
│   │   ├── style.css               # Main stylesheet (responsive, design system)
│   │   ├── components.css          # Component-specific styles
│   │   └── responsive.css          # Mobile/tablet breakpoints
│   └── js/
│       ├── main.js                 # Global interactivity
│       ├── search.js               # Search filtering logic
│       ├── requests.js             # Request submission & management
│       └── admin.js                # Admin panel interactions
├── config.py                       # Configuration (dev, test, prod)
├── run.py                          # Entry point
├── seed.py                         # Database seeding with sample data
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
└── README.md                       # Setup and usage instructions
```

---

## Backend Implementation

### 1. **config.py** - Configuration Management
- Define `Config` base class with SQLite database path, secret key, session settings
- Create `DevelopmentConfig`, `TestingConfig`, `ProductionConfig` subclasses
- Load environment variables (SECRET_KEY, DATABASE_URL, DEBUG)
- Support for `.env` file via `python-dotenv`

### 2. **app/__init__.py** - App Factory
- Implement Flask app factory pattern
- Initialize SQLAlchemy database
- Register blueprints (auth, student, teacher, admin)
- Register error handlers
- Configure session management and CSRF protection
- Return configured app instance

### 3. **app/models.py** - Database Models
Define SQLAlchemy models with relationships:

| Model              | Fields                                                                                   | Purpose                   |
| ------------------ | ---------------------------------------------------------------------------------------- | ------------------------- |
| **User**           | id, email, password_hash, name, role (student/teacher/admin), created_at                 | Base user entity          |
| **Student**        | id, user_id, budget_min, budget_max, subjects_interested                                 | Student profile           |
| **Tutor**          | id, user_id, subjects_taught, hourly_rate, bio, location_lat, location_lon, availability | Teacher profile           |
| **TuitionRequest** | id, student_id, tutor_id, subject, status (pending/accepted/rejected), created_at        | Request tracking          |
| **Availability**   | id, tutor_id, day_of_week, start_time, end_time                                          | Weekly availability slots |

- Implement relationships (User → Student, User → Tutor, Student → Requests, Tutor → Requests)
- Add timestamps (created_at, updated_at) to all models
- Include password hashing via `werkzeug.security`
- Add model methods: `set_password()`, `check_password()`, `to_dict()` for JSON serialization

### 4. **app/auth.py** - Authentication Routes
- **POST /register**: Accept email, password, name, role; validate input; hash password; create User + Student/Tutor profile; redirect to login
- **POST /login**: Accept email, password; validate credentials; create session; redirect to dashboard
- **GET /logout**: Clear session; redirect to home
- Include CSRF protection on all forms
- Flash messages for success/error feedback

### 5. **app/student.py** - Student Routes
- **GET /student/dashboard**: Render student dashboard with search form
- **GET /api/search**: Query tutors by subject, location (radius), budget; return JSON with tutor cards
- **POST /api/request**: Accept tutor_id, subject; create TuitionRequest; return success/error
- **GET /student/requests**: Show sent requests with status
- Implement distance calculation (haversine formula) for location-based search

### 6. **app/teacher.py** - Teacher Routes
- **GET /teacher/dashboard**: Render teacher profile and request management
- **POST /api/profile/update**: Update bio, subjects, rate, location, availability
- **GET /api/requests**: Fetch incoming requests with status
- **POST /api/request/:id/accept**: Update request status to accepted
- **POST /api/request/:id/reject**: Update request status to rejected
- **GET /teacher/availability**: Manage weekly availability slots

### 7. **app/admin.py** - Admin Routes
- **GET /admin/dashboard**: Render admin panel with user list and statistics
- **GET /api/admin/users**: Fetch all users with role, created_at; support pagination
- **POST /api/admin/users/:id/delete**: Soft delete user (mark inactive)
- **GET /api/admin/stats**: Return user counts by role, total requests, active tutors

### 8. **app/decorators.py** - Authentication Decorators
- `@login_required`: Redirect to login if not authenticated
- `@role_required(role)`: Check user role; return 403 if unauthorized
- `@admin_only`: Shorthand for `@role_required('admin')`

### 9. **app/errors.py** - Error Handlers
- Handle 404 (Not Found): Render 404.html with message
- Handle 403 (Forbidden): Render 403.html with message
- Handle 500 (Server Error): Log error; render 500.html
- Handle 400 (Bad Request): Return JSON error for API endpoints

### 10. **app/utils.py** - Utility Functions
- `hash_password(password)`: Hash using werkzeug
- `verify_password(password, hash)`: Verify hash
- `calculate_distance(lat1, lon1, lat2, lon2)`: Haversine formula (returns km)
- `validate_email(email)`: Basic email validation
- `validate_password(password)`: Enforce minimum length, complexity
- `get_current_user()`: Retrieve user from session

### 11. **requirements.txt** - Dependencies
```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
SQLAlchemy==2.0.0
python-dotenv==1.0.0
Werkzeug==2.3.0
```

### 12. **run.py** - Entry Point
```python
from app import create_app, db
from app.models import User, Student, Tutor, TuitionRequest, Availability

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### 13. **seed.py** - Database Seeding
- Create 5 sample students with varied budgets and subjects
- Create 5 sample tutors with subjects, rates, locations, availability
- Create 3 sample requests (pending, accepted, rejected)
- Clear existing data before seeding (for development)
- Run via `python seed.py`

### 14. **.env.example** - Environment Template
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///tuition_marketplace.db
DEBUG=True
```

---

## Frontend Implementation

### HTML Templates

#### **base.html** - Base Template
- Semantic HTML5 structure (`<header>`, `<nav>`, `<main>`, `<footer>`)
- Navigation bar with logo, links (Home, Dashboard, Logout), responsive hamburger menu
- Flash message container for alerts
- Footer with copyright, links
- CSS/JS includes
- `{% block content %}` for child templates

#### **index.html** - Landing Page
- Hero section: headline, subheadline, CTA buttons (Find Tutor / Become Tutor)
- Search bar: subject dropdown, location input, budget range slider
- Featured tutors section: 3-4 tutor cards (name, subject, rate, location, rating placeholder)
- How it works section: 3 steps (Find, Connect, Learn)
- Call-to-action footer section

#### **register.html** - Registration Form
- Form fields: email, password, confirm password, name, role (radio: Student/Teacher)
- Conditional fields: if Teacher, show subjects_taught, hourly_rate, bio
- Submit button, link to login
- Client-side validation feedback

#### **login.html** - Login Form
- Form fields: email, password
- Remember me checkbox
- Submit button, link to register
- Error messages for failed login

#### **student_dashboard.html** - Student Search & Requests
- Left sidebar: search filters (subject, location, budget range, availability)
- Main content: tutor cards grid (responsive: 1 col mobile, 2 col tablet, 3 col desktop)
- Tutor card: name, subjects, rate, location, distance, "Send Request" button
- Right sidebar: sent requests list with status badges (pending, accepted, rejected)
- Pagination for tutor results

#### **teacher_dashboard.html** - Teacher Profile & Requests
- Profile section: editable fields (name, bio, subjects, rate, location, availability)
- Save profile button
- Incoming requests section: request cards with student name, subject, status, Accept/Reject buttons
- Availability management: weekly grid (days × time slots)

#### **admin_dashboard.html** - Admin User Management
- User table: columns (ID, Name, Email, Role, Created, Actions)
- Search/filter by role, email
- Delete button (soft delete)
- Statistics cards: total users, students, tutors, requests
- Pagination for user list

#### **components/tutor_card.html** - Reusable Tutor Card
- Card layout: avatar placeholder, name, subjects (badges), rate, location, distance
- Hover effect: shadow, slight scale
- "View Profile" and "Send Request" buttons

#### **components/request_card.html** - Reusable Request Card
- Card layout: student/tutor name, subject, status badge, timestamp
- Accept/Reject buttons (for teacher view)
- Status indicator (color-coded: yellow pending, green accepted, red rejected)

#### **components/navbar.html** - Navigation Component
- Logo/brand link
- Nav links: Home, Dashboard (role-specific), Admin (if admin)
- User dropdown: Profile, Logout
- Responsive hamburger menu (mobile)

### CSS Design System

#### **style.css** - Main Stylesheet
- **Color Palette**:
  - Primary: #3B82F6 (blue)
  - Secondary: #10B981 (green)
  - Danger: #EF4444 (red)
  - Neutral: #6B7280 (gray)
  - Background: #F9FAFB (light gray)
  - Text: #1F2937 (dark gray)

- **Typography**:
  - Font family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
  - Base font size: 16px
  - Line height: 1.5
  - Headings: h1 (2.5rem), h2 (2rem), h3 (1.5rem)

- **Spacing System** (8px base):
  - xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px

- **Components**:
  - Buttons: primary (blue bg, white text), secondary (outline), danger (red)
  - Cards: white bg, rounded corners (8px), shadow, padding (md)
  - Forms: input fields with focus states, labels, error messages
  - Badges: inline labels for status/subjects (small, rounded)
  - Alerts: success (green), error (red), info (blue) with icons

- **Utilities**:
  - Flexbox layout helpers (.flex, .flex-center, .flex-between)
  - Grid layout (.grid, .grid-cols-2, .grid-cols-3)
  - Spacing (.mt-md, .mb-lg, .px-lg)
  - Text utilities (.text-center, .text-sm, .font-bold)

#### **components.css** - Component Styles
- Navbar: sticky header, flex layout, dropdown menu
- Tutor card: grid layout, hover effects, button styling
- Request card: status badge colors, action buttons
- Search filters: form layout, range slider styling
- Modal/overlay: backdrop, centered content
- Pagination: numbered buttons, active state

#### **responsive.css** - Responsive Breakpoints
- Mobile (< 640px): single column, full-width cards, hamburger menu
- Tablet (640px - 1024px): 2-column grid, adjusted spacing
- Desktop (> 1024px): 3-column grid, sidebar layouts, full navigation

---

## JavaScript Implementation

### **main.js** - Global Interactivity
- Hamburger menu toggle
- Flash message auto-dismiss (5 seconds)
- Form validation (email, password strength)
- Smooth scroll to sections
- Dark mode toggle (optional)

### **search.js** - Search Filtering
- Real-time filter updates on input change
- Distance calculation display
- Budget range slider interaction
- Subject multi-select
- API call to `/api/search` with filters
- Render tutor cards dynamically
- Pagination controls

### **requests.js** - Request Management
- Send request button: POST to `/api/request` with tutor_id
- Accept/Reject buttons: POST to `/api/request/:id/accept` or `//reject`
- Status badge updates after action
- Success/error toast notifications
- Disable buttons during API call (loading state)

### **admin.js** - Admin Panel
- User table sorting (by name, role, created_at)
- Delete user confirmation modal
- Filter by role dropdown
- Search by email
- Pagination controls

---

## Database & Initialization

### **seed.py** - Sample Data
```python
from app import create_app, db
from app.models import User, Student, Tutor, TuitionRequest, Availability

app = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # Create sample students
    student1 = User(email='student1@example.com', name='Alice', role='student')
    student1.set_password('password123')
    db.session.add(student1)
    db.session.commit()
    
    Student(user_id=student1.id, budget_min=500, budget_max=2000, 
            subjects_interested='Math, Physics').save()
    
    # Create sample tutors
    tutor1 = User(email='tutor1@example.com', name='Bob', role='teacher')
    tutor1.set_password('password123')
    db.session.add(tutor1)
    db.session.commit()
    
    Tutor(user_id=tutor1.id, subjects_taught='Math, Physics', hourly_rate=1000,
          location_lat=40.7128, location_lon=-74.0060).save()
    
    # Create sample requests
    request1 = TuitionRequest(student_id=student1.id, tutor_id=tutor1.id, 
                              subject='Math', status='pending')
    db.session.add(request1)
    db.session.commit()
    
    print("Database seeded successfully!")
```

---

## Execution & Deployment

### **Running the Application**
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and update SECRET_KEY
3. Run: `python run.py`
4. Access at `http://localhost:5000`

### **First-Time Setup**
- Database tables created automatically on first run
- Seed sample data: `python seed.py`
- Login with sample credentials (email: student1@example.com, password: password123)

---

## Acceptance Criteria

- [ ] Given all backend files are present, When `python run.py` is executed, Then the Flask app starts on port 5000 without errors
- [ ] Given the app is running, When a user navigates to `http://localhost:5000`, Then the landing page loads with hero section, search bar, and featured tutors
- [ ] Given a new user visits the app, When they click "Register", Then they can create a Student or Teacher account with email, password, and role
- [ ] Given a user is logged in as a student, When they search for tutors by subject and location, Then the API returns matching tutors within the specified budget range
- [ ] Given a student views a tutor profile, When they click "Send Request", Then a TuitionRequest is created and stored in the database with status "pending"
- [ ] Given a teacher is logged in, When they view their dashboard, Then they see incoming requests with student names, subjects, and Accept/Reject buttons
- [ ] Given a teacher clicks "Accept" on a request, When the action completes, Then the request status updates to "accepted" and the student sees the updated status
- [ ] Given an admin is logged in, When they access `/admin/dashboard`, Then they see a user management table with delete functionality and statistics cards
- [ ] Given the database is empty, When `python seed.py` is executed, Then 5 students, 5 tutors, and 3 sample requests are created
- [ ] Given all HTML templates are present, When each route is accessed, Then the correct template renders with proper CSS styling and responsive layout on mobile (< 640px), tablet (640-1024px), and desktop (> 1024px)
- [ ] Given JavaScript files are loaded, When a user interacts with search filters, request buttons, or admin actions, Then the corresponding API calls are made and UI updates without page reload
- [ ] Given the app is deployed, When a user logs out, When they try to access a protected route, Then they are redirected to the login page
- [ ] Given all files are in place, When a developer runs `pip install -r requirements.txt`, Then all dependencies install without conflicts
- [ ] Given the .env.example file exists, When a developer copies it to .env and updates SECRET_KEY, Then the app runs in development mode with proper configuration