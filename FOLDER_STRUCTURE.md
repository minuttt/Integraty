# Integraty - Project Folder Structure

## Repository Structure

```
integraty/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
├── package.json
├── requirements.txt
├── pyproject.toml
│
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md
│   ├── API_DESIGN.md
│   ├── DATABASE_SCHEMA.md
│   ├── UI_WIREFRAMES.md
│   ├── SECURITY_MODEL.md
│   ├── PRIVACY_MODEL.md
│   ├── DEPLOYMENT.md
│   ├── CONTRIBUTING.md
│   ├── USER_GUIDE.md
│   ├── ADMIN_GUIDE.md
│   └── DEVELOPER_GUIDE.md
│
├── frontend/                       # Electron + React Frontend
│   ├── package.json
│   ├── tsconfig.json
│   ├── webpack.config.js
│   ├── .eslintrc.js
│   ├── .prettierrc
│   │
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── assets/
│   │       ├── icons/
│   │       ├── images/
│   │       └── fonts/
│   │
│   ├── src/
│   │   ├── main/                  # Electron main process
│   │   │   ├── main.ts
│   │   │   ├── ipc-handlers.ts
│   │   │   ├── system-tray.ts
│   │   │   ├── window-manager.ts
│   │   │   └── auto-updater.ts
│   │   │
│   │   ├── renderer/              # React application
│   │   │   ├── index.tsx
│   │   │   ├── App.tsx
│   │   │   │
│   │   │   ├── components/        # Reusable components
│   │   │   │   ├── common/
│   │   │   │   │   ├── Button/
│   │   │   │   │   │   ├── Button.tsx
│   │   │   │   │   │   ├── Button.test.tsx
│   │   │   │   │   │   └── Button.module.css
│   │   │   │   │   ├── Input/
│   │   │   │   │   ├── Card/
│   │   │   │   │   ├── Modal/
│   │   │   │   │   ├── Table/
│   │   │   │   │   ├── Toast/
│   │   │   │   │   └── Spinner/
│   │   │   │   │
│   │   │   │   ├── layout/
│   │   │   │   │   ├── Header/
│   │   │   │   │   ├── Sidebar/
│   │   │   │   │   ├── Footer/
│   │   │   │   │   └── Layout.tsx
│   │   │   │   │
│   │   │   │   ├── session/
│   │   │   │   │   ├── SessionCard/
│   │   │   │   │   ├── SessionList/
│   │   │   │   │   ├── SessionDetails/
│   │   │   │   │   ├── SessionTimeline/
│   │   │   │   │   ├── CreateSessionForm/
│   │   │   │   │   └── LiveMonitor/
│   │   │   │   │
│   │   │   │   ├── detection/
│   │   │   │   │   ├── DetectionCard/
│   │   │   │   │   ├── DetectionList/
│   │   │   │   │   ├── DetectionReview/
│   │   │   │   │   └── ConfidenceScore/
│   │   │   │   │
│   │   │   │   ├── screenshot/
│   │   │   │   │   ├── ScreenshotGallery/
│   │   │   │   │   ├── ScreenshotModal/
│   │   │   │   │   └── ScreenshotTimeline/
│   │   │   │   │
│   │   │   │   ├── report/
│   │   │   │   │   ├── ReportGenerator/
│   │   │   │   │   ├── ReportViewer/
│   │   │   │   │   └── ReportDownload/
│   │   │   │   │
│   │   │   │   ├── consent/
│   │   │   │   │   ├── ConsentScreen/
│   │   │   │   │   └── ConsentCheckbox/
│   │   │   │   │
│   │   │   │   └── charts/
│   │   │   │       ├── TimelineChart/
│   │   │   │       ├── TrendChart/
│   │   │   │       └── RiskChart/
│   │   │   │
│   │   │   ├── pages/             # Route pages
│   │   │   │   ├── Login/
│   │   │   │   │   └── LoginPage.tsx
│   │   │   │   ├── Dashboard/
│   │   │   │   │   └── DashboardPage.tsx
│   │   │   │   ├── Sessions/
│   │   │   │   │   ├── SessionsListPage.tsx
│   │   │   │   │   ├── SessionDetailPage.tsx
│   │   │   │   │   ├── NewSessionPage.tsx
│   │   │   │   │   └── LiveMonitorPage.tsx
│   │   │   │   ├── Reports/
│   │   │   │   │   └── ReportsPage.tsx
│   │   │   │   ├── Config/
│   │   │   │   │   ├── ConfigPage.tsx
│   │   │   │   │   ├── AIToolsConfig.tsx
│   │   │   │   │   └── SystemConfig.tsx
│   │   │   │   ├── Users/
│   │   │   │   │   └── UsersPage.tsx
│   │   │   │   ├── AuditLogs/
│   │   │   │   │   └── AuditLogsPage.tsx
│   │   │   │   └── Consent/
│   │   │   │       └── ConsentPage.tsx
│   │   │   │
│   │   │   ├── hooks/             # Custom React hooks
│   │   │   │   ├── useAuth.ts
│   │   │   │   ├── useSession.ts
│   │   │   │   ├── useWebSocket.ts
│   │   │   │   ├── useDetections.ts
│   │   │   │   └── useLocalStorage.ts
│   │   │   │
│   │   │   ├── contexts/          # React contexts
│   │   │   │   ├── AuthContext.tsx
│   │   │   │   ├── SessionContext.tsx
│   │   │   │   └── ThemeContext.tsx
│   │   │   │
│   │   │   ├── services/          # API client services
│   │   │   │   ├── api.ts
│   │   │   │   ├── auth.service.ts
│   │   │   │   ├── session.service.ts
│   │   │   │   ├── detection.service.ts
│   │   │   │   ├── report.service.ts
│   │   │   │   └── websocket.service.ts
│   │   │   │
│   │   │   ├── store/             # State management (Redux/Zustand)
│   │   │   │   ├── index.ts
│   │   │   │   ├── slices/
│   │   │   │   │   ├── authSlice.ts
│   │   │   │   │   ├── sessionSlice.ts
│   │   │   │   │   └── uiSlice.ts
│   │   │   │   └── middleware/
│   │   │   │       └── logger.ts
│   │   │   │
│   │   │   ├── utils/             # Utility functions
│   │   │   │   ├── date.ts
│   │   │   │   ├── format.ts
│   │   │   │   ├── validation.ts
│   │   │   │   ├── encryption.ts
│   │   │   │   └── constants.ts
│   │   │   │
│   │   │   ├── types/             # TypeScript types
│   │   │   │   ├── session.types.ts
│   │   │   │   ├── detection.types.ts
│   │   │   │   ├── user.types.ts
│   │   │   │   └── api.types.ts
│   │   │   │
│   │   │   ├── styles/            # Global styles
│   │   │   │   ├── global.css
│   │   │   │   ├── variables.css
│   │   │   │   ├── themes.css
│   │   │   │   └── animations.css
│   │   │   │
│   │   │   └── assets/            # Static assets
│   │   │       ├── icons/
│   │   │       ├── images/
│   │   │       └── fonts/
│   │   │
│   │   └── preload/               # Electron preload scripts
│   │       └── preload.ts
│   │
│   ├── tests/                     # Frontend tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   │
│   └── build/                     # Build output
│       ├── icons/
│       └── installers/
│
├── backend/                       # Python Backend Service
│   ├── pyproject.toml
│   ├── setup.py
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── mypy.ini
│   ├── .flake8
│   │
│   ├── integraty/                 # Main package
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI application entry
│   │   ├── config.py              # Configuration management
│   │   ├── constants.py
│   │   │
│   │   ├── api/                   # API layer
│   │   │   ├── __init__.py
│   │   │   ├── deps.py            # Dependencies
│   │   │   ├── middleware.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── auth.py
│   │   │           ├── sessions.py
│   │   │           ├── screenshots.py
│   │   │           ├── detections.py
│   │   │           ├── reports.py
│   │   │           ├── config.py
│   │   │           ├── users.py
│   │   │           ├── audit.py
│   │   │           └── websocket.py
│   │   │
│   │   ├── core/                  # Core business logic
│   │   │   ├── __init__.py
│   │   │   ├── session_manager.py
│   │   │   ├── screen_capture.py
│   │   │   ├── window_monitor.py
│   │   │   ├── browser_monitor.py
│   │   │   ├── ocr_engine.py
│   │   │   ├── detection_engine.py
│   │   │   ├── privacy_controller.py
│   │   │   └── report_generator.py
│   │   │
│   │   ├── detection/             # Detection modules
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Base detector
│   │   │   ├── signature_detector.py
│   │   │   ├── visual_detector.py
│   │   │   ├── behavioral_detector.py
│   │   │   ├── ocr_detector.py
│   │   │   └── confidence_scorer.py
│   │   │
│   │   ├── monitoring/            # Monitoring modules
│   │   │   ├── __init__.py
│   │   │   ├── screen.py
│   │   │   ├── window.py
│   │   │   ├── browser.py
│   │   │   └── process.py
│   │   │
│   │   ├── models/                # Database models
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── organization.py
│   │   │   ├── session.py
│   │   │   ├── screenshot.py
│   │   │   ├── window_event.py
│   │   │   ├── browser_event.py
│   │   │   ├── ocr_result.py
│   │   │   ├── detection_event.py
│   │   │   ├── report.py
│   │   │   ├── ai_tool_config.py
│   │   │   └── audit_log.py
│   │   │
│   │   ├── schemas/               # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── session.py
│   │   │   ├── screenshot.py
│   │   │   ├── detection.py
│   │   │   ├── report.py
│   │   │   └── auth.py
│   │   │
│   │   ├── services/              # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── session_service.py
│   │   │   ├── detection_service.py
│   │   │   ├── report_service.py
│   │   │   ├── user_service.py
│   │   │   └── audit_service.py
│   │   │
│   │   ├── db/                    # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   ├── init_db.py
│   │   │   ├── migrations/        # Alembic migrations
│   │   │   │   ├── env.py
│   │   │   │   ├── script.py.mako
│   │   │   │   └── versions/
│   │   │   └── repositories/
│   │   │       ├── __init__.py
│   │   │       ├── base.py
│   │   │       ├── session_repo.py
│   │   │       ├── detection_repo.py
│   │   │       └── user_repo.py
│   │   │
│   │   ├── utils/                 # Utility modules
│   │   │   ├── __init__.py
│   │   │   ├── encryption.py
│   │   │   ├── hashing.py
│   │   │   ├── datetime.py
│   │   │   ├── validation.py
│   │   │   ├── image_processing.py
│   │   │   └── file_storage.py
│   │   │
│   │   ├── security/              # Security modules
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── permissions.py
│   │   │   ├── jwt.py
│   │   │   ├── oauth.py
│   │   │   └── rate_limit.py
│   │   │
│   │   ├── integrations/          # External integrations
│   │   │   ├── __init__.py
│   │   │   ├── sso/
│   │   │   │   ├── saml.py
│   │   │   │   └── oauth2.py
│   │   │   └── webhooks/
│   │   │       └── webhook_sender.py
│   │   │
│   │   └── workers/               # Background workers
│   │       ├── __init__.py
│   │       ├── ocr_worker.py
│   │       ├── detection_worker.py
│   │       ├── report_worker.py
│   │       └── cleanup_worker.py
│   │
│   ├── tests/                     # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── unit/
│   │   │   ├── test_session_manager.py
│   │   │   ├── test_detection_engine.py
│   │   │   └── test_ocr_engine.py
│   │   ├── integration/
│   │   │   ├── test_api_sessions.py
│   │   │   ├── test_api_detections.py
│   │   │   └── test_database.py
│   │   └── e2e/
│   │       └── test_full_session.py
│   │
│   ├── scripts/                   # Utility scripts
│   │   ├── init_db.py
│   │   ├── seed_data.py
│   │   ├── import_ai_tools.py
│   │   └── generate_report.py
│   │
│   └── logs/                      # Log files
│       └── .gitkeep
│
├── browser-extension/             # Optional browser extension
│   ├── manifest.json
│   ├── package.json
│   │
│   ├── src/
│   │   ├── background.ts
│   │   ├── content.ts
│   │   └── popup/
│   │       ├── popup.html
│   │       └── popup.ts
│   │
│   └── build/
│
├── shared/                        # Shared code/types
│   ├── types/
│   │   ├── session.ts
│   │   ├── detection.ts
│   │   └── api.ts
│   └── constants/
│       └── ai-tools.json
│
├── data/                          # Data directory (gitignored)
│   ├── screenshots/
│   ├── reports/
│   ├── database/
│   └── logs/
│
├── config/                        # Configuration files
│   ├── ai_tools.json
│   ├── detection_rules.json
│   ├── default_config.json
│   └── nginx/
│       └── nginx.conf
│
├── scripts/                       # Build & deployment scripts
│   ├── build.sh
│   ├── deploy.sh
│   ├── docker-build.sh
│   ├── test.sh
│   └── release.sh
│
├── deployment/                    # Deployment configurations
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   └── Dockerfile.nginx
│   │
│   ├── kubernetes/
│   │   ├── namespace.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   │   └── configmap.yaml
│   │
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   └── ansible/
│       ├── playbook.yml
│       └── inventory/
│
├── .github/                       # GitHub Actions
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── cd.yml
│   │   ├── release.yml
│   │   └── security-scan.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .vscode/                       # VS Code settings
│   ├── settings.json
│   ├── launch.json
│   └── extensions.json
│
└── tools/                         # Development tools
    ├── linters/
    ├── formatters/
    └── generators/
```

