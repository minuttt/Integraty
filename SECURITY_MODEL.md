# Integraty - Security Model

## Security Philosophy

**Defense in Depth**: Multiple layers of security controls
**Least Privilege**: Minimum necessary access rights
**Zero Trust**: Verify every request, trust nothing
**Privacy by Design**: Security and privacy built-in from the start
**Transparency**: Open about security practices and incidents

---

## 1. Authentication & Authorization

### 1.1 Authentication Methods

#### Local Mode (Standalone)
- **OS-Level Authentication**: Leverage operating system user accounts
- **Session Tokens**: JWT tokens for application-level auth
- **Auto-Lock**: Lock after configurable inactivity period

#### Enterprise Mode
- **SAML 2.0**: Enterprise SSO integration
- **OAuth 2.0**: Support for Google, Microsoft, Okta
- **LDAP/Active Directory**: Direct directory integration
- **Multi-Factor Authentication**: 
  - TOTP (Time-based One-Time Password)
  - Hardware security keys (FIDO2/WebAuthn)
  - SMS backup (discouraged, but supported)

### 1.2 JWT Token Management

**Token Structure**:
```json
{
  "sub": "user-uuid",
  "role": "proctor",
  "org": "org-uuid",
  "iat": 1687785600,
  "exp": 1687789200,
  "jti": "token-unique-id"
}
```

**Token Types**:
- **Access Token**: Short-lived (1 hour), for API requests
- **Refresh Token**: Long-lived (30 days), for token renewal
- **Session Token**: Very short-lived (15 minutes), for active monitoring

**Token Security**:
- Signed with HMAC-SHA256 or RSA
- Stored in httpOnly cookies (not localStorage)
- Refresh token rotation on each use
- Token revocation list for logout/compromise

### 1.3 Role-Based Access Control (RBAC)

**Roles**:
1. **Admin**: Full system access
2. **Proctor**: Create/monitor sessions, view reports
3. **Reviewer**: View sessions and reports, mark detections
4. **Auditor**: Read-only access to all data
5. **Examinee**: Limited to own session consent/view

**Permission Matrix**:

| Action | Admin | Proctor | Reviewer | Auditor | Examinee |
|--------|-------|---------|----------|---------|----------|
| Create Session | ✓ | ✓ | ✗ | ✗ | ✗ |
| Monitor Session | ✓ | ✓ | ✗ | ✗ | ✗ |
| View Own Session | ✓ | ✓ | ✓ | ✓ | ✓ |
| View All Sessions | ✓ | ✓ | ✓ | ✓ | ✗ |
| Generate Report | ✓ | ✓ | ✓ | ✗ | ✗ |
| Review Detections | ✓ | ✓ | ✓ | ✗ | ✗ |
| Manage Users | ✓ | ✗ | ✗ | ✗ | ✗ |
| Configure System | ✓ | ✗ | ✗ | ✗ | ✗ |
| View Audit Logs | ✓ | ✗ | ✗ | ✓ | ✗ |
| Delete Data | ✓ | ✗ | ✗ | ✗ | ✗ |

### 1.4 Session Management

**Security Controls**:
- Session timeout after 30 minutes of inactivity
- Concurrent session limits per user
- Session hijacking prevention (IP binding optional)
- Secure session storage (encrypted cookies)
- Automatic logout on browser close

---

## 2. Data Encryption

### 2.1 Encryption at Rest

**Database Encryption**:
- **SQLite**: SQLCipher with AES-256 encryption
- **PostgreSQL**: pgcrypto extension for column-level encryption
- **Key Management**: Per-organization encryption keys

**File Encryption**:
- Screenshots: AES-256-GCM encryption
- Reports: AES-256-GCM encryption
- OCR results: Encrypted in database
- Encryption keys stored separately from data

**Encryption Hierarchy**:
```
Master Key (HSM/KMS)
    ↓
Organization Key (per org)
    ↓
Session Key (per session)
    ↓
Data Encryption Keys (per file/record)
```

**Key Derivation**:
- PBKDF2 with 100,000 iterations
- Argon2id for password hashing
- Random salt per user/organization

### 2.2 Encryption in Transit

**TLS Configuration**:
- TLS 1.3 only (TLS 1.2 fallback for compatibility)
- Strong cipher suites only:
  - `TLS_AES_256_GCM_SHA384`
  - `TLS_CHACHA20_POLY1305_SHA256`
  - `TLS_AES_128_GCM_SHA256`
