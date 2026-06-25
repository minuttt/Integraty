# Integraty - Database Schema

## Database Design Principles

1. **Audit Trail**: Every record is immutable with full history
2. **Evidence Integrity**: Cryptographic hashes for verification
3. **Privacy by Design**: Sensitive data encrypted at column level
4. **Query Performance**: Optimized indexes for common queries
5. **Compliance Ready**: Support for data retention and deletion

---

## Entity Relationship Diagram

```
┌─────────────────┐
│     users       │
│─────────────────│
│ id (PK)         │──┐
│ username        │  │
│ email           │  │
│ role            │  │
│ created_at      │  │
└─────────────────┘  │
                      │
                      │ 1:N
                      │
┌─────────────────────▼───────────┐
│        sessions                 │
│─────────────────────────────────│
│ id (PK)                         │──┐
│ user_id (FK)                    │  │
│ uuid                            │  │
│ start_time                      │  │
│ end_time                        │  │
│ status                          │  │
│ config_snapshot                 │  │
│ integrity_score                 │  │
│ encryption_key_hash             │  │
└─────────────────────────────────┘  │
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                │ 1:N                 │ 1:N                 │ 1:N
                │                     │                     │
┌───────────────▼──────┐  ┌──────────▼─────────┐  ┌────────▼──────────┐
│   screenshots        │  │   window_events    │  │  browser_events   │
│──────────────────────│  │────────────────────│  │───────────────────│
│ id (PK)              │  │ id (PK)            │  │ id (PK)           │
│ session_id (FK)      │  │ session_id (FK)    │  │ session_id (FK)   │
│ timestamp            │  │ timestamp          │  │ timestamp         │
│ file_path (enc)      │  │ process_name       │  │ domain            │
│ thumbnail_path       │  │ window_title (enc) │  │ tab_title (enc)   │
│ sha256_hash          │  │ start_time         │  │ duration          │
│ width                │  │ end_time           │  │ browser_name      │
│ height               │  │ duration           │  │ url_hash          │
│ file_size            │  │ process_id         │  └───────────────────┘
└──────────────────────┘  └────────────────────┘
        │                         │
        │ 1:N                     │ 1:N
        │                         │
┌───────▼─────────────┐   ┌───────▼──────────────┐
│   ocr_results       │   │  detection_events    │
│─────────────────────│   │──────────────────────│
│ id (PK)             │   │ id (PK)              │
│ screenshot_id (FK)  │   │ session_id (FK)      │
│ timestamp           │   │ timestamp            │
│ text_content (enc)  │   │ event_type           │
│ confidence          │   │ tool_name            │
│ language            │   │ confidence_score     │
│ processing_time     │   │ evidence_type        │
└─────────────────────┘   │ screenshot_id (FK)   │
                          │ window_event_id (FK) │
                          │ browser_event_id (FK)│
                          │ ocr_result_id (FK)   │
                          │ metadata (JSON)      │
                          └──────────────────────┘
                                    │
                                    │ 1:1
                                    │
                          ┌─────────▼───────────┐
                          │  evidence_metadata  │
                          │─────────────────────│
                          │ id (PK)             │
                          │ detection_event_id  │
                          │ key                 │
                          │ value (enc)         │
                          └─────────────────────┘

┌──────────────────┐       ┌─────────────────────┐       ┌──────────────────┐
│  audit_logs      │       │   reports           │       │  ai_tool_config  │
│──────────────────│       │─────────────────────│       │──────────────────│
│ id (PK)          │       │ id (PK)             │       │ id (PK)          │
│ timestamp        │       │ session_id (FK)     │       │ tool_name        │
│ user_id (FK)     │       │ generated_at        │       │ tool_type        │
│ action           │       │ report_type         │       │ domains (JSON)   │
│ entity_type      │       │ file_path (enc)     │       │ keywords (JSON)  │
│ entity_id        │       │ file_hash           │       │ processes (JSON) │
│ old_value        │       │ format              │       │ enabled          │
│ new_value        │       │ generated_by        │       │ priority         │
│ ip_address       │       └─────────────────────┘       │ created_at       │
└──────────────────┘                                     │ updated_at       │
                                                          └──────────────────┘
```

---

## Schema Definition

