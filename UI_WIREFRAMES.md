# Integraty - UI Wireframes & Design Specifications

## Design System

### Color Palette

**Primary Colors**:
- Primary Blue: `#2563EB` (Trust, Security)
- Primary Dark: `#1E40AF`
- Primary Light: `#60A5FA`

**Status Colors**:
- Success Green: `#10B981`
- Warning Yellow: `#F59E0B`
- Error Red: `#EF4444`
- Info Blue: `#3B82F6`

**Neutral Colors**:
- Gray 50: `#F9FAFB` (Background)
- Gray 100: `#F3F4F6`
- Gray 200: `#E5E7EB`
- Gray 500: `#6B7280` (Secondary text)
- Gray 700: `#374151` (Primary text)
- Gray 900: `#111827` (Headers)

**Semantic Colors**:
- Risk Critical: `#DC2626`
- Risk High: `#F59E0B`
- Risk Medium: `#FBBF24`
- Risk Low: `#34D399`
- Risk None: `#10B981`

### Typography

**Font Family**: 
- Primary: `Inter, system-ui, -apple-system, sans-serif`
- Monospace: `'Fira Code', 'Courier New', monospace`

**Font Sizes**:
- XS: 12px
- SM: 14px
- Base: 16px
- LG: 18px
- XL: 20px
- 2XL: 24px
- 3XL: 30px
- 4XL: 36px

**Font Weights**:
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700

### Spacing Scale
- 1: 4px
- 2: 8px
- 3: 12px
- 4: 16px
- 5: 20px
- 6: 24px
- 8: 32px
- 10: 40px
- 12: 48px
- 16: 64px

### Border Radius
- SM: 4px
- Base: 6px
- MD: 8px
- LG: 12px
- XL: 16px
- Full: 9999px

---