- Perfect Forward Secrecy (ECDHE key exchange)
- Certificate pinning for mobile clients

**API Security**:
- All API endpoints HTTPS only
- HTTP Strict Transport Security (HSTS)
- Certificate transparency monitoring

**Internal Communication**:
- IPC between frontend and backend encrypted
- WebSocket connections over WSS
- Database connections over SSL/TLS

### 2.3 Key Management

**Key Storage**:
- **Development**: File-based (encrypted with environment key)
- **Production**: 
  - Cloud KMS (AWS KMS, Azure Key Vault, GCP KMS)
  - Hardware Security Module (HSM) for enterprise
  - Encrypted key storage with access control

**Key Rotation**:
- Automatic rotation every 90 days
- On-demand rotation on security incident
- Re-encryption jobs for rotated keys
- Audit trail of all key operations

**Key Backup**:
- Encrypted key backups
- Split key custody (multiple admins required)
- Secure offline backup for disaster recovery

---

## 3. Input Validation & Sanitization

### 3.1 API Input Validation

**Validation Layers**:
1. **Schema Validation**: Pydantic models (backend), Zod (frontend)
2. **Type Checking**: TypeScript (frontend), MyPy (backend)
3. **Business Logic Validation**: Custom validators
4. **Database Constraints**: Foreign keys, unique constraints

**Common Validations**:
- Email: RFC 5322 compliant
- URLs: Whitelist allowed schemes (https only)
- File uploads: Magic byte validation, size limits
- SQL injection: Parameterized queries only
- XSS: Output encoding, CSP headers
- Path traversal: Validate and sanitize file paths

### 3.2 Output Encoding

**Context-Specific Encoding**:
- HTML: Escape `<`, `>`, `&`, `"`, `'`
- JavaScript: JSON encoding
- URL: URL encoding
- SQL: Parameterized queries (never string concatenation)

**Content Security Policy (CSP)**:
```
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self' wss://localhost:8080;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
```

---

## 4. Network Security

### 4.1 Firewall Rules

**Inbound Rules**:
- 443 (HTTPS): Public access
- 22 (SSH): Admin IP whitelist only
- 5432 (PostgreSQL): Internal network only
- 8080 (Backend API): Internal/localhost only

**Outbound Rules**:
- 443 (HTTPS): Allowed for external APIs
- 80 (HTTP): Blocked
- 53 (DNS): Allowed
- All other ports: Blocked by default

### 4.2 DDoS Protection

**Rate Limiting**:
- Per IP: 100 requests/minute
- Per User: 1000 requests/minute
- Per Endpoint: Custom limits
  - Login: 5 attempts/minute
  - Report generation: 10/hour
  - Screenshot upload: 1/second

**Rate Limit Algorithm**: Token bucket with Redis backend

**Additional Protections**:
- CloudFlare/AWS Shield for DDoS mitigation
- IP reputation filtering
- Geo-blocking for untrusted regions
- Request size limits (max 10MB)

### 4.3 API Security

**Security Headers**:
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

**CORS Configuration**:
- Whitelist allowed origins
- Credentials allowed only for same-origin
- Preflight request caching

---

## 5. Secure Development Practices

### 5.1 Code Security

**Static Analysis**:
- **Frontend**: ESLint security plugins, Snyk
- **Backend**: Bandit, Semgrep
- **Dependencies**: Dependabot, npm audit, pip-audit

**Code Review Requirements**:
- All code reviewed by at least one other developer
- Security-critical code reviewed by security team
- Automated security checks in CI/CD

### 5.2 Dependency Management

**Vulnerability Scanning**:
- Daily dependency vulnerability scans
- Automated PR creation for security updates
- CVSS score threshold for immediate patching (7.0+)

**Dependency Policies**:
- Prefer well-maintained libraries (active commits, large user base)
- Avoid deprecated or unmaintained dependencies
- Pin exact versions in production
- Regular dependency updates (monthly)

### 5.3 Secret Management

**Secret Storage**:
- Never commit secrets to Git
- Use environment variables
- Vault (HashiCorp Vault, AWS Secrets Manager)
- Encrypted configuration files

**Secret Detection**:
- Pre-commit hooks (detect-secrets, gitleaks)
- GitHub secret scanning
- Automated secret rotation

---

## 6. Infrastructure Security

### 6.1 Server Hardening

