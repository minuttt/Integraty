# Integraty - API Design

## API Architecture

**Pattern**: RESTful API with WebSocket support for real-time updates

**Base URL**: 
- Local: `http://localhost:8080/api/v1`
- Enterprise: `https://api.integraty.com/v1`

**Authentication**: 
- JWT tokens (local mode)
- OAuth2 / SAML (enterprise mode)

**Content Type**: `application/json`

---

## Authentication Endpoints

### POST /auth/login
**Description**: Authenticate user and receive JWT token

**Request**:
```json
{
  "username": "user@example.com",
  "password": "********",
  "organization": "acme-corp"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "refresh_token_here",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "username": "user@example.com",
    "full_name": "John Doe",
    "role": "proctor"
  }
}
```

### POST /auth/refresh
**Description**: Refresh access token

**Request**:
```json
{
  "refresh_token": "refresh_token_here"
}
```

**Response** (200 OK):
```json
{
  "access_token": "new_token",
  "expires_in": 3600
}
```

### POST /auth/logout
**Description**: Invalidate tokens

**Headers**: `Authorization: Bearer <token>`

**Response** (204 No Content)

---

## Session Management Endpoints

### POST /sessions
**Description**: Create a new monitoring session

**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "session_name": "Final Exam - Computer Science 101",
  "session_type": "exam",
  "user_id": "user-uuid",
  "scheduled_duration_minutes": 120,
  "config": {
    "screenshot_interval_seconds": 30,
    "enable_ocr": true,
    "enable_browser_monitoring": true,
    "enable_window_monitoring": true,
    "privacy_mode": "standard",
    "monitors_to_capture": "all"
  },
  "proctor_id": "proctor-uuid",
  "notes": "Midterm examination"
}
```

**Response** (201 Created):
```json
{
  "id": "session-uuid",
  "status": "pending",
  "start_url": "integraty://start-session/session-uuid",
  "encryption_key": "base64-encoded-key",
  "created_at": "2026-06-26T10:00:00Z"
}
```

### GET /sessions
**Description**: List all sessions (with filtering)

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `status`: Filter by status (pending, active, completed, etc.)
- `user_id`: Filter by user
- `session_type`: Filter by type (exam, interview, etc.)
- `start_date`: From date (ISO 8601)
- `end_date`: To date (ISO 8601)
- `risk_level`: Filter by risk level
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `sort`: Sort field (default: start_time)
- `order`: Sort order (asc, desc)

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "session-uuid-1",
      "session_name": "Final Exam",
      "user": {
        "id": "user-uuid",
        "username": "student@example.com",
        "full_name": "Jane Student"
      },
      "session_type": "exam",
      "start_time": "2026-06-26T10:00:00Z",
      "end_time": "2026-06-26T12:00:00Z",
      "status": "completed",
      "integrity_score": 0.92,
      "risk_level": "low",
      "detection_count": 2,
      "high_confidence_detection_count": 0
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

### GET /sessions/:sessionId
**Description**: Get detailed session information

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "id": "session-uuid",
  "session_name": "Final Exam",
  "session_type": "exam",
  "user": {
    "id": "user-uuid",
    "username": "student@example.com",
    "full_name": "Jane Student"
  },
  "proctor": {
    "id": "proctor-uuid",
    "full_name": "Prof. Smith"
  },
  "start_time": "2026-06-26T10:00:00Z",
  "end_time": "2026-06-26T12:00:00Z",
  "actual_duration_minutes": 120,
  "status": "completed",
  "integrity_score": 0.92,
  "risk_level": "low",
  "config": {
    "screenshot_interval_seconds": 30,
    "enable_ocr": true,
    "enable_browser_monitoring": true
  },
  "statistics": {
    "screenshot_count": 240,
    "window_event_count": 145,
    "browser_event_count": 52,
    "detection_event_count": 2,
    "high_confidence_detection_count": 0,
    "unique_tools_detected": 1
  },
  "notes": "Midterm examination",
  "created_at": "2026-06-26T09:55:00Z",
  "updated_at": "2026-06-26T12:01:00Z"
}
```

### PATCH /sessions/:sessionId
**Description**: Update session (limited fields)

