# Tuition System - Location-Based Offline Tuition Marketplace

A professional full-stack web application for finding home tutors and connecting students with teachers. Built with Flask and Firebase, featuring a premium "Tuition Station" design system.

## Overview

Help students find nearby home tutors by subject and budget, and give teachers a way to manage their availability and incoming student requests. The platform serves as a location-based marketplace that makes tutor discovery fast and local, while giving teachers control over their profile, availability, and incoming requests.

**Value Proposition:** Students struggle to find qualified home tutors in their area—they rely on word-of-mouth, scattered ads, or expensive tutoring centers. Teachers have no centralized way to connect with students seeking their expertise. This platform solves this by making tutor discovery efficient and building direct connections between supply and demand.

## Quick Start (5 Steps)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tuition_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env and add your Firebase configuration
   ```

5. **Run the application**
   ```bash
   python run.py
   ```
   Access at `http://localhost:5000`

## Test Credentials

| Role    | Email             | Password    | Purpose                             |
| ------- | ----------------- | ----------- | ----------------------------------- |
| Admin   | admin@tuition.com | admin123    | User management, system oversight    |
| Student | rahim@student.com | password123 | Search tutors, send requests        |
| Student | karim@student.com | password123 | Alternative student account          |
| Teacher | ahmed@tutor.com   | password123 | Manage profile, respond to requests  |
| Teacher | sarah@tutor.com   | password123 | Alternative teacher account           |

## Features

### Landing Page (Public)
- **Hero Section**: Compelling headline with role-based signup CTAs
- **Search Bar**: Find tutors by location and subject (no authentication required)
- **Featured Tutors**: Grid display with ratings, rates, and profiles
- **How It Works**: Visual guide explaining the platform

### Student Features
- Search tutors by subject, location, and budget
- Filter tutors with multiple criteria (AND logic)
- View detailed teacher profiles with ratings and reviews
- Send tuition requests to teachers
- Message teachers directly
- Add reviews and rate teachers
- Save favorite tutors

### Teacher Features
- Create and manage professional profile
- Set subjects, fees, location, and bio
- Upload profile picture and CV
- Manage tuition requests (accept/reject)
- Set availability status (Available/Busy)
- View messages and reviews from students

### Admin Features
- Dashboard with system statistics
- Manage users (activate/block/delete)
- Approve teacher profiles
- Monitor all requests and messages
- User role management

## Project Structure

```
tuition_system/
├── run.py                      # Application entry point
├── app.py                      # Flask app factory
├── config.py                   # Configuration settings
├── firebase_config.py          # Firebase initialization
├── firebase_db.py              # Firebase database operations
├── requirements.txt            # Python dependencies
├── seed.py                     # Database seeding script
├── .env.example                # Environment template
├── README.md                   # This file
├── TODO.md                     # Implementation tracking
├── schema.sql                  # Database schema (MySQL reference)
│
├── routes/                     # Flask blueprints
│   ├── __init__.py
│   ├── auth.py                # Authentication routes
│   ├── student.py             # Student routes
│   ├── teacher.py             # Teacher routes
│   ├── admin.py               # Admin routes
│   └── todo.py                # ToDo functionality
│
├── templates/                  # Jinja2 templates
│   ├── base.html              # Base template with nav/footer
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── developer.html         # Developer info page
│   ├── student/               # Student templates
│   │   ├── dashboard.html
│   │   ├── search.html
│   │   ├── teacher_profile.html
│   │   ├── messages.html
│   │   └── edit_profile.html
│   ├── teacher/               # Teacher templates
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   └── messages.html
│   └── admin/                 # Admin templates
│       ├── dashboard.html
│       ├── users.html
│       ├── requests.html
│       └── messages.html
│
├── static/                    # Static assets
│   ├── css/
│   │   ├── atelier.css        # Tuition Station design system
│   │   └── style.css         # Legacy styles
│   ├── js/
│   │   └── main.js           # JavaScript functionality
│   ├── Assets/                # Images and media
│   │   └── Image/
│   └── uploads/               # User uploads (profile pics, CVs)
│
└── instance/                  # Instance-specific files
    └── tuition.db             # SQLite database (if used)
```

## Available Routes

### Public Routes
| Route                | Method | Description                    |
| -------------------- | ------ | ------------------------------ |
| `/` or `/landing`    | GET    | Landing page (public)          |
| `/login`             | GET/POST | Login page                   |
| `/register`          | GET/POST | Registration page             |
| `/logout`            | GET    | Logout user                    |

