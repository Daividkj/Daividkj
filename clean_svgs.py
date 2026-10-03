import urllib.request, re, os

os.makedirs('assets/icons', exist_ok=True)

def generate_custom_icon(slug, color):
    url = f'https://unpkg.com/simple-icons@13.14.0/icons/{slug}.svg'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        svg_data = urllib.request.urlopen(req).read().decode('utf-8')
        path_match = re.search(r'<path.*?(?:/>|</path>)', svg_data, re.DOTALL)
        path_str = path_match.group(0)
        
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

generate_custom_icon('salesforce', '00A1E0')
generate_custom_icon('tableau', 'E97627')

powerbi_svg = '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="48" height="48" rx="14" fill="#242938"/>
    <g transform="translate(12, 12) scale(0.75)">
        <path fill="#F2C811" d="M22,2 h8 v30 h-8 Z M12,10 h8 v22 h-8 Z M2,18 h8 v14 h-8 Z"/>
    </g>
</svg>'''
with open('assets/icons/powerbi.svg', 'w', encoding='utf-8') as f:
    f.write(powerbi_svg)
print('Successfully generated powerbi.svg')

