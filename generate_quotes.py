import os

quotes = [
    {
        "text": '"If you dont take risks, you cant create a future."',
        "author": "> Monkey D. Luffy (One Piece)"
    },
    {
        "text": '"Stand up and walk. Keep moving forward. Youve got two good legs."',
        "author": "> Edward Elric (Fullmetal Alchemist)"
    },
    {
        "text": '"There is no such thing as perfect... but we must still strive for it."',
        "author": "> Mayuri Kurotsuchi (Bleach)"
    },
    {
        "text": '"The ticket to the future is always open."',
        "author": "> Vash the Stampede (Trigun)"
    },
    {
        "text": '"Simplicity is the easiest path to true beauty."',
        "author": "> Seishuu Handa (Barakamon)"
    }
]

def get_animate_tags(index, total):
    segment = 1.0 / total
    start = index * segment
    fade_in_end = start + (segment * 0.15)
    hold_end = start + (segment * 0.85)
    fade_out_end = start + segment
    
    keyTimes = []
    values = []
    
    if index == 0:
        values = ["0", "1", "1", "0", "0"]
        keyTimes = ["0", f"{fade_in_end:.3f}", f"{hold_end:.3f}", f"{fade_out_end:.3f}", "1"]
    else:
        values = ["0", "0", "1", "1", "0", "0"]
        keyTimes = ["0", f"{start:.3f}", f"{fade_in_end:.3f}", f"{hold_end:.3f}", f"{fade_out_end:.3f}", "1"]
        if index == total - 1:
            values = ["0", "0", "1", "1", "0"]
            keyTimes = ["0", f"{start:.3f}", f"{fade_in_end:.3f}", f"{hold_end:.3f}", "1"]
            
    return f'<animate attributeName="opacity" values="{";".join(values)}" keyTimes="{";".join(keyTimes)}" dur="25s" repeatCount="indefinite" />'

svg_content = """<svg width="800" height="120" viewBox="0 0 800 120" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="120" rx="10" fill="#0D1117" stroke="#00FFFF" stroke-width="1">
        <animate attributeName="stroke" values="#00FFFF;#FF00FF;#00FFFF" dur="10s" repeatCount="indefinite" />
    </rect>
    <circle cx="740" cy="60" r="25" fill="none" stroke="#FF00FF" stroke-width="2" stroke-dasharray="4 4">
        <animateTransform attributeName="transform" type="rotate" from="0 740 60" to="360 740 60" dur="20s" repeatCount="indefinite" />
    </circle>
    <circle cx="740" cy="60" r="15" fill="none" stroke="#00FFFF" stroke-width="1">
        <animate attributeName="r" values="12;16;12" dur="4s" repeatCount="indefinite" />
    </circle>
    <circle cx="740" cy="60" r="5" fill="#FF00FF">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite" />
    </circle>
    <line x1="600" y1="20" x2="650" y2="20" stroke="#00FFFF" stroke-width="2"/>
    <line x1="600" y1="100" x2="700" y2="100" stroke="#FF00FF" stroke-width="2"/>
"""

for i, q in enumerate(quotes):
    anim = get_animate_tags(i, len(quotes))
    text = q['text'].replace("dont", "don't").replace("cant", "can't").replace("Youve", "You've")
    author = q['author']
    svg_content += f'''
    <g opacity="0">
        {anim}
        <text x="40" y="55" font-family="Courier New, monospace" font-size="16" fill="#00FFFF" font-style="italic">{text}</text>
        <text x="40" y="90" font-family="Courier New, monospace" font-size="14" fill="#FF00FF" font-weight="bold">{author}</text>
    </g>
'''

svg_content += '</svg>'

with open('assets/anime_quote.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)
