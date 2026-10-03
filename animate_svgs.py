import os, glob

for filepath in glob.glob('assets/icons/*.svg'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<style>' not in content:
        style_block = '''<style>
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
        100% { transform: translateY(0px); }
    }
    .animated-icon { animation: float 4s cubic-bezier(0.25, 1, 0.5, 1) infinite; }
</style>'''
        content = content.replace('<svg', '<svg\n    '+style_block, 1)
        content = content.replace('<g transform=', '<g class="animated-icon" transform=')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

access_denied_svg = '''<svg width="400" height="200" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
    <style>
        @keyframes pulse {
            0% { opacity: 1; box-shadow: 0 0 0 0 rgba(255, 0, 85, 0.7); }
            50% { opacity: 0.7; }
            100% { opacity: 1; box-shadow: 0 0 0 10px rgba(255, 0, 85, 0); }
        }
        @keyframes glitch {
            0% { transform: translate(0) }
            20% { transform: translate(-2px, 1px) }
            40% { transform: translate(-1px, -1px) }
            60% { transform: translate(2px, 1px) }
            80% { transform: translate(1px, -1px) }
            100% { transform: translate(0) }
        }
        .pulse-rect { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; stroke: #FF0055; stroke-width: 2; fill: #0B0B0C; }
        .glitch-text { animation: glitch 3s infinite; font-family: 'Courier New', monospace; font-size: 24px; fill: #FF0055; font-weight: bold; text-anchor: middle; }
        .blink-text { animation: pulse 1.5s infinite; font-family: 'Courier New', monospace; font-size: 14px; fill: #888888; text-anchor: middle; }
    </style>
    <rect class="pulse-rect" width="400" height="200" />
    <text x="200" y="100" class="glitch-text">[ ACCESS DENIED ]</text>
    <text x="200" y="130" class="blink-text">CLASSIFIED ARCHITECTURE</text>
    <line x1="50" y1="150" x2="350" y2="150" stroke="#FF0055" stroke-width="1" opacity="0.5" stroke-dasharray="4 4"/>
</svg>'''
with open('assets/access_denied.svg', 'w', encoding='utf-8') as f:
    f.write(access_denied_svg)

anime_quote_svg = '''<svg width="800" height="120" viewBox="0 0 800 120" xmlns="http://www.w3.org/2000/svg">
    <style>
        @keyframes gradientMove {
            0% { stop-color: #00FFFF; }
            50% { stop-color: #FF00FF; }
            100% { stop-color: #00FFFF; }
        }
        @keyframes breathe {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .bg-rect { fill: #0D1117; stroke: url(#grad1); stroke-width: 2; }
        .quote-text { font-family: 'Courier New', monospace; font-size: 16px; fill: #00FFFF; font-style: italic; }
        .author-text { font-family: 'Courier New', monospace; font-size: 14px; fill: #FF00FF; font-weight: bold; }
        .circle-outer { fill: none; stroke: url(#grad1); stroke-width: 2; stroke-dasharray: 4 4; transform-origin: 740px 60px; animation: rotate 10s linear infinite; }
        .circle-inner { fill: none; stroke: #00FFFF; stroke-width: 1; transform-origin: 740px 60px; animation: breathe 4s cubic-bezier(0.4, 0, 0.2, 1) infinite; }
        .circle-dot { fill: #FF00FF; animation: breathe 2s infinite; transform-origin: 740px 60px; }
    </style>
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#00FFFF">
                <animate attributeName="stop-color" values="#00FFFF;#FF00FF;#00FFFF" dur="5s" repeatCount="indefinite" />
            </stop>
            <stop offset="100%" stop-color="#FF00FF">
                <animate attributeName="stop-color" values="#FF00FF;#00FFFF;#FF00FF" dur="5s" repeatCount="indefinite" />
            </stop>
        </linearGradient>
    </defs>
    <rect class="bg-rect" width="800" height="120" rx="10" />
    <text x="40" y="45" class="quote-text">"If you don't take risks, you can't create a future."</text>
    <text x="40" y="80" class="author-text">> Monkey D. Luffy</text>
    
    <circle class="circle-outer" cx="740" cy="60" r="25" />
    <circle class="circle-inner" cx="740" cy="60" r="15" />
    <circle class="circle-dot" cx="740" cy="60" r="5" />
    
    <line x1="600" y1="20" x2="650" y2="20" stroke="#00FFFF" stroke-width="2"/>
    <line x1="600" y1="100" x2="700" y2="100" stroke="#FF00FF" stroke-width="2"/>
</svg>'''
with open('assets/anime_quote.svg', 'w', encoding='utf-8') as f:
    f.write(anime_quote_svg)

divider_svg = '''<svg width="800" height="30" viewBox="0 0 800 30" xmlns="http://www.w3.org/2000/svg">
    <style>
        @keyframes pan {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        .track { fill: rgba(255, 255, 255, 0.05); }
        .bar { fill: url(#glow); animation: pan 3s cubic-bezier(0.65, 0, 0.35, 1) infinite; }
    </style>
    <defs>
        <linearGradient id="glow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="transparent" />
            <stop offset="50%" stop-color="#00FFFF" />
            <stop offset="100%" stop-color="transparent" />
        </linearGradient>
    </defs>
    <rect class="track" width="800" height="2" y="14" rx="1" />
    <mask id="bar-mask">
        <rect width="800" height="2" y="14" rx="1" fill="white" />
    </mask>
    <g mask="url(#bar-mask)">
        <rect class="bar" width="800" height="2" y="14" rx="1" />
    </g>
</svg>'''
with open('assets/divider.svg', 'w', encoding='utf-8') as f:
    f.write(divider_svg)

print('Animations generated.')
