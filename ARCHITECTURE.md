# Integraty - System Architecture

## Executive Summary

**Integraty** is a professional desktop monitoring application designed to detect AI tool usage during monitored sessions such as examinations, interviews, certifications, training, and meetings where AI assistance is restricted.

**Core Principle**: Evidence-based detection through transparent monitoring with explicit consent, not content analysis.

---

## 1. System Overview

### 1.1 Architecture Pattern
**Modular Monolith with Plugin Architecture**

- Core monitoring engine
- Pluggable detection modules
- Local-first data processing
- Optional cloud synchronization

### 1.2 Technology Stack

#### Desktop Application
- **Framework**: Electron + React
- **Alternative**: PyQt6 for lower resource footprint
- **Language**: TypeScript (frontend), Python (backend services)

#### Backend Services
- **Runtime**: Python 3.11+
- **Framework**: FastAPI (internal API server)
- **Process Communication**: IPC via named pipes / socket.io

#### Database
- **Development/SMB**: SQLite with WAL mode
- **Enterprise**: PostgreSQL 14+
- **Encryption**: SQLCipher for SQLite, pgcrypto for PostgreSQL

#### Core Libraries
- **Screen Capture**: MSS (cross-platform), Pillow
- **OCR**: Tesseract 5.0+, EasyOCR (fallback)
- **Window Monitoring**: 
  - Windows: `pywin32`, `psutil`
  - macOS: `Quartz`, `AppKit`
  - Linux: `python-xlib`, `ewmh`
- **Browser Detection**: 
  - Native messaging protocol
  - Process monitoring fallback
- **Cryptography**: `cryptography` library, Fernet encryption
- **Computer Vision**: OpenCV 4.x

---

## 2. Core Modules

### 2.1 Session Manager
**Responsibility**: Session lifecycle management

**Components**:
- Session initialization with consent workflow
- State machine (idle → active → paused → completed)
- Session configuration management
- Graceful shutdown handling

**Key Features**:
- Pre-flight permission checks
- Session UUID generation
- Audit log initialization
- Resource allocation

### 2.2 Screen Capture Engine
**Responsibility**: Periodic screenshot capture

**Components**:
- Multi-monitor support
- Configurable capture intervals (5s - 60s)
- Adaptive quality compression
- SHA-256 hashing for integrity

**Storage Strategy**:
- Original screenshots encrypted at rest
- Thumbnails for timeline view
- Metadata stored separately

**Performance**:
- Async capture pipeline
- Buffer management (max 1000 screenshots in memory)
- Automatic compression for long sessions

### 2.3 Active Window Monitor
**Responsibility**: Track foreground applications

**Data Collected**:
- Process name and PID
- Window title
- Focus duration
- Transition timestamps
- Screen coordinates (for multi-monitor)

**Privacy Controls**:
- Exclude password managers
- Sanitize sensitive window titles
- Configurable blacklist

### 2.4 Browser Activity Monitor
**Responsibility**: Track browser-based activity

**Implementation**:
- **Primary**: Browser extension (optional, consent-based)
- **Fallback**: Window title parsing + URL detection

**Data Collected**:
- Domain names only (no full URLs)
- Tab titles
- Active tab duration
- Navigation events

**Supported Browsers**:
- Chrome/Chromium
- Firefox
- Edge
- Safari (limited)

### 2.5 OCR Analysis Engine
**Responsibility**: Extract text from screenshots

**Pipeline**:
1. Preprocessing (contrast enhancement, deskew)
2. Region of Interest (ROI) detection
3. Tesseract OCR execution
4. Text normalization
5. Keyword matching

**Optimization**:
- Incremental processing (diff detection)
- GPU acceleration where available
- Text caching to avoid redundant OCR

**Accuracy Improvements**:
- Multi-language support
- Custom training data for AI tool interfaces
- Confidence thresholding

### 2.6 AI Tool Detection Engine
**Responsibility**: Identify AI tool usage patterns

**Detection Methods**:

#### 2.6.1 Signature Detection
- Domain matching (chatgpt.com, claude.ai, etc.)
- Process name matching (GitHub Copilot, Cursor, etc.)
- Window title patterns

#### 2.6.2 Visual Pattern Recognition
- Interface detection (ChatGPT UI elements)
- Logo detection via template matching
- Color scheme analysis

#### 2.6.3 Behavioral Heuristics
- Copy-paste patterns from AI tools
- Rapid content generation detection
- Tab switching patterns

#### 2.6.4 OCR-Based Detection
- Keyword extraction from screenshots
- Prompt/response pattern recognition
- AI disclaimer text detection

