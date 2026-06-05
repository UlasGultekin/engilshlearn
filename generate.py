import re
import json

def parse_markdown_table(text):
    rows = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
        if line.startswith('| # |') or line.startswith('|:--'):
            continue
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) >= 2:
            rows.append(parts)
    return rows

def create_html(day_num, title, kaliplar, kelimeler, cumleler, aktivite_html):
    html_template = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gün {day_num} - {title}</title>
<style>
:root {{
    --bg-color: #FAFAFA;
    --text-color: #333;
    --heading-color: #2C3E50;
    --primary-color: #3498DB;
    --primary-hover: #2980B9;
    --card-bg: #FFFFFF;
    --shadow: 0 2px 12px rgba(0,0,0,0.08);
    --border-radius: 12px;
}}
[data-theme="dark"] {{
    --bg-color: #1a1a1a;
    --text-color: #f0f0f0;
    --heading-color: #e0e0e0;
    --primary-color: #3498DB;
    --card-bg: #2d2d2d;
    --shadow: 0 2px 12px rgba(0,0,0,0.3);
}}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    padding: 20px;
    transition: background-color 0.3s, color 0.3s;
}}
.container {{
    max-width: 750px;
    margin: 0 auto;
}}
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}}
h1, h2, h3 {{
    color: var(--heading-color);
}}
.theme-toggle {{
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: var(--text-color);
}}
.tabs {{
    display: flex;
    overflow-x: auto;
    border-bottom: 2px solid #ddd;
    margin-bottom: 10px;
}}
.tab {{
    padding: 10px 15px;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    font-weight: bold;
    color: #777;
    white-space: nowrap;
}}
.tab.active {{
    color: var(--primary-color);
    border-bottom-color: var(--primary-color);
}}
.progress-container {{
    height: 4px;
    background: #ddd;
    border-radius: 2px;
    margin-bottom: 20px;
    overflow: hidden;
}}
.progress-bar {{
    height: 100%;
    background: var(--primary-color);
    width: 20%;
    transition: width 0.3s;
}}
.tab-content {{
    display: none;
}}
.tab-content.active {{
    display: block;
    animation: fadeIn 0.3s;
}}
@keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
.card {{
    background: var(--card-bg);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    padding: 20px;
    margin-bottom: 15px;
}}
button {{
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
}}
button:hover {{
    background-color: var(--primary-hover);
}}
button.success {{ background-color: #2ECC71; }}
button.success:hover {{ background-color: #27AE60; }}
button.warning {{ background-color: #E67E22; }}
button.warning:hover {{ background-color: #D35400; }}
button.icon-btn {{
    padding: 5px 10px;
    margin-left: 10px;
}}
.grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}}
@media (max-width: 600px) {{
    .grid-2 {{ grid-template-columns: 1fr; }}
}}
.hidden {{ display: none !important; }}
.sentence-card {{
    text-align: center;
    padding: 40px 20px;
}}
.tr-sentence {{
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 20px;
}}
.en-sentence {{
    font-size: 20px;
    color: var(--primary-color);
    margin-bottom: 20px;
    min-height: 30px;
}}
.action-buttons {{
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
}}
.milestone {{
    text-align: center;
    font-size: 24px;
    color: var(--primary-color);
    margin: 30px 0;
}}
</style>
</head>
<body>
<div class="container">
    <header>
        <h2>Gün {day_num}: {title}</h2>
        <button class="theme-toggle" id="themeToggle" title="Tema Değiştir">🌙</button>
    </header>

    <div class="tabs">
        <div class="tab active" data-target="gramer">📘 Gramer</div>
        <div class="tab" data-target="kelimeler">📝 Kelimeler</div>
        <div class="tab" data-target="kaliplar">💬 Kalıplar</div>
        <div class="tab" data-target="cumleler">✍️ Cümleler</div>
        <div class="tab" data-target="aktivite">✅ Aktivite</div>
    </div>
    
    <div class="progress-container">
        <div class="progress-bar" id="tabProgress" style="width: 20%;"></div>
    </div>

    <!-- 1. GRAMER -->
    <div id="gramer" class="tab-content active">
        <div class="card">
            <h3>Gramer Konusu: {title}</h3>
            <p>Aşağıda bu günün temel kalıpları ve örnekleri yer almaktadır.</p>
            <ul>
"""
    for k in kaliplar[:4]:
        html_template += f"                <li><strong>{k['tr']}</strong> <br> <span style='color: var(--primary-color);'>{k['en']}</span></li>\n"
        
    html_template += """            </ul>
            <div style="margin-top: 20px;">
                <button onclick="switchTab(1)">Anladım, Devam Et →</button>
            </div>
        </div>
    </div>

    <!-- 2. KELİMELER -->
    <div id="kelimeler" class="tab-content">
        <div style="margin-bottom: 15px;">
            <button onclick="toggleAllWords()">Türkçesini Göster/Gizle</button>
        </div>
        <div class="grid-2">
"""
    for i, w in enumerate(kelimeler):
        html_template += f"""            <div class="card word-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>{w['en']}</strong>
                    <button class="icon-btn" onclick="speak(`{w['en']}`)">🔊</button>
                </div>
                <div class="word-tr hidden" style="margin-top: 10px; color: #777;">{w['tr']}</div>
            </div>
"""
    html_template += """        </div>
        <div style="margin-top: 20px;">
            <button onclick="switchTab(2)">Kelimeleri Öğrendim →</button>
        </div>
    </div>

    <!-- 3. KALIPLAR -->
    <div id="kaliplar" class="tab-content">
        <div class="grid-2">
"""
    for i, k in enumerate(kaliplar):
        enc_en = k['en'].replace('`', '\\`')
        html_template += f"""            <div class="card pattern-card">
                <h3 style="margin-top: 0;">{k['tr']}</h3>
                <div class="pattern-en hidden" style="color: var(--primary-color); margin-bottom: 10px;">{k['en']}</div>
                <div style="display: flex; gap: 10px;">
                    <button onclick="togglePattern(this)">Göster/Gizle</button>
                    <button class="icon-btn" onclick="speak(`{enc_en}`)">🔊</button>
                </div>
            </div>
"""
    html_template += """        </div>
        <div style="margin-top: 20px;">
            <button onclick="switchTab(3)">Kalıpları Öğrendim →</button>
        </div>
    </div>

    <!-- 4. CÜMLELER -->
    <div id="cumleler" class="tab-content">
        <div class="card sentence-card" id="sentenceContainer">
            <div style="text-align: left; margin-bottom: 10px; font-weight: bold;">Cümle <span id="sIndex">1</span> / <span id="sTotal">100</span></div>
            <div class="progress-container" style="height: 6px;">
                <div class="progress-bar" id="sentenceProgress" style="width: 1%;"></div>
            </div>
            
            <div id="milestoneMsg" class="milestone hidden"></div>

            <div id="sentenceStudyArea">
                <div class="tr-sentence" id="trSentence">Türkçe cümle burada</div>
                <div class="en-sentence hidden" id="enSentence">English sentence here</div>
                
                <button id="showAnswerBtn" onclick="showAnswer()">Cevabı Göster</button>
                
                <div class="action-buttons hidden" id="answerBtns">
                    <button class="success" onclick="nextSentence(true)">✅ Doğru Bildim</button>
                    <button class="warning" onclick="nextSentence(false)">🔄 Tekrar Et</button>
                </div>
            </div>
        </div>

        <div class="card">
            <h3 style="cursor: pointer; margin: 0;" onclick="toggleWrongList()">Tekrar Listesi (<span id="wrongCount">0</span> cümle) 🔽</h3>
            <div id="wrongListContainer" class="hidden" style="margin-top: 15px;">
                <ul id="wrongList"></ul>
                <button onclick="startWrongListReview()" id="reviewBtn" class="hidden" style="margin-top: 10px;">Tümünü Tekrar Et</button>
            </div>
        </div>
    </div>

    <!-- 5. AKTİVİTE -->
    <div id="aktivite" class="tab-content">
        <div class="card">
            <h3>Günün Aktivitesi</h3>
            <div style="line-height: 1.6; margin-bottom: 20px;">
"""
    act_html = aktivite_html.replace('\n', '<br>')
    html_template += f"""                {act_html}
            </div>
            <label style="display: flex; align-items: center; cursor: pointer; font-size: 18px;">
                <input type="checkbox" style="width: 20px; height: 20px; margin-right: 10px;">
                Tamamladım ✅
            </label>
        </div>
        
        <div class="card" style="text-align: center; font-style: italic; color: var(--primary-color);">
            "Success is the sum of small efforts, repeated day in and day out."
        </div>
    </div>
</div>

<script>
    // Data
    const sentences = {json.dumps(cumleler, ensure_ascii=False)};
    
    // Theme logic
    const themeToggle = document.getElementById('themeToggle');
    let isDark = false;
    themeToggle.addEventListener('click', () => {{
        isDark = !isDark;
        document.body.setAttribute('data-theme', isDark ? 'dark' : 'light');
        themeToggle.textContent = isDark ? '☀️' : '🌙';
    }});

    // Tab logic
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const tabProgress = document.getElementById('tabProgress');
    
    function switchTab(index) {{
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        tabs[index].classList.add('active');
        const target = tabs[index].getAttribute('data-target');
        document.getElementById(target).classList.add('active');
        tabProgress.style.width = ((index + 1) / tabs.length * 100) + '%';
        window.scrollTo(0,0);
    }}

    tabs.forEach((tab, index) => {{
        tab.addEventListener('click', () => switchTab(index));
    }});

    // Words logic
    let wordsVisible = false;
    function toggleAllWords() {{
        wordsVisible = !wordsVisible;
        document.querySelectorAll('.word-tr').forEach(el => {{
            if(wordsVisible) el.classList.remove('hidden');
            else el.classList.add('hidden');
        }});
    }}

    // Patterns logic
    function togglePattern(btn) {{
        const enDiv = btn.parentElement.parentElement.querySelector('.pattern-en');
        enDiv.classList.toggle('hidden');
    }}

    // TTS
    function speak(text) {{
        if ('speechSynthesis' in window) {{
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance);
        }}
    }}

    // Sentences logic
    let currentIndex = 0;
    let wrongSentences = [];
    let isReviewMode = false;
    let currentList = sentences;

    const trEl = document.getElementById('trSentence');
    const enEl = document.getElementById('enSentence');
    const showBtn = document.getElementById('showAnswerBtn');
    const ansBtns = document.getElementById('answerBtns');
    const sIndexEl = document.getElementById('sIndex');
    const sTotalEl = document.getElementById('sTotal');
    const sProgEl = document.getElementById('sentenceProgress');
    const studyArea = document.getElementById('sentenceStudyArea');
    const milestoneMsg = document.getElementById('milestoneMsg');

    function loadSentence() {{
        if (currentIndex >= currentList.length) {{
            studyArea.classList.add('hidden');
            milestoneMsg.classList.remove('hidden');
            milestoneMsg.innerHTML = isReviewMode ? "Tekrar tamamlandı! 🎉<br><br><button onclick='location.reload()'>Başa Dön</button>" : "Tüm cümleler tamamlandı! 🎉";
            return;
        }}
        
        studyArea.classList.remove('hidden');
        milestoneMsg.classList.add('hidden');
        
        trEl.textContent = currentList[currentIndex].tr;
        enEl.textContent = currentList[currentIndex].en;
        enEl.classList.add('hidden');
        showBtn.classList.remove('hidden');
        ansBtns.classList.add('hidden');
        
        sIndexEl.textContent = currentIndex + 1;
        sTotalEl.textContent = currentList.length;
        sProgEl.style.width = ((currentIndex + 1) / currentList.length * 100) + '%';
    }}

    function showAnswer() {{
        enEl.classList.remove('hidden');
        showBtn.classList.add('hidden');
        ansBtns.classList.remove('hidden');
        speak(currentList[currentIndex].en);
    }}

    function nextSentence(knewIt) {{
        if (!knewIt) {{
            if (!isReviewMode) {{
                wrongSentences.push(currentList[currentIndex]);
                updateWrongListUI();
            }} else {{
                wrongSentences.push(currentList[currentIndex]);
            }}
        }}

        currentIndex++;
        
        if (!isReviewMode && currentIndex > 0) {{
            if (currentIndex === 50) {{
                showMilestone("Yarı yoldasın! 🎯");
                return;
            }} else if (currentIndex % 10 === 0 && currentIndex !== currentList.length && currentIndex !== 50) {{
                showMilestone(currentIndex + " cümle tamamlandı! ☕");
                return;
            }}
        }}
        
        loadSentence();
    }}
    
    function showMilestone(msg) {{
        studyArea.classList.add('hidden');
        milestoneMsg.classList.remove('hidden');
        milestoneMsg.innerHTML = msg + '<br><br><button onclick="loadSentence()">Devam Et</button>';
    }}

    function updateWrongListUI() {{
        document.getElementById('wrongCount').textContent = wrongSentences.length;
        const ul = document.getElementById('wrongList');
        ul.innerHTML = '';
        wrongSentences.forEach((s) => {{
            const li = document.createElement('li');
            li.textContent = s.tr + " - " + s.en;
            li.style.marginBottom = "5px";
            ul.appendChild(li);
        }});
        if(wrongSentences.length > 0) document.getElementById('reviewBtn').classList.remove('hidden');
    }}

    function toggleWrongList() {{
        document.getElementById('wrongListContainer').classList.toggle('hidden');
    }}
    
    function startWrongListReview() {{
        if(wrongSentences.length === 0) return;
        isReviewMode = true;
        currentList = [...wrongSentences];
        wrongSentences = []; 
        updateWrongListUI();
        currentIndex = 0;
        document.getElementById('wrongListContainer').classList.add('hidden');
        loadSentence();
    }}

    loadSentence();
</script>
</body>
</html>"""
    return html_template

def process_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    days = re.split(r'## 📘 GÜN \d+:', text)[1:]
    
    for i, day_text in enumerate(days):
        if i >= 6: break
        day_num = i + 1
        
        # title
        title_match = re.search(r'(.+)', day_text)
        title = title_match.group(1).strip() if title_match else ""
        
        # kaliplar
        kalip_match = re.search(r'### 🧱 10 Temel Kalıp(.*?)(?=### 📚)', day_text, re.DOTALL)
        kaliplar = []
        if kalip_match:
            for line in kalip_match.group(1).strip().split('\\n'):
                m = re.match(r'\d+\.\s+(.*?)\s+\((.*?)\)', line.strip())
                if m:
                    kaliplar.append({'en': m.group(1).strip(), 'tr': m.group(2).strip()})
        
        # kelimeler
        kelime_match = re.search(r'### 📚 20 Hedef Kelime(.*?)### 📝', day_text, re.DOTALL)
        kelimeler = []
        if kelime_match:
            table_data = parse_markdown_table(kelime_match.group(1))
            for row in table_data:
                if len(row) >= 3:
                    kelimeler.append({'en': row[1], 'tr': row[2]})
                    
        # cumleler
        cumle_match = re.search(r'### 📝 100 CÜMLE(.*?)### 🎯', day_text, re.DOTALL)
        cumleler = []
        if cumle_match:
            table_data = parse_markdown_table(cumle_match.group(1))
            for row in table_data:
                if len(row) >= 3:
                    cumleler.append({'tr': row[1], 'en': row[2]})
                    
        # aktiviteler
        aktivite_match = re.search(r'### 🎯 GÜN \d+ AKTİVİTELERİ(.*?)---', day_text, re.DOTALL)
        if not aktivite_match:
            aktivite_match = re.search(r'### 🎯 GÜN \d+ AKTİVİTELERİ(.*?)## 📊', day_text, re.DOTALL)
        aktivite = aktivite_match.group(1).strip() if aktivite_match else ""
        
        html_output = create_html(day_num, title, kaliplar, kelimeler, cumleler, aktivite)
        with open(f'd:/ingilizce/gun{day_num}.html', 'w', encoding='utf-8') as out_f:
            out_f.write(html_output)
        print(f'gun{day_num}.html created successfully! Kelimeler: {len(kelimeler)}, Cümleler: {len(cumleler)}')

if __name__ == '__main__':
    process_file('d:/ingilizce/1-6gün.txt')
