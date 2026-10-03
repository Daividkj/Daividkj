import math
import os

os.makedirs('assets', exist_ok=True)
os.makedirs('assets/headers', exist_ok=True)

# 1. HEADERS
new_headers = [
    {"filename": "radar", "text": "[ ARCHITECTURE_RADAR ]", "color1": "#00FFFF", "color2": "#FF00FF"},
    {"filename": "3d", "text": "[ ISOMETRIC_CONTRIBUTIONS ]", "color1": "#00FF00", "color2": "#FFFF00"},
    {"filename": "terminal", "text": "[ LIVE_SYSTEM_LOGS ]", "color1": "#FF00FF", "color2": "#00FFFF"},
    {"filename": "languages", "text": "[ LANGUAGE_DISTRIBUTION ]", "color1": "#F2C811", "color2": "#E36826"}
]

for sec in new_headers:
    svg = f'''<svg width="800" height="60" viewBox="0 0 800 60" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(0, 15)">
        <rect x="0" y="0" width="8" height="24" fill="{sec['color1']}">
             <animate attributeName="opacity" values="1;0.3;1;1;0.1;1" keyTimes="0;0.05;0.1;0.8;0.85;1" dur="3s" repeatCount="indefinite" />
        </rect>
        <rect x="12" y="4" width="4" height="16" fill="{sec['color2']}">
             <animate attributeName="opacity" values="1;1;0.2;1" keyTimes="0;0.4;0.5;1" dur="2s" repeatCount="indefinite" />
        </rect>
    </g>
    <text x="30" y="34" font-family="Courier New, monospace" font-size="22" font-weight="bold" fill="#E6EDF3" letter-spacing="2">{sec['text']}</text>
    <rect x="30" y="45" width="770" height="1" fill="#30363D" />
    <rect x="30" y="44" width="40" height="3" fill="{sec['color1']}">
        <animate attributeName="x" values="30; 760; 30" dur="10s" repeatCount="indefinite" />
    </rect>
</svg>'''
    with open(f"assets/headers/header_{sec['filename']}.svg", "w", encoding="utf-8") as f:
        f.write(svg)


# 2. HIGHLY DETAILED ARCHITECTURE RADAR
labels = ["SYSTEM ARCHITECTURE", "AI & AGENT SYSTEMS", "CLOUD & DEVOPS", "BACKEND & APIS", "FRONTEND & MOBILE"]
sub_labels = [
    ["Microservices, Zero-Trust", "Design Patterns"],
    ["Local LLMs, Agentic Workflows", "Qwen, Llama, Prompt Eng"],
    ["AWS, Docker, K8s", "CI/CD, Cloudflare Tunnels"],
    ["Node.js, FastAPI, Python", "PostgreSQL, GraphQL"],
    ["React, Next.js, Flutter", "Impeccable UI/UX"]
]
scores_expert = [0.95, 0.90, 0.85, 0.95, 0.80]
scores_hands_on = [0.80, 0.95, 0.90, 0.90, 0.85]

center_x, center_y = 400, 220
radius = 140

def get_point(angle_deg, r):
    angle_rad = math.radians(angle_deg)
    return (center_x + r * math.cos(angle_rad), center_y + r * math.sin(angle_rad))

angles = [-90, -18, 54, 126, 198]

# Concentric polygons (20%, 40%, 60%, 80%, 100%)
webs_svg = ""
for level in [0.2, 0.4, 0.6, 0.8, 1.0]:
    pts = [get_point(a, radius * level) for a in angles]
    points_str = " ".join([f"{x},{y}" for x, y in pts])
    opacity = 0.2 if level < 1.0 else 0.6
    webs_svg += f'<polygon points="{points_str}" fill="none" stroke="#00FFFF" stroke-width="1" opacity="{opacity}"/>\n'

# Axes
axes_svg = ""
for a in angles:
    px, py = get_point(a, radius)
    axes_svg += f'<line x1="{center_x}" y1="{center_y}" x2="{px}" y2="{py}" stroke="#00FFFF" stroke-width="1" opacity="0.4"/>\n'