## Application Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Top Navigation Bar                                         │
├────────┬────────────────────────────────────────────────────┤
│        │                                                    │
│  Side  │                                                    │
│  Nav   │            Main Content Area                       │
│        │                                                    │
│        │                                                    │
└────────┴────────────────────────────────────────────────────┘
```

---

## 1. Login Screen

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                         INTEGRATY                            │
│                    Integrity Monitoring                      │
│                                                              │
│              ┌─────────────────────────────┐                │
│              │  [Icon] Email Address       │                │
│              │  user@example.com           │                │
│              └─────────────────────────────┘                │
│                                                              │
│              ┌─────────────────────────────┐                │
│              │  [Icon] Password            │                │
│              │  ••••••••••                 │                │
│              └─────────────────────────────┘                │
│                                                              │
│              ☐ Remember me                                   │
│                                                              │
│              ┌─────────────────────────────┐                │
│              │      Sign In                │                │
│              └─────────────────────────────┘                │
│                                                              │
│              Forgot Password? | SSO Login                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Features**:
- Clean, professional login
- Support for email/password and SSO
- Remember me checkbox
- Forgot password link
- Organization code field (optional, for multi-tenant)

---

## 2. Dashboard (Home Screen)

```
┌──────────────────────────────────────────────────────────────────┐
│  INTEGRATY            [Search]         [Notifications] [Profile] │
├──────────┬───────────────────────────────────────────────────────┤
│          │                                                       │
│  [Icon]  │  Dashboard                              [+ New Session]│
│  Home    │                                                       │
│          │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  [Icon]  │  │   250    │ │    12    │ │   3.5    │ │   94%    │ │
│ Sessions │  │  Total   │ │  Active  │ │   Avg    │ │  Avg     │ │
│          │  │ Sessions │ │ Sessions │ │  Hours   │ │Integrity │ │
│  [Icon]  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│ Reports  │                                                       │
│          │  Recent Sessions                    [View All →]      │
│  [Icon]  │  ┌─────────────────────────────────────────────────┐ │
│  Config  │  │ Final Exam - CS101          Started 2h ago      │ │
│          │  │ Student: Jane Doe           ●●●●◐ 92% Integrity │ │
│  [Icon]  │  │ [View] [Report]                                 │ │
│  Users   │  ├─────────────────────────────────────────────────┤ │
│          │  │ Midterm - Data Structures   Completed           │ │
│ ─────────│  │ Student: John Smith         ●●●●● 98% Integrity │ │
│          │  │ [View] [Report]                                 │ │
│  [Icon]  │  ├─────────────────────────────────────────────────┤ │
│  Audit   │  │ Coding Interview            Active              │ │
│  Logs    │  │ Candidate: Alex Johnson     ●●●◐◯ 67% ! Warning │ │
│          │  │ [Monitor Live]                                  │ │
│  [Icon]  │  └─────────────────────────────────────────────────┘ │
│  Help    │                                                       │
│          │  Detection Trends (Last 30 Days)                     │
│          │  ┌─────────────────────────────────────────────────┐ │
│          │  │  [Line Chart: Detections over time]             │ │
│          │  │                                                  │ │
│          │  └─────────────────────────────────────────────────┘ │
│          │                                                       │
└──────────┴───────────────────────────────────────────────────────┘
```

**Key Metrics Cards**:
1. Total Sessions
2. Active Sessions (real-time count)
3. Average Session Duration
4. Average Integrity Score

**Recent Sessions List**:
- Session name and type
- User/Candidate name
- Time (relative or absolute)
- Integrity score with visual indicator
- Quick actions (View, Report, Monitor Live)

**Charts**:
- Detection trends over time
- Tool detection breakdown
- Risk level distribution

---

## 3. Session List View

```
┌──────────────────────────────────────────────────────────────────┐
│  Sessions                                [Filter ▾] [+ New]      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Search sessions...]          [Status ▾] [Type ▾] [Date Range] │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Session Name        User          Type    Status  Integrity │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ Final Exam CS101   Jane Doe       Exam    Active   ●●●●◐    │ │
│  │ 2026-06-26 10:00   student@..     120min           92%      │ │
│  │ [Monitor] [Details] [Report]                       🔍 2     │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ Midterm Exam       John Smith     Exam    Done     ●●●●●    │ │
│  │ 2026-06-25 14:00   john@..        90min            98%      │ │
│  │ [Details] [Report]                                 ✓ 0      │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ Coding Challenge   Alex Johnson   Interview Active ●●◐◯◯    │ │
│  │ 2026-06-26 09:30   alex@..        60min            45%      │ │
│  │ [Monitor] [Details] [Report]                       ⚠ 8      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Showing 1-10 of 250        [1] [2] [3] ... [25] [Next →]      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Features**:
- Search bar (by name, user, date)
- Filters: Status, Type, Date Range, Risk Level
- Sort: By date, integrity score, status
- Color-coded integrity scores
- Quick detection count indicator
- Action buttons contextual to status

**Integrity Score Visualization**:
- ●●●●● (5/5): 90-100% - Green
- ●●●●◐ (4.5/5): 80-89% - Light Green
- ●●●●◯ (4/5): 70-79% - Yellow
- ●●●◐◯ (3.5/5): 60-69% - Orange
- ●●◐◯◯ (2.5/5): Below 60% - Red

---

## 4. New Session Setup

