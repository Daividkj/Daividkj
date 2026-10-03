import os
import requests
import math

TOKEN = os.getenv("GH_TOKEN")
USERNAME = os.getenv("GITHUB_ACTOR", "Daividkj")

if not TOKEN:
    svg = '''<svg width="800" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
        <rect width="800" height="250" rx="10" fill="#0D1117" stroke="#30363D" stroke-width="1"/>
        <text x="400" y="125" font-family="Courier New" font-size="16" fill="#8B949E" text-anchor="middle">
            Awaiting Authorization Token to decrypt Language Metrics...
        </text>
    </svg>'''
    os.makedirs('assets', exist_ok=True)
    with open('assets/languages.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Placeholder generated.")
    exit(0)

headers = {"Authorization": f"Bearer {TOKEN}"}

query = """
query {
  user(login: "%s") {
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      nodes {
        name
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
      }
    }
  }
}
""" % USERNAME

response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)

langs = {}
total_size = 0

if response.status_code == 200:
    data = response.json()
    repos = data.get("data", {}).get("user", {}).get("repositories", {}).get("nodes", [])
    for repo in repos:
        for edge in repo.get("languages", {}).get("edges", []):
            name = edge["node"]["name"]
            color = edge["node"]["color"] or "#CCCCCC"
            size = edge["size"]
            if name not in langs:
                langs[name] = {"size": 0, "color": color}
            langs[name]["size"] += size
            total_size += size

if total_size == 0:
    total_size = 1

sorted_langs = sorted(langs.items(), key=lambda x: x[1]["size"], reverse=True)[:6]

svg = '''<svg width="800" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="250" rx="10" fill="#0D1117" stroke="#30363D" stroke-width="1"/>
    <!-- Cyberpunk grid background -->
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
        <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#ffffff" stroke-width="1" stroke-opacity="0.02" />
    </pattern>
    <rect width="800" height="250" fill="url(#grid)" />
    
    <g transform="translate(250, 125)">
'''

radius = 80
stroke_width = 30
circumference = 2 * math.pi * radius
current_angle = -90

donut_svg = ""
labels_svg = "<g transform='translate(160, -70)'>"

for i, (name, info) in enumerate(sorted_langs):
    pct = info["size"] / total_size
    seg_length = pct * circumference
    
    donut_svg += f'''
        <circle cx="0" cy="0" r="{radius}" fill="none" stroke="{info['color']}" stroke-width="{stroke_width}" 
                stroke-dasharray="{seg_length} {circumference}" stroke-dashoffset="{seg_length}" transform="rotate({current_angle})">
            <animate attributeName="stroke-dashoffset" from="{seg_length}" to="0" dur="1s" fill="freeze" begin="{i*0.2}s" />
        </circle>
    '''
    
    pct_text = pct * 100
    ly = i * 30
    labels_svg += f'''
        <circle cx="0" cy="{ly - 4}" r="5" fill="{info['color']}" />
        <text x="15" y="{ly}" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#E6EDF3">{name} <tspan fill="{info['color']}">{pct_text:.1f}%</tspan></text>
    '''
    current_angle += pct * 360

svg += donut_svg
svg += '''
        <!-- Inner glow/decoration -->
        <circle cx="0" cy="0" r="50" fill="#0D1117" stroke="#30363D" stroke-width="2" />
        <text x="0" y="5" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#8B949E" text-anchor="middle">CODE</text>
    </g>
'''

svg += labels_svg
svg += '''
    </g>
</svg>
'''

os.makedirs('assets', exist_ok=True)
with open('assets/languages.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print("Language Donut SVG generated!")