**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "status": "paused",
  "notes": "Student requested bathroom break"
}
```

**Response** (200 OK): Updated session object

### POST /sessions/:sessionId/start
**Description**: Start monitoring session

**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "consent_acknowledged": true,
  "system_info": {
    "os": "Windows 11",
    "os_version": "10.0.26200",
    "monitor_count": 2,
    "screen_resolution": "1920x1080"
  }
}
```

**Response** (200 OK):
```json
{
  "status": "active",
  "start_time": "2026-06-26T10:00:00Z",
  "websocket_url": "ws://localhost:8080/ws/sessions/session-uuid"
}
```

### POST /sessions/:sessionId/pause
**Description**: Pause monitoring session

**Response** (200 OK):
```json
{
  "status": "paused",
  "paused_at": "2026-06-26T10:30:00Z"
}
```

### POST /sessions/:sessionId/resume
**Description**: Resume paused session

**Response** (200 OK):
```json
{
  "status": "active",
  "resumed_at": "2026-06-26T10:35:00Z"
}
```

### POST /sessions/:sessionId/complete
**Description**: Complete monitoring session

**Request**:
```json
{
  "reason": "time_limit_reached"
}
```

**Response** (200 OK):
```json
{
  "status": "completed",
  "end_time": "2026-06-26T12:00:00Z",
  "final_integrity_score": 0.92,
  "risk_level": "low"
}
```

### DELETE /sessions/:sessionId
**Description**: Delete session (soft delete or hard delete based on policy)

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `hard_delete`: true/false (default: false)

**Response** (204 No Content)

---

## Evidence Endpoints

### GET /sessions/:sessionId/screenshots
**Description**: List screenshots for a session

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `page`: Page number
- `limit`: Items per page
- `start_time`: Filter from timestamp
- `end_time`: Filter to timestamp

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "screenshot-uuid",
      "timestamp": "2026-06-26T10:00:30Z",
      "sequence_number": 1,
      "thumbnail_url": "/api/v1/screenshots/screenshot-uuid/thumbnail",
      "full_url": "/api/v1/screenshots/screenshot-uuid",
      "width": 1920,
      "height": 1080,
      "file_size": 245678,
      "sha256_hash": "abc123...",
      "ocr_processed": true,
      "has_detections": false
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 240
  }
}
```

### GET /screenshots/:screenshotId
**Description**: Get screenshot image

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
- Content-Type: `image/png`
- Body: Binary image data

### GET /screenshots/:screenshotId/thumbnail
**Description**: Get screenshot thumbnail

**Response** (200 OK):
- Content-Type: `image/jpeg`
- Body: Binary image data

### GET /screenshots/:screenshotId/metadata
**Description**: Get screenshot metadata and OCR results

**Response** (200 OK):
```json
{
  "id": "screenshot-uuid",
  "timestamp": "2026-06-26T10:00:30Z",
  "width": 1920,
  "height": 1080,
  "sha256_hash": "abc123...",
  "ocr_results": {
    "text_preview": "First 200 characters...",
    "confidence": 0.94,
    "word_count": 145,
    "language": "eng"
  },
  "detections": [
    {
      "tool_name": "ChatGPT",
      "confidence_level": "medium",
      "confidence_score": 0.65
    }
  ]
}
```

### GET /sessions/:sessionId/window-events
**Description**: List window events for a session

**Query Parameters**:
- `page`, `limit`, `start_time`, `end_time`
- `process_name`: Filter by process

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "event-uuid",
      "timestamp": "2026-06-26T10:01:00Z",
      "process_name": "chrome.exe",
      "window_title": "ChatGPT - Google Chrome",
      "duration_seconds": 45,
      "is_ai_tool": true
    }
  ],
  "pagination": {...}
}
```

### GET /sessions/:sessionId/browser-events
**Description**: List browser events for a session

