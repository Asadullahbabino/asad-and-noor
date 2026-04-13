import re
import json
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove intro names UI
html = re.sub(r'<div class="intro-names">.*?</div>\s*</div>', '</div>', html, flags=re.DOTALL)
html = re.sub(r'<div class="intro-names">.*?</div>\s*</div>\s*<button id="intro-enter-btn"', '<button id="intro-enter-btn"', html, flags=re.DOTALL)

# 2. Hardcode Names
html = re.sub(r'(<span class="title-him" id="hero-him-name">)[^<]+(</span>)', r'\g<1>Hamza\g<2>', html)
html = re.sub(r'(<span class="title-her gradient-text" id="hero-her-name">)[^<]+(</span>)', r'\g<1>Nafisa\g<2>', html)
html = re.sub(r'(id="about-name-him".*?>)[^<]+(</h3>)', r'\g<1>Hamza\g<2>', html)
html = re.sub(r'(id="about-name-her".*?>)[^<]+(</h3>)', r'\g<1>Nafisa\g<2>', html)
html = re.sub(r'(class="letter-signature".*?>)[^<]+(</p>)', r'\g<1>Hamza ♥\g<2>', html)

# 3. Clean up JS binding for intro inputs
js_remove_pattern = r'const himInp\s*=\s*document\.getElementById\(\'intro-his-name\'\);.*?\}\);'
html = re.sub(js_remove_pattern, '', html, flags=re.DOTALL)
sync_pattern = r'\[himInp,\s*herInp\].*?\}\);'
html = re.sub(sync_pattern, '', html, flags=re.DOTALL)

# 4. Inject Media
media = json.load(open('media.json', 'r', encoding='utf-8'))
imgs = media['imgs']
vids = media['vids']

imgs_js = "const albumImages = " + json.dumps(imgs) + ";"
vids_js = "const albumVideos = " + json.dumps(vids) + ";"

gallery_init_pattern = r'\(function initGallery\(\)\s*\{.*?\/\* Placeholder cards \*\/'
custom_gallery_init = r"""(function initGallery() {
        const grid = document.getElementById('gallery-grid');
        const upload = document.getElementById('gallery-upload');
        if (!grid) return;

        """ + imgs_js + """
        
        const captions = [
          '"Moments we will never forget." ✨',
          '"In your eyes, I found home." ✨',
          '"A love like ours is rare." 💕',
          '"Every second with you counts." 🌙',
          '"My favourite person, always." 💗',
          '"Where we go, love follows." 🌸',
          '"Written in the stars, you and me." 💝',
          '"Forever is still not enough." 🥀'
        ];
        
        let cardIdx = 0;
        
        albumImages.forEach(img => {
            const caption = captions[cardIdx % captions.length];
            cardIdx++;
            const scene = document.createElement('div');
            scene.className = 'gallery-card-scene';
            scene.innerHTML = `
            <div class="gallery-flip-card">
              <div class="gallery-front">
                <img src="./Album 1/${img}" alt="Memory" loading="lazy" />
                <div class="gallery-front-overlay"></div>
                <button class="gallery-del-btn" aria-label="Remove photo">✕</button>
              </div>
              <div class="gallery-back">
                <div class="gallery-back-heart">♥</div>
                <p class="gallery-back-caption">${caption}</p>
                <p class="gallery-back-num">✦ Memory #${cardIdx} ✦</p>
              </div>
            </div>`;
            
            scene.querySelector('.gallery-del-btn').addEventListener('click', (e) => {
              e.stopPropagation();
              scene.style.opacity = '0';
              scene.style.transform = 'scale(0.85)';
              setTimeout(() => scene.remove(), 420);
            });
            grid.appendChild(scene);
        });
"""
html = re.sub(gallery_init_pattern, custom_gallery_init, html, flags=re.DOTALL)
html = re.sub(r'for\s*\(let i = 0;.+?gallery-placeholder.+?\}\n?', '', html, flags=re.DOTALL)

video_init_pattern = r'const vTitles = \[.*?const fmtDur = [^\n]+;'
custom_video_init = r"""const vTitles = [
          'Our perfect day together 💕', 'This moment, forever ♥',
          'You make me smile always ✨', 'Us, laughing forever 🌹',
          'My favourite memory 💫', 'Where time stood still 🌙',
          'The moment I knew 💗', 'Just us, always 🌸'
        ];
        let vIdx = 0;

        """ + vids_js + """
        
        const fmtDur = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
        
        function createVideoCard(src, title) {
          const vGrid = document.getElementById('video-grid');
          if (!vGrid) return;
          const card = document.createElement('div');
          card.className = 'video-card';
          card.innerHTML = `
            <video class="video-thumb" src="${src}" muted preload="metadata"></video>
            <div class="video-card-overlay"><div class="vc-play-btn">▶</div></div>
            <p class="vc-title">"${title}"</p>
            <span class="vc-duration">--:--</span>
            <button class="vc-delete" aria-label="Remove video">✕</button>
          `;
          const thumb = card.querySelector('.video-thumb');
          const dur = card.querySelector('.vc-duration');
          thumb.addEventListener('loadedmetadata', () => {
            dur.textContent = isFinite(thumb.duration) ? fmtDur(thumb.duration) : '--:--';
            thumb.currentTime = Math.min(1, thumb.duration * 0.1);
          });
          card.querySelector('.vc-delete').addEventListener('click', (e) => {
            e.stopPropagation();
            card.style.opacity = '0'; card.style.transform = 'scale(0.85)';
            setTimeout(() => { card.remove(); updateVCount(); }, 420);
          });
          card.addEventListener('click', (e) => { if (!e.target.classList.contains('vc-delete')) openLightbox(src, title); });
          
          vGrid.appendChild(card);
        }
        
        const vGrid = document.getElementById('video-grid');
        if (vGrid) {
            vGrid.innerHTML = '';
            albumVideos.forEach(vid => {
                const title = vTitles[vIdx % vTitles.length];
                vIdx++;
                createVideoCard(`./Album 1/${vid}`, title);
            });
            updateVCount();
        }
"""
html = re.sub(video_init_pattern, custom_video_init, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated HTML successfully!")
