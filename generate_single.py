import re
import json

def parse_markdown_table(text):
    rows = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
        if line.startswith('| # |') or line.startswith('|:--') or line.startswith('| Gün |'):
            continue
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) >= 2:
            rows.append(parts)
    return rows

def process_files(input_paths):
    text = ""
    for input_path in input_paths:
        with open(input_path, 'r', encoding='utf-8') as f:
            text += f.read() + "\n"

    days_raw = re.split(r'## 📘 GÜN \d+:', text)[1:]
    
    grammar_table_match = re.search(r'## 🎯 GENEL GRAMER ODAKLARI.*?\n(.*?)(?=\n---)', text, re.DOTALL)
    grammar_info = {}
    if grammar_table_match:
        gt = parse_markdown_table(grammar_table_match.group(1))
        for row in gt:
            if len(row) >= 3:
                day_key = row[0].replace('**', '').strip()
                grammar_info[day_key] = row[2]

    all_days_data = []

    for i, day_text in enumerate(days_raw):
        day_num = str(i + 1)
        
        title_match = re.search(r'(.+)', day_text)
        title = title_match.group(1).strip() if title_match else ""
        
        kalip_match = re.search(r'### 🧱 10 Temel Kalıp(.*?)(?=### 📚)', day_text, re.DOTALL)
        kaliplar = []
        if kalip_match:
            for line in kalip_match.group(1).strip().split('\n'):
                m = re.match(r'\d+\.\s+(.*?)\s+\((.*?)\)', line.strip())
                if m:
                    kaliplar.append({'en': m.group(1).strip(), 'tr': m.group(2).strip()})
        
        kelime_match = re.search(r'### 📚 20 Hedef Kelime(.*?)### 📝', day_text, re.DOTALL)
        kelimeler = []
        if kelime_match:
            table_data = parse_markdown_table(kelime_match.group(1))
            for row in table_data:
                if len(row) >= 3:
                    ex = row[3] if len(row) >= 4 else ""
                    kelimeler.append({'en': row[1], 'tr': row[2], 'ex': ex})
                    
        cumle_match = re.search(r'### 📝 100 CÜMLE(.*?)### 🎯', day_text, re.DOTALL)
        cumleler = []
        if cumle_match:
            table_data = parse_markdown_table(cumle_match.group(1))
            for row in table_data:
                if len(row) >= 3:
                    cumleler.append({'tr': row[1], 'en': row[2]})
                    
        aktivite_match = re.search(r'### 🎯 GÜN \d+ AKTİVİTELERİ(.*?)---', day_text, re.DOTALL)
        if not aktivite_match:
            aktivite_match = re.search(r'### 🎯 GÜN \d+ AKTİVİTELERİ(.*?)## 📊', day_text, re.DOTALL)
        aktivite = aktivite_match.group(1).strip() if aktivite_match else ""
        
        gramer_desc = grammar_info.get(day_num, "Bu günün gramer yapısını çalışacağız.")
        
        all_days_data.append({
            'dayNum': day_num,
            'title': title,
            'gramerDesc': gramer_desc,
            'kaliplar': kaliplar,
            'kelimeler': kelimeler,
            'cumleler': cumleler,
            'aktivite': aktivite.replace('\n', '<br>')
        })

    html_template = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>İngilizce Çalışma - 72 Günlük Kapsamlı Program (FİNAL)</title>
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
    flex-wrap: wrap;
    gap: 15px;
}}
h1, h2, h3 {{
    color: var(--heading-color);
}}
.day-selector {{
    padding: 8px 12px;
    font-size: 16px;
    border-radius: 8px;
    border: 1px solid #ccc;
    background-color: var(--card-bg);
    color: var(--text-color);
    cursor: pointer;
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
    margin-bottom: 5px;
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
    position: relative;
}}
.progress-bar {{
    height: 100%;
    background: var(--primary-color);
    width: 20%;
    transition: width 0.3s;
}}
#tabProgressText {{
    text-align: right;
    font-size: 12px;
    color: #888;
    margin-bottom: 10px;
    font-weight: bold;
}}
.tab-content {{
    display: none;
}}
.tab-content.active {{
    display: block;
    animation: fadeIn 0.3s;
}}
@keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
.fade-in-anim {{
    animation: fadeIn 0.8s ease-in-out forwards;
}}
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
    transition: background 0.3s, transform 0.1s;
}}
button:hover {{
    background-color: var(--primary-hover);
}}
button:active {{
    transform: scale(0.98);
}}
button.success {{ background-color: #2ECC71; }}
button.success:hover {{ background-color: #27AE60; }}
button.warning {{ background-color: #E67E22; }}
button.warning:hover {{ background-color: #D35400; }}
button.icon-btn {{
    padding: 5px 10px;
    margin-left: 10px;
}}
button.selected {{
    box-shadow: 0 0 0 4px rgba(0,0,0,0.2);
    transform: scale(1.05);
}}
.grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}}
.gramer-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-top: 15px;
}}
.gramer-cell {{
    padding: 10px;
    background: var(--bg-color);
    border-radius: 8px;
    border-left: 4px solid var(--primary-color);
}}
.gramer-cell-en {{
    border-left-color: #2ECC71;
    color: var(--primary-color);
    font-weight: 500;
}}
@media (max-width: 600px) {{
    .grid-2, .gramer-grid {{ grid-template-columns: 1fr; }}
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
    gap: 15px;
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
        <div style="display: flex; align-items: center; gap: 15px;">
            <h2 style="margin:0;" id="dayTitle">Gün Seçiniz</h2>
            <select id="daySelector" class="day-selector">
                {chr(10).join(f'<option value="{j}">Gün {j+1}</option>' for j in range(len(all_days_data)))}
            </select>
        </div>
        <button class="theme-toggle" id="themeToggle" title="Tema Değiştir">🌙</button>
    </header>

    <div class="tabs">
        <div class="tab active" data-target="gramer">📘 Gramer</div>
        <div class="tab" data-target="kelimeler">📝 Kelimeler</div>
        <div class="tab" data-target="kaliplar">💬 Kalıplar</div>
        <div class="tab" data-target="cumleler">✍️ Cümleler</div>
        <div class="tab" data-target="aktivite">✅ Aktivite</div>
    </div>
    
    <div id="tabProgressText">1/5</div>
    <div class="progress-container">
        <div class="progress-bar" id="tabProgress" style="width: 20%;"></div>
    </div>

    <!-- 1. GRAMER -->
    <div id="gramer" class="tab-content active">
        <div class="card">
            <h3 id="gramerTitle">Gramer Konusu</h3>
            <p id="gramerDesc"></p>
            
            <h4 style="margin-top: 20px; margin-bottom: 10px;">Örnek Cümleler:</h4>
            <div class="gramer-grid" id="gramerGrid">
                <!-- Gramer examples generated via JS -->
            </div>
            
            <div style="margin-top: 30px; text-align: center;">
                <button onclick="switchTab(1)" style="width:100%; padding: 15px; font-size:18px;">Anladım, Devam Et →</button>
            </div>
        </div>
    </div>

    <!-- 2. KELİMELER -->
    <div id="kelimeler" class="tab-content">
        <div style="margin-bottom: 15px; display: flex; justify-content: flex-end;">
            <button onclick="toggleAllWords()">Türkçesini Göster/Gizle</button>
        </div>
        <div class="grid-2" id="wordsContainer">
        </div>
        <div style="margin-top: 30px; text-align: center;">
            <button onclick="switchTab(2)" style="width:100%; padding: 15px; font-size:18px;">Kelimeleri Öğrendim →</button>
        </div>
    </div>

    <!-- 3. KALIPLAR -->
    <div id="kaliplar" class="tab-content">
        <div class="grid-2" id="patternsContainer">
        </div>
        <div style="margin-top: 30px; text-align: center;">
            <button onclick="switchTab(3)" style="width:100%; padding: 15px; font-size:18px;">Kalıpları Öğrendim →</button>
        </div>
    </div>

    <!-- 4. CÜMLELER -->
    <div id="cumleler" class="tab-content">
        <div class="card sentence-card" id="sentenceContainer">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: bold; font-size: 14px;">
                <span>İlerleme:</span>
                <span>Cümle <span id="sIndex">1</span> / <span id="sTotal">100</span></span>
            </div>
            <div class="progress-container" style="height: 6px; margin-bottom: 40px;">
                <div class="progress-bar" id="sentenceProgress" style="width: 1%;"></div>
            </div>
            
            <div id="milestoneMsg" class="milestone hidden"></div>

            <div id="sentenceStudyArea">
                <div class="tr-sentence" id="trSentence">Türkçe cümle burada</div>
                
                <button id="showAnswerBtn" onclick="showAnswer()" style="padding: 15px 30px; font-size:18px; margin-top:20px;">Cevabı Göster</button>
                
                <div class="en-sentence hidden" id="enSentence" style="margin-top:20px;">English sentence here</div>
                
                <div class="action-buttons hidden" id="answerBtns">
                    <button id="btnKnew" class="success" onclick="selectAnswer(true)" style="flex:1;">✅ Doğru Bildim</button>
                    <button id="btnRepeat" class="warning" onclick="selectAnswer(false)" style="flex:1;">🔄 Tekrar Et</button>
                </div>
                
                <button id="nextSentenceBtn" class="hidden" onclick="goToNextSentence()" style="width: 100%; padding: 15px; font-size: 18px; margin-top: 20px; background-color: #2C3E50;">Sonraki Cümle →</button>
            </div>
        </div>

        <div class="card">
            <h3 style="cursor: pointer; margin: 0; display: flex; justify-content: space-between;" onclick="toggleWrongList()">
                <span>Tekrar Listesi (<span id="wrongCount">0</span> cümle)</span>
                <span>🔽</span>
            </h3>
            <div id="wrongListContainer" class="hidden" style="margin-top: 15px;">
                <ul id="wrongList" style="padding-left: 20px; line-height: 1.6;"></ul>
                <button onclick="startWrongListReview()" id="reviewBtn" class="hidden warning" style="margin-top: 15px; width: 100%;">Tümünü Tekrar Et</button>
            </div>
        </div>
    </div>

    <!-- 5. AKTİVİTE -->
    <div id="aktivite" class="tab-content">
        <div class="card">
            <h3 style="margin-top: 0;">Günün Aktivitesi</h3>
            <div style="line-height: 1.6; margin-bottom: 20px; font-size: 16px;" id="activityContainer">
            </div>
            <label style="display: inline-flex; align-items: center; cursor: pointer; font-size: 18px; background: #e8f5e9; padding: 15px 20px; border-radius: 8px; width: 100%; box-sizing: border-box; border: 1px solid #c8e6c9;">
                <input type="checkbox" id="activityCheckbox" style="width: 25px; height: 25px; margin-right: 15px; cursor: pointer;">
                <strong>Tamamladım ✅</strong>
            </label>
        </div>
        
        <div class="card" style="text-align: center; font-style: italic; color: var(--primary-color); font-size: 18px; padding: 30px;">
            "Success is the sum of small efforts, repeated day in and day out."
        </div>
    </div>
</div>

<script>
    const appData = {json.dumps(all_days_data, ensure_ascii=False)};
    
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
    const tabProgressText = document.getElementById('tabProgressText');
    
    function switchTab(index) {{
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        tabs[index].classList.add('active');
        const target = tabs[index].getAttribute('data-target');
        document.getElementById(target).classList.add('active');
        
        let perc = ((index + 1) / tabs.length * 100);
        tabProgress.style.width = perc + '%';
        tabProgressText.textContent = (index + 1) + '/' + tabs.length;
        window.scrollTo(0,0);
    }}

    tabs.forEach((tab, index) => {{
        tab.addEventListener('click', () => switchTab(index));
    }});

    function speak(text) {{
        if ('speechSynthesis' in window) {{
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance);
        }}
    }}

    let wordsVisible = false;
    function toggleAllWords() {{
        wordsVisible = !wordsVisible;
        document.querySelectorAll('.word-tr').forEach(el => {{
            if(wordsVisible) el.classList.remove('hidden');
            else el.classList.add('hidden');
        }});
    }}

    function showPattern(btn) {{
        const enDiv = btn.parentElement.parentElement.querySelector('.pattern-en');
        enDiv.classList.remove('hidden');
        enDiv.classList.add('fade-in-anim');
        btn.style.display = 'none'; // hide the button after revealing
    }}

    // App State
    let currentDayIndex = 0;
    let sentences = [];
    let currentIndex = 0;
    let wrongSentences = [];
    let isReviewMode = false;
    let currentList = [];
    let answerSelection = null; // true for knew, false for repeat

    // Selectors
    const trEl = document.getElementById('trSentence');
    const enEl = document.getElementById('enSentence');
    const showBtn = document.getElementById('showAnswerBtn');
    const ansBtns = document.getElementById('answerBtns');
    const nextBtn = document.getElementById('nextSentenceBtn');
    const btnKnew = document.getElementById('btnKnew');
    const btnRepeat = document.getElementById('btnRepeat');
    
    const sIndexEl = document.getElementById('sIndex');
    const sTotalEl = document.getElementById('sTotal');
    const sProgEl = document.getElementById('sentenceProgress');
    const studyArea = document.getElementById('sentenceStudyArea');
    const milestoneMsg = document.getElementById('milestoneMsg');

    function escapeHtml(unsafe) {{
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }}

    function renderDay(index) {{
        currentDayIndex = index;
        const dayData = appData[index];
        
        document.getElementById('dayTitle').textContent = `Gün ${{dayData.dayNum}}: ${{dayData.title}}`;
        document.getElementById('gramerTitle').textContent = dayData.title;
        document.getElementById('gramerDesc').textContent = dayData.gramerDesc;
        
        // Gramer examples in 2 columns
        let gramerHtml = "";
        dayData.kaliplar.forEach(k => {{
            gramerHtml += `
            <div class="gramer-cell">${{escapeHtml(k.tr)}}</div>
            <div class="gramer-cell gramer-cell-en">${{escapeHtml(k.en)}}</div>
            `;
        }});
        document.getElementById('gramerGrid').innerHTML = gramerHtml;

        // Words
        let wordsHtml = "";
        dayData.kelimeler.forEach(w => {{
            let exHtml = w.ex ? `<div style="font-size:13px; color:#999; margin-top:8px; font-style:italic;">Örn: ${{escapeHtml(w.ex)}}</div>` : "";
            wordsHtml += `
            <div class="card word-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="font-size: 18px;">${{escapeHtml(w.en)}}</strong>
                    <button class="icon-btn" onclick="speak(\`${{w.en.replace(/`/g, '\\`')}}\`)">🔊</button>
                </div>
                <div class="word-tr hidden" style="margin-top: 15px; border-top: 1px dashed #ddd; padding-top: 10px;">
                    <strong style="color: var(--primary-color);">${{escapeHtml(w.tr)}}</strong>
                    ${{exHtml}}
                </div>
            </div>`;
        }});
        document.getElementById('wordsContainer').innerHTML = wordsHtml;
        wordsVisible = false;

        // Patterns
        let patHtml = "";
        dayData.kaliplar.forEach(k => {{
            patHtml += `
            <div class="card pattern-card">
                <h3 style="margin-top: 0; font-size: 20px;">${{escapeHtml(k.tr)}}</h3>
                <div class="pattern-en hidden" style="color: var(--primary-color); margin-bottom: 15px; font-size: 18px; font-weight: 500;">${{escapeHtml(k.en)}}</div>
                <div style="display: flex; gap: 10px;">
                    <button onclick="showPattern(this)">Göster</button>
                    <button class="icon-btn" onclick="speak(\`${{k.en.replace(/`/g, '\\`')}}\`)">🔊</button>
                </div>
            </div>`;
        }});
        document.getElementById('patternsContainer').innerHTML = patHtml;

        // Sentences
        sentences = dayData.cumleler;
        currentList = sentences;
        currentIndex = 0;
        wrongSentences = [];
        isReviewMode = false;
        updateWrongListUI();
        document.getElementById('wrongListContainer').classList.add('hidden');
        loadSentence();

        // Activity
        document.getElementById('activityContainer').innerHTML = dayData.aktivite;
        document.getElementById('activityCheckbox').checked = false;
        
        switchTab(0);
    }}

    function loadSentence() {{
        if (currentIndex >= currentList.length) {{
            studyArea.classList.add('hidden');
            milestoneMsg.classList.remove('hidden');
            milestoneMsg.innerHTML = isReviewMode ? "Tekrar tamamlandı! 🎉<br><br><button onclick='endReview()'>Geri Dön</button>" : "Tüm cümleler tamamlandı! 🎉";
            return;
        }}
        
        studyArea.classList.remove('hidden');
        milestoneMsg.classList.add('hidden');
        
        trEl.textContent = currentList[currentIndex].tr;
        enEl.textContent = currentList[currentIndex].en;
        
        // Reset state
        enEl.classList.add('hidden');
        enEl.classList.remove('fade-in-anim');
        showBtn.classList.remove('hidden');
        ansBtns.classList.add('hidden');
        nextBtn.classList.add('hidden');
        btnKnew.classList.remove('selected');
        btnRepeat.classList.remove('selected');
        answerSelection = null;
        
        sIndexEl.textContent = currentIndex + 1;
        sTotalEl.textContent = currentList.length;
        sProgEl.style.width = ((currentIndex + 1) / currentList.length * 100) + '%';
    }}

    function showAnswer() {{
        showBtn.classList.add('hidden');
        
        enEl.classList.remove('hidden');
        enEl.classList.add('fade-in-anim');
        
        ansBtns.classList.remove('hidden');
        nextBtn.classList.remove('hidden');
        
        speak(currentList[currentIndex].en);
    }}

    function selectAnswer(knewIt) {{
        answerSelection = knewIt;
        if(knewIt) {{
            btnKnew.classList.add('selected');
            btnRepeat.classList.remove('selected');
        }} else {{
            btnRepeat.classList.add('selected');
            btnKnew.classList.remove('selected');
        }}
    }}

    function goToNextSentence() {{
        if (answerSelection === null) {{
            alert("Lütfen önce Doğru Bildim veya Tekrar Et seçeneğini işaretleyin.");
            return;
        }}

        if (!answerSelection) {{
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
                showMilestone("Harika! " + currentIndex + " cümle tamamlandı! ☕");
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
            li.innerHTML = `<strong>${{escapeHtml(s.tr)}}</strong> <br> <span style="color:var(--primary-color);">${{escapeHtml(s.en)}}</span>`;
            li.style.marginBottom = "10px";
            ul.appendChild(li);
        }});
        if(wrongSentences.length > 0) {{
            document.getElementById('reviewBtn').classList.remove('hidden');
        }} else {{
            document.getElementById('reviewBtn').classList.add('hidden');
        }}
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

    function endReview() {{
        isReviewMode = false;
        currentList = sentences;
        currentIndex = currentList.length; // to show the completed screen again
        updateWrongListUI();
        loadSentence();
    }}

    document.getElementById('daySelector').addEventListener('change', (e) => {{
        renderDay(parseInt(e.target.value));
    }});

    // Init first day
    renderDay(0);
</script>
</body>
</html>"""
    
    with open('d:/ingilizce/TEK_DOSYA_ingilizce_uygulamasi.html', 'w', encoding='utf-8') as out_f:
        out_f.write(html_template)
    print("TEK_DOSYA_ingilizce_uygulamasi.html created successfully!")

if __name__ == '__main__':
    process_files(['d:/ingilizce/1-6gün.txt', 'd:/ingilizce/7-12gün.txt', 'd:/ingilizce/13-18gün.txt', 'd:/ingilizce/19-24gün.txt', 'd:/ingilizce/25-30gun.txt', 'd:/ingilizce/31-36gun.txt', 'd:/ingilizce/37-42gün.txt', 'd:/ingilizce/43-48gün.txt', 'd:/ingilizce/49-54gün.txt', 'd:/ingilizce/55-60gün.txt', 'd:/ingilizce/61-66gün.txt', 'd:/ingilizce/67-72gün.txt'])