```
┌──────────────────────────────────────────────────────────────────┐
│  Create New Session                           [Cancel] [Start]   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Session Information                                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Session Name *                                             │ │
│  │ [Final Exam - Computer Science 101                       ] │ │
│  │                                                              │ │
│  │ Session Type *        Duration (minutes) *                   │ │
│  │ [Exam           ▾]    [120                ]                 │ │
│  │                                                              │ │
│  │ Participant *                                                │ │
│  │ [student@university.edu                  ] [Search]         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Monitoring Configuration                                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Screenshot Interval                                          │ │
│  │ ◯ 15 seconds  ● 30 seconds  ◯ 60 seconds  ◯ Custom         │ │
│  │                                                              │ │
│  │ ☑ Enable screen capture                                     │ │
│  │ ☑ Enable window monitoring                                  │ │
│  │ ☑ Enable browser monitoring                                 │ │
│  │ ☑ Enable OCR analysis                                       │ │
│  │                                                              │ │
│  │ Privacy Mode                                                 │ │
│  │ ● Standard  ◯ Privacy-Enhanced  ◯ Minimal                   │ │
│  │                                                              │ │
│  │ Monitor Configuration                                        │ │
│  │ ● All monitors  ◯ Primary monitor only                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Additional Settings                                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Proctor (optional)                                           │ │
│  │ [Prof. Smith                      ] [Select]                │ │
│  │                                                              │ │
│  │ Notes                                                        │ │
│  │ [Final examination for CS101 - Spring 2026                ] │ │
│  │ [                                                          ] │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│              [Cancel]                    [Create Session]        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Form Sections**:
1. **Session Information**: Basic details
2. **Monitoring Configuration**: Technical settings
3. **Additional Settings**: Optional metadata

**Validation**:
- Required fields marked with *
- Real-time validation
- Clear error messages

---

## 5. Consent Screen (User-Facing)

```
┌──────────────────────────────────────────────────────────────────┐
│                         INTEGRATY                                │
│                   Monitoring Consent                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Session: Final Exam - Computer Science 101                      │
│  Duration: 120 minutes                                           │
│  Proctor: Prof. Smith                                            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  📸 What Will Be Monitored                                       │
│                                                                  │
│  ✓ Screen captures every 30 seconds                             │
│  ✓ Active windows and applications                              │
│  ✓ Browser activity (domains only, not full URLs)               │
│  ✓ Text recognition for AI tool detection                       │
│                                                                  │
│  🔒 Your Privacy                                                 │
│                                                                  │
│  ✓ All data encrypted and stored securely                       │
│  ✓ Access limited to authorized personnel only                  │
│  ✓ Data will be retained for 90 days                            │
│  ✓ You may request your data at any time                        │
│  ✓ Passwords and financial information excluded                 │
│                                                                  │
│  ⚖️ Your Rights                                                  │
│                                                                  │
│  ✓ You may decline monitoring (session cannot proceed)          │
│  ✓ You may request a data export                                │
│  ✓ You may file an appeal if flagged incorrectly                │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ☐ I have read and understood the monitoring disclosure         │
│  ☐ I consent to monitoring during this session                  │
│  ☐ I confirm no prohibited AI tools will be used                │
│                                                                  │
│                                                                  │
│          [Decline]                      [Accept & Start]         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Key Elements**:
- Clear description of what is monitored
- Privacy protections highlighted
- User rights explicitly stated
- Three consent checkboxes (all required)
- Decline option prominently displayed

---

## 6. Active Monitoring View (User-Facing)

```
┌──────────────────────────────────────────────────────────────────┐
│  🔴 RECORDING                   Final Exam - CS101               │
│                                                                  │
│  ⏱️  01:23:45 / 02:00:00                      [Pause] [End]      │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Status: Monitoring Active                                       │
│                                                                  │
│  Last screenshot: 15 seconds ago                                 │
│  Events captured: 187                                            │
│                                                                  │
│  ⚠️ No issues detected                                           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  📋 Minimize this window to continue your work                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Minimal Design**:
- Always-on-top indicator
- Timer display
- Simple status
- Minimal distraction
- Can be minimized to system tray

**System Tray Icon**:
- 🔴 Red dot when recording
- ⏸️ Pause icon when paused
- Quick menu: Status, Pause, End Session

---

## 7. Live Monitoring Dashboard (Proctor View)

```
┌──────────────────────────────────────────────────────────────────┐
│  Live Monitor: Jane Doe - Final Exam                      [Back] │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────┐  ┌─────────────────────────────┐  │
│  │                          │  │ Session Info                │  │
│  │                          │  │ Student: Jane Doe           │  │
│  │   [Latest Screenshot]    │  │ Started: 10:00 AM          │  │
│  │                          │  │ Elapsed: 01:23:45          │  │
│  │     [Updating every     │  │ Status: ●●●●◐ 92%          │  │
│  │       30 seconds]        │  │                             │  │
│  │                          │  │ Detections: 2               │  │
│  │                          │  │ ⚠️ Low risk                 │  │
│  │                          │  └─────────────────────────────┘  │
│  └──────────────────────────┘                                   │
│                                                                  │
│  Recent Activity                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 01:23:45  📸 Screenshot captured                           │ │
│  │ 01:23:30  🪟 Window: Microsoft Word - Exam.docx            │ │
│  │ 01:22:15  🌐 Browser: stackoverflow.com (5 min)            │ │
│  │ 01:15:30  ⚠️ Detection: ChatGPT domain visited (Medium)   │ │
│  │ 01:10:00  🪟 Window: Visual Studio Code                    │ │
│  │ 01:05:00  📸 Screenshot captured                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Detections                                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ⚠️ ChatGPT                    01:15:30    Medium           │ │
│  │    Browser visit detected                                    │ │
│  │    Duration: 45 seconds                                      │ │
│  │    [View Screenshot] [Mark as False Positive]               │ │
│  │                                                              │ │
│  │ ℹ️ GitHub Copilot             00:45:00    Low              │ │
│  │    Keyword detected via OCR                                  │ │
│  │    [View Screenshot] [Mark as False Positive]               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Pause Session] [End Session] [Generate Report]                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Key Features**:
- Live screenshot preview (auto-refreshing)
- Real-time activity feed
- Detection alerts with severity
- Quick actions (pause, end, report)
- Proctor can mark false positives