### 1. Users Table

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),  -- NULL for SSO users
    full_name VARCHAR(255),
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'proctor', 'reviewer', 'auditor', 'examinee')),
    organization_id BIGINT REFERENCES organizations(id),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_organization ON users(organization_id);
CREATE INDEX idx_users_role ON users(role);
```

### 2. Organizations Table

```sql
CREATE TABLE organizations (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    domain VARCHAR(255),
    license_type VARCHAR(50) CHECK (license_type IN ('free', 'pro', 'enterprise')),
    max_concurrent_sessions INT DEFAULT 10,
    retention_days INT DEFAULT 90,
    encryption_key_version INT DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    settings JSONB
);

CREATE INDEX idx_organizations_domain ON organizations(domain);
```

### 3. Sessions Table

```sql
CREATE TABLE sessions (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    organization_id BIGINT REFERENCES organizations(id),
    session_name VARCHAR(255),
    session_type VARCHAR(50) CHECK (session_type IN ('exam', 'interview', 'certification', 'training', 'meeting', 'other')),
    
    -- Timestamps
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    scheduled_duration_minutes INT,
    actual_duration_minutes INT,
    
    -- Status
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'active', 'paused', 'completed', 'cancelled', 'error')),
    
    -- Configuration
    config_snapshot JSONB NOT NULL,  -- Snapshot of monitoring config at session start
    
    -- Integrity Assessment
    integrity_score DECIMAL(5,4) CHECK (integrity_score BETWEEN 0 AND 1),  -- 0.0000 to 1.0000
    risk_level VARCHAR(20) CHECK (risk_level IN ('none', 'low', 'medium', 'high', 'critical')),
    
    -- Security
    encryption_key_hash VARCHAR(64) NOT NULL,  -- SHA-256 of session encryption key
    data_retention_until TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    proctor_id BIGINT REFERENCES users(id),
    notes TEXT,
    metadata JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_sessions_start_time ON sessions(start_time DESC);
