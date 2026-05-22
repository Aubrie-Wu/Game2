import streamlit as st
import random

# Set page configuration
st.set_page_config(page_title="VocabVibe", page_icon="🧠", layout="centered")

# Custom HTML/CSS styling for a polished UI
st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 10px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .subtitle {
        font-size: 18px;
        color: #555555;
        text-align: center;
        margin-bottom: 30px;
    }
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .word-highlight {
        color: #1E3A8A;
        font-weight: bold;
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Setup the word database
VOCAB_BANK = [
    {
        "word": "Ephemeral",
        "definition": "Lasting for a very short time.",
        "choices": ["Lasting for a very short time.", "Extremely beautiful and delicate.", "Deeply religious.", "Having a huge appetite."]
    },
    {
        "word": "Capricious",
        "definition": "Given to sudden and unaccountable changes of mood or behavior.",
        "choices": ["Strict and orderly.", "Given to sudden and unaccountable changes of mood or behavior.", "Very generous with money.", "Lacking courage."]
    },
    {
        "word": "Meticulous",
        "definition": "Showing great attention to detail; very careful and precise.",
        "choices": ["Lazy and careless.", "Highly aggressive.", "Showing great attention to detail; very careful and precise.", "Deeply sorrowful."]
    },
    {
        "word": "Loquacious",
        "definition": "Tending to talk a great deal; talkative.",
        "choices": ["Silent and reserved.", "Tending to talk a great deal; talkative.", "Easily broken.", "Incredibly wealthy."]
    },
    {
        "word": "Mitigate",
        "definition": "Make less severe, serious, or painful.",
        "choices": ["To make worse.", "To celebrate intensely.", "Make less severe, serious, or painful.", "To copy someone else's work."]
    }
]

# 2. Initialize Streamlit Session States
if "score" not in st.session_state:
    st.session_state.score = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(VOCAB_BANK)
if "answered" not in st.session_state:
    st.session_state.answered = False
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Helper function to fetch a new word
def next_question():
    st.session_state.current_question = random.choice(VOCAB_BANK)
    st.session_state.answered = False
    st.session_state.feedback = ""

# --- UI Header via HTML ---
st.markdown('<div class="main-title">🧠 VocabVibe</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Level up your lexicon and build your ultimate high score!</div>', unsafe_allow_html=True)

# Sidebar Scoreboard
with st.sidebar:
    st.header("🏆 Scoreboard")
    st.metric(label="Total Score", value=st.session_state.score)
    st.metric(label="🔥 Current Streak", value=st.session_state.streak)
    
    st.markdown("---")
    if st.button("🔄 Reset Game", use_container_width=True):
        st.session_state.score = 0
        st.session_state.streak = 0
        next_question()
        st.rerun()

# --- Game Modes Tabs ---
tab1, tab2 = st.tabs(["🧩 Multiple Choice", "✍️ Spelling Bee"])
current = st.session_state.current_question

# TAB 1: Multiple Choice Game
with tab1:
    # Presenting the word inside a custom HTML card
    st.markdown(f"""
        <div class="card">
            What is the correct definition for the word:<br>
            <span class="word-highlight">{current['word']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Render choices as radio buttons
    user_choice = st.radio("Choose wisely:", current["choices"], index=None, key="mc_radio")
    
    if st.button("Submit Answer", disabled=st.session_state.answered, use_container_width=True):
        if user_choice is None:
            st.warning("Please pick an answer option first!")
        else:
            st.session_state.answered = True
            if user_choice == current["definition"]:
                st.session_state.score += 10
                st.session_state.streak += 1
                st.session_state.feedback = "correct"
            else:
                st.session_state.streak = 0
                st.session_state.feedback = "wrong"
                
    # Display Feedback
    if st.session_state.answered:
        if st.session_state.feedback == "correct":
            st.success("🎉 Correct! You earned +10 points.")
        elif st.session_state.feedback == "wrong":
            st.error(f"❌ Incorrect. The correct answer was:\n\n*{current['definition']}*")
            
        if st.button("Next Word ➡️", on_click=next_question, use_container_width=True):
            st.rerun()

# TAB 2: Spelling Challenge Game
with tab2:
    st.markdown(f"""
        <div class="card">
            Identify the word that matches this definition:<br>
            <span class="word-highlight">"{current['definition']}"</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Visual HTML hint element
    st.markdown(f"""
        <small style="color: #666;">💡 Hint: The word starts with <b>'{current['word'][0]}'</b> 
        and spans exactly <b>{len(current['word'])}</b> letters.</small>
    """, unsafe_allow_html=True)
    
    user_spelling = st.text_input("Type your answer here:", key="spelling_input").strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Check Spelling", use_container_width=True):
            if user_spelling.lower() == current["word"].lower():
                st.success(f"🎯 Spot on! The word is **{current['word']}** (+20 points).")
                st.session_state.score += 20
                st.session_state.streak += 1
            else:
                st.error("Not quite right! Check your spelling or try again.")
                st.session_state.streak = 0
                
    with col2:
        if st.button("Skip Word ➡️", key="skip_spelling", on_click=next_question, use_container_width=True):
            st.rerun()