---

## 8. Session Detail View (Post-Session)

```
┌──────────────────────────────────────────────────────────────────┐
│  ← Back to Sessions                                    [Export]   │
│                                                                  │
│  Final Exam - Computer Science 101                               │
│                                                                  │
│  ┌──────────────────────┬──────────────────────────────────────┐ │
│  │ Student              │ Jane Doe (student@university.edu)    │ │
│  │ Session Type         │ Exam                                 │ │
│  │ Date & Time          │ June 26, 2026 at 10:00 AM            │ │
│  │ Duration             │ 2 hours (120 minutes scheduled)      │ │
│  │ Status               │ ✓ Completed                          │ │
│  │ Proctor              │ Prof. Smith                          │ │
│  └──────────────────────┴──────────────────────────────────────┘ │
│                                                                  │
│  Integrity Assessment                                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                              │ │
│  │           Integrity Score: 92%  ●●●●◐                       │ │
│  │                                                              │ │
│  │           Risk Level: LOW                                    │ │
│  │                                                              │ │
│  │  Evidence suggests minimal AI-assisted activity may have    │ │
│  │  occurred during this session. 2 low-confidence detections  │ │
│  │  were recorded.                                              │ │
│  │                                                              │ │
│  │  [Generate Full Report]                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────┬────────────────┬───────────────────────────┐ │
│  │ [Timeline]     │ [Detections]   │ [Screenshots]   [Reports] │ │
│  └────────────────┴────────────────┴───────────────────────────┘ │
│                                                                  │
│  Timeline                                                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                              │ │
│  │ 10:00 ─────────────────────────────────────────────── 12:00 │ │
│  │   │                                                       │  │ │
│  │   ├─ 📸 Screenshots (240)                               │  │ │
│  │   ├─ 🪟 Window Changes (45)                             │  │ │
│  │   ├─ 🌐 Browser Navigation (12)                         │  │ │
│  │   └─ ⚠️ Detections (2)                                  │  │ │
│  │                                                              │ │
│  │   10:15          10:45                      11:30            │ │
│  │     ⚠️            📸                         🪟              │ │
│  │                                                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Key Events                                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 10:00:00  Session started                                  │ │
│  │ 10:15:30  ⚠️ ChatGPT domain detected (Medium confidence)  │ │
│  │ 10:45:00  Long focus on browser (15 minutes)              │ │
│  │ 11:30:00  Window switch to IDE                             │ │
│  │ 12:00:00  Session completed                                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Tabs**:
1. **Timeline**: Visual timeline with events
2. **Detections**: List of all AI tool detections
3. **Screenshots**: Gallery of captured screenshots
4. **Reports**: Generated reports

---

## 9. Detections Tab

```
┌──────────────────────────────────────────────────────────────────┐
│  [Timeline]  [Detections]  [Screenshots]  [Reports]              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AI Tool Detections (2)                      [Filter ▾] [Sort ▾] │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ⚠️ ChatGPT                              10:15:30  MEDIUM    │ │
│  │ ─────────────────────────────────────────────────────────── │ │
│  │ Detection Method: Browser domain matching                    │ │
│  │ Confidence Score: 65%                                        │ │
│  │                                                              │ │
│  │ Evidence:                                                    │ │
│  │ • Browser visit to chatgpt.com                              │ │
│  │ • Duration: 45 seconds                                       │ │
│  │ • Tab title: "ChatGPT"                                      │ │
│  │                                                              │ │
│  │ ┌─────────────────┐                                         │ │
│  │ │                 │  Screenshot shows browser window        │ │
│  │ │ [Screenshot]    │  with chatgpt.com domain visible        │ │
│  │ │                 │  [View Full Size]                       │ │
│  │ └─────────────────┘                                         │ │
│  │                                                              │ │
│  │ Review Status: ◯ Pending                                    │ │
│  │ [Confirm] [Mark as False Positive] [Add Note]               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ℹ️ GitHub Copilot                       10:45:00  LOW      │ │
│  │ ─────────────────────────────────────────────────────────── │ │
│  │ Detection Method: OCR keyword matching                       │ │
│  │ Confidence Score: 35%                                        │ │
│  │                                                              │ │
│  │ Evidence:                                                    │ │
│  │ • Keyword "Copilot" detected via OCR                        │ │
│  │ • Context: Code editor window                               │ │
│  │                                                              │ │
│  │ ┌─────────────────┐                                         │ │
│  │ │                 │  OCR detected "Copilot" text            │ │
│  │ │ [Screenshot]    │  in code editor                         │ │
│  │ │                 │  [View Full Size]                       │ │
│  │ └─────────────────┘                                         │ │
│  │                                                              │ │
│  │ Review Status: ✓ Marked as False Positive                   │ │
│  │ Reviewer: Prof. Smith                                        │ │
│  │ Note: Student was reading documentation mentioning Copilot  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Detection Card Elements**:
- Tool name and icon
- Time of detection
- Confidence level (with color coding)
- Detection method
- Evidence list
- Screenshot thumbnail
- Review controls

