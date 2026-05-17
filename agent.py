from dotenv import load_dotenv
import json
import datetime
import os
import streamlit as st
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import cast

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediBot — Symptom Advisor",
    page_icon="🩺",
    layout="centered",
)

# ── Config ────────────────────────────────────────────────────────────────────
LOG_FILE = "feedback_log.json"

SYSTEM_PROMPT = """You are MediBot, a compassionate AI medical symptom advisor.

Your role:
- Help users understand possible causes of their symptoms
- Give practical, actionable advice (including OTC medicine options where relevant)
- Always recommend when to see a doctor

Response structure:
1. EMPATHY — one sentence acknowledging how they feel
2. POSSIBLE CAUSES — 2-3 brief possibilities
3. HOME CARE / OTC OPTIONS — if user asks about medicine, lead with
   common safe over-the-counter options, THEN add safety notes
4. SEE A DOCTOR IF — clear, specific warning signs

Rules:
- Keep responses under 160 words
- Never make a definitive diagnosis
- Use plain, friendly language

End every response with:
⚕️ This is educational information only — consult a doctor or pharmacist for personal advice."""

load_dotenv()  # Load environment variables from .env file
# ── Groq client (free) ───────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

# ── Logging ───────────────────────────────────────────────────────────────────
def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_log(user_input, agent_response, feedback):
    logs = load_logs()
    logs.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "user_input": user_input,
        "agent_response": agent_response,
        "feedback": feedback,
    })
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

# ── LLM call ──────────────────────────────────────────────────────────────────
def run_agent(user_input, history):
    client = get_client()
    messages: list[ChatCompletionMessageParam] = [
        cast(ChatCompletionMessageParam, {"role": "system", "content": SYSTEM_PROMPT})
    ]
    messages.extend(cast(list[ChatCompletionMessageParam], history))
    messages.append(cast(ChatCompletionMessageParam, {"role": "user", "content": user_input}))
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        if not getattr(response, "choices", None):
            return "⚠️ Error: no response choices returned."
        choice = response.choices[0]
        message = getattr(choice, "message", None)
        if message is None:
            return "⚠️ Error: no message returned from the model."
        content = getattr(message, "content", None)
        if content is None:
            return "⚠️ Error: no content returned from the model."
        return content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # {role, content}
if "pending_feedback" not in st.session_state:
    st.session_state.pending_feedback = None  # {user_input, agent_response}
if "history" not in st.session_state:
    st.session_state.history = []           # for LLM context

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.disclaimer-box {
    background: #fff8e1;
    border-left: 4px solid #f59e0b;
    padding: 10px 14px;
    border-radius: 6px;
    font-size: 13px;
    color: #92400e;
    margin-bottom: 1rem;
}
.stat-label { font-size: 13px; color: #6b7280; }
.stat-value { font-size: 22px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 8])
with col1:
    st.markdown("## 🩺")
with col2:
    st.markdown("## MediBot")
    st.caption("AI Medical Symptom Advisor")

st.markdown("""
<div class="disclaimer-box">
⚠️ <strong>Disclaimer:</strong> MediBot is for educational purposes only.
Always consult a qualified healthcare professional for medical advice.
</div>
""", unsafe_allow_html=True)

# ── Stats sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Session Stats")
    logs = load_logs()
    total = len(logs)
    good  = sum(1 for e in logs if e.get("feedback") == "good")
    bad   = sum(1 for e in logs if e.get("feedback") == "bad")
    rate  = round((good / (good + bad)) * 100) if (good + bad) > 0 else 0

    c1, c2 = st.columns(2)
    c1.metric("Total", total)
    c2.metric("👍 Good", good)
    c1.metric("👎 Bad", bad)
    c2.metric("Rate", f"{rate}%")

    st.divider()

    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.pending_feedback = None
        st.rerun()

    if st.button("📋 Run analyze.py"):
        import subprocess
        result = subprocess.run(
            ["python", "analyze.py"],
            capture_output=True, text=True
        )
        st.code(result.stdout or result.stderr)

    st.divider()
    st.markdown("**Quick symptoms:**")
    quick = [
        "I have a headache and fever",
        "My chest hurts when I breathe",
        "I feel dizzy and nauseous",
        "I have a sore throat and cough",
        "My stomach hurts after eating",
    ]
    for q in quick:
        if st.button(q, key=q):
            st.session_state["quick_input"] = q
            st.rerun()

# ── Chat history display ──────────────────────────────────────────────────────
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🩺"):
        st.markdown(msg["content"])

# ── Pending feedback buttons ──────────────────────────────────────────────────
if st.session_state.pending_feedback:
    pf = st.session_state.pending_feedback
    st.markdown("**Was this response helpful?**")
    col_g, col_b, col_skip = st.columns([1, 1, 3])

    with col_g:
        if st.button("👍 Good", key="good_btn", type="primary"):
            save_log(pf["user_input"], pf["agent_response"], "good")
            st.session_state.pending_feedback = None
            st.rerun()

    with col_b:
        if st.button("👎 Bad", key="bad_btn"):
            save_log(pf["user_input"], pf["agent_response"], "bad")
            st.session_state.pending_feedback = None
            st.rerun()

    with col_skip:
        if st.button("Skip", key="skip_btn"):
            save_log(pf["user_input"], pf["agent_response"], "skipped")
            st.session_state.pending_feedback = None
            st.rerun()

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Describe your symptoms...")

# handle quick button click
if "quick_input" in st.session_state:
    user_input = st.session_state.pop("quick_input")

if user_input and not st.session_state.pending_feedback:
    # show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # get agent response with spinner
    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Analyzing symptoms..."):
            response = run_agent(user_input, st.session_state.history)
        st.markdown(response)

    # update history and messages
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": response})

    # keep last 6 exchanges only
    if len(st.session_state.history) > 12:
        st.session_state.history = st.session_state.history[-12:]

    # set pending feedback
    st.session_state.pending_feedback = {
        "user_input": user_input,
        "agent_response": response,
    }
    st.rerun()

elif user_input and st.session_state.pending_feedback:
    st.warning("Please rate the last response before sending a new message.")