---

## Data Directory Structure

### Local Development

```
~/.integraty/                      # User data directory
├── config/
│   ├── settings.json
│   └── encryption_keys/
├── data/
│   ├── database/
│   │   └── integraty.db
│   ├── screenshots/
│   │   ├── session-uuid-1/
│   │   │   ├── screenshot-001.png
│   │   │   ├── screenshot-002.png
│   │   │   └── thumbnails/
│   │   └── session-uuid-2/
│   ├── reports/
│   │   ├── report-uuid-1.pdf
│   │   └── report-uuid-2.html
│   └── logs/
│       ├── application.log
│       └── monitoring.log
└── cache/
    └── ocr/
```

### Production Deployment

```
/var/integraty/                    # Production data directory
├── config/
│   ├── production.json
│   ├── ssl/
│   │   ├── cert.pem
│   │   └── key.pem
│   └── secrets/
│       ├── db_password
│       └── jwt_secret
├── data/
│   ├── database/                  # If using SQLite
│   │   └── integraty.db
│   ├── screenshots/               # Or object storage
│   ├── reports/
│   └── backups/
│       ├── db/
│       └── files/
└── logs/
    ├── app/
    │   ├── access.log
    │   ├── error.log
    │   └── audit.log
    └── monitoring/
        └── metrics.log
```