---

## 10. Screenshots Gallery Tab

```
┌──────────────────────────────────────────────────────────────────┐
│  [Timeline]  [Detections]  [Screenshots]  [Reports]              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Screenshots (240)                [Grid View] [Timeline View]    │
│                                                                  │
│  Filter: [All] [With Detections] [OCR Processed]                │
│  Jump to: [10:00] [10:30] [11:00] [11:30] [12:00]              │
│                                                                  │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐      │
│  │          │          │          │          │          │      │
│  │  [img]   │  [img]   │  [img]   │  [img]   │  [img]   │      │
│  │          │          │     ⚠️    │          │          │      │
│  │ 10:00:00 │ 10:00:30 │ 10:01:00 │ 10:01:30 │ 10:02:00 │      │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘      │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐      │
│  │          │          │          │          │          │      │
│  │  [img]   │  [img]   │  [img]   │  [img]   │  [img]   │      │
│  │          │          │          │          │          │      │
│  │ 10:02:30 │ 10:03:00 │ 10:03:30 │ 10:04:00 │ 10:04:30 │      │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘      │
│                                                                  │
│  [Load More]                             Showing 1-20 of 240     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Screenshot Modal (when clicked)**:

```
┌──────────────────────────────────────────────────────────────────┐
│  Screenshot: 10:15:30                              [← Previous] │
│                                                    [Next →]  [X] │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │                                                            │ │
│  │                  [Full Screenshot Image]                   │ │
│  │                                                            │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ⚠️ This screenshot contains 1 detection                        │
│                                                                  │
│  Metadata                                                        │
│  • Timestamp: June 26, 2026 at 10:15:30 AM                     │
│  • Resolution: 1920x1080                                         │
│  • File size: 245 KB                                            │
│  • OCR processed: Yes                                           │
│  • SHA-256: abc123...                                           │
│                                                                  │
│  OCR Results                                                     │
│  [Show extracted text]                                           │
│                                                                  │
│  [Download] [Add to Report] [Flag for Review]                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 11. Report Generation