**Confidence Scoring System**:
```
Low (0.0 - 0.3):    Generic AI keywords detected
Medium (0.3 - 0.6): AI website visited, minimal interaction
High (0.6 - 0.8):   Active AI tool usage detected
Very High (0.8 - 1.0): Repeated AI interactions with evidence
```

**Configurable Detection List**:
```json
{
  "chatbots": [
    {"name": "ChatGPT", "domains": ["chatgpt.com", "chat.openai.com"], "keywords": ["ChatGPT", "OpenAI"]},
    {"name": "Claude", "domains": ["claude.ai"], "keywords": ["Claude", "Anthropic"]},
    {"name": "Gemini", "domains": ["gemini.google.com"], "keywords": ["Gemini", "Bard"]}
  ],
  "code_assistants": [
    {"name": "GitHub Copilot", "processes": ["Copilot"], "keywords": ["Copilot suggestion"]},
    {"name": "Cursor", "processes": ["Cursor"], "keywords": ["Cursor AI"]}
  ],
  "image_generation": [
    {"name": "Midjourney", "domains": ["midjourney.com"], "keywords": ["Midjourney"]},
    {"name": "DALL-E", "domains": ["labs.openai.com"], "keywords": ["DALL·E", "DALL-E"]}
  ]
}
```

### 2.7 Evidence Database
**Responsibility**: Secure storage of monitoring data

**Schema Design**: See DATABASE_SCHEMA.md

**Key Features**:
- Full audit trail
- Immutable evidence records
- Cryptographic integrity verification
- Efficient querying for report generation

### 2.8 Report Generator
**Responsibility**: Create comprehensive integrity reports

**Report Types**:
- **Summary Report**: Executive overview
- **Detailed Report**: Complete timeline with evidence
- **Evidence Pack**: Raw data export for third-party review

**Output Formats**:
- PDF (primary)
- HTML (interactive)
- JSON (machine-readable)

**Report Sections**:
1. Session Metadata
2. Executive Summary
3. Timeline Visualization
4. Evidence Summary
5. Confidence Assessment
6. Flagged Events
7. Screenshots Gallery
8. Technical Appendix

**Language Guidelines**:
- Evidence-based, not accusatory
- Clear confidence levels
- Avoid definitive claims
- Example: "Evidence suggests possible AI-assisted activity (confidence: high)" vs "User cheated with AI"

### 2.9 Privacy Controller
**Responsibility**: Enforce privacy policies

**Features**:
- Consent management
- Data minimization
- Sensitive data filtering
- Retention policy enforcement
- User data access (GDPR/CCPA compliance)

**Privacy Modes**:
- **Standard**: Full monitoring
- **Privacy-Enhanced**: Exclude non-work applications
- **Minimal**: Window titles only, no screenshots

### 2.10 Administrative Dashboard
**Responsibility**: Session management and review interface

**Features**:
- Session list with search/filter
- Real-time monitoring view
- Evidence review interface
- Bulk operations
- Export functionality
- User management
- Configuration management

---

## 3. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     INTEGRATY DESKTOP APP                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Electron UI (React + TypeScript)              │ │
│  │  ┌─────────────┬─────────────┬──────────────┬───────────┐ │ │
│  │  │   Session   │   Live      │   Report     │   Admin   │ │ │
│  │  │   Control   │   Monitor   │   Viewer     │   Panel   │ │ │
│  │  └─────────────┴─────────────┴──────────────┴───────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    IPC Bridge Layer                        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │               Python Backend Service (FastAPI)             │ │
│  │  ┌────────────────────────────────────────────────────┐   │ │
│  │  │              Session Manager                        │   │ │
│  │  └────────────────────────────────────────────────────┘   │ │
│  │  ┌──────────────┬─────────────┬────────────┬──────────┐   │ │
│  │  │   Screen     │   Window    │  Browser   │   OCR    │   │ │
│  │  │   Capture    │   Monitor   │  Monitor   │  Engine  │   │ │
│  │  └──────────────┴─────────────┴────────────┴──────────┘   │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │          AI Tool Detection Engine                     │ │ │
│  │  │  ┌──────────┬────────────┬─────────────┬──────────┐ │ │ │
│  │  │  │Signature │  Visual    │ Behavioral  │   OCR    │ │ │ │
│  │  │  │Detection │  Pattern   │ Heuristics  │  Based   │ │ │ │
│  │  │  └──────────┴────────────┴─────────────┴──────────┘ │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │  ┌────────────────────────────────────────────────────┐   │ │
│  │  │              Privacy Controller                     │   │ │
│  │  └────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  Evidence Database                         │ │
│  │              (SQLite/PostgreSQL + SQLCipher)              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  Report Generator                          │ │
│  │              (PDF/HTML/JSON Export)                       │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │   Optional Cloud Sync  │
                  │   (Enterprise Only)    │
                  └────────────────────────┘