CREATE INDEX idx_sessions_uuid ON sessions(uuid);
CREATE INDEX idx_sessions_organization ON sessions(organization_id);
```

### 4. Screenshots Table

```sql
CREATE TABLE screenshots (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    
    -- Timing
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    sequence_number INT NOT NULL,
    
    -- File Information
    file_path TEXT NOT NULL,  -- Encrypted at application layer
    thumbnail_path TEXT,
    file_size BIGINT NOT NULL,  -- Bytes
    sha256_hash VARCHAR(64) NOT NULL,  -- For integrity verification
    
    -- Image Properties
    width INT NOT NULL,
    height INT NOT NULL,
    format VARCHAR(10) DEFAULT 'PNG',
    compression_quality INT DEFAULT 85,
    
    -- Multi-Monitor
    monitor_count INT DEFAULT 1,
    monitor_index INT DEFAULT 0,
    
    -- Processing Status
    ocr_processed BOOLEAN DEFAULT FALSE,
    ocr_processed_at TIMESTAMP WITH TIME ZONE,
    analysis_completed BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    metadata JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_screenshots_session ON screenshots(session_id);
CREATE INDEX idx_screenshots_timestamp ON screenshots(timestamp);
CREATE INDEX idx_screenshots_sequence ON screenshots(session_id, sequence_number);
CREATE INDEX idx_screenshots_hash ON screenshots(sha256_hash);
```

### 5. Window Events Table

```sql
CREATE TABLE window_events (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    
    -- Timing
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    duration_seconds INT,
    
    -- Window Information
    process_name VARCHAR(255) NOT NULL,
    process_id INT,
    window_title TEXT,  -- Encrypted at application layer
    window_class VARCHAR(255),
    
    -- Position (for multi-monitor)
    x_position INT,
    y_position INT,
    window_width INT,
    window_height INT,
    is_fullscreen BOOLEAN DEFAULT FALSE,
    
    -- Classification
    is_browser BOOLEAN DEFAULT FALSE,
    is_ide BOOLEAN DEFAULT FALSE,
    is_ai_tool BOOLEAN DEFAULT FALSE,
    category VARCHAR(50),
    
    -- Metadata
    metadata JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_window_events_session ON window_events(session_id);
CREATE INDEX idx_window_events_timestamp ON window_events(timestamp);
CREATE INDEX idx_window_events_process ON window_events(process_name);
CREATE INDEX idx_window_events_ai_tool ON window_events(is_ai_tool) WHERE is_ai_tool = TRUE;
```

### 6. Browser Events Table

```sql
CREATE TABLE browser_events (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    
    -- Timing
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_seconds INT,
    
    -- Browser Information
    browser_name VARCHAR(50) NOT NULL,
    browser_version VARCHAR(50),
    
    -- Navigation
    domain VARCHAR(255) NOT NULL,  -- Only domain, not full URL for privacy
    tab_title TEXT,  -- Encrypted at application layer
    url_hash VARCHAR(64),  -- SHA-256 of full URL (for deduplication without storing URL)
    
    -- Event Type
    event_type VARCHAR(50) CHECK (event_type IN ('navigation', 'tab_open', 'tab_close', 'tab_switch', 'page_load')),
    
    -- Classification
    is_ai_domain BOOLEAN DEFAULT FALSE,
    ai_tool_name VARCHAR(100),
    
    -- Metadata
    referrer_domain VARCHAR(255),
    metadata JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_browser_events_session ON browser_events(session_id);
CREATE INDEX idx_browser_events_timestamp ON browser_events(timestamp);
CREATE INDEX idx_browser_events_domain ON browser_events(domain);
CREATE INDEX idx_browser_events_ai_domain ON browser_events(is_ai_domain) WHERE is_ai_domain = TRUE;
```

### 7. OCR Results Table

```sql
CREATE TABLE ocr_results (
    id BIGSERIAL PRIMARY KEY,
    screenshot_id BIGINT NOT NULL REFERENCES screenshots(id) ON DELETE CASCADE,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    
    -- Timing
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    processing_time_ms INT,
    
    -- OCR Output
    text_content TEXT NOT NULL,  -- Encrypted at application layer
    raw_output JSONB,  -- Tesseract raw output with bounding boxes
    
    -- Quality Metrics
    confidence DECIMAL(5,4) CHECK (confidence BETWEEN 0 AND 1),
    language VARCHAR(10) DEFAULT 'eng',
    word_count INT,
    
    -- Processing Info
    ocr_engine VARCHAR(50) DEFAULT 'tesseract',
    engine_version VARCHAR(20),
    preprocessing_applied JSONB,
    
    -- Metadata
    metadata JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ocr_results_screenshot ON ocr_results(screenshot_id);
CREATE INDEX idx_ocr_results_timestamp ON ocr_results(timestamp);
CREATE INDEX idx_ocr_results_confidence ON ocr_results(confidence);
-- Full-text search on encrypted field must be done at application layer
```

### 8. Detection Events Table

```sql
CREATE TABLE detection_events (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    
    -- Timing
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Event Classification
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN 
        ('ai_website_visit', 'ai_process_detected', 'ai_keyword_found', 
         'ai_visual_pattern', 'ai_interaction', 'suspicious_behavior')),
    
    -- Tool Information
    tool_name VARCHAR(100) NOT NULL,
    tool_type VARCHAR(50) CHECK (tool_type IN ('chatbot', 'code_assistant', 'image_generator', 'search_engine', 'other')),
    
    -- Confidence Scoring
    confidence_score DECIMAL(5,4) NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    confidence_level VARCHAR(20) CHECK (confidence_level IN ('low', 'medium', 'high', 'very_high')),
    
    -- Evidence Links
    evidence_type VARCHAR(50) NOT NULL CHECK (evidence_type IN ('screenshot', 'window', 'browser', 'ocr', 'behavioral', 'multiple')),
    screenshot_id BIGINT REFERENCES screenshots(id),
    window_event_id BIGINT REFERENCES window_events(id),
    browser_event_id BIGINT REFERENCES browser_events(id),
    ocr_result_id BIGINT REFERENCES ocr_results(id),
    
    -- Detection Details
    detection_method VARCHAR(50) NOT NULL,  -- 'domain_match', 'keyword_match', 'visual_pattern', etc.
    matched_patterns JSONB,  -- What specifically was matched
    
    -- Human Review
    reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by BIGINT REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    review_verdict VARCHAR(50) CHECK (review_verdict IN ('confirmed', 'false_positive', 'uncertain', 'dismissed')),
    review_notes TEXT,
    
    -- Metadata
    metadata JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_detection_events_session ON detection_events(session_id);
CREATE INDEX idx_detection_events_timestamp ON detection_events(timestamp);
CREATE INDEX idx_detection_events_tool ON detection_events(tool_name);
CREATE INDEX idx_detection_events_confidence ON detection_events(confidence_score DESC);
CREATE INDEX idx_detection_events_reviewed ON detection_events(reviewed);
CREATE INDEX idx_detection_events_type ON detection_events(event_type);
```

### 9. Evidence Metadata Table

```sql
CREATE TABLE evidence_metadata (
    id BIGSERIAL PRIMARY KEY,
    detection_event_id BIGINT NOT NULL REFERENCES detection_events(id) ON DELETE CASCADE,
    
    -- Key-Value Storage for flexible evidence attributes
    key VARCHAR(255) NOT NULL,
    value TEXT,  -- Encrypted at application layer if sensitive
    value_type VARCHAR(50) DEFAULT 'string',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_evidence_metadata_detection ON evidence_metadata(detection_event_id);
CREATE INDEX idx_evidence_metadata_key ON evidence_metadata(key);
```

### 10. Reports Table

```sql
CREATE TABLE reports (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    
    -- Report Information
    report_type VARCHAR(50) NOT NULL CHECK (report_type IN ('summary', 'detailed', 'evidence_pack', 'custom')),
    report_name VARCHAR(255),
    
    -- File Information
    file_path TEXT NOT NULL,  -- Encrypted at application layer
    file_format VARCHAR(10) NOT NULL CHECK (file_format IN ('pdf', 'html', 'json', 'docx')),
    file_size BIGINT,
    file_hash VARCHAR(64),  -- SHA-256 for integrity
    
    -- Generation
    generated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    generated_by BIGINT REFERENCES users(id),
    generation_time_ms INT,
    
    -- Digital Signature
    digital_signature TEXT,  -- Cryptographic signature for authenticity
    signature_algorithm VARCHAR(50) DEFAULT 'RSA-SHA256',
    
    -- Access Control
    is_public BOOLEAN DEFAULT FALSE,
    access_count INT DEFAULT 0,
    last_accessed_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    metadata JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_reports_session ON reports(session_id);
CREATE INDEX idx_reports_generated_at ON reports(generated_at DESC);
CREATE INDEX idx_reports_type ON reports(report_type);
CREATE INDEX idx_reports_uuid ON reports(uuid);
```

### 11. AI Tool Configuration Table

```sql
CREATE TABLE ai_tool_config (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    
    -- Tool Identity
    tool_name VARCHAR(100) UNIQUE NOT NULL,
    tool_type VARCHAR(50) NOT NULL CHECK (tool_type IN ('chatbot', 'code_assistant', 'image_generator', 'search_engine', 'other')),
    
    -- Detection Signatures
    domains JSONB,  -- Array of domain patterns
    keywords JSONB,  -- Array of keyword patterns
    processes JSONB,  -- Array of process name patterns
    visual_signatures JSONB,  -- Visual pattern matching data
    
    -- Configuration
    enabled BOOLEAN DEFAULT TRUE,
    priority INT DEFAULT 100,  -- Higher priority checked first
    confidence_weight DECIMAL(3,2) DEFAULT 1.0,
    
    -- Version
    version INT DEFAULT 1,
    last_updated_by BIGINT REFERENCES users(id),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Metadata
    description TEXT,
    metadata JSONB
);

CREATE INDEX idx_ai_tool_config_enabled ON ai_tool_config(enabled) WHERE enabled = TRUE;
CREATE INDEX idx_ai_tool_config_type ON ai_tool_config(tool_type);
CREATE INDEX idx_ai_tool_config_priority ON ai_tool_config(priority DESC);
```

### 12. Audit Logs Table

```sql
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    
    -- Who
    user_id BIGINT REFERENCES users(id),
    username VARCHAR(255),  -- Denormalized for audit trail
    
    -- What
    action VARCHAR(100) NOT NULL,  -- 'create', 'update', 'delete', 'view', 'export', etc.
    entity_type VARCHAR(100) NOT NULL,  -- 'session', 'report', 'user', 'config', etc.
    entity_id BIGINT,
    entity_uuid UUID,
    
    -- Changes
    old_value JSONB,
    new_value JSONB,
    
    -- When & Where
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    
    -- Context
    session_id BIGINT REFERENCES sessions(id),
    organization_id BIGINT REFERENCES organizations(id),
    
    -- Result
    status VARCHAR(50) CHECK (status IN ('success', 'failure', 'unauthorized')),
    error_message TEXT,
    
    -- Metadata
    metadata JSONB
);

CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_session ON audit_logs(session_id);
```

### 13. System Settings Table

```sql
CREATE TABLE system_settings (
    id BIGSERIAL PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    value_type VARCHAR(50) DEFAULT 'string',
    category VARCHAR(100),
    description TEXT,
    is_encrypted BOOLEAN DEFAULT FALSE,
    updated_by BIGINT REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_system_settings_category ON system_settings(category);
```

---

## Views

### Session Summary View

```sql
CREATE VIEW session_summary AS
SELECT 
    s.id,
    s.uuid,
    s.session_name,
    s.start_time,
    s.end_time,
    s.actual_duration_minutes,
    s.status,
    s.integrity_score,
    s.risk_level,
    u.username,
    u.full_name,
    COUNT(DISTINCT sc.id) as screenshot_count,
    COUNT(DISTINCT de.id) as detection_event_count,
    COUNT(DISTINCT CASE WHEN de.confidence_level = 'high' OR de.confidence_level = 'very_high' THEN de.id END) as high_confidence_detections,
    COUNT(DISTINCT r.id) as report_count
FROM sessions s
LEFT JOIN users u ON s.user_id = u.id
LEFT JOIN screenshots sc ON s.id = sc.session_id
LEFT JOIN detection_events de ON s.id = de.session_id
LEFT JOIN reports r ON s.id = r.session_id
GROUP BY s.id, u.username, u.full_name;
```

### AI Tool Detection Summary View

```sql
CREATE VIEW ai_tool_detection_summary AS
SELECT 
    de.tool_name,
    de.tool_type,
    COUNT(*) as detection_count,
    AVG(de.confidence_score) as avg_confidence,
    COUNT(DISTINCT de.session_id) as sessions_affected,
    COUNT(CASE WHEN de.confidence_level = 'very_high' THEN 1 END) as very_high_confidence_count,
    MIN(de.timestamp) as first_detection,
    MAX(de.timestamp) as last_detection
FROM detection_events de
GROUP BY de.tool_name, de.tool_type
ORDER BY detection_count DESC;
```

---

## Stored Procedures

### Calculate Session Integrity Score

```sql
CREATE OR REPLACE FUNCTION calculate_integrity_score(p_session_id BIGINT)
RETURNS DECIMAL(5,4)
LANGUAGE plpgsql
AS $$
DECLARE
    v_score DECIMAL(5,4);
    v_detection_count INT;
    v_high_confidence_count INT;
    v_unique_tools_count INT;
BEGIN
    SELECT 
        COUNT(*),
        COUNT(CASE WHEN confidence_level IN ('high', 'very_high') THEN 1 END),
        COUNT(DISTINCT tool_name)
    INTO 
        v_detection_count,
        v_high_confidence_count,
        v_unique_tools_count
    FROM detection_events
    WHERE session_id = p_session_id;
    
    -- Scoring algorithm
    -- Start at 1.0 (perfect integrity)
    -- Deduct based on detections
    v_score := 1.0;
    
    -- Deduct 0.1 for each high-confidence detection
    v_score := v_score - (v_high_confidence_count * 0.1);
    
    -- Deduct 0.05 for each regular detection
    v_score := v_score - ((v_detection_count - v_high_confidence_count) * 0.05);
    
    -- Deduct 0.05 for each unique tool detected
    v_score := v_score - (v_unique_tools_count * 0.05);
    
    -- Ensure score is between 0 and 1
    v_score := GREATEST(0.0, LEAST(1.0, v_score));
    
    -- Update session
    UPDATE sessions
    SET integrity_score = v_score,
        risk_level = CASE
            WHEN v_score >= 0.9 THEN 'none'
            WHEN v_score >= 0.7 THEN 'low'
            WHEN v_score >= 0.5 THEN 'medium'
            WHEN v_score >= 0.3 THEN 'high'
            ELSE 'critical'
        END,
        updated_at = NOW()
    WHERE id = p_session_id;
    
    RETURN v_score;
END;
$$;
```

---

## Triggers

### Update Timestamp Trigger

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### Auto-Calculate Integrity Score Trigger

```sql
CREATE OR REPLACE FUNCTION auto_calculate_integrity_score()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM calculate_integrity_score(NEW.session_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calculate_integrity_score
AFTER INSERT OR UPDATE ON detection_events
FOR EACH ROW EXECUTE FUNCTION auto_calculate_integrity_score();
```

---

## Data Retention Policy

### Automatic Deletion Function

```sql
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    -- Delete sessions past retention date
    DELETE FROM sessions
    WHERE data_retention_until < NOW();
    
    -- Log deletion
    INSERT INTO audit_logs (action, entity_type, timestamp, metadata)
    VALUES ('auto_delete', 'session', NOW(), 
            jsonb_build_object('reason', 'retention_policy', 'executed_by', 'system'));
END;
$$;

-- Schedule via cron or application-level scheduler
```

---

## Sample Queries

### Get Session with All Detection Events

```sql
SELECT 
    s.uuid as session_uuid,
    s.session_name,
    s.start_time,
    s.integrity_score,
    s.risk_level,
    de.timestamp,
    de.tool_name,
    de.confidence_level,
    de.event_type,
    sc.file_path as screenshot_path
FROM sessions s
LEFT JOIN detection_events de ON s.id = de.session_id
LEFT JOIN screenshots sc ON de.screenshot_id = sc.id
WHERE s.uuid = 'session-uuid-here'
ORDER BY de.timestamp;
```

### Find Sessions with High-Risk AI Usage

```sql
SELECT 
    s.uuid,
    s.session_name,
    s.start_time,
    u.username,
    s.integrity_score,
    COUNT(de.id) as total_detections,
    STRING_AGG(DISTINCT de.tool_name, ', ') as tools_detected
FROM sessions s
JOIN users u ON s.user_id = u.id
JOIN detection_events de ON s.id = de.session_id
WHERE de.confidence_level IN ('high', 'very_high')
GROUP BY s.id, u.username
HAVING COUNT(de.id) >= 3
ORDER BY s.integrity_score ASC;
```

### Timeline of Events for a Session

```sql
WITH all_events AS (
    SELECT 
        'screenshot' as event_type,
        timestamp,
        'Screenshot captured' as description
    FROM screenshots
    WHERE session_id = 123
    
    UNION ALL
    
    SELECT 
        'window' as event_type,
        timestamp,
        'Window: ' || process_name as description
    FROM window_events
    WHERE session_id = 123
    
    UNION ALL
    
    SELECT 
        'browser' as event_type,
        timestamp,
        'Browser: ' || domain as description
    FROM browser_events
    WHERE session_id = 123
    
    UNION ALL
    
    SELECT 
        'detection' as event_type,
        timestamp,
        'AI Detection: ' || tool_name || ' (' || confidence_level || ')' as description
    FROM detection_events
    WHERE session_id = 123
)
SELECT * FROM all_events
ORDER BY timestamp;
```

---

## Performance Optimization

### Partitioning Strategy (for large-scale deployments)

```sql
-- Partition sessions by month
CREATE TABLE sessions_2026_06 PARTITION OF sessions
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

-- Partition detection_events by month
CREATE TABLE detection_events_2026_06 PARTITION OF detection_events
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
```

### Index Optimization

```sql
-- Composite index for common query patterns
CREATE INDEX idx_detection_events_session_confidence 
    ON detection_events(session_id, confidence_score DESC);

-- Partial index for active sessions
CREATE INDEX idx_sessions_active 
    ON sessions(start_time) 
    WHERE status = 'active';
```

---

## Security Considerations

1. **Column-Level Encryption**: Encrypt sensitive fields at application layer
   - `window_title`
   - `tab_title`
   - `text_content` (OCR)
   - File paths

2. **Row-Level Security**: Implement PostgreSQL RLS for multi-tenant isolation

3. **Audit Trail**: Every data modification logged to `audit_logs`

4. **Immutability**: Core evidence tables (screenshots, detection_events) should be append-only

5. **Backup Strategy**: 
   - Daily encrypted backups
   - Point-in-time recovery
   - Off-site backup storage

---

## Document Version
- **Version**: 1.0
- **Last Updated**: 2026-06-26
- **Author**: Integraty Development Team