---

## Build Artifacts

### Frontend Build Output

```
frontend/build/
├── icons/
│   ├── 16x16.png
│   ├── 32x32.png
│   ├── 64x64.png
│   ├── 128x128.png
│   ├── 256x256.png
│   ├── 512x512.png
│   └── icon.icns
│
├── installers/
│   ├── Integraty-Setup-1.0.0.exe        # Windows installer
│   ├── Integraty-1.0.0.dmg              # macOS installer
│   ├── Integraty-1.0.0.AppImage         # Linux AppImage
│   └── Integraty-1.0.0.deb              # Debian package
│
└── dist/
    ├── win-unpacked/                     # Unpacked Windows
    ├── mac/                              # macOS app
    └── linux-unpacked/                   # Unpacked Linux
```

### Backend Build Output

```
backend/dist/
├── integraty-1.0.0-py3-none-any.whl
└── integraty-1.0.0.tar.gz
```

---

## Environment Files

### Development

**.env.development**
```bash
# Application
APP_ENV=development
APP_DEBUG=true
APP_PORT=8080

# Database
DATABASE_URL=sqlite:///./integraty.db

# Security
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET=dev-jwt-secret
ENCRYPTION_KEY=dev-encryption-key

# Monitoring
SCREENSHOT_INTERVAL=30
OCR_ENABLED=true

# Logging
LOG_LEVEL=DEBUG
```

