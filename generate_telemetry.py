import os
import requests
import json
from datetime import datetime

# GitHub API setup
TOKEN = os.getenv("GH_TOKEN")
USERNAME = os.getenv("GITHUB_ACTOR", "Daividkj")

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"

def get_total_commits():
    # Search commits requires a specific preview header
    h = HEADERS.copy()
    h["Accept"] = "application/vnd.github.cloak-preview"
    url = f"https://api.github.com/search/commits?q=author:{USERNAME}"
    response = requests.get(url, headers=h)
    if response.status_code == 200:
        return response.json().get("total_count", 0)
    return "???"

def get_total_prs():
    url = f"https://api.github.com/search/issues?q=type:pr+author:{USERNAME}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("total_count", 0)
    return "???"

def get_total_issues():
    url = f"https://api.github.com/search/issues?q=type:issue+author:{USERNAME}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("total_count", 0)
    return "???"

def get_total_stars_and_repos():
    # Fetch all repos (including private if authenticated)
    url = f"https://api.github.com/user/repos?per_page=100&affiliation=owner"
    if not TOKEN:
        # Fallback if no token is provided
        url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    
    response = requests.get(url, headers=HEADERS)
    stars = 0
    private_repos = 0
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            stars += repo.get("stargazers_count", 0)
            if repo.get("private", False):
                private_repos += 1
        return stars, private_repos
    return "???", "???"

print("Fetching GitHub Stats...")
commits = get_total_commits()
prs = get_total_prs()
issues = get_total_issues()
stars, private = get_total_stars_and_repos()

print(f"Commits: {commits}, PRs: {prs}, Issues: {issues}, Stars: {stars}, Private Repos: {private}")

# Generate Cyberpunk SVG
svg_content = f"""<svg width="800" height="200" viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#00FFFF"/>
            <stop offset="100%" stop-color="#FF00FF"/>
        </linearGradient>
        <filter id="glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Background -->
    <rect width="800" height="200" rx="15" fill="#0D1117" stroke="url(#grad)" stroke-width="2" />
    
    <!-- Cyberpunk grid/lines -->
    <path d="M 0 50 L 800 50" stroke="#FF00FF" stroke-width="0.5" stroke-dasharray="10 10" opacity="0.3"/>
    <path d="M 0 150 L 800 150" stroke="#00FFFF" stroke-width="0.5" stroke-dasharray="10 10" opacity="0.3"/>
    <path d="M 200 0 L 200 200" stroke="#FF00FF" stroke-width="0.5" stroke-dasharray="5 5" opacity="0.1"/>
    <path d="M 600 0 L 600 200" stroke="#00FFFF" stroke-width="0.5" stroke-dasharray="5 5" opacity="0.1"/>

    <!-- Title -->
    <text x="40" y="35" font-family="Courier New, monospace" font-size="18" font-weight="bold" fill="#E6EDF3" letter-spacing="2">
        <tspan fill="#FF00FF">></tspan> SYSTEM_TELEMETRY_DATABANK
    </text>

    <!-- Stats -->
    <!-- Column 1 -->
    <text x="50" y="90" font-family="Courier New, monospace" font-size="14" fill="#8B949E">TOTAL_COMMITS</text>
    <text x="50" y="125" font-family="Courier New, monospace" font-size="32" font-weight="bold" fill="#00FFFF" filter="url(#glow)">{commits}</text>

    <!-- Column 2 -->
    <text x="250" y="90" font-family="Courier New, monospace" font-size="14" fill="#8B949E">PULL_REQUESTS</text>
    <text x="250" y="125" font-family="Courier New, monospace" font-size="32" font-weight="bold" fill="#FF00FF" filter="url(#glow)">{prs}</text>

    <!-- Column 3 -->
    <text x="450" y="90" font-family="Courier New, monospace" font-size="14" fill="#8B949E">ISSUES_OPENED</text>
    <text x="450" y="125" font-family="Courier New, monospace" font-size="32" font-weight="bold" fill="#FFFF00" filter="url(#glow)">{issues}</text>

    <!-- Column 4 -->
    <text x="650" y="90" font-family="Courier New, monospace" font-size="14" fill="#8B949E">SECRET_REPOS</text>
    <text x="650" y="125" font-family="Courier New, monospace" font-size="32" font-weight="bold" fill="#FF5555" filter="url(#glow)">{private}</text>

    <!-- Footer -->
    <text x="40" y="180" font-family="Courier New, monospace" font-size="12" fill="#484F58">
        LAST_SYNC: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC | AUTHORIZED_ACCESS
    </text>

    <!-- Blinking cursor -->
    <rect x="750" y="22" width="10" height="15" fill="#00FFFF">
        <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
    </rect>
</svg>
"""

os.makedirs('assets', exist_ok=True)
with open('assets/telemetry.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("Telemetry SVG generated successfully.")
