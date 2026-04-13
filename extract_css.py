import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
if style_match:
    style_content = style_match.group(1)
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(style_content)
    
    html = html.replace(style_match.group(0), '<link rel="stylesheet" href="style.css">')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("CSS extracted to style.css")
else:
    print("No style tag found.")
