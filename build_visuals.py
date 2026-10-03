import math
import os

os.makedirs('assets', exist_ok=True)
os.makedirs('assets/headers', exist_ok=True)

# 1. GENERATE NEW HEADERS
new_headers = [
    {"filename": "radar", "text": "[ ARCHITECTURE_RADAR ]", "color1": "#00FFFF", "color2": "#FF00FF"},
    {"filename": "3d", "text": "[ ISOMETRIC_CONTRIBUTIONS ]", "color1": "#00FF00", "color2": "#FFFF00"},
    {"filename": "terminal", "text": "[ LIVE_SYSTEM_LOGS ]", "color1": "#FF00FF", "color2": "#00FFFF"}
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


# 2. GENERATE ARCHITECTURE RADAR
# 5 Axes: Architecture, AI Systems, Cloud & DevOps, Backend, Frontend & Mobile
labels = ["SYSTEM ARCHITECTURE", "AI & AGENT SYSTEMS", "CLOUD & DEVOPS", "BACKEND & APIS", "FRONTEND & MOBILE"]
scores = [0.95, 0.90, 0.85, 0.95, 0.80]

center_x, center_y = 400, 200
radius = 120

def get_point(angle_deg, r):
    angle_rad = math.radians(angle_deg)
    return (center_x + r * math.cos(angle_rad), center_y + r * math.sin(angle_rad))

angles = [-90, -18, 54, 126, 198]

# Background webs
web_levels = [0.2, 0.4, 0.6, 0.8, 1.0]
webs_svg = ""
for level in web_levels:
    pts = [get_point(a, radius * level) for a in angles]
    points_str = " ".join([f"{x},{y}" for x, y in pts])
    webs_svg += f'<polygon points="{points_str}" fill="none" stroke="#30363D" stroke-width="1"/>\n'

# Axes lines
axes_svg = ""
for a in angles:
    px, py = get_point(a, radius)
    axes_svg += f'<line x1="{center_x}" y1="{center_y}" x2="{px}" y2="{py}" stroke="#30363D" stroke-width="1"/>\n'

# Data Polygon
data_pts = [get_point(angles[i], radius * scores[i]) for i in range(5)]
data_points_str = " ".join([f"{x},{y}" for x, y in data_pts])
data_polygon = f'''
<polygon points="{data_points_str}" fill="rgba(0, 255, 255, 0.2)" stroke="#00FFFF" stroke-width="2">
    <animate attributeName="opacity" values="0.7; 1; 0.7" dur="4s" repeatCount="indefinite" />
</polygon>
'''

# Dots on data points
dots_svg = ""
for x, y in data_pts:
    dots_svg += f'''
    <circle cx="{x}" cy="{y}" r="4" fill="#FF00FF">
        <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite"/>
    </circle>
    '''

# Labels
labels_svg = ""
label_offsets = [(0, -20), (30, -5), (20, 20), (-20, 20), (-30, -5)]
text_anchors = ["middle", "start", "start", "end", "end"]
for i in range(5):
    lx, ly = get_point(angles[i], radius + 15)
    ox, oy = label_offsets[i]
    labels_svg += f'''
    <text x="{lx + ox}" y="{ly + oy}" font-family="Courier New, monospace" font-size="12" font-weight="bold" fill="#E6EDF3" text-anchor="{text_anchors[i]}">
        {labels[i]}
    </text>
    '''

radar_svg = f'''<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="bgGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#00FFFF" stop-opacity="0.05" />
            <stop offset="100%" stop-color="#0D1117" stop-opacity="0" />
        </radialGradient>
    </defs>
    <rect width="800" height="400" fill="#0D1117" rx="15" />
    <circle cx="400" cy="200" r="{radius}" fill="url(#bgGrad)" />
    
    {webs_svg}
    {axes_svg}
    {data_polygon}
    {dots_svg}
    {labels_svg}
    
    <!-- Rotating decorative outer ring -->
    <circle cx="400" cy="200" r="{radius + 50}" fill="none" stroke="#FF00FF" stroke-width="1" stroke-dasharray="2 10" opacity="0.3">
        <animateTransform attributeName="transform" type="rotate" from="0 400 200" to="360 400 200" dur="40s" repeatCount="indefinite"/>
    </circle>
</svg>'''

with open('assets/radar.svg', 'w', encoding='utf-8') as f:
    f.write(radar_svg)

print("Radar and headers generated!")
