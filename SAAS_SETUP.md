# Integraty SaaS - Complete Setup Guide

## 🎯 Overview

Integraty is now a full SaaS platform with:
- **Web Dashboard** (Next.js) - For teachers/admins to manage everything
- **Backend API** (FastAPI) - Central server with authentication & database
- **Student App** (Electron) - Desktop app for monitored sessions

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATY SAAS PLATFORM                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐       ┌──────────────┐    ┌─────────────┐│
│  │   Teacher    │◄──────┤   Backend    ├───►│   Student   ││
│  │   Website    │       │   API +      │    │   Desktop   ││
│  │  (Next.js)   │       │   Database   │    │   App       ││
│  │  Vercel      │       │  PostgreSQL  │    │  (Electron) ││
│  └──────────────┘       └──────────────┘    └─────────────┘│
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ What's Been Implemented

### Backend (FastAPI)
- ✅ User authentication (JWT)
- ✅ Multi-tenant organizations
- ✅ User roles (Admin, Teacher, Student)
- ✅ Database models (PostgreSQL/SQLite)
- ✅ Session management with unique codes
- ✅ Screenshot storage system
- ✅ Detection event logging
- ✅ Authentication endpoints:
  - POST /api/v1/auth/register
  - POST /api/v1/auth/login
  - POST /api/v1/auth/refresh
  - GET /api/v1/auth/me

### Database Schema
- ✅ Users table (multi-role support)
- ✅ Organizations table (with plans)
- ✅ Sessions table (with 6-digit codes)
- ✅ SessionParticipants table
- ✅ Screenshots table
- ✅ DetectionEvents table
- ✅ WindowEvents table

### Frontend (Preparation)
- ✅ Next.js project structure created
- ✅ Package.json configured
- 🔄 UI components (next phase)
- 🔄 Authentication flow (next phase)

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run server
python -m integraty.main
```

**Backend runs on**: http://localhost:8080

### 2. Test Authentication

```bash
# Register a new teacher account
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher@school.com",
    "password": "securepassword",
    "full_name": "John Teacher",
    "organization_name": "My School",
    "role": "teacher"
  }'

# Login
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher@school.com",
    "password": "securepassword"
  }'

# Copy the access_token from response

# Get current user info
curl http://localhost:8080/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Web Dashboard Setup (Coming Soon)

```bash
cd web
npm install
npm run dev
```

Opens at: http://localhost:3000

### 4. Student App

The existing Electron app will be refactored to:
- Show login screen
- Connect to backend API
- Upload data in real-time

---

## 📋 User Workflows

### Teacher Workflow

1. **Sign Up**
   - Go to https://integraty.vercel.app
   - Register with email
   - Create organization

2. **Add Students**
   - Manually add students one-by-one
   - Or bulk upload CSV
   - Students receive login credentials

3. **Create Session**
   - Set session name (e.g., "Final Exam - Math 101")
   - Pick date and time
   - Select monitoring settings
   - Assign students
   - Get 6-digit session code

4. **Share Code**
   - Give students the session code
   - Students enter code in app

5. **Monitor Live**
   - See who's online
   - View real-time screenshots
   - See AI detection alerts

6. **Review Results**
   - View completed sessions
   - Check integrity scores
   - Generate PDF reports

### Student Workflow

1. **Download App**
   - Download from https://integraty.com/download
   - Install on Windows/Mac/Linux

2. **Login**
   - Enter email and password
   - App connects to server

3. **View Sessions**
   - See assigned sessions
   - See upcoming sessions

4. **Start Session**
   - Enter 6-digit session code
   - Or click on assigned session
   - Accept consent
   - Monitoring begins automatically

5. **Complete**
   - Session ends automatically
   - Or click "Complete"
   - Data uploaded to server

---

## 🗄️ Database Schema Details

### Users
```sql
id (UUID)
email (unique)
password_hash
full_name
role (admin/teacher/student)
organization_id (FK)
is_active
last_login
created_at
```

### Organizations
```sql
id (UUID)
name
plan (free/pro/enterprise)
max_students
max_sessions_per_month
data_retention_days
```

### Sessions
```sql
id (UUID)
organization_id (FK)
name
session_code (6-digit unique)
scheduled_start
scheduled_end
status (pending/active/completed)
config (JSON)
created_by (FK)
```

