import urllib.request
import re

slug = 'bruno'
color = 'E36826'  # Bruno brand color (Orange)

url = f'https://unpkg.com/simple-icons@13.14.0/icons/{slug}.svg'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    svg_data = urllib.request.urlopen(req).read().decode('utf-8')
    path_match = re.search(r'<path.*?(?:/>|</path>)', svg_data, re.DOTALL)
    path_str = path_match.group(0)
    
    # Simple icons usually lack a fill attribute on the path itself because they inherit it.
    path_str = path_str.replace('<path', f'<path fill="#{color}"')
    
    new_svg = f'''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="48" height="48" rx="14" fill="#242938"/>
    <g transform="translate(12, 12)">
        {path_str}
    </g>
</svg>'''
    with open(f'assets/icons/{slug}.svg', 'w', encoding='utf-8') as f:
        f.write(new_svg)
    print(f'Successfully generated {slug}.svg')
except Exception as e:
    print(f'Failed {slug}: {e}')