```
┌──────────────────────────────────────────────────────────────────┐
│  Generate Integrity Report                     [Cancel] [Generate]│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Session: Final Exam - CS101 (Jane Doe)                          │
│  Date: June 26, 2026                                             │
│                                                                  │
│  Report Type                                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ● Summary Report                                            │ │
│  │   Executive overview with key findings (5-10 pages)         │ │
│  │                                                              │ │
│  │ ◯ Detailed Report                                           │ │
│  │   Complete analysis with all evidence (20-50 pages)         │ │
│  │                                                              │ │
│  │ ◯ Evidence Pack                                             │ │
│  │   Raw data export for third-party review                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Report Format                                                   │
│  ● PDF    ◯ HTML    ◯ JSON                                      │
│                                                                  │
│  Include in Report                                               │
│  ☑ Executive summary                                            │
│  ☑ Session metadata                                             │
│  ☑ Timeline visualization                                       │
│  ☑ Detection summary                                            │
│  ☑ Screenshots (thumbnails)                                     │
│  ☐ Screenshots (full resolution)                                │
│  ☑ Evidence details                                             │
│  ☑ Integrity assessment                                         │
│  ☐ OCR text extracts                                            │
│  ☐ Raw data appendix                                            │
│                                                                  │
│  Privacy Options                                                 │
│  ☐ Anonymize student information                                │
│  ☐ Redact sensitive window titles                               │
│  ☐ Exclude non-detection screenshots                            │
│                                                                  │
│  Digital Signature                                               │
│  ☑ Include cryptographic signature for authenticity             │
│                                                                  │
│  [Cancel]                                  [Generate Report]     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 12. Report Viewer

```
┌──────────────────────────────────────────────────────────────────┐
│  Report: Final Exam - CS101                    [Download] [Print]│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  INTEGRITY REPORT                            │ │
│  │                                                              │ │
│  │  Session: Final Exam - Computer Science 101                 │ │
│  │  Participant: Jane Doe                                       │ │
│  │  Date: June 26, 2026                                         │ │
│  │  Duration: 2 hours (10:00 AM - 12:00 PM)                    │ │
│  │                                                              │ │
│  │  ═══════════════════════════════════════════════════════    │ │
│  │                                                              │ │
│  │  EXECUTIVE SUMMARY                                           │ │
│  │                                                              │ │
│  │  Integrity Score: 92%  (Low Risk)                           │ │
│  │                                                              │ │
│  │  This report documents the monitoring session conducted     │ │
│  │  for Jane Doe on June 26, 2026. Evidence suggests minimal   │ │
│  │  AI-assisted activity may have occurred during this         │ │
│  │  session.                                                    │ │
│  │                                                              │ │
│  │  Key Findings:                                               │ │
│  │  • 2 detection events recorded                              │ │
│  │  • 1 medium-confidence detection                            │ │
│  │  • 1 low-confidence detection (marked false positive)       │ │
│  │  • Total session duration: 120 minutes                      │ │
│  │  • 240 screenshots captured                                  │ │
│  │                                                              │ │
│  │  [Continue reading...]                                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Page 1 of 8]                              [← Previous] [Next →]│
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 13. Configuration Screen

