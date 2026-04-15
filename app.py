import streamlit as st
from generator import generate_flashcards
from parser import extract_text
from utils import export_to_csv

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FlashForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --card: #16161f;
    --accent: #c8f135;
    --accent2: #6c63ff;
    --text: #e8e8f0;
    --muted: #6b6b80;
    --border: #2a2a38;
}

html, body, [class*="css"] {
    font-family: 'Space Mono', monospace;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.main { background-color: var(--bg) !important; }
.block-container { padding: 2rem 3rem !important; max-width: 1100px !important; }

.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.8rem;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -2px;
    line-height: 1;
    margin: 0;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.badge {
    display: inline-block;
    background: rgba(200,241,53,0.12);
    color: var(--accent);
    border: 1px solid rgba(200,241,53,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.9rem;
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.8rem;
}

.input-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.5rem;
}

.flashcard {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.8rem 2rem;
    position: relative;
    margin-bottom: 1.2rem;
    transition: border-color 0.2s, transform 0.2s;
}
.flashcard:hover { border-color: var(--accent2); transform: translateY(-2px); }
.card-number {
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.card-q {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1rem;
    line-height: 1.4;
}
.card-a {
    font-size: 0.88rem;
    color: var(--accent);
    line-height: 1.6;
    border-top: 1px solid var(--border);
    padding-top: 0.8rem;
}
.card-tag {
    position: absolute;
    top: 1.2rem;
    right: 1.2rem;
    font-size: 0.65rem;
    background: var(--accent2);
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.quiz-card {
    background: var(--card);
    border: 2px solid var(--accent2);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    min-height: 200px;
}
.quiz-q {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1rem;
    line-height: 1.4;
}
.quiz-a {
    font-size: 0.95rem;
    color: var(--accent);
    padding: 1rem 1.5rem;
    background: rgba(200,241,53,0.07);
    border-radius: 8px;
    margin-top: 1.2rem;
    text-align: left;
    line-height: 1.7;
}
.score-bar {
    background: var(--border);
    border-radius: 20px;
    height: 8px;
    overflow: hidden;
    margin: 1rem 0;
}
.score-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
    border-radius: 20px;
}

.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
    background: var(--card) !important;
    color: var(--text) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: var(--muted) !important;
    border: none !important;
}
.stTabs [aria-selected="true"] { color: var(--accent) !important; }

.stTextArea textarea, .stSelectbox > div > div {
    background: var(--card) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
}

div[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
}
hr { border-color: var(--border) !important; }

.empty-state {
    text-align: center;
    padding: 4rem;
    color: var(--muted);
}
.empty-state .icon { font-size: 3rem; }
.empty-state p { font-family: 'Syne', sans-serif; font-size: 1.1rem; margin-top: 1rem; }
.empty-state small { font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1 class="hero-title">Flash<span>Forge</span> ⚡</h1>
    <p class="hero-sub">AI-Powered Flashcard Generator</p>
    <span class="badge">✦ No API Key · Runs Offline · Pure Python</span>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("flashcards", []),
    ("quiz_index", 0),
    ("show_answer", False),
    ("score", 0),
    ("quiz_done", []),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["⚡ Generate", "📚 Flashcards", "🎯 Quiz Mode"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Generate
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown('<p class="input-label">📄 Input your notes</p>', unsafe_allow_html=True)
        input_mode = st.radio("", ["Paste text", "Upload file"], horizontal=True, label_visibility="collapsed")

        notes_text = ""
        if input_mode == "Paste text":
            notes_text = st.text_area(
                "", height=300,
                placeholder="Paste your study notes here...\n\nExample:\nPhotosynthesis is the process by which plants use sunlight, water and carbon dioxide to produce oxygen and energy in the form of glucose. Chlorophyll is the green pigment in plants that absorbs light energy...",
                label_visibility="collapsed",
            )
        else:
            uploaded = st.file_uploader("", type=["txt", "pdf"], label_visibility="collapsed")
            if uploaded:
                with st.spinner("Extracting text..."):
                    notes_text = extract_text(uploaded)
                if notes_text:
                    word_count = len(notes_text.split())
                    st.success(f"✓ Extracted {word_count} words from {uploaded.name}")
                    with st.expander("Preview extracted text"):
                        st.text(notes_text[:1000] + ("..." if len(notes_text) > 1000 else ""))
                else:
                    st.error("Could not extract text. Try a .txt file instead.")

    with col2:
        st.markdown('<p class="input-label">⚙️ Settings</p>', unsafe_allow_html=True)

        num_cards = st.slider("Number of flashcards", min_value=3, max_value=20, value=8)

        difficulty = st.selectbox(
            "Difficulty level",
            ["Easy — recall", "Medium — understanding", "Hard — analysis"],
        )

        st.markdown("---")
        st.markdown("""
        <div style="font-size:0.78rem; color:#6b6b80; line-height:1.7;">
            <b style="color:#c8f135;">How it works:</b><br>
            ① Extracts key phrases from your notes using RAKE algorithm<br>
            ② Finds the best matching sentence as the answer<br>
            ③ Generates a question using templates
        </div>
        """, unsafe_allow_html=True)

        generate_btn = st.button("⚡ Generate Flashcards", use_container_width=True)

    # ── Generate ──
    if generate_btn:
        if not notes_text.strip():
            st.warning("Please paste or upload some notes first.")
        elif len(notes_text.split()) < 30:
            st.warning("Notes are too short. Please add at least a few paragraphs.")
        else:
            diff_map = {
                "Easy — recall": "easy",
                "Medium — understanding": "medium",
                "Hard — analysis": "hard",
            }

            with st.spinner("🧠 Extracting keyphrases and building flashcards..."):
                cards = generate_flashcards(
                    notes_text,
                    num_cards=num_cards,
                    difficulty=diff_map[difficulty],
                )

            if cards:
                st.session_state.flashcards = cards
                st.session_state.quiz_index = 0
                st.session_state.show_answer = False
                st.session_state.score = 0
                st.session_state.quiz_done = [False] * len(cards)
                st.success(f"✓ Generated {len(cards)} flashcards! Head to the Flashcards tab.")
            else:
                st.error("Could not generate flashcards. Try adding more detailed notes.")

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Flashcards
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    cards = st.session_state.flashcards

    if not cards:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🃏</div>
            <p>No flashcards yet</p>
            <small>Go to the Generate tab and create some!</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Cards", len(cards))
        c2.metric("Quiz Score", f"{st.session_state.score}/{len(cards)}")
        c3.metric("Completed", f"{sum(st.session_state.quiz_done)}/{len(cards)}")

        st.markdown("---")

        csv_data = export_to_csv(cards)
        st.download_button(
            "⬇ Export as CSV",
            data=csv_data,
            file_name="flashcards.csv",
            mime="text/csv",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        for i, card in enumerate(cards):
            st.markdown(f"""
            <div class="flashcard">
                <span class="card-tag">card {i+1:02d}</span>
                <div class="card-number">Question</div>
                <div class="card-q">{card['question']}</div>
                <div class="card-a">▶ {card['answer']}</div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Quiz Mode
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    cards = st.session_state.flashcards

    if not cards:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🎯</div>
            <p>Generate flashcards first!</p>
            <small>Then come back here to test yourself.</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        idx = st.session_state.quiz_index
        total = len(cards)
        answered = sum(st.session_state.quiz_done)
        pct = int((answered / total) * 100)

        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span style="font-size:0.75rem; color:#6b6b80; letter-spacing:2px; text-transform:uppercase;">Progress</span>
            <span style="font-size:0.75rem; color:#c8f135;">{answered}/{total}</span>
        </div>
        <div class="score-bar"><div class="score-fill" style="width:{pct}%"></div></div>
        """, unsafe_allow_html=True)

        if idx < total:
            card = cards[idx]
            answer_html = (
                f'<div class="quiz-a">{card["answer"]}</div>'
                if st.session_state.show_answer else ""
            )
            st.markdown(f"""
            <div class="quiz-card">
                <div style="font-size:0.7rem; color:#6b6b80; letter-spacing:3px; text-transform:uppercase; margin-bottom:1rem;">
                    Card {idx+1} of {total}
                </div>
                <div class="quiz-q">{card['question']}</div>
                {answer_html}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)

            with b1:
                if not st.session_state.show_answer:
                    if st.button("👁 Reveal Answer", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()

            if st.session_state.show_answer:
                with b2:
                    if st.button("✅ Got it!", use_container_width=True):
                        st.session_state.score += 1
                        st.session_state.quiz_done[idx] = True
                        st.session_state.quiz_index += 1
                        st.session_state.show_answer = False
                        st.rerun()
                with b3:
                    if st.button("❌ Missed", use_container_width=True):
                        st.session_state.quiz_done[idx] = True
                        st.session_state.quiz_index += 1
                        st.session_state.show_answer = False
                        st.rerun()

        else:
            # ── Results ──
            score = st.session_state.score
            result_pct = int((score / total) * 100)
            emoji = "🏆" if result_pct >= 80 else "👍" if result_pct >= 50 else "📖"
            msg = (
                "Excellent work! 🎉" if result_pct >= 80
                else "Good effort! Keep studying." if result_pct >= 50
                else "Review your notes and try again!"
            )

            st.markdown(f"""
            <div style="text-align:center; padding:3rem;">
                <div style="font-size:4rem">{emoji}</div>
                <div style="font-family:'Syne',sans-serif; font-size:2.5rem; font-weight:800;
                            color:#e8e8f0; margin:1rem 0;">{score} / {total}</div>
                <div style="font-size:1rem; color:#6b6b80;">{result_pct}% correct</div>
                <div style="font-size:0.9rem; color:#c8f135; margin-top:0.5rem;">{msg}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔄 Restart Quiz", use_container_width=False):
                st.session_state.quiz_index = 0
                st.session_state.show_answer = False
                st.session_state.score = 0
                st.session_state.quiz_done = [False] * total
                st.rerun()