### SessionParticipants
```sql
id (UUID)
session_id (FK)
student_id (FK)
status (pending/active/completed)
start_time
end_time
integrity_score (0.0-1.0)
detection_count
```

---

## 🔑 Authentication Flow

### Registration
```
POST /api/v1/auth/register
{
  "email": "teacher@school.com",
  "password": "password123",
  "full_name": "John Teacher",
  "organization_name": "My School"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "teacher@school.com",
    "role": "teacher",
    "organization_id": "uuid"
  }
}
```

### Using Protected Endpoints
```bash
curl http://localhost:8080/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🎨 UI Design (Web Dashboard)

### Pages

1. **/login** - Login page
2. **/register** - Registration
3. **/dashboard** - Overview stats
4. **/students** - Manage students
5. **/sessions** - All sessions
6. **/sessions/new** - Create session
7. **/sessions/[id]** - Session details
8. **/sessions/[id]/live** - Live monitoring
9. **/sessions/[id]/report** - View report
10. **/settings** - Organization settings

---

## 🔒 Security Features

### Authentication
- ✅ JWT tokens (access + refresh)
- ✅ Password hashing (bcrypt)
- ✅ Token expiration
- ✅ Role-based access control

### Data Protection
- ✅ Encrypted password storage
- ✅ HTTPS required (production)
- ✅ CORS configured
- ✅ SQL injection prevention (ORM)

### Privacy
- ✅ GDPR compliant architecture
- ✅ Data retention policies
- ✅ User data deletion support
- ✅ Audit logging ready

---

## 📊 Pricing Plans

### Free Tier
- 1 organization
- Up to 10 students
- 5 sessions/month
- 7-day data retention
- Basic support

### Pro ($49/month)
- Unlimited students
- Unlimited sessions
- 90-day retention
- Priority support
- Custom branding
- Advanced analytics

### Enterprise (Custom)
- Everything in Pro
- On-premise option
- SSO integration
- Dedicated support
- SLA guarantee
- Custom features

---

## 🚀 Deployment

### Backend (Railway / Render)

1. Push code to GitHub
2. Connect to Railway/Render
3. Set environment variables:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=...
   JWT_SECRET=...
   ```
4. Deploy!

### Web Dashboard (Vercel)

1. Push code to GitHub
2. Import project to Vercel
3. Set environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://api.integraty.com
   ```
4. Deploy!

### Student App (GitHub Releases)

1. Build for each platform:
   ```bash
   npm run build:win
   npm run build:mac
   npm run build:linux
   ```
2. Upload to GitHub Releases
3. Update download links

---

## 📝 Next Steps

### Phase 1: Web Dashboard (Week 1-2)
- [ ] Build authentication UI
- [ ] Dashboard layout
- [ ] Student management
- [ ] Session creation form
- [ ] Live monitoring view

### Phase 2: Student App Refactor (Week 2-3)
- [ ] Add login screen
- [ ] Session list view
- [ ] Real-time upload
- [ ] Offline support

### Phase 3: Production Deploy (Week 3-4)
- [ ] Deploy backend to Railway
- [ ] Deploy web to Vercel
- [ ] Set up PostgreSQL
- [ ] Configure S3/storage
- [ ] Custom domain

### Phase 4: Polish (Week 4+)
- [ ] Report generation
- [ ] Email notifications
- [ ] Analytics dashboard
- [ ] Mobile responsive
- [ ] Documentation site

---

## 🛠️ Development Tips

### Testing Authentication

Use this script to test:

```python
import requests

API_URL = "http://localhost:8080"

# Register
response = requests.post(f"{API_URL}/api/v1/auth/register", json={
    "email": "test@test.com",
    "password": "test123",
    "full_name": "Test User",
    "organization_name": "Test Org"
})
print("Register:", response.json())

# Login
response = requests.post(f"{API_URL}/api/v1/auth/login", json={
    "email": "test@test.com",
    "password": "test123"
})
token = response.json()["access_token"]
print("Token:", token)

# Get user info
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{API_URL}/api/v1/auth/me", headers=headers)
print("User:", response.json())
```

---

## 📚 API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

---

## 🤝 Support

- GitHub: https://github.com/minuttt/Integraty
- Issues: https://github.com/minuttt/Integraty/issues

---

**Version**: 2.0.0  
**Status**: SaaS Architecture Implemented  
**Last Updated**: 2026-06-26
