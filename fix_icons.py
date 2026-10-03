import os, glob

# Rerun generation to get clean SVGs
os.system('python generate_svgs.py')

for filepath in glob.glob('assets/icons/*.svg'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<style>' not in content:
        style_block = '''
    <style>
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
        100% { transform: translateY(0px); }
    }
    .animated-icon { animation: float 4s cubic-bezier(0.25, 1, 0.5, 1) infinite; }
    </style>'''
        # Properly insert <style> AFTER the closing > of <svg ...>
        content = content.replace('xmlns="http://www.w3.org/2000/svg">', 'xmlns="http://www.w3.org/2000/svg">' + style_block)
        content = content.replace('<g transform=', '<g class="animated-icon" transform=')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Icons fixed and animated.')
