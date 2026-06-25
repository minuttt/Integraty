# Integraty - Enterprise Architecture

## Overview

Integraty is now a full SaaS platform with:
- **Web Dashboard**: For administrators to manage sessions
- **Backend API**: Central server handling all logic
- **Student App**: Desktop application for monitored sessions

---

## Architecture Components

### 1. Web Dashboard (Next.js + Vercel)
**URL**: https://integraty.vercel.app

**Features**:
- Teacher/Admin registration and login
- Create and manage student accounts
- Create monitoring sessions
- Configure monitoring rules
- Real-time session monitoring
- View session recordings
- Generate reports
- Analytics dashboard

**Tech Stack**:
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Query for API calls
- NextAuth for authentication
- Deployed on Vercel

---

### 2. Backend API (Python FastAPI)
**URL**: https://api.integraty.com (or your domain)

**Features**:
- User authentication (JWT)
- Session management
- Real-time data collection
- Screenshot storage (S3/local)
- AI detection processing
- Report generation
- WebSocket for real-time updates

**Database**:
- PostgreSQL (production)
- SQLite (development)

**Deployment**:
- Railway / Render / DigitalOcean
- Docker container

---

### 3. Student Desktop App (Electron)
**Download**: https://integraty.com/download

**Features**:
- Student login
- View assigned sessions
- Start monitoring session
- Automatic screenshot upload
- Window activity tracking
- Offline support with sync
- System tray monitoring

**Platforms**:
- Windows (.exe)
- macOS (.dmg)
- Linux (.AppImage)

---

## User Flows

### Admin/Teacher Flow:
1. Sign up at https://integraty.vercel.app
2. Create organization
3. Add students (bulk upload CSV)
4. Create monitoring session with:
   - Session name
   - Date/time
   - Duration
   - Monitoring rules
   - Assigned students
5. Share session code with students
6. Monitor live sessions
7. Review completed sessions
8. Generate reports

### Student Flow:
1. Download Integraty app
2. Login with credentials
3. See assigned sessions
4. Click "Start Session"
5. Accept consent
6. Monitoring begins automatically
7. Complete session
8. Data uploaded to server

---

## Database Schema

### Users Table
- id (UUID)
- email
- password_hash
- role (admin, teacher, student)
- organization_id
- full_name
- created_at

### Organizations Table
- id (UUID)
- name
- plan (free, pro, enterprise)
- created_at

### Sessions Table
- id (UUID)
- organization_id
- name
- session_code (unique 6-digit)
- scheduled_start
- scheduled_end
- status
- config (JSON)
- created_by (user_id)

### SessionParticipants Table
- session_id
- student_id
- status (pending, active, completed)
- start_time
- end_time
- integrity_score

### Screenshots Table
- id (UUID)
- session_id
- student_id
- timestamp
- file_url (S3/storage)
- thumbnail_url
- sha256_hash

### DetectionEvents Table
- id (UUID)
- session_id
- student_id
- timestamp
- tool_name
- confidence_score
- evidence (JSON)

---

## API Endpoints

### Authentication
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/refresh
- POST /api/auth/logout

### Organizations
- GET /api/organizations/me
- PATCH /api/organizations/me
- GET /api/organizations/students
- POST /api/organizations/students (bulk)

### Sessions
- POST /api/sessions
- GET /api/sessions
- GET /api/sessions/:id
- PATCH /api/sessions/:id
- DELETE /api/sessions/:id
- POST /api/sessions/:id/start (student)
- POST /api/sessions/:id/complete (student)

### Monitoring
- POST /api/monitoring/screenshot (student uploads)
- POST /api/monitoring/window-event (student uploads)
- POST /api/monitoring/heartbeat (student ping)

### Reports
- GET /api/sessions/:id/report
- POST /api/sessions/:id/generate-report

### Real-time
- WS /api/ws/session/:id (live monitoring)

---

## Security

### Authentication
- JWT tokens with refresh
- Password hashing (bcrypt)
- Rate limiting
- CORS configured

### Data Protection
- Screenshots encrypted at rest
- SSL/TLS in transit
- Role-based access control
- Audit logging

### Privacy
- GDPR compliant
- Data retention policies
- Student data anonymization options
- Right to deletion

---

## Deployment Strategy

### Phase 1: Development
- Local development setup
- SQLite database
- Local file storage

### Phase 2: Beta
- Deploy backend to Railway/Render
- Deploy web to Vercel
- PostgreSQL database
- S3 for screenshots

### Phase 3: Production
- Custom domain
- CDN for assets
- Database backups
- Monitoring/alerting
- Auto-scaling

---

## Pricing Model

### Free Tier
- 1 organization
- Up to 10 students
- 5 sessions/month
- 7 day data retention

### Pro ($49/month)
- Unlimited students
- Unlimited sessions
- 90 day retention
- Priority support
- Custom branding

### Enterprise (Custom)
- On-premise deployment
- Custom integration
- SLA guarantee
- Dedicated support
- Custom features

---

## Development Roadmap

### Week 1: Backend
- [x] Add database models
- [x] Implement authentication
- [x] Update API endpoints
- [x] Add file upload
- [x] WebSocket setup

### Week 2: Web Dashboard
- [ ] Create Next.js project
- [ ] Build authentication UI
- [ ] Dashboard layout
- [ ] Session management
- [ ] Live monitoring view

### Week 3: Student App
- [ ] Refactor Electron app
- [ ] Add login screen
- [ ] Session selection
- [ ] Upload functionality
- [ ] Offline support

### Week 4: Integration & Testing
- [ ] End-to-end testing
- [ ] Security audit
- [ ] Performance optimization
- [ ] Documentation
- [ ] Deploy to staging

---

## Technical Decisions

### Why Next.js?
- Server-side rendering
- Great developer experience
- Vercel deployment (free)
- Built-in API routes
- TypeScript support

### Why PostgreSQL?
- ACID compliance
- JSON support
- Mature ecosystem
- Great for production
- Free tier available

### Why S3 for storage?
- Scalable
- Cost-effective
- CDN integration
- Reliable
- Industry standard

---

## Monitoring & Analytics

### Application Monitoring
- Sentry for error tracking
- LogRocket for session replay
- Plausible for web analytics

### Infrastructure
- Uptime monitoring
- Performance metrics
- Database metrics
- API response times

---

**Version**: 2.0.0  
**Architecture**: SaaS Multi-tenant  
**Status**: In Development
