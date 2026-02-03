import streamlit as st
import random
import os
import time

# --- \U0001F4C2 1. Data Layer (數據層) ---
# 架構師註記：將數據與邏輯分離。
# 音檔檔名預設為：單字(小寫).m4a，若有特殊檔名可在此手動覆蓋。

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

# --- ⚙️ 2. Service Layer (服務層 - 邏輯引擎) ---

class ResourceManager:
    """處理資源加載與路徑防禦"""
    
    # 設定音檔基礎路徑 (可根據實際部署環境修改)
    BASE_AUDIO_PATH = "Teacher_Course22/audio"

    @staticmethod
    def get_audio_bytes(filename: str):
        """
        安全地讀取音檔。
        Returns: bytes or None
        """
        # 組合路徑
        file_path = os.path.join(ResourceManager.BASE_AUDIO_PATH, filename)
        
        # 防禦性檢查：檔案是否存在？
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, "rb") as f:
                return f.read()
        except Exception as e:
            # 記錄錯誤但不崩潰 (Log error but don't crash)
            print(f"Error reading file {file_path}: {e}")
            return None

class QuizEngine:
    """動態題庫生成器 (Scalability Core)"""
    
    @staticmethod
    def generate_quiz(num_questions=4):
        """
        自動從單字表中生成題目。
        邏輯：隨機選一個單字當答案，再隨機選3個其他單字當錯誤選項。
        """
        pool = VOCAB_DATA.copy()
        # 確保單字量足夠
        if len(pool) < 4:
            return []
            
        selected_targets = random.sample(pool, num_questions)
        quiz_set = []
        
        for target in selected_targets:
            # 正確答案
            answer = target['amis']
            question_text = f"「{target['chi']}」的阿美語怎麼說？"
            
            # 生成干擾項 (Distractors)
            distractors = [w['amis'] for w in pool if w['amis'] != answer]
            wrong_options = random.sample(distractors, 2) # 選2個錯誤答案
            
            # 組合選項並洗牌
            options = wrong_options + [answer]
            random.shuffle(options)
            
            quiz_set.append({
                "q": question_text,
                "audio": target['audio'],
                "options": options,
                "ans": answer,
                "hint": f"提示：{target['source']} - {target['icon']}"
            })
            
        return quiz_set

# --- 邏輯層結束 ---
