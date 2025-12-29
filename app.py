import os
import time
from dotenv import load_dotenv
import streamlit as st
from utils import get_rashomon_perspectives, yield_rashomon_perspectives

load_dotenv()

st.set_page_config(layout="wide", page_title="The Bias Detective (Rashomon Edition)", page_icon="🕵️")
st.title("The Bias Detective")
st.markdown("*An AI-Powered Interface for Epistemic Diversity*")

st.sidebar.header("Settings")
st.sidebar.write("")
user_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
st.sidebar.caption("Enter your key to unlock real-time AI analysis. Otherwise, the system runs in Demo Mode.")

user_input = st.text_area(
    "Input",
    height=180,
    placeholder="Paste a news snippet or type a historical event (e.g., 'The Discovery of America')..."
)

analyze = st.button("Analyze Perspectives")
env_key = os.getenv("OPENAI_API_KEY", "")
effective_api_key = user_api_key.strip() if user_api_key.strip() else (env_key.strip() if env_key.strip() else None)

if not effective_api_key:
    st.warning("⚠️ **Demo Mode Active:** System is using pre-generated mock data. Enter an API Key in the sidebar for real-time analysis.")

if analyze:
    event = user_input.strip() if user_input.strip() else "the event"
    start_t = time.perf_counter()
    
    results = {}
    with st.status("🔍 Analyzing through 3 Lenses...", expanded=True) as status:
        st.write("✨ Dispatching AI agents to parallel dimensions...")
        for name, text in yield_rashomon_perspectives(event, effective_api_key):
            st.write(f"✅ Applied Lens: **{name}**")
            results[name] = text
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    end_t = time.perf_counter()
    st.session_state["results"] = results
    st.session_state["latency_s"] = end_t - start_t
    st.session_state["last_event"] = event

if "results" in st.session_state:
    st.success(f"⚡ AI Analysis generated in {st.session_state.get('latency_s', 0.0):.2f}s (Concurrent Parallel Execution)")
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown("### :blue[🏛️ The Establishment]")
        st.write(st.session_state["results"].get("The Establishment", ""))
    with col2:
        st.markdown("### :green[💰 Follow the Money]")
        st.write(st.session_state["results"].get("Follow the Money", ""))
    with col3:
        st.markdown("### :violet[🎭 The Subtext]")
        st.write(st.session_state["results"].get("The Subtext", ""))

    st.subheader("Step 2: Sensemaking")
    choice_a = st.selectbox(
        "Which perspective aligns most with your initial view?",
        ["The Establishment", "Follow the Money", "The Subtext"],
        key="sense_a",
    )
    choice_b = st.selectbox(
        "Which perspective challenged you the most?",
        ["The Establishment", "Follow the Money", "The Subtext"],
        key="sense_b",
    )
    if st.button("Synthesize Perspectives"):
        st.write(
            f"Interesting choice! You started with {choice_a} but found {choice_b} most challenging. "
            "This creates a cognitive gap that allows for new insights."
        )
        st.balloons()