```
┌──────────────────────────────────────────────────────────────────┐
│  Configuration                                          [Save]    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┬────────────────────────────────────────────┐ │
│  │ General        │                                            │ │
│  │                │ Default Monitoring Settings                 │ │
│  │ AI Tools       │ ┌────────────────────────────────────────┐ │ │
│  │                │ │ Screenshot Interval                    │ │ │
│  │ Privacy        │ │ [30         ] seconds                  │ │ │
│  │                │ │                                          │ │ │
│  │ Data Retention │ │ Default Session Duration               │ │ │
│  │                │ │ [120        ] minutes                  │ │ │
│  │ Security       │ │                                          │ │ │
│  │                │ │ ☑ Enable OCR by default               │ │ │
│  │ Notifications  │ │ ☑ Enable browser monitoring            │ │ │
│  │                │ │ ☑ Enable window monitoring             │ │ │
│  │ Integrations   │ │                                          │ │ │
│  │                │ │ Privacy Mode                           │ │ │
│  │ Advanced       │ │ ● Standard  ◯ Enhanced  ◯ Minimal     │ │ │
│  │                │ └────────────────────────────────────────┘ │ │
│  │                │                                            │ │
│  │                │ System Settings                             │ │
│  │                │ ┌────────────────────────────────────────┐ │ │
│  │                │ │ Data Retention                         │ │ │
│  │                │ │ [90         ] days                     │ │ │
│  │                │ │                                          │ │ │
│  │                │ │ Max Concurrent Sessions                │ │ │
│  │                │ │ [50         ]                          │ │ │
│  │                │ │                                          │ │ │
│  │                │ │ ☑ Require explicit consent             │ │ │
│  │                │ │ ☐ Enable system telemetry              │ │ │
│  │                │ └────────────────────────────────────────┘ │ │
│  └────────────────┴────────────────────────────────────────────┘ │
│                                                                  │
│                                       [Cancel]  [Save Changes]   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 14. AI Tools Configuration

```
┌──────────────────────────────────────────────────────────────────┐
│  AI Tool Detection Configuration                   [+ Add Tool]  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Configured AI Tools (25)                    [Search...]         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Tool Name          Type            Priority    Enabled      │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ ChatGPT           Chatbot          100         [●]     ⚙️   │ │
│  │ Claude            Chatbot          100         [●]     ⚙️   │ │
│  │ Gemini            Chatbot          95          [●]     ⚙️   │ │
│  │ GitHub Copilot    Code Assistant   90          [●]     ⚙️   │ │
│  │ Cursor            Code Assistant   85          [●]     ⚙️   │ │
│  │ Midjourney        Image Generator  80          [●]     ⚙️   │ │
│  │ DALL-E            Image Generator  80          [●]     ⚙️   │ │
│  │ Perplexity        Search Engine    75          [●]     ⚙️   │ │
│  │ ...                                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Edit Tool Modal**:

```
┌──────────────────────────────────────────────────────────────────┐
│  Edit AI Tool: ChatGPT                        [Delete] [Cancel] [Save]│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Tool Name:        [ChatGPT                                    ] │
│                                                                  │
│  Tool Type:        [Chatbot                             ▾]      │
│                                                                  │
│  Priority:         [100                                        ] │
│                    (Higher priority = checked first)             │
│                                                                  │
│  Detection Signatures                                            │
│                                                                  │
│  Domains (comma-separated):                                      │
│  [chatgpt.com, chat.openai.com                                 ] │
│                                                                  │
│  Keywords (comma-separated):                                     │
│  [ChatGPT, OpenAI, regenerate response, continue generating    ] │
│                                                                  │
│  Process Names (comma-separated):                                │
│  [                                                             ] │
│                                                                  │
│  Confidence Weight:  [1.0    ] (0.1 - 2.0)                      │
│                                                                  │
│  ☑ Enabled                                                      │
│                                                                  │
│  [Delete Tool]                            [Cancel]  [Save]       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 15. User Management (Admin)

```
┌──────────────────────────────────────────────────────────────────┐
│  User Management                                    [+ Add User] │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Search users...]         [Role ▾] [Organization ▾] [Status ▾] │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Name             Email              Role      Status   Actions│ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ Prof. Smith     smith@uni.edu      Admin     Active    ⚙️ 🗑️│ │
│  │ Jane Doe        jane@uni.edu       Examinee  Active    ⚙️ 🗑️│ │
│  │ John Proctor    proctor@uni.edu    Proctor   Active    ⚙️ 🗑️│ │
│  │ Sarah Review    sarah@uni.edu      Reviewer  Active    ⚙️ 🗑️│ │
│  │ ...                                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Showing 1-10 of 150               [1] [2] [3] ... [15] [Next]  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 16. Audit Log Viewer