```

---

## 4. Security Model

### 4.1 Data Encryption
- **At Rest**: AES-256 encryption for all evidence
- **In Transit**: TLS 1.3 for cloud sync
- **Key Management**: User-specific encryption keys, secure key derivation

### 4.2 Authentication & Authorization
- **Local Mode**: OS-level authentication
- **Enterprise Mode**: SSO integration (SAML, OAuth2)
- **Role-Based Access Control**: Admin, Proctor, Reviewer, Auditor

### 4.3 Integrity Verification
- SHA-256 hashing of all evidence
- Digital signatures for reports
- Audit log with cryptographic chain

### 4.4 Privacy Protection
- Data minimization by design
- Anonymization options
- Secure deletion (overwrite + unlink)
- No external telemetry without consent

---

## 5. Compliance & Legal

### 5.1 Consent Management
- Explicit opt-in before monitoring
- Clear disclosure of data collection
- Right to refuse and consequences
- Session-by-session consent option

### 5.2 Data Protection
- GDPR compliance (EU)
- CCPA compliance (California)
- FERPA compliance (Educational institutions)
- HIPAA considerations (Healthcare)

### 5.3 Transparency
- Open source detection rules
- User-accessible monitoring data
- Clear reporting language
- Appeal process support

---

## 6. Performance Requirements

### 6.1 Resource Usage
- **CPU**: < 5% average utilization
- **Memory**: < 500MB RAM
- **Disk**: ~100MB per hour of monitoring
- **Network**: Minimal (local-first)

### 6.2 Scalability
- Support 8+ hour sessions
- Handle 10,000+ screenshots per session
- Sub-second report generation for standard sessions
- Support 1000+ concurrent sessions (enterprise server)

### 6.3 Reliability
- 99.9% uptime during monitoring
- Automatic recovery from crashes
- Evidence integrity preservation
- Graceful degradation

---

## 7. Deployment Architecture

### 7.1 Standalone Desktop
- Single executable installer
- Local SQLite database
- No server required
- Offline operation

### 7.2 Enterprise Server
```
┌─────────────────────────────────────────┐
│         Load Balancer (nginx)           │
└─────────────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Server  │  │ Server  │  │ Server  │
│ Node 1  │  │ Node 2  │  │ Node 3  │
└─────────┘  └─────────┘  └─────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   PostgreSQL Cluster │
        │   (Primary/Replica)  │
        └──────────────────────┘
                   │
                   ▼
          ┌─────────────────┐
          │   Object Storage │
          │   (Screenshots)  │
          └─────────────────┘
```

### 7.3 Cloud-Managed Service (SaaS)
- Multi-tenant architecture
- Per-organization data isolation
- Managed infrastructure
- Auto-scaling
- Backup & disaster recovery

---

## 8. Extensibility

### 8.1 Plugin System
- Custom detection modules
- Third-party integrations
- Custom report templates
- Webhook notifications

### 8.2 API Design
- RESTful API for enterprise integrations
- Webhook endpoints for events
- OAuth2 for third-party access
- GraphQL for flexible queries

---

## 9. Monitoring & Observability

### 9.1 Application Monitoring
- Health check endpoints
- Performance metrics
- Error tracking
- Usage analytics (anonymized)

### 9.2 Audit Logging
- All administrative actions
- Session lifecycle events
- Data access logs
- Configuration changes

---

## 10. Testing Strategy

### 10.1 Unit Tests
- Core logic coverage > 90%
- Detection algorithm validation
- Privacy controller tests

### 10.2 Integration Tests
- End-to-end session workflows
- Database integrity tests
- Report generation validation

### 10.3 Security Tests
- Penetration testing
- Encryption validation
- Access control verification
- Data leak prevention

### 10.4 Performance Tests
- Load testing (concurrent sessions)
- Resource usage benchmarks
- Long-session stability tests

---

## 11. Development Roadmap

See ROADMAP.md for detailed timeline.

---

## 12. Non-Functional Requirements

### 12.1 Usability
- Installation in < 5 minutes
- Session start in < 30 seconds
- Intuitive UI for non-technical users
- Comprehensive documentation

### 12.2 Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
- High contrast mode

### 12.3 Internationalization
- Multi-language UI (English, Spanish, French, German, Chinese)
- Locale-specific date/time formatting
- RTL language support

### 12.4 Maintainability
- Modular architecture
- Comprehensive logging
- Automated testing
- Clear code documentation

---

## Document Version
- **Version**: 1.0
- **Last Updated**: 2026-06-26
- **Author**: Integraty Development Team
