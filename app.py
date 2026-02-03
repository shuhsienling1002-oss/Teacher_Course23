import streamlit as st
import random
import os
import time

# --- 🛠️ 0. 系統配置 (必須在第一行) ---
st.set_page_config(
    page_title="Foting - 阿美語海洋教室",
    page_icon="🐟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 🎨 1. CSS 美化 (水系主題：海洋藍/溪流青) ---
st.markdown("""
    <style>
    /* 全局字體 */
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    /* 標題樣式 */
    h1 { color: #0277BD; text-align: center; margin-bottom: 0px; }
    .subtitle { text-align: center; color: #455A64; margin-top: 5px; font-size: 18px; }
    .author-tag { text-align: center; color: #00838F; font-weight: bold; margin-bottom: 30px; font-size: 16px; }
    
    /* 單字卡 (水藍色漸層) */
    .word-card {
        background: linear-gradient(135deg, #E1F5FE 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #0288D1; /* 深藍底線 */
        transition: transform 0.2s;
    }
    .word-card:hover { transform: translateY(-5px); }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 24px; font-weight: bold; color: #01579B; margin-bottom: 5px; }
    .chinese-text { font-size: 16px; color: #546E7A; }
    .source-tag { font-size: 12px; color: #90A4AE; text-align: right; font-style: italic; margin-top: 10px;}
    
    /* 句子框 (淺青色背景) */
    .sentence-box {
        background-color: #E0F7FA;
        border-left: 5px solid #00BCD4;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    .sent-amis { font-size: 20px; color: #006064; font-weight: bold; }
    .sent-chi { font-size: 16px; color: #37474F; margin-top: 5px; }

    /* 按鈕樣式 (海洋風格) */
    .stButton>button {
        width: 100%; 
        border-radius: 12px; 
        font-size: 18px; 
        font-weight: 600;
        background-color: #B3E5FC; 
        color: #01579B; 
        border: 2px solid #4FC3F7; 
        padding: 10px;
    }
    .stButton>button:hover { 
        background-color: #81D4FA; 
        border-color: #039BE5; 
        color: #fff;
    }
    
    /* 進度條顏色 */
    .stProgress > div > div > div > div { background-color: #0288D1; }
    </style>
""", unsafe_allow_html=True)

# --- 📂 2. Data Layer (數據層) ---
VOCAB_DATA = [
    {"amis": "Foting", "chi": "魚", "icon": "🐟", "source": "核心單字", "audio": "foting.m4a"},
    {"amis": "Misalilan", "chi": "用魚網抓來的", "icon": "🕸️", "source": "動作/描述", "audio": "misalilan.m4a"},
    {"amis": "’Aredet", "chi": "味道十足", "icon": "😋", "source": "形容詞", "audio": "aredet.m4a"},
    {"amis": "Tada’anglis", "chi": "魚腥味很濃", "icon": "👃", "source": "形容詞", "audio": "tadaanglis.m4a"},
    {"amis": "’Aloay", "chi": "溪澗的", "icon": "🏞️", "source": "地點", "audio": "aloay.m4a"},
    {"amis": "Riyaray", "chi": "海水的", "icon": "🌊", "source": "地點", "audio": "riyaray.m4a"},
    {"amis": "Mitafokod", "chi": "網魚", "icon": "🎣", "source": "動作", "audio": "mitafokod.m4a"},
]

SENTENCE_DATA = [
    {"amis": "Mifotingan ni wama konini a foting.", "chi": "這些魚是爸爸抓來的。", "icon": "👨", "audio": "sent_01.m4a"},
    {"amis": "O misalilan no kaka ako kona foting.", "chi": "那些魚是我的哥哥用魚網抓來的。", "icon": "🧑", "audio": "sent_02.m4a"},
    {"amis": "Ono ’alo a foting ko kaolahan ni ama.", "chi": "爸爸比較喜歡溪流的魚。", "icon": "🏞️", "audio": "sent_03.m4a"},
    {"amis": "’Aredet ko kohaw no i ’aloay a foting.", "chi": "溪流的魚湯吃起來味道十足。", "icon": "🍲", "audio": "sent_04.m4a"},
    {"amis": "Tada’anglis ko foting no i riyaray.", "chi": "海魚的魚腥味很濃。", "icon": "🌊", "audio": "sent_05.m4a"},
    {"amis": "Mafana’ ci Kacaw a mitafokod to foting.", "chi": "Kacaw 善於網魚。", "icon": "👍", "audio": "sent_06.m4a"},
]

# --- ⚙️ 3. Service Layer (核心邏輯) ---

def safe_rerun():
    """兼容不同版本的 Streamlit 重整指令"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

class ResourceManager:
    """資源管理器：負責安全地讀取檔案"""
    # 若您的 GitHub 資料夾結構不同，請修改這裡
    BASE_AUDIO_PATH = "Teacher_Course22/audio"

    @staticmethod
    def play_audio(filename: str):
        """播放音檔，若檔案不存在則顯示提示"""
        file_path = os.path.join(ResourceManager.BASE_AUDIO_PATH, filename)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format='audio/mp4')
            except Exception as e:
                st.error(f"播放失敗: {e}")
        else:
            # 溫馨提示，不報錯
            st.warning(f"⚠️ 找不到音檔: {filename} (請確認檔案是否已上傳至 {file_path})")

class QuizEngine:
    """題庫生成引擎"""
    @staticmethod
    def generate_quiz(num_questions=4):
        pool = VOCAB_DATA.copy()
        if len(pool) < 4: return []
        
        selected_targets = random.sample(pool, num_questions)
        quiz_set = []
        
        for target in selected_targets:
            answer = target['amis']
            distractors = [w['amis'] for w in pool if w['amis'] != answer]
            wrong_options = random.sample(distractors, 2)
            options = wrong_options + [answer]
            random.shuffle(options)
            
            quiz_set.append({
                "q": f"「{target['chi']}」的阿美語怎麼說？",
                "audio": target['audio'],
                "options": options,
                "ans": answer,
                "hint": f"提示：{target['source']} - {target['icon']}"
            })
        return quiz_set

# --- 📱 4. Presentation Layer (UI 介面) ---

def main():
    # 標題區 (已更新講師資訊)
    st.markdown("<h1 style='text-align: center;'>🐟 Foting 魚的世界</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>阿美語海洋教室 | 主題：捕魚與飲食文化</div>", unsafe_allow_html=True)
    st.markdown("<div class='author-tag'>講師：高春美 | 教材提供者：高春美</div>", unsafe_allow_html=True)

    # 初始化 Session State
    if 'init' not in st.session_state:
        st.session_state.score = 0
        st.session_state.current_q_idx = 0
        st.session_state.quiz_questions = QuizEngine.generate_quiz()
        st.session_state.init = True

    # 分頁導航
    tab1, tab2 = st.tabs(["📖 學習單字與句型", "🎲 隨機挑戰"])

    # === Tab 1: 學習模式 ===
    with tab1:
        st.subheader("📝 核心單字 (Vocabulary)")
        col1, col2 = st.columns(2)
        for i, word in enumerate(VOCAB_DATA):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                <div class="word-card">
                    <div class="emoji-icon">{word['icon']}</div>
                    <div class="amis-text">{word['amis']}</div>
                    <div class="chinese-text">{word['chi']}</div>
                    <div class="source-tag">{word['source']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🔊 播放", key=f"btn_vocab_{i}"):
                    ResourceManager.play_audio(word['audio'])

        st.markdown("---")
        st.subheader("🗣️ 實用句型 (Sentences)")
        for i, sent in enumerate(SENTENCE_DATA):
            st.markdown(f"""
            <div class="sentence-box">
                <div class="sent-amis">{sent['icon']} {sent['amis']}</div>
                <div class="sent-chi">{sent['chi']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"▶️ 朗讀句子", key=f"btn_sent_{i}"):
                ResourceManager.play_audio(sent['audio'])

    # === Tab 2: 測驗模式 ===
    with tab2:
        st.subheader("🧠 隨機測驗")
        
        questions = st.session_state.quiz_questions
        current_idx = st.session_state.current_q_idx
        
        if current_idx < len(questions):
            q_data = questions[current_idx]
            
            # 進度條
            progress = current_idx / len(questions)
            st.progress(progress)
            
            st.markdown(f"### Q{current_idx + 1}: {q_data['q']}")
            
            if st.button("🔊 聽聽看", key=f"quiz_audio_{current_idx}"):
                ResourceManager.play_audio(q_data['audio'])
            
            # 選項區
            cols = st.columns(len(q_data['options']))
            if f"answered_{current_idx}" not in st.session_state:
                for idx, opt in enumerate(q_data['options']):
                    if cols[idx].button(opt, key=f"opt_{current_idx}_{idx}"):
                        if opt == q_data['ans']:
                            st.success(f"🎉 正確！ {q_data['ans']}")
                            st.session_state.score += 25
                        else:
                            st.error(f"❌ 答錯了，正確答案是：{q_data['ans']}")
                            st.info(q_data['hint'])
                        
                        st.session_state[f"answered_{current_idx}"] = True
                        time.sleep(1.5)
                        st.session_state.current_q_idx += 1
                        safe_rerun()
            else:
                st.info("載入下一題中...")
                
        else:
            # 結算畫面
            st.progress(1.0)
            st.balloons()
            final_score = st.session_state.score
            
            st.markdown(f"""
            <div style="text-align: center; padding: 30px; background-color: #E1F5FE; border-radius: 20px; border: 2px solid #0288D1;">
                <h2 style="color: #01579B;">測驗完成！</h2>
                <h1 style="font-size: 60px; color: #0277BD;">{final_score} 分</h1>
                <p>Mafana’ kiso to foting! (你很懂魚喔！)</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 再玩一次"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                safe_rerun()

# --- 程式入口點 ---
if __name__ == "__main__":
    main()
