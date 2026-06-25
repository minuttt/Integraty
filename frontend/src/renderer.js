// API Configuration
let API_BASE_URL = localStorage.getItem('apiUrl') || 'http://localhost:8080';

// State
let currentSession = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    checkServerStatus();
    loadDashboardStats();

    // Auto-refresh every 5 seconds
    setInterval(() => {
        if (document.getElementById('dashboard-page').classList.contains('active')) {
            checkServerStatus();
            loadDashboardStats();
        }
    }, 5000);
});

// Navigation
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const page = item.dataset.page;
            switchPage(page);

            // Update active nav item
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
        });
    });
}

function switchPage(pageName) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));

    const targetPage = document.getElementById(`${pageName}-page`);
    if (targetPage) {
        targetPage.classList.add('active');

        // Load page-specific data
        if (pageName === 'sessions') {
            loadSessions();
        } else if (pageName === 'settings') {
            document.getElementById('apiUrl').value = API_BASE_URL;
        }
    }
}

// Server Status
async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        const indicator = document.getElementById('statusIndicator');
        const statusText = indicator.querySelector('.status-text');

        indicator.classList.add('connected');
        statusText.textContent = 'Connected';

        document.getElementById('serverStatus').textContent = 'Online';
    } catch (error) {
        const indicator = document.getElementById('statusIndicator');
        const statusText = indicator.querySelector('.status-text');

        indicator.classList.remove('connected');
        statusText.textContent = 'Disconnected';

        document.getElementById('serverStatus').textContent = 'Offline';
    }
}

// Dashboard
async function loadDashboardStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/sessions/`);
        const sessions = await response.json();

        const activeSessions = sessions.filter(s => s.status === 'active').length;
        const totalSessions = sessions.length;

        document.getElementById('activeSessions').textContent = activeSessions;
        document.getElementById('totalSessions').textContent = totalSessions;

        // Calculate total detections
        const totalDetections = sessions.reduce((sum, s) => sum + (s.stats.detections || 0), 0);
        document.getElementById('detectionsToday').textContent = totalDetections;

    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// New Session
document.getElementById('newSessionForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        user_id: document.getElementById('userId').value,
        session_name: document.getElementById('sessionName').value,
        session_type: document.getElementById('sessionType').value,
        screenshot_interval: parseInt(document.getElementById('screenshotInterval').value),
        enable_ocr: document.getElementById('enableOcr').checked,
        enable_window_monitoring: document.getElementById('enableWindowMonitoring').checked,
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/sessions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        const result = await response.json();

        if (response.ok) {
            currentSession = result;
            document.getElementById('createdSessionId').textContent = result.session_id;
            document.getElementById('newSessionForm').style.display = 'none';
            document.getElementById('sessionCreated').style.display = 'block';

            // Setup start button
            document.getElementById('startSessionBtn').onclick = () => startSession(result.session_id);
        } else {
            alert('Error creating session: ' + JSON.stringify(result));
        }
    } catch (error) {
        alert('Error creating session: ' + error.message);
    }
});

async function startSession(sessionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/sessions/${sessionId}/start`, {
            method: 'POST',
        });

        const result = await response.json();

        if (response.ok) {
            alert('Session started successfully!');
            switchPage('dashboard');
        } else {
            alert('Error starting session: ' + JSON.stringify(result));
        }
    } catch (error) {
        alert('Error starting session: ' + error.message);
    }
}

// Sessions List
async function loadSessions() {
    const container = document.getElementById('sessionsList');
    container.innerHTML = '<p class="empty-state">Loading sessions...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/sessions/`);
        const sessions = await response.json();

        if (sessions.length === 0) {
            container.innerHTML = '<p class="empty-state">No sessions found</p>';
            return;
        }

        container.innerHTML = '';

        sessions.forEach(session => {
            const card = createSessionCard(session);
            container.appendChild(card);
        });

    } catch (error) {
        container.innerHTML = '<p class="empty-state">Error loading sessions</p>';
        console.error('Error loading sessions:', error);
    }
}

function createSessionCard(session) {
    const card = document.createElement('div');
    card.className = 'session-card';

    const statusClass = session.status === 'active' ? 'active' : 'completed';

    card.innerHTML = `
        <div class="session-header">
            <div class="session-name">${session.user_id}</div>
            <span class="session-status ${statusClass}">${session.status}</span>
        </div>
        <div class="session-info">
            <span>Screenshots: ${session.stats.screenshots_captured}</span>
            <span>Detections: ${session.stats.detections}</span>
            <span>Windows: ${session.stats.window_changes}</span>
        </div>
        <div class="session-actions">
            ${session.status === 'active' ? `
                <button class="btn btn-secondary" onclick="pauseSession('${session.session_id}')">Pause</button>
                <button class="btn btn-danger" onclick="completeSession('${session.session_id}')">Complete</button>
            ` : ''}
            ${session.status === 'paused' ? `
                <button class="btn btn-primary" onclick="resumeSession('${session.session_id}')">Resume</button>
            ` : ''}
            <button class="btn btn-secondary" onclick="viewSession('${session.session_id}')">View Details</button>
        </div>
    `;

    return card;
}

async function pauseSession(sessionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/sessions/${sessionId}/pause`, {
            method: 'POST',
        });

        if (response.ok) {
            loadSessions();
        }
    } catch (error) {
        console.error('Error pausing session:', error);
    }
}

async function resumeSession(sessionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/sessions/${sessionId}/resume`, {
            method: 'POST',
        });

        if (response.ok) {
            loadSessions();
        }
    } catch (error) {
        console.error('Error resuming session:', error);
    }
}

async function completeSession(sessionId) {
    if (!confirm('Are you sure you want to complete this session?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/sessions/${sessionId}/complete`, {
            method: 'POST',
        });

        if (response.ok) {
            alert('Session completed successfully!');
            loadSessions();
            loadDashboardStats();
        }
    } catch (error) {
        console.error('Error completing session:', error);
    }
}

async function viewSession(sessionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/sessions/${sessionId}`);
        const session = await response.json();

        alert(JSON.stringify(session, null, 2));
    } catch (error) {
        console.error('Error viewing session:', error);
    }
}

// Settings
function saveSettings() {
    const apiUrl = document.getElementById('apiUrl').value;
    localStorage.setItem('apiUrl', apiUrl);
    API_BASE_URL = apiUrl;
    alert('Settings saved! Reconnecting...');
    checkServerStatus();
}
