# Integraty

**AI Usage Monitoring Application** - Professional desktop application for monitoring computer activity during assessments, interviews, and meetings where AI assistance is prohibited.

## 🚀 Quick Start

### Backend Setup

1. **Install Python Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Run the Backend Server**
```bash
cd backend
python -m integraty.main
```

The API will be available at `http://localhost:8080`

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## 📋 Features

### Core Monitoring
- ✅ Screen capture (configurable intervals)
- ✅ Active window monitoring
- ✅ Session lifecycle management (start, pause, resume, complete)
- ✅ OCR text extraction
- ✅ AI tool detection (12 tools configured)
- ✅ Electron desktop app

### Current Status
**Phase 1: Core Backend** ✅
- Session management
- Screen capture engine
- Window monitoring
- REST API endpoints

**Phase 2: Detection Engine** ✅
- OCR integration with Tesseract
- AI tool signature detection (ChatGPT, Claude, Gemini, Copilot, etc.)
- Confidence scoring system
- Multi-signal analysis

**Phase 3: Frontend** ✅
- Electron desktop app
- Dashboard with real-time stats
- Session management UI
- Settings configuration

**Phase 4: Database** 🔄 (Next)
- Persistent storage
- Session history
- Report generation

## 🧪 Testing the API

### Create a Session
```bash
curl -X POST http://localhost:8080/api/v1/sessions/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "session_name": "Test Session",
    "session_type": "exam",
    "screenshot_interval": 30
  }'
```

### Start Monitoring
```bash
curl -X POST http://localhost:8080/api/v1/sessions/{session_id}/start
```

### Get Session Status
```bash
curl http://localhost:8080/api/v1/sessions/{session_id}
```

### Complete Session
```bash
curl -X POST http://localhost:8080/api/v1/sessions/{session_id}/complete
```

## 📁 Project Structure

```
integraty/
├── backend/                    # Python backend
│   ├── integraty/
│   │   ├── api/               # REST API
│   │   ├── core/              # Core monitoring logic
│   │   ├── detection/         # AI detection algorithms
│   │   └── main.py            # FastAPI app
│   └── requirements.txt
│
├── frontend/                   # Electron + React (coming soon)
├── config/                     # Configuration files
└── data/                       # Local data storage
    ├── screenshots/
    ├── reports/
    └── database/
```

## 🔧 Configuration

Edit `.env` file to customize settings:

```env
SCREENSHOT_INTERVAL=30          # Seconds between screenshots
SCREENSHOT_QUALITY=85           # JPEG quality (1-100)
OCR_ENABLED=true               # Enable text extraction
```

## 📊 API Endpoints

### Sessions
- `POST /api/v1/sessions/` - Create new session
- `GET /api/v1/sessions/` - List all sessions
- `GET /api/v1/sessions/{id}` - Get session details
- `POST /api/v1/sessions/{id}/start` - Start monitoring
- `POST /api/v1/sessions/{id}/pause` - Pause session
- `POST /api/v1/sessions/{id}/resume` - Resume session
- `POST /api/v1/sessions/{id}/complete` - End session
- `DELETE /api/v1/sessions/{id}` - Delete session

### Health Check
- `GET /health` - System health status

## 🛠️ Development

### Requirements
- Python 3.11+
- Windows 10/11 (for window monitoring)

### Install Development Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
pytest
```

## 📝 License

Proprietary - All rights reserved

## 🤝 Contributing

This is a private project. Contact the team for contribution guidelines.

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-26
