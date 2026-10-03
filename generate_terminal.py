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
            if event['type'] in ['PushEvent', 'IssuesEvent', 'PullRequestEvent', 'ReleaseEvent']:
                events.append(event)
            if len(events) >= 6:
                break
    return events

events = get_recent_events()
log_lines = []
for ev in events:
    repo = ev['repo']['name'].replace('Daividkj/', '')
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

    timestamp = created_at.strftime("%b %d %H:%M:%S")

    if ev_type == 'PushEvent':
        commits = ev['payload'].get('size', 1)
        log_lines.append(f"{timestamp} sys kernel: [ {repo} ] Pushed {commits} commit(s) ({time_str})")
    elif ev_type == 'IssuesEvent':
        action = ev['payload'].get('action')
        log_lines.append(f"{timestamp} sys kernel: [ {repo} ] Issue {action} ({time_str})")
    elif ev_type == 'PullRequestEvent':
        action = ev['payload'].get('action')
        log_lines.append(f"{timestamp} sys kernel: [ {repo} ] PR {action} ({time_str})")
    elif ev_type == 'ReleaseEvent':
        log_lines.append(f"{timestamp} sys kernel: [ {repo} ] Release published ({time_str})")

if not log_lines:
    log_lines = [f"{datetime.now(timezone.utc).strftime('%b %d %H:%M:%S')} sys kernel: [ daemon ] System idle, awaiting tasks..."]

# Add realistic boot lines
boot_lines = [
    f"{datetime.now(timezone.utc).strftime('%b %d %H:%M:%S')} sys init: Arch OS v10.4.1 boot sequence initiated",
    f"{datetime.now(timezone.utc).strftime('%b %d %H:%M:%S')} sys network: Secure connection established to GitHub API",
    f"{datetime.now(timezone.utc).strftime('%b %d %H:%M:%S')} sys auth: RSA key fingerprint verified",
    f"{datetime.now(timezone.utc).strftime('%b %d %H:%M:%S')} sys daemon: fetching recent operations..."
]

all_lines = boot_lines + log_lines

lines_svg = ""
for i, line in enumerate(all_lines):
    safe_line = html.escape(line)
    y_pos = 90 + (i * 20)
    # White text for standard realistic terminal
    lines_svg += f'''
    <clipPath id="clipLine{i}">
        <rect x="15" y="{y_pos - 15}" width="0" height="20">
            <animate attributeName="width" from="0" to="770" dur="1s" begin="{i * 0.4}s" fill="freeze" />
        </rect>
    </clipPath>
    <text x="15" y="{y_pos}" font-family="Consolas, 'Courier New', monospace" font-size="13" fill="#D4D4D4" clip-path="url(#clipLine{i})">
        {safe_line}
    </text>
    '''

svg = f'''<svg width="800" height="300" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
    <!-- Terminal Window -->
    <rect width="800" height="300" rx="8" fill="#0A0A0A" stroke="#333333" stroke-width="1"/>
    
    <!-- macOS style top bar -->
    <rect width="800" height="25" rx="8" fill="#1C1C1E" />
    <path d="M 0 25 L 800 25" stroke="#333333" stroke-width="1" />
    <circle cx="15" cy="12.5" r="5.5" fill="#FF5F56" />
    <circle cx="35" cy="12.5" r="5.5" fill="#FFBD2E" />
    <circle cx="55" cy="12.5" r="5.5" fill="#27C93F" />
    
    <!-- Title -->
    <text x="400" y="17" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="12" fill="#888888" text-anchor="middle" font-weight="500">
        admin@architect-node:~ — bash — 80x24
    </text>

    <!-- Prompt -->
    <text x="15" y="55" font-family="Consolas, 'Courier New', monospace" font-size="13" font-weight="bold">
        <tspan fill="#4AF626">admin@architect-node</tspan><tspan fill="#D4D4D4">:</tspan><tspan fill="#3B8EEA">~</tspan><tspan fill="#D4D4D4">$ ./system_monitor.sh --tail 6</tspan>
    </text>

    <!-- Logs -->
    {lines_svg}

    <!-- Blinking Cursor -->
    <rect x="15" y="{90 + len(all_lines)*20 - 10}" width="8" height="15" fill="#D4D4D4">
        <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" begin="{len(all_lines)*0.4}s"/>
    </rect>
</svg>'''

os.makedirs('assets', exist_ok=True)
with open('assets/terminal.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print("Realistic Terminal SVG generated!")
