import streamlit as st
import time

# Page Config for that "Pastel" look
st.set_page_config(page_title="Mindbloom", page_icon="🌱")

# Custom "Pure Python" Styling (No CSS files!)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FFF2F2 0%, #E5E0FF 50%, #D7E5CA 100%);
    }
    .main-title {
        color: #5A639C;
        font-family: 'Helvetica';
        text-align: center;
        font-size: 50px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Mindbloom</p>', unsafe_allow_html=True)
st.write("---")

# Session State for Gamification
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1

# Layout
col1, col2 = st.columns(2)
with col1:
    st.metric("Level", st.session_state.level)
with col2:
    st.metric("XP", f"{st.session_state.xp}/100")

# Progress Bar
st.progress(st.session_state.xp / 100)

if st.button("✨ Click to Bloom ✨"):
    st.session_state.xp += 20
    if st.session_state.xp >= 100:
        st.session_state.xp = 0
        st.session_state.level += 1
        st.balloons() # THE WOW FACTOR!
        st.success(f"LEVEL UP! You are now Level {st.session_state.level}!")
    else:
        st.toast("Nurturing your mind...")

st.info("A pure Python digital garden. Click the button to grow.")
