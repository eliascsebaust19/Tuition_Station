# Tuition Management System (Pyhon Flask + SQL Server)

Production-oriented full-stack backend for a Tuition Management System with payment-gated activation, role-based access, and dashboard workflows.

## Features Implemented
- Student and teacher registration (`inactive` by default)
- Activation only after 100 BDT payment submission (`bKash` / `Nagad`)
- Admin payment verification flow
- Session-based login with role checks (`admin`, `teacher`, `student`)
- Only `active` users can access protected dashboard APIs
- Admin dashboard: users, status management, payment queue, reports, contacts
- Teacher dashboard: create/manage classes, view students, record attendance, upload marks
- Student dashboard: view teachers, enroll classes, track attendance/marks, payment history
- Public site: MySQL-backed content + contact form submission

## Tech Stack
- Node.js + Express
- MySQL (`mysql2/promise`)
- `bcrypt` password hashing
- `express-session` auth session
- `dotenv` environment config

## Folder Structure
- `config/db.js`
- `models/User.js`, `models/Payment.js`
- `controllers/*.js`
- `routes/*.js`
- `middleware/auth.js`
- `public/js/*.js`
- `sql/schema.sql`
- `server.js`

## Setup
1. Open terminal in project root.
2. Install dependencies:
   - `npm install`
3. Create env file:
   - `copy .env.example .env`
4. Update `.env` values (DB + session secret).
5. Import database:
   - `mysql -u root -p < sql/schema.sql`
6. Start server:
   - `npm run dev`
7. Open:
   - `http://localhost:3000/`
   - `http://localhost:3000/admin-panel.html`
   - `http://localhost:3000/teacher-dashboard.html`
   - `http://localhost:3000/student-dashboard.html`

## Core API Endpoints
### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/submit-payment`
- `GET /api/auth/me`
- `POST /api/auth/logout`

### Admin (auth + admin + active)
- `GET /api/admin/dashboard`
- `GET /api/admin/users?role=&status=`
- `PATCH /api/admin/users/:id/status`
- `GET /api/admin/payments/pending`
- `POST /api/admin/payments/:id/verify`
- `GET /api/admin/reports/summary`
- `GET /api/admin/contacts`

### Teacher (auth + teacher + active)
- `GET /api/teacher/dashboard`
- `GET /api/teacher/classes`
- `POST /api/teacher/classes`
- `GET /api/teacher/classes/:id/students`
- `POST /api/teacher/classes/:id/attendance`
- `POST /api/teacher/classes/:id/marks`

### Student (auth + student + active)
- `GET /api/student/dashboard`
- `GET /api/student/teachers`
- `GET /api/student/classes`
- `POST /api/student/enroll`
- `GET /api/student/enrollments`
- `GET /api/student/attendance`
- `GET /api/student/marks`
- `GET /api/student/payments`

### Public
- `GET /api/public/content`
- `POST /api/public/contact`

## Security Controls
- Prepared statements for all SQL
- `bcrypt` password hashing (cost 12)
- Session cookie with `httpOnly` and `sameSite=lax`
- Role-based middleware + active account checks
- Server-side validation and sanitization
- Frontend output escaping for rendered dynamic strings

## Notes
- Default admin account can be auto-created via `.env` values:
  - `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_NAME`, `ADMIN_PHONE`
- Existing landing page `script.js` now reads content from `/api/public/content`.
- Contact form on homepage stores submissions into `contact_submissions`.
