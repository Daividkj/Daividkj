import os
import requests
from datetime import datetime, timezone
import html

TOKEN = os.getenv("GH_TOKEN")
USERNAME = os.getenv("GITHUB_ACTOR", "Daividkj")

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"

def get_recent_events():
    url = f"https://api.github.com/users/{USERNAME}/events"
    response = requests.get(url, headers=HEADERS)
    events = []
    if response.status_code == 200:
        for event in response.json():
            # Filter meaningful events
            if event['type'] in ['PushEvent', 'IssuesEvent', 'PullRequestEvent', 'ReleaseEvent']:
                events.append(event)
            if len(events) >= 5:
                break
    return events

events = get_recent_events()
log_lines = []
for ev in events:
    repo = ev['repo']['name']
    ev_type = ev['type']
    created_at = datetime.strptime(ev['created_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = now - created_at
    hours_ago = int(diff.total_seconds() / 3600)
    
    if hours_ago == 0:
        time_str = "just now"
    elif hours_ago < 24:
        time_str = f"{hours_ago}h ago"
    else:
        time_str = f"{hours_ago // 24}d ago"

    if ev_type == 'PushEvent':
        commits = len(ev['payload'].get('commits', []))
        log_lines.append(f"> [DEV] Pushed {commits} commit(s) to {repo} ({time_str})")
    elif ev_type == 'IssuesEvent':
        action = ev['payload'].get('action')
        log_lines.append(f"> [OPS] {action.capitalize()} issue in {repo} ({time_str})")
    elif ev_type == 'PullRequestEvent':
        action = ev['payload'].get('action')
        log_lines.append(f"> [SYS] {action.capitalize()} PR in {repo} ({time_str})")
    elif ev_type == 'ReleaseEvent':
        log_lines.append(f"> [REL] Published release in {repo} ({time_str})")

if not log_lines:
    log_lines = ["> [SYS] Monitoring secure channels...", "> [SYS] All systems operational.", "> [DEV] Committing to encrypted storage."]

# Format SVG
lines_svg = ""
for i, line in enumerate(log_lines):
    safe_line = html.escape(line)
    y_pos = 100 + (i * 25)
    # Typewriter animation by animating stroke-dasharray or a masking rect
    # We will use a simple clipping mask that expands over time
    lines_svg += f'''
    <clipPath id="clipLine{i}">
        <rect x="20" y="{y_pos - 15}" width="0" height="20">
            <animate attributeName="width" from="0" to="760" dur="2s" begin="{i * 0.8}s" fill="freeze" />
        </rect>
    </clipPath>
    <text x="20" y="{y_pos}" font-family="Courier New, monospace" font-size="14" fill="#00FFFF" clip-path="url(#clipLine{i})">
        {safe_line}
    </text>
    '''

svg = f'''<svg width="800" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="250" rx="10" fill="#0D1117" stroke="#30363D" stroke-width="2"/>
    <!-- Mac-style top bar -->
    <rect width="800" height="30" rx="10" fill="#161B22" />
    <circle cx="20" cy="15" r="6" fill="#FF5F56" />
    <circle cx="40" cy="15" r="6" fill="#FFBD2E" />
    <circle cx="60" cy="15" r="6" fill="#27C93F" />
    <text x="400" y="20" font-family="Courier New, monospace" font-size="12" fill="#8B949E" text-anchor="middle">
        root@architect-sys:~# /bin/bash
    </text>

    <!-- Terminal Content -->
    <text x="20" y="60" font-family="Courier New, monospace" font-size="14" fill="#E6EDF3" font-weight="bold">
        $ ./fetch_recent_activity.sh --secure
    </text>
    <text x="20" y="80" font-family="Courier New, monospace" font-size="12" fill="#8B949E">
        [+] ESTABLISHING SECURE CONNECTION... OK
    </text>

    {lines_svg}

    <!-- Blinking Cursor -->
    <rect x="20" y="{100 + len(log_lines)*25}" width="10" height="15" fill="#FF00FF">
        <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
    </rect>
</svg>'''

os.makedirs('assets', exist_ok=True)
with open('assets/terminal.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print("Terminal SVG generated!")
