# Integraty - Quick Start Guide

## Complete Setup in 3 Minutes

### Prerequisites
- Python 3.7+ installed
- Node.js 16+ installed (for frontend)
- Windows 10/11 (for full window monitoring support)

---

## Step 1: Clone Repository

```bash
git clone https://github.com/minuttt/Integraty.git
cd Integraty
```

---

## Step 2: Setup Backend (Python)

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m integraty.main
```

**Backend is now running on http://localhost:8080**

Keep this terminal window open!

---

## Step 3: Setup Frontend (Electron)

Open a NEW terminal window:

```bash
# Navigate to frontend
cd frontend

# Install Node dependencies
npm install

# Start Electron app
npm run dev
```

**The desktop app will open automatically!**

---

## Step 4: Test the Application

### Option A: Use the Desktop App

1. Click "New Session" in the sidebar
2. Fill in the form:
   - Session Name: "Test Session"
   - User ID: "test-user"
   - Leave other settings as default
3. Click "Create Session"
4. Click "Start Monitoring"
5. The app will start capturing screenshots every 30 seconds

### Option B: Use the API

```bash
# Create a session
curl -X POST http://localhost:8080/api/v1/sessions/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "session_name": "API Test Session",
    "session_type": "exam",
    "screenshot_interval": 30
  }'

# Copy the session_id from response

# Start monitoring
curl -X POST http://localhost:8080/api/v1/sessions/{session_id}/start

# Check status
curl http://localhost:8080/api/v1/sessions/{session_id}

# Complete session
curl -X POST http://localhost:8080/api/v1/sessions/{session_id}/complete
```

---

## What Happens During Monitoring?

1. **Screenshots**: Captured every 30 seconds
   - Stored in: `data/screenshots/{session_id}/`

2. **Window Tracking**: Active window changes logged
   - Process name, window title, duration

3. **OCR Processing**: Text extracted from screenshots
   - Async processing in background

4. **AI Detection**: Scans for AI tool usage
   - ChatGPT, Claude, Gemini, GitHub Copilot, etc.
   - Checks: domains, keywords, process names

---

## View the Results

### In the Desktop App:
1. Go to "Dashboard" to see active sessions
2. Go to "Sessions" to see all sessions
3. Click "View Details" on any session

### Via API:
```bash
# Get all sessions
curl http://localhost:8080/api/v1/sessions/

# Get specific session
curl http://localhost:8080/api/v1/sessions/{session_id}
```

---

## Stopping Monitoring

### Desktop App:
- Click "Complete" button on active session

### API:
```bash
curl -X POST http://localhost:8080/api/v1/sessions/{session_id}/complete
```

---

## Troubleshooting

### Backend won't start
- **Error**: `ModuleNotFoundError`
  - Solution: `pip install -r requirements.txt`

- **Error**: `Address already in use`
  - Solution: Port 8080 is busy, kill process or change port in `.env`

### Frontend won't start
- **Error**: `npm: command not found`
  - Solution: Install Node.js from https://nodejs.org

- **Error**: Can't connect to backend
  - Solution: Make sure backend is running on http://localhost:8080

### No screenshots captured
- **Issue**: `data/screenshots/` folder empty
  - Check: Backend is running and session is started
  - Check: User permissions to write files

### OCR not working
- **Error**: `pytesseract not found`
  - Solution (Windows): Download Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
  - Add Tesseract to PATH or set in `.env`: `TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe`

---

## Configuration

### Backend Configuration (`.env` file):

```env
# Monitoring
SCREENSHOT_INTERVAL=30          # Seconds between screenshots
SCREENSHOT_QUALITY=85           # Image quality (1-100)
OCR_ENABLED=true               # Enable OCR processing

# Server
HOST=localhost
PORT=8080
```

### Frontend Configuration:
- Open app
- Go to "Settings"
- Change API URL if needed
- Click "Save Settings"

---

## Data Storage

All monitoring data is stored in the `data/` directory:

```
data/
├── screenshots/
│   └── {session-id}/
│       ├── screenshot_*.png
│       └── thumbnails/
├── reports/
├── database/
└── logs/
```

**Important**: Add `data/` to `.gitignore` (already configured)

---

## Next Steps

1. **Test AI Detection**:
   - Open ChatGPT or Claude during a session
   - Check detection in session stats

2. **Customize AI Tools**:
   - Edit `config/ai_tools.json`
   - Add custom tools or keywords

3. **Generate Reports**:
   - Coming in next update
   - Will export PDF reports with evidence

4. **Deploy Production**:
   - See `DEPLOYMENT.md` for production setup
   - Includes database setup, SSL, multi-user support

---

## Need Help?

- **Documentation**: See `docs/` folder
- **API Reference**: http://localhost:8080/docs
- **Issues**: https://github.com/minuttt/Integraty/issues

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-26