```
┌──────────────────────────────────────────────────────────────────┐
│  Audit Logs                                     [Export] [Filter]│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Search...]              [Action ▾] [User ▾] [Date Range]      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Timestamp         User          Action        Entity        │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ 2026-06-26 10:00  admin@uni     CREATE        Session       │ │
│  │ Details: Created session "Final Exam CS101"                 │ │
│  │                                                              │ │
│  │ 2026-06-26 09:55  proctor@uni   UPDATE        User          │ │
│  │ Details: Changed role from 'reviewer' to 'proctor'          │ │
│  │                                                              │ │
│  │ 2026-06-26 09:50  admin@uni     DELETE        AI Tool       │ │
│  │ Details: Deleted tool configuration "Old Tool"              │ │
│  │                                                              │ │
│  │ ...                                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Showing 1-20 of 5,432                    [1] [2] ... [Next →]  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Responsive Design

### Desktop (1920x1080+)
- Full dashboard with sidebar
- Multi-column layouts
- Large preview images

### Tablet (768px - 1919px)
- Collapsible sidebar
- Stacked columns
- Optimized touch targets

### Mobile (< 768px)
- Bottom navigation
- Single column layout
- Touch-optimized controls
- Limited to essential features (view-only mode)

---

## Accessibility

### WCAG 2.1 AA Compliance

**Keyboard Navigation**:
- Tab navigation through all interactive elements
- Arrow keys for lists and grids
- Enter/Space for activation
- Escape to close modals

**Screen Reader Support**:
- Semantic HTML
- ARIA labels and descriptions
- Live regions for dynamic content
- Status announcements

**Visual**:
- Minimum contrast ratio 4.5:1
- Focus indicators (2px outline)
- No information conveyed by color alone
- Scalable text (supports 200% zoom)

**Interaction**:
- Touch targets minimum 44x44px
- No time-based interactions
- Alternative input methods supported

---

## Animation & Transitions

**Timing**:
- Fast: 150ms (hover states)
- Normal: 250ms (page transitions)
- Slow: 400ms (complex animations)

**Easing**:
- `ease-in-out` for most transitions
- `ease-out` for entrances
- `ease-in` for exits

**Reduced Motion**:
- Respect `prefers-reduced-motion`
- Disable animations if requested
- Use instant transitions instead

---

## Loading States

### Skeleton Screens
- Use for initial page load
- Match layout of final content
- Subtle pulsing animation

### Spinners
- Use for async actions (< 2 seconds)
- Center in container
- With descriptive text

### Progress Bars
- Use for long operations (> 2 seconds)
- Show percentage if calculable
- Indeterminate if not

---

## Empty States

### No Data
```
┌──────────────────────────────────────────┐
│                                          │
│            [Illustration]                │
│                                          │
│         No sessions yet                  │
│                                          │
│    Get started by creating your          │
│         first monitoring session         │
│                                          │
│        [+ Create Session]                │
│                                          │
└──────────────────────────────────────────┘
```

### No Search Results
```
┌──────────────────────────────────────────┐
│            [Search Icon]                 │
│                                          │
│      No results found for "xyz"          │
│                                          │
│    Try adjusting your search or filters  │
│                                          │
│        [Clear Filters]                   │
└──────────────────────────────────────────┘
```

---

## Error States

### Inline Error
```
┌────────────────────────────────────┐
│ Email Address                      │
│ [user@                          ]  │
│ ❌ Please enter a valid email     │
└────────────────────────────────────┘
```

### Page Error
```
┌──────────────────────────────────────────┐
│         [Error Illustration]             │
│                                          │
│        Something went wrong              │
│                                          │
│   We couldn't load this session.         │
│   Please try again.                      │
│                                          │
│   [Try Again]  [Go Home]                 │
└──────────────────────────────────────────┘
```

### Toast Notification
```
┌─────────────────────────────────────────┐
│ ✓ Session started successfully     [×] │
└─────────────────────────────────────────┘
```

---

## Document Version
- **Version**: 1.0
- **Last Updated**: 2026-06-26
- **Author**: Integraty Development Team
