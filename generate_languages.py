import os
import requests

TOKEN = os.getenv("GH_TOKEN")
USERNAME = os.getenv("GITHUB_ACTOR", "Daividkj")

if not TOKEN:
    # Generate a placeholder if no token
    svg = '''<svg width="800" height="150" viewBox="0 0 800 150" xmlns="http://www.w3.org/2000/svg">
        <rect width="800" height="150" rx="10" fill="#0D1117" stroke="#30363D" stroke-width="1"/>
        <text x="400" y="75" font-family="Courier New" font-size="16" fill="#8B949E" text-anchor="middle">
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
    total_size = 1 # prevent div by zero

# Sort by size
sorted_langs = sorted(langs.items(), key=lambda x: x[1]["size"], reverse=True)[:6]

# Build SVG
svg = '''<svg width="800" height="150" viewBox="0 0 800 150" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="150" rx="10" fill="#0D1117" stroke="#30363D" stroke-width="1"/>
    
    <!-- Progress Bar -->
    <g transform="translate(40, 40)">
        <rect x="0" y="0" width="720" height="12" rx="6" fill="#30363D" />
'''

current_x = 0
bar_width = 720

for name, info in sorted_langs:
    pct = info["size"] / total_size
    w = pct * bar_width
    if w > 0:
        svg += f'''
        <rect x="{current_x}" y="0" width="{w}" height="12" fill="{info['color']}">
            <animate attributeName="width" from="0" to="{w}" dur="1.5s" fill="freeze" />
        </rect>
        '''
        current_x += w

svg += '''
    </g>
    <!-- Labels -->
    <g transform="translate(40, 80)">
'''

for i, (name, info) in enumerate(sorted_langs):
    pct = (info["size"] / total_size) * 100
    row = i // 3
    col = i % 3
    lx = col * 250
    ly = row * 30
    
    svg += f'''
        <circle cx="{lx}" cy="{ly - 4}" r="4" fill="{info['color']}" />
        <text x="{lx + 15}" y="{ly}" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#E6EDF3">{name} {pct:.1f}%</text>
    '''

svg += '''
    </g>
</svg>
'''

os.makedirs('assets', exist_ok=True)
with open('assets/languages.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print("Language SVG generated!")