**Query Parameters**:
- `page`, `limit`, `start_time`, `end_time`
- `domain`: Filter by domain
- `is_ai_domain`: Filter AI domains only

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "event-uuid",
      "timestamp": "2026-06-26T10:01:15Z",
      "browser_name": "Chrome",
      "domain": "chatgpt.com",
      "tab_title": "ChatGPT",
      "duration_seconds": 30,
      "is_ai_domain": true,
      "ai_tool_name": "ChatGPT"
    }
  ],
  "pagination": {...}
}
```

### GET /sessions/:sessionId/detections
**Description**: List detection events for a session

**Query Parameters**:
- `page`, `limit`
- `confidence_level`: Filter by level (low, medium, high, very_high)
- `tool_name`: Filter by tool
- `tool_type`: Filter by type
- `reviewed`: Filter by review status

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "detection-uuid",
      "timestamp": "2026-06-26T10:15:30Z",
      "event_type": "ai_website_visit",
      "tool_name": "ChatGPT",
      "tool_type": "chatbot",
      "confidence_score": 0.85,
      "confidence_level": "high",
      "detection_method": "domain_match",
      "evidence": {
        "screenshot_id": "screenshot-uuid",
        "browser_event_id": "browser-event-uuid"
      },
      "reviewed": false
    }
  ],
  "pagination": {...}
}
```

### PATCH /detections/:detectionId/review
**Description**: Review and update detection event

**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "verdict": "confirmed",
  "notes": "Confirmed AI tool usage during restricted period"
}
```

**Response** (200 OK): Updated detection object

### GET /sessions/:sessionId/timeline
**Description**: Get unified timeline of all events

**Query Parameters**:
- `start_time`, `end_time`
- `event_types`: Comma-separated (screenshot,window,browser,detection)

**Response** (200 OK):
```json
{
  "timeline": [
    {
      "timestamp": "2026-06-26T10:00:00Z",
      "event_type": "session_start",
      "description": "Session started"
    },
    {
      "timestamp": "2026-06-26T10:00:30Z",
      "event_type": "screenshot",
      "data": {"id": "screenshot-uuid"}
    },
    {
      "timestamp": "2026-06-26T10:01:00Z",
      "event_type": "window",
      "data": {"process": "chrome.exe", "title": "Google Chrome"}
    },
    {
      "timestamp": "2026-06-26T10:15:30Z",
      "event_type": "detection",
      "data": {
        "tool": "ChatGPT",
        "confidence": "high",
        "id": "detection-uuid"
      }
    }
  ]
}
```

---

## Report Endpoints

### POST /sessions/:sessionId/reports
**Description**: Generate a new report

**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "report_type": "detailed",
  "format": "pdf",
  "options": {
    "include_screenshots": true,
    "include_timeline": true,
    "include_evidence": true,
    "anonymize": false
  }
}
```

**Response** (202 Accepted):
```json
{
  "report_id": "report-uuid",
  "status": "generating",
  "estimated_time_seconds": 30
}
```

### GET /reports/:reportId
**Description**: Get report metadata

**Response** (200 OK):
```json
{
  "id": "report-uuid",
  "session_id": "session-uuid",
  "report_type": "detailed",
  "format": "pdf",
  "status": "completed",
  "generated_at": "2026-06-26T12:05:00Z",
  "file_size": 2458345,
  "download_url": "/api/v1/reports/report-uuid/download"
}
```

### GET /reports/:reportId/download
**Description**: Download report file

**Response** (200 OK):
- Content-Type: `application/pdf` or `text/html` or `application/json`
- Content-Disposition: `attachment; filename="report.pdf"`
- Body: File content

### GET /sessions/:sessionId/reports
**Description**: List reports for a session

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "report-uuid",
      "report_type": "summary",
      "format": "pdf",
      "generated_at": "2026-06-26T12:05:00Z",
      "download_url": "/api/v1/reports/report-uuid/download"
    }
  ]
}
```

---

## Configuration Endpoints

### GET /config/ai-tools
**Description**: Get list of configured AI tools for detection

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "tools": [
    {
      "id": "tool-uuid",
      "tool_name": "ChatGPT",
      "tool_type": "chatbot",
      "enabled": true,
      "domains": ["chatgpt.com", "chat.openai.com"],
      "keywords": ["ChatGPT", "OpenAI", "regenerate response"],
      "priority": 100
    },
    {
      "id": "tool-uuid-2",
      "tool_name": "GitHub Copilot",
      "tool_type": "code_assistant",
      "enabled": true,
      "processes": ["Copilot"],
      "keywords": ["Copilot suggestion"],
      "priority": 90
    }
  ]
}
```

### POST /config/ai-tools
**Description**: Add new AI tool configuration

