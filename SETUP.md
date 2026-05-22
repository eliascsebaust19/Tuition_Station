# TuitionStation - Complete Setup Guide

## Prerequisites

1. **Python 3.9+** installed
2. **Microsoft SQL Server** (SSMS) installed
3. **ODBC Driver 17 for SQL Server** installed
4. **Git** (optional)

---

## Step 1: Clone & Navigate

```bash
cd E:\Level 2 term II\DBMS\tuition_system
```

## Step 2: Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Setup SQL Server Database

### Option A: Using SSMS
1. Open **SQL Server Management Studio**
2. Connect to your local instance (Windows Auth)
3. Open and execute `schema.sql` file

### Option B: Using Command Line
```bash
sqlcmd -S localhost -E -i schema.sql
```

This creates the `tuition_station` database with all tables, stored procedures, views, triggers, indexes, and seed data.

### Verify Database
```sql
USE tuition_station;
SELECT * FROM subscription_plans;
-- Should show 3 plans: Free, Standard, Premium
```

## Step 5: Configure Environment

The `.env` file is already configured. Verify these settings:

```
DATABASE_URL=mssql+pyodbc://localhost/tuition_station?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server
SECRET_KEY=tuition-station-secret-key-2024
```

### If using SQL Server Authentication:
```
DATABASE_URL=mssql+pyodbc://sa:YourPassword@localhost:1433/tuition_station?driver=ODBC+Driver+17+for+SQL+Server
```

### If using a different SQL Server instance name:
```
DATABASE_URL=mssql+pyodbc://localhost\SQLEXPRESS/tuition_station?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server
```

## Step 6: Run the Application

```bash
python run.py
```

The app will:
1. Create all tables (if not already created)
2. Seed subscription plans
3. Create default admin account
4. Create sample teachers and students
5. Start on **http://localhost:5000**

## Step 7: Login Credentials

### Admin Panel
- **Email:** admin@tuition.com
- **Password:** admin123

### Sample Teachers
| Name | Email | Password |
|------|-------|----------|
| Dr. Ahmed Hassan | ahmed@tutor.com | password123 |
| Sarah Rahman | sarah@tutor.com | password123 |
| Mohammad Khan | khan@tutor.com | password123 |
| Fatima Begum | fatima@tutor.com | password123 |
| Abu Bakar | abubakar@tutor.com | password123 |
| Lisa Ahmed | lisa@tutor.com | password123 |

### Sample Students
| Name | Email | Password |
|------|-------|----------|
| Rahim Miya | rahim@student.com | password123 |
| Karim Ahmed | karim@student.com | password123 |

---

## Project Structure

```
E:\Level 2 term II\DBMS\tuition_system\
├── app.py              # App factory
├── run.py              # Entry point
├── config.py           # Configuration
├── config/
│   └── config.py       # Extended config with CSRF
├── models/
│   └── __init__.py     # All SQLAlchemy models
├── routes/
│   ├── auth.py         # Authentication
│   ├── admin.py        # Admin panel
│   ├── student.py      # Student dashboard
│   ├── teacher.py      # Teacher dashboard
│   ├── subscriptions.py # Subscription plans
│   ├── payments.py     # Payment processing
│   ├── chat.py         # Real-time messaging
│   └── todo.py         # To-do list
├── templates/
│   ├── base.html       # Base layout
│   ├── index.html      # Landing page
│   ├── auth_new.html   # Login/Register
│   ├── admin/          # Admin templates
│   ├── student/        # Student templates
│   ├── teacher/        # Teacher templates
│   ├── chat/           # Chat templates
│   ├── subscriptions/  # Subscription templates
│   └── payments/       # Payment templates
├── static/
│   ├── css/atelier.css # Main stylesheet
│   ├── js/             # JavaScript files
│   └── Assets/         # Images and icons
├── schema.sql          # Complete DB schema
└── requirements.txt    # Python dependencies
```

---

## Key Features

### Authentication
- Email/password registration and login
- Role-based access (Admin, Teacher, Student)
- Session management with Flask-Login
- Password hashing with Werkzeug