### Production

**.env.production**
```bash
# Application
APP_ENV=production
APP_DEBUG=false
APP_PORT=8080
APP_HOST=0.0.0.0

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/integraty

# Security
SECRET_KEY=${SECRET_KEY}
JWT_SECRET=${JWT_SECRET}
ENCRYPTION_KEY=${ENCRYPTION_KEY}

# Monitoring
SCREENSHOT_INTERVAL=30
OCR_ENABLED=true

# Storage
STORAGE_TYPE=s3
S3_BUCKET=integraty-screenshots
S3_REGION=us-east-1

# Logging
LOG_LEVEL=INFO
SENTRY_DSN=${SENTRY_DSN}
```

---

## Configuration Files

### package.json (Frontend)

```json
{
  "name": "integraty",
  "version": "1.0.0",
  "description": "AI Usage Monitoring Application",
  "main": "src/main/main.ts",
  "scripts": {
    "start": "electron-forge start",
    "build": "electron-forge make",
    "test": "jest",
    "lint": "eslint src/",
    "format": "prettier --write src/"
  },
  "devDependencies": {
    "@electron-forge/cli": "^7.0.0",
    "typescript": "^5.0.0",
    "webpack": "^5.0.0"
  },
  "dependencies": {
    "react": "^18.0.0",
    "electron": "^28.0.0"
  }
}
```