**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "tool_name": "New AI Tool",
  "tool_type": "chatbot",
  "domains": ["newtool.ai"],
  "keywords": ["New Tool"],
  "enabled": true
}
```

**Response** (201 Created): Created tool object

### PATCH /config/ai-tools/:toolId
**Description**: Update AI tool configuration

**Request**:
```json
{
  "enabled": false
}
```

**Response** (200 OK): Updated tool object

### DELETE /config/ai-tools/:toolId
**Description**: Delete AI tool configuration

**Response** (204 No Content)

### GET /config/system
**Description**: Get system settings

**Response** (200 OK):
```json
{
  "settings": {
    "default_screenshot_interval": 30,
    "max_session_duration_hours": 8,
    "data_retention_days": 90,
    "require_consent": true,
    "enable_telemetry": false
  }
}
```

### PATCH /config/system
**Description**: Update system settings

**Request**:
```json
{
  "data_retention_days": 180
}
```

**Response** (200 OK): Updated settings object

---

## User Management Endpoints

### GET /users
**Description**: List users (admin only)

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `role`: Filter by role
- `organization_id`: Filter by organization
- `is_active`: Filter by active status

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "user-uuid",
      "username": "user@example.com",
      "full_name": "John Doe",
      "role": "proctor",
      "is_active": true,
      "created_at": "2026-01-15T10:00:00Z"
    }
  ],
  "pagination": {...}
}
```

### POST /users
**Description**: Create new user (admin only)

**Request**:
```json
{
  "username": "newuser@example.com",
  "email": "newuser@example.com",
  "full_name": "New User",
  "role": "reviewer",
  "password": "temporary_password",
  "organization_id": "org-uuid"
}
```

**Response** (201 Created): Created user object

### GET /users/:userId
**Description**: Get user details

**Response** (200 OK): User object

### PATCH /users/:userId
**Description**: Update user

**Request**:
```json
{
  "full_name": "Updated Name",
  "role": "admin"
}
```

**Response** (200 OK): Updated user object

### DELETE /users/:userId
**Description**: Deactivate user

**Response** (204 No Content)

---

## Statistics & Analytics Endpoints

### GET /statistics/overview
**Description**: Get system-wide statistics

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `start_date`, `end_date`: Date range

**Response** (200 OK):
```json
{
  "period": {
    "start": "2026-06-01T00:00:00Z",
    "end": "2026-06-30T23:59:59Z"
  },
  "sessions": {
    "total": 1250,
    "completed": 1180,
    "active": 5,
    "cancelled": 65
  },
  "detections": {
    "total": 342,
    "high_confidence": 89,
    "unique_tools": 12
  },
  "integrity": {
    "average_score": 0.87,
    "high_risk_sessions": 23,
    "flagged_users": 15
  }
}
```

### GET /statistics/tools
**Description**: Get AI tool detection statistics

**Response** (200 OK):
```json
{
  "tools": [
    {
      "tool_name": "ChatGPT",
      "detection_count": 145,
      "session_count": 78,
      "avg_confidence": 0.82
    },
    {
      "tool_name": "GitHub Copilot",
      "detection_count": 89,
      "session_count": 45,
      "avg_confidence": 0.91
    }
  ]
}
```

### GET /statistics/users/:userId
**Description**: Get user-specific statistics

**Response** (200 OK):
```json
{
  "user_id": "user-uuid",
  "sessions": {
    "total": 15,
    "completed": 14,
    "average_duration_minutes": 95
  },
  "integrity": {
    "average_score": 0.94,
    "best_score": 1.0,
    "worst_score": 0.78
  },
  "detections": {
    "total": 3,
    "high_confidence": 1
  }
}
```

---

## Audit Log Endpoints

### GET /audit-logs
**Description**: Retrieve audit logs (admin only)

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `user_id`: Filter by user
- `action`: Filter by action type
- `entity_type`: Filter by entity
- `start_date`, `end_date`
- `page`, `limit`

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "log-uuid",
      "timestamp": "2026-06-26T10:00:00Z",
      "user": {
        "id": "user-uuid",
        "username": "admin@example.com"
      },
      "action": "create",
      "entity_type": "session",
      "entity_id": "session-uuid",
      "ip_address": "192.168.1.100",
      "status": "success"
    }
  ],
  "pagination": {...}
}
```

---

## WebSocket API

### Connection
**URL**: `ws://localhost:8080/ws/sessions/:sessionId`

**Authentication**: Send JWT token in connection query parameter
```
ws://localhost:8080/ws/sessions/session-uuid?token=jwt_token_here
```