### Student Routes (Requires Login)
| Route                          | Method | Description                    |
| ------------------------------ | ------ | ------------------------------ |
| `/student/dashboard`           | GET    | Student dashboard              |
| `/student/search`              | GET    | Search tutors                  |
| `/student/teacher/<id>`        | GET    | View teacher profile           |
| `/student/request/<id>`        | POST   | Send tuition request           |
| `/student/review/<id>`         | POST   | Add review                    |
| `/student/messages`            | GET    | View messages                 |
| `/student/send_message/<id>`   | POST   | Send message to teacher       |
| `/student/profile/edit`        | GET/POST | Edit student profile        |

### Teacher Routes (Requires Login)
| Route                              | Method | Description                    |
| ---------------------------------- | ------ | ------------------------------ |
| `/teacher/dashboard`               | GET    | Teacher dashboard              |
| `/teacher/profile`                 | GET/POST | Manage profile              |
| `/teacher/upload-picture`          | POST   | Upload profile picture         |
| `/teacher/upload-cv`               | POST   | Upload CV                     |
| `/teacher/request/<id>/<action>`   | GET    | Accept/reject request         |
| `/teacher/messages`                | GET    | View messages                 |
| `/teacher/reply_message/<id>`      | POST   | Reply to student              |

### Admin Routes (Requires Admin Role)
| Route                          | Method | Description                    |
| ------------------------------ | ------ | ------------------------------ |
| `/admin/dashboard`             | GET    | Admin dashboard                |
| `/admin/users`                 | GET    | Manage users                   |
| `/admin/user/<id>/toggle`      | GET    | Activate/block user           |
| `/admin/user/<id>/delete`      | GET    | Delete user                    |
| `/admin/teacher/<id>/approve`  | GET    | Approve teacher               |
| `/admin/requests`              | GET    | View all requests             |
| `/admin/messages`              | GET    | View all messages             |

## Setup Instructions (Detailed)

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Firebase project (for authentication and database)

### Step 1: Clone and Setup
```bash
git clone <repository-url>
cd tuition_system
```

### Step 2: Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Firebase Configuration
1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com)
2. Enable Authentication (Email/Password)
3. Create Firestore database
4. Generate a private key for admin SDK
5. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
6. Update `.env` with your Firebase credentials

### Step 5: Run the Application
```bash
python run.py
```

The app will:
- Start Flask development server on `http://localhost:5000`
- Create admin account if not exists
- Seed sample data (5 teachers, 2 students) if no teachers exist

## Database Seeding

The application automatically seeds sample data on first run, or you can manually run:

```bash
python seed.py
```

**Sample Data Created:**
- 1 Admin account
- 5 Teacher accounts with profiles
- 2 Student accounts
- Teachers have demo profile pictures from `/static/Assets/Image/`

**Reset Database:**
```bash
python seed.py --reset
```

## Design System

This project uses the **Tuition Station** design language featuring:
- **Editorial Sophistication**: Intentional asymmetry and high-contrast typography
- **No-Line Design**: Boundaries defined through tonal surface layers
- **Premium Aesthetics**: Glassmorphism, ambient shadows, and curated imagery

### Color Palette
- **Primary**: `#004ac6` (Deep Blue)
- **Secondary**: `#006c49` (Growth Green)
- **Surface**: `#faf8ff` (Soft White)
- **Background**: `#faf8ff`

## Troubleshooting

### "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### "Module not found"
Ensure virtual environment is activated:
```bash
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### Firebase Connection Issues
- Verify `.env` file has correct Firebase credentials
- Check Firebase project is set up correctly
- Ensure Firestore database is created in Firebase Console

### Sample Data Not Created
Manually run the seed script:
```bash
python seed.py
```

## Next Steps

1. **Customize** - Modify test credentials in `seed.py` for custom testing
2. **Explore** - Use test accounts to explore all features
3. **Extend** - Add new features like payment integration, advanced matching, or mobile app
4. **Deploy** - Deploy to production (Heroku, Railway, or other platforms)

## Technology Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: Firebase Firestore (NoSQL)
- **Authentication**: Flask-Login, Firebase Auth
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: Custom "Tuition Station" Design System
- **Icons**: Font Awesome 6+
- **Storage**: Firebase Storage (profile pictures, CVs)

## License

MIT License

---

**Built with ❤️ for connecting students and teachers**