**Operating System**:
- Minimal OS install (no unnecessary services)
- Regular security updates (automated)
- Fail2ban for brute force protection
- SELinux/AppArmor mandatory access control

**Application Hardening**:
- Non-root user for application process
- Restricted file permissions (600 for sensitive files)
- Disable directory listing
- Remove default/test credentials

### 6.2 Database Security

**Access Control**:
- Separate database users per application component
- Principle of least privilege (read-only where possible)
- No direct database access from internet
- VPN required for admin access

**Database Hardening**:
- Encrypted connections (SSL/TLS)
- Strong password policy
- Regular backups (encrypted)
- Point-in-time recovery enabled

### 6.3 Container Security (Docker/Kubernetes)

**Container Best Practices**:
- Minimal base images (Alpine Linux)
- Multi-stage builds (no build tools in production image)
- Non-root user in containers
- Read-only root filesystem where possible
- Resource limits (CPU, memory)

**Image Scanning**:
- Trivy, Clair for vulnerability scanning
- Sign images with Docker Content Trust
- Private container registry

**Kubernetes Security**:
- Network policies (restrict pod-to-pod communication)
- Pod security policies/standards
- RBAC for cluster access
- Secrets management (sealed secrets, external secrets)

---

## 7. Monitoring & Incident Response

### 7.1 Security Monitoring

**Logging**:
- All authentication attempts (success and failure)
- Authorization failures
- API requests (endpoint, user, timestamp, IP)
- Data access (who accessed what, when)
- Configuration changes
- Security events (rate limit exceeded, suspicious activity)

**Log Aggregation**:
- Centralized logging (ELK stack, Splunk, Datadog)
- Log retention: 1 year minimum
- Encrypted log storage
- Access control on logs

**Alerting**:
- Failed login attempts (> 5 in 5 minutes)
- Privilege escalation attempts
- Unusual data access patterns
- Security tool alerts (IDS/IPS)
- Certificate expiration warnings

### 7.2 Intrusion Detection

**Host-based IDS**:
- OSSEC, Wazuh for file integrity monitoring
- Rootkit detection
- Log analysis and correlation

**Network-based IDS**:
- Snort, Suricata for network monitoring
- Anomaly detection
- Signature-based detection

### 7.3 Incident Response Plan

**Incident Severity Levels**:
1. **Critical**: Data breach, system compromise
2. **High**: Privilege escalation, significant vulnerability
3. **Medium**: Suspicious activity, minor vulnerability
4. **Low**: Policy violation, informational

**Response Procedures**:
1. **Detection**: Automated alerts + manual review
2. **Triage**: Assess severity and impact
3. **Containment**: Isolate affected systems
4. **Eradication**: Remove threat, patch vulnerability
5. **Recovery**: Restore systems, verify integrity
6. **Post-Incident**: Review, document, improve

**Communication Plan**:
- Internal notification (security team, management)
- External notification (customers, regulators)
- Incident disclosure timeline
- Status page updates

---

## 8. Compliance & Auditing

### 8.1 Regulatory Compliance

**GDPR (General Data Protection Regulation)**:
- Data minimization
- Right to access (data export)
- Right to erasure (data deletion)
- Data portability
- Breach notification (72 hours)
- Privacy by design