### Events (Server → Client)

#### Session Status Update
```json
{
  "event": "session.status",
  "data": {
    "session_id": "session-uuid",
    "status": "active",
    "timestamp": "2026-06-26T10:00:00Z"
  }
}
```

#### New Screenshot
```json
{
  "event": "screenshot.captured",
  "data": {
    "id": "screenshot-uuid",
    "timestamp": "2026-06-26T10:00:30Z",
    "sequence_number": 1,
    "thumbnail_url": "/api/v1/screenshots/screenshot-uuid/thumbnail"
  }
}
```

#### New Detection
```json
{
  "event": "detection.new",
  "data": {
    "id": "detection-uuid",
    "timestamp": "2026-06-26T10:15:30Z",
    "tool_name": "ChatGPT",
    "confidence_level": "high",
    "confidence_score": 0.85
  }
}
```

#### Integrity Score Update
```json
{
  "event": "integrity.updated",
  "data": {
    "session_id": "session-uuid",
    "integrity_score": 0.92,
    "risk_level": "low",
    "timestamp": "2026-06-26T10:15:31Z"
  }
}
```

### Commands (Client → Server)

#### Heartbeat
```json
{
  "command": "ping"
}
```

**Response**:
```json
{
  "event": "pong",
  "timestamp": "2026-06-26T10:00:00Z"
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Session with ID 'xyz' not found",
    "details": {
      "resource_type": "session",
      "resource_id": "xyz"
    },
    "timestamp": "2026-06-26T10:00:00Z",
    "request_id": "req_abc123"
  }
}
```

### HTTP Status Codes

- **200 OK**: Success
- **201 Created**: Resource created
- **202 Accepted**: Request accepted, processing asynchronously
- **204 No Content**: Success, no body
- **400 Bad Request**: Invalid input
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict (e.g., duplicate)
- **422 Unprocessable Entity**: Validation error
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Service temporarily unavailable

### Error Codes

- `AUTHENTICATION_FAILED`
- `AUTHORIZATION_FAILED`
- `RESOURCE_NOT_FOUND`
- `VALIDATION_ERROR`
- `DUPLICATE_RESOURCE`
- `SESSION_ALREADY_ACTIVE`
- `SESSION_NOT_ACTIVE`
- `INVALID_SESSION_STATE`
- `ENCRYPTION_ERROR`
- `STORAGE_ERROR`
- `RATE_LIMIT_EXCEEDED`
- `INTERNAL_ERROR`

---

## Rate Limiting

**Default Limits**:
- Anonymous: 10 requests/minute
- Authenticated: 100 requests/minute
- Admin: 500 requests/minute

**Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1687785600
```

---

## Versioning

**URL Versioning**: `/api/v1/...`

**Deprecation Notice**: Via response headers
```
Deprecation: true
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
Link: <https://docs.integraty.com/api/v2>; rel="successor-version"
```

---

## Pagination

**Query Parameters**:
- `page`: Page number (1-indexed)
- `limit`: Items per page (max 100)

**Response Format**:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_previous": false,
    "next_page": 2,
    "previous_page": null
  }
}
```

---

## Filtering & Sorting

**Filter Format**: Query parameters
```
GET /sessions?status=active&risk_level=high&start_date=2026-06-01
```

**Sort Format**: 
```
GET /sessions?sort=start_time&order=desc
```

**Multiple Sorts**:
```
GET /sessions?sort=risk_level,start_time&order=desc,desc
```

---

## Webhooks (Enterprise)

### Configuration
**POST /webhooks**

**Request**:
```json
{
  "url": "https://customer.com/webhooks/integraty",
  "events": ["session.completed", "detection.high_confidence"],
  "secret": "webhook_secret_key"
}
```

### Webhook Payload

**Headers**:
```
X-Integraty-Event: session.completed
X-Integraty-Signature: sha256=...
Content-Type: application/json
```

**Body**:
```json
{
  "event": "session.completed",
  "timestamp": "2026-06-26T12:00:00Z",
  "data": {
    "session_id": "session-uuid",
    "user_id": "user-uuid",
    "integrity_score": 0.92,
    "risk_level": "low",
    "detection_count": 2
  }
}
```

---

## Document Version
- **Version**: 1.0
- **Last Updated**: 2026-06-26
- **Author**: Integraty Development Team
