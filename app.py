import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 18: Adada", page_icon="🚑", layout="centered")

# --- CSS 美化 (醫療綠) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #E0F2F1 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #009688;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #00796B; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #E0F2F1;
        border-left: 5px solid #4DB6AC;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #B2DFDB; color: #00695C; border: 2px solid #009688; padding: 12px;
    }
    .stButton>button:hover { background-color: #80CBC4; border-color: #00796B; }
    .stProgress > div > div > div > div { background-color: #009688; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 18) ---
vocab_data = [
    {"amis": "Adada", "chi": "痛 / 生病", "icon": "🤕", "source": "Row 273"},
    {"amis": "Fongoh", "chi": "頭", "icon": "🤯", "source": "Unit 1"},
    {"amis": "Tiya'", "chi": "肚子", "icon": "🤰", "source": "Unit 1"},
    {"amis": "Mata", "chi": "眼睛", "icon": "👁️", "source": "Unit 1"},
    {"amis": "Walis", "chi": "牙齒", "icon": "🦷", "source": "Unit 1"},
    {"amis": "Pipaisingan", "chi": "醫院", "icon": "🏥", "source": "Row 273"},
    {"amis": "Ising", "chi": "醫生", "icon": "👨‍⚕️", "source": "Row 273"},
    {"amis": "Sapaiyo", "chi": "藥", "icon": "💊", "source": "Row 3804"},
    {"amis": "Mangiha'", "chi": "牙痛 / 呻吟", "icon": "😖", "source": "Row 5119"},
    {"amis": "Malo'", "chi": "累", "icon": "😫", "source": "Row 245 (Var)"},
]

sentences = [
    {"amis": "Adada ko fongoh.", "chi": "頭痛。", "icon": "🤯", "source": "Adada + Fongoh"},
    {"amis": "Adada ko tiya'.", "chi": "肚子痛。", "icon": "🤰", "source": "Adada + Tiya'"},
    {"amis": "Tayra i pipaisingan.", "chi": "去醫院。", "icon": "🏥", "source": "Row 273 (Modified)"},
    {"amis": "Mangiha' ko wawa.", "chi": "小孩在呻吟(牙痛)。", "icon": "🦷", "source": "Row 5119"},
    {"amis": "Komomaen to sapaiyo.", "chi": "吃藥。", "icon": "💊", "source": "Komaen + Sapaiyo"},
]

# --- 3. 隨機題庫 (定義) ---
raw_quiz_pool = [
    {
        "q": "Adada ko fongoh.",
        "audio": "Adada ko fongoh",
        "options": ["頭痛", "肚子痛", "牙齒痛"],
        "ans": "頭痛",
        "hint": "Fongoh 是頭"
    },
    {
        "q": "Adada ko tiya'.",
        "audio": "Adada ko tiya'",
        "options": ["肚子痛", "眼睛痛", "腳痛"],
        "ans": "肚子痛",
        "hint": "Tiya' 是肚子"
    },
    {
        "q": "Tayra i pipaisingan.",
        "audio": "Tayra i pipaisingan",
        "options": ["去醫院", "去學校", "去市場"],
        "ans": "去醫院",
        "hint": "Pipaisingan 是醫院 (看醫生的地方)"
    },
    {
        "q": "單字測驗：Sapaiyo",
        "audio": "Sapaiyo",
        "options": ["藥", "醫生", "痛"],
        "ans": "藥",
        "hint": "生病要吃 Sapaiyo"
    },
    {
        "q": "單字測驗：Ising",
        "audio": "Ising",
        "options": ["醫生", "老師", "學生"],
        "ans": "醫生",
        "hint": "在醫院工作的人"
    },
    {
        "q": "Mangiha' ko wawa.",
        "audio": "Mangiha' ko wawa",
        "options": ["小孩在呻吟(牙痛)", "小孩在睡覺", "小孩在玩耍"],
        "ans": "小孩在呻吟(牙痛)",
        "hint": "Mangiha' (Row 5119)"
    },
    {
        "q": "「生病/痛」的阿美語怎麼說？",
        "audio": None,
        "options": ["Adada", "Lipahak", "Malo'"],
        "ans": "Adada",
        "hint": "Row 273: Ano adada..."
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #00796B;'>Unit 18: Adada</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>生病與身體狀態 (Health)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #00695C;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #B2DFDB; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #00695C;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會表達身體不舒服了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