### pyproject.toml (Backend)

```toml
[tool.poetry]
name = "integraty"
version = "1.0.0"
description = "AI Usage Monitoring Backend"
authors = ["Integraty Team <team@integraty.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.110.0"
sqlalchemy = "^2.0.0"
pydantic = "^2.0.0"
opencv-python = "^4.9.0"
pytesseract = "^0.3.10"
mss = "^9.0.0"
cryptography = "^42.0.0"
psutil = "^5.9.0"

[tool.poetry.dev-dependencies]
pytest = "^8.0.0"
black = "^24.0.0"
mypy = "^1.8.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

---

## Git Ignore

**.gitignore**
```gitignore
# Environment files
.env
.env.local
.env.production
*.env

# Dependencies
node_modules/
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/

# Build output
dist/
build/
*.egg-info/
frontend/build/
backend/dist/

# Data directories
data/
screenshots/
reports/
*.db
*.sqlite

# Logs
logs/
*.log

# OS files
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.swp
*.swo

# Secrets
secrets/
*.pem
*.key
*.crt

# Backups
*.bak
*.backup
```

---

## Documentation Structure

```
docs/
├── architecture/
│   ├── system-overview.md
│   ├── data-flow.md
│   └── component-interaction.md
│
├── api/
│   ├── authentication.md
│   ├── sessions.md
│   ├── detections.md
│   └── reports.md
│
├── guides/
│   ├── user-guide.md
│   ├── admin-guide.md
│   ├── developer-guide.md
│   └── deployment-guide.md
│
├── security/
│   ├── security-model.md
│   ├── privacy-model.md
│   ├── encryption.md
│   └── compliance.md
│
├── development/
│   ├── setup.md
│   ├── contributing.md
│   ├── coding-standards.md
│   └── testing.md
│
└── operations/
    ├── deployment.md
    ├── monitoring.md
    ├── backup.md
    └── troubleshooting.md
```

---

## Testing Structure

### Frontend Tests

```
frontend/tests/
├── unit/
│   ├── components/
│   │   ├── Button.test.tsx
│   │   └── SessionCard.test.tsx
│   ├── hooks/
│   │   └── useAuth.test.ts
│   └── utils/
│       └── validation.test.ts
│
├── integration/
│   ├── api/
│   │   └── session.test.ts
│   └── flows/
│       └── create-session.test.tsx
│
└── e2e/
    ├── login.test.ts
    ├── session-lifecycle.test.ts
    └── report-generation.test.ts
```

### Backend Tests

```
backend/tests/
├── unit/
│   ├── test_session_manager.py
│   ├── test_detection_engine.py
│   ├── test_ocr_engine.py
│   └── test_privacy_controller.py
│
├── integration/
│   ├── test_api_auth.py
│   ├── test_api_sessions.py
│   ├── test_api_detections.py
│   └── test_database.py
│
└── e2e/
    └── test_full_monitoring_cycle.py
```

---

## CI/CD Structure

```
.github/workflows/
├── ci.yml                  # Continuous Integration
├── cd.yml                  # Continuous Deployment
├── release.yml             # Release automation
├── security-scan.yml       # Security scanning
└── docs.yml                # Documentation generation
```

---

## License Files

```
licenses/
├── LICENSE                 # Main license (MIT/Apache)
├── NOTICE                  # Third-party notices
└── THIRD_PARTY_LICENSES    # Bundled library licenses
```

---

## Document Version
- **Version**: 1.0
- **Last Updated**: 2026-06-26
- **Author**: Integraty Development Team