### Subscription Plans
| Plan | Price | Features |
|------|-------|----------|
| Free | BDT 0 | 3 applications/month, basic visibility |
| Standard | BDT 499/month | Unlimited apps, verified badge, priority ranking |
| Premium | BDT 999/month | All Standard + featured, analytics, priority support |

### Payment System
- bKash and Nagad integration
- Transaction ID upload
- Manual admin verification
- Auto subscription activation on approval

### Admin Panel
- Dashboard with analytics
- User management (activate/block/delete)
- Teacher approval
- Payment verification
- Post management
- Revenue reports
- Activity logs

### Tutor Dashboard
- Application tracking
- Profile management
- Subscription status
- Analytics with charts
- Browse and apply to tuition posts

### Student Dashboard
- Browse/search tutors
- Create tuition posts
- Save favorite tutors
- Review tutors
- Track applications

### Real-time Chat
- Direct messaging between students and tutors
- Unread message indicators
- Notification system

---

## Troubleshooting

### Database Connection Issues
```
Error: ('08001', '[08001] SQL Server Network Interfaces...')
```
**Fix:** Ensure SQL Server is running and TCP/IP is enabled:
1. Open SQL Server Configuration Manager
2. SQL Server Network Configuration → Protocols for MSSQLSERVER
3. Enable TCP/IP
4. Restart SQL Server

### ODBC Driver Error
```
Error: ('01000', "[01000] [Microsoft][ODBC Driver Manager]...")
```
**Fix:** Download and install "ODBC Driver 17 for SQL Server" from Microsoft.

### Port Already in Use
```
Error: Address already in use
```
**Fix:** Change port in `run.py` or kill the process using port 5000:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## Deployment Guide

### Option 1: IIS (Windows Server)
1. Install IIS with CGI feature
2. Install `wfastcgi` Python package
3. Configure IIS handler for Flask
4. Deploy the project to inetpub/wwwroot

### Option 2: Azure App Service
1. Create Azure Web App (Python stack)
2. Configure SQL Server Database in Azure
3. Update `DATABASE_URL` with Azure SQL connection string
4. Deploy via Git or FTP

### Option 3: Docker
Build a Docker image with:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

---

## API Endpoints

### Chat API
- `GET /chat/api/unread` - Get unread count for current user

### Teacher API
- `GET /teacher/api/stats` - Get teacher's application statistics

---

## Database: Stored Procedures

| Procedure | Description |
|-----------|-------------|
| `sp_GetTeacherDashboardStats` | Get teacher's dashboard statistics |
| `sp_GetAdminDashboardStats` | Get admin's dashboard statistics |
| `sp_GetMonthlyRevenue` | Get monthly revenue data |
| `sp_VerifyPayment` | Verify payment and activate subscription (transactional) |
| `sp_AutoDowngradeExpiredSubscriptions` | Deactivate expired subscriptions |
| `sp_CreateNotification` | Create a notification for a user |
| `sp_SearchTutors` | Advanced tutor search with ranking |

## Database: Views

| View | Description |
|------|-------------|
| `vw_TutorPublicProfiles` | Public tutor profiles with subscription and rating info |
| `vw_AdminRevenueReport` | Revenue aggregation by month and plan |
| `vw_SubscriptionStatus` | Subscription status with days remaining |
| `vw_TutorAnalytics` | Tutor performance analytics |

## Database: Triggers

| Trigger | Description |
|---------|-------------|
| `trg_UpdateUserTimestamp` | Auto-update `updated_at` on users |
| `trg_UpdateTeacherProfileTimestamp` | Auto-update `updated_at` on teacher_profiles |
| `trg_NewPaymentNotification` | Notify user and admins on new payment |
| `trg_SubscriptionExpiryNotification` | Notify 7 days before subscription expiry |
| `trg_NewMessageNotification` | Notify on new message |

---

## Support

**Developed by:** Elias, Sayadul, Mehejabin  
**Course:** CSE 2205, Level 2 Term II  
**Email:** TuitionStationdev@gmail.com