**CCPA (California Consumer Privacy Act)**:
- Data disclosure requirements
- Opt-out of data sale (not applicable, we don't sell data)
- Data deletion requests
- Non-discrimination

**FERPA (Family Educational Rights and Privacy Act)**:
- Student data protection (for educational use)
- Parental consent for minors
- Access restrictions

**SOC 2 Type II**:
- Security controls audit
- Availability controls
- Processing integrity
- Confidentiality
- Privacy

### 8.2 Audit Logging

**Audit Events**:
- User login/logout
- Session create/update/delete
- Data access (view, download)
- Configuration changes
- User management (create, update, delete)
- Report generation
- Detection review (confirm, false positive)
- Data export
- Data deletion

**Audit Log Format**:
```json
{
  "timestamp": "2026-06-26T10:00:00Z",
  "user_id": "user-uuid",
  "username": "admin@example.com",
  "action": "CREATE",
  "entity_type": "session",
  "entity_id": "session-uuid",
  "old_value": null,
  "new_value": {"session_name": "Final Exam"},
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "status": "success"
}
```

**Audit Log Integrity**:
- Append-only (no updates or deletes)
- Cryptographic hashing (chain of hashes)
- Separate database for audit logs
- Read-only access for non-admins

---

## 9. Backup & Disaster Recovery

### 9.1 Backup Strategy

**Backup Types**:
- **Full Backup**: Weekly (Sunday 2 AM)
- **Incremental Backup**: Daily (2 AM)
- **Transaction Log Backup**: Every 15 minutes

**Backup Scope**:
- Database (all tables)
- File storage (screenshots, reports)
- Configuration files
- Encryption keys (separate secure storage)

**Backup Security**:
- AES-256 encryption
- Stored in geographically separate location
- Access restricted to disaster recovery team
- Regular restore testing (monthly)

### 9.2 Disaster Recovery Plan

**Recovery Time Objective (RTO)**: 4 hours
**Recovery Point Objective (RPO)**: 15 minutes

**DR Procedures**:
1. **Declare Disaster**: Incident commander decision
2. **Activate DR Site**: Failover to backup infrastructure
3. **Restore Data**: Latest backup + transaction logs
4. **Verify Integrity**: Data validation, system checks
5. **Resume Operations**: DNS cutover, notify users
6. **Post-Recovery**: Incident review, plan updates

**DR Testing**:
- Quarterly disaster recovery drills
- Annual full failover test
- Documented results and improvements

---

## 10. Physical Security (Enterprise Deployments)

### 10.1 Data Center Security

**Access Control**:
- Biometric authentication
- 24/7 security personnel
- Video surveillance
- Access logs

**Environmental Controls**:
- Fire suppression systems
- Climate control
- Redundant power (UPS, generators)
- Network redundancy

### 10.2 Device Security (Endpoints)

**Endpoint Protection**:
- Mandatory antivirus/EDR
- Full disk encryption (BitLocker, FileVault)
- Automatic security updates
- Remote wipe capability

**Physical Access**:
- Lock screens after inactivity
- BIOS/UEFI passwords
- Disable boot from external media
- Cable locks for laptops

---

## 11. Third-Party Security

### 11.1 Vendor Risk Assessment

**Assessment Criteria**:
- Security certifications (SOC 2, ISO 27001)
- Data handling practices
- Incident response capabilities
- Financial stability
- Service level agreements

**Regular Reviews**:
- Annual vendor security review
- Continuous monitoring of security posture
- Incident notification requirements

### 11.2 Data Processing Agreements

**Requirements**:
- GDPR-compliant DPA
- Data residency specifications
- Sub-processor disclosure
- Right to audit
- Data breach notification

---

## 12. Security Testing

### 12.1 Automated Testing

**Security Test Suite**:
- SQL injection tests
- XSS tests
- CSRF tests
- Authentication/authorization tests
- Encryption tests
- Input validation tests

**CI/CD Integration**:
- Security tests in every build
- Block deployment on security test failures
- Automated security regression testing

### 12.2 Manual Security Testing

**Penetration Testing**:
- Annual third-party penetration test
- Quarterly internal penetration test
- Scope: All external-facing components
- Remediation timeline: Critical (7 days), High (30 days)

**Security Code Review**:
- Security-critical code manually reviewed
- Focus areas: Authentication, authorization, encryption, data handling
- Security team sign-off required

### 12.3 Bug Bounty Program

**Program Structure**:
- Responsible disclosure policy
- Severity-based rewards ($100 - $10,000)
- Scope: All production systems
- Out of scope: Physical attacks, social engineering, DoS

---

## 13. Security Training

### 13.1 Developer Training

**Topics**:
- OWASP Top 10
- Secure coding practices
- Cryptography basics
- Threat modeling
- Incident response

**Frequency**: Quarterly security training sessions

### 13.2 User Security Awareness

**Topics**:
- Password best practices
- Phishing awareness
- Social engineering
- Data handling
- Incident reporting

**Frequency**: Annual security awareness training

---

## 14. Security Roadmap

### Phase 1 (MVP)
- Basic authentication (local + JWT)
- AES-256 encryption at rest
- TLS 1.3 in transit
- Basic rate limiting
- Audit logging

### Phase 2 (Enterprise Ready)
- SSO integration (SAML, OAuth)
- MFA support
- Advanced rate limiting
- Comprehensive security monitoring
- Penetration testing

### Phase 3 (Hardened)
- HSM integration
- Advanced threat detection
- Zero-trust architecture
- Security certifications (SOC 2, ISO 27001)
- Bug bounty program

---

## Document Version
- **Version**: 1.0
- **Last Updated**: 2026-06-26
- **Author**: Integraty Development Team
