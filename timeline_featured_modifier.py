import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

media = json.load(open('media.json', 'r', encoding='utf-8'))
imgs = media['imgs']
vids = media['vids']

# Timeline images replacement
for i in range(1, 5):
    if i <= len(imgs):
        img_src = f"./Album 1/{imgs[i-1]}"
        tl_pattern = rf'<label for="tl-upload-{i}".+?</label>\s*<input type="file" id="tl-upload-{i}"[^>]+>'
        tl_replace = f'<div class="tl-photo-label"><img class="tl-photo" src="{img_src}" alt="Memory" style="display:block; opacity:1;" /></div>'
        html = re.sub(tl_pattern, tl_replace, html, flags=re.DOTALL)

# Featured Video replacement
if len(vids) > 0:
    fv_src = f"./Album 1/{vids[0]}"
    fv_pattern = r'<label for="featured-video-upload".+?</label>\s*<input type="file" id="featured-video-upload"[^>]+>\s*<video id="featured-video-player"[^>]+></video>'
    fv_replace = f'<video id="featured-video-player" class="featured-video-player active" src="{fv_src}" controls preload="metadata"></video>'
    html = re.sub(fv_pattern, fv_replace, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated timeline and featured video HTML successfully!")