# Expert Polygon (Strategic/Architecture)
pts_exp = [get_point(angles[i], radius * scores_expert[i]) for i in range(5)]
str_exp = " ".join([f"{x},{y}" for x, y in pts_exp])
poly_exp = f'''
<polygon points="{str_exp}" fill="rgba(255, 0, 255, 0.2)" stroke="#FF00FF" stroke-width="2">
    <animate attributeName="opacity" values="0.6; 1; 0.6" dur="3s" repeatCount="indefinite" />
</polygon>
'''

# Hands-on Polygon (Implementation)
pts_hands = [get_point(angles[i], radius * scores_hands_on[i]) for i in range(5)]
str_hands = " ".join([f"{x},{y}" for x, y in pts_hands])
poly_hands = f'''
<polygon points="{str_hands}" fill="rgba(0, 255, 255, 0.3)" stroke="#00FFFF" stroke-width="1" stroke-dasharray="4 2">
    <animate attributeName="opacity" values="0.8; 0.4; 0.8" dur="4s" repeatCount="indefinite" />
</polygon>
'''

# Labels & Sub-labels
labels_svg = ""
label_offsets = [(0, -35), (35, -10), (25, 25), (-25, 25), (-35, -10)]
text_anchors = ["middle", "start", "start", "end", "end"]
for i in range(5):
    lx, ly = get_point(angles[i], radius + 15)
    ox, oy = label_offsets[i]
    labels_svg += f'''
    <text x="{lx + ox}" y="{ly + oy}" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#E6EDF3" text-anchor="{text_anchors[i]}">{labels[i].replace("&", "&amp;")}</text>
    <text x="{lx + ox}" y="{ly + oy + 16}" font-family="Courier New, monospace" font-size="11" fill="#8B949E" text-anchor="{text_anchors[i]}">{sub_labels[i][0]}</text>
    <text x="{lx + ox}" y="{ly + oy + 30}" font-family="Courier New, monospace" font-size="11" fill="#8B949E" text-anchor="{text_anchors[i]}">{sub_labels[i][1]}</text>
    '''

# Legend
legend_svg = '''
<g transform="translate(20, 20)">
    <rect x="0" y="0" width="12" height="12" fill="rgba(255, 0, 255, 0.4)" stroke="#FF00FF" stroke-width="1"/>
    <text x="20" y="10" font-family="Courier New, monospace" font-size="12" fill="#E6EDF3">Strategic Design &amp; Architecture</text>
    
    <rect x="0" y="25" width="12" height="12" fill="rgba(0, 255, 255, 0.4)" stroke="#00FFFF" stroke-width="1" stroke-dasharray="2 2"/>
    <text x="20" y="35" font-family="Courier New, monospace" font-size="12" fill="#E6EDF3">Hands-on Execution &amp; Coding</text>
</g>
'''

radar_svg = f'''<svg width="800" height="450" viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="450" fill="#0D1117" rx="15" stroke="#30363D" stroke-width="1" />
    
    <!-- Tech Grid Background -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#ffffff" stroke-width="1" stroke-opacity="0.03" />
    </pattern>
    <rect width="800" height="450" fill="url(#grid)" />

    {legend_svg}
    {webs_svg}
    {axes_svg}
    {poly_exp}
    {poly_hands}
    {labels_svg}
    
    <!-- Outer Ring -->
    <circle cx="{center_x}" cy="{center_y}" r="{radius + 10}" fill="none" stroke="#30363D" stroke-width="1" stroke-dasharray="5 5">
        <animateTransform attributeName="transform" type="rotate" from="0 {center_x} {center_y}" to="360 {center_x} {center_y}" dur="60s" repeatCount="indefinite"/>
    </circle>
</svg>'''

with open('assets/radar.svg', 'w', encoding='utf-8') as f:
    f.write(radar_svg)

print("Advanced Radar and headers generated!")
