import os
import sys
import re
import streamlit as st

# Ensure project root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agent.agent import run_bot

# Streamlit UI config
st.set_page_config(page_title="Duke Chatbot", layout="wide")

st.markdown("""
    <style>
    /* Global app styling */
    body, .stApp {
        background-color: #f5f5f5;
        font-family: 'Georgia', serif;
        color: #012169;
    }

    /* Header banner styled like Duke.edu */
    .duke-header {
        background-color: #012169;
        padding: 1.5rem 2rem;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        letter-spacing: 0.5px;
        text-align: left;
        margin-bottom: 2rem;
        border-bottom: 4px solid #00539B;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc;
        border-radius: 4px;
    }

    .stTextInput label {
        color: #012169 !important;
        font-weight: bold;
    }

    /* Button styling */
    .stButton>button {
        background-color: #012169 !important;
        color: white !important;
        border-radius: 6px;
        font-weight: bold;
        padding: 10px 20px;
        font-size: 1rem;
        border: none;
    }

    .stButton>button:hover {
        background-color: #2541a2 !important;
    }

    /* Alert or response styling */
    .stAlert {
        background-color: #e0eafc !important;
        color: #012169 !important;
        border-left: 6px solid #00539B !important;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 1rem;
    }

    .stAlert > div {
        font-size: 1.05rem !important;
        color: #012169 !important;
    }

    /* Markdown defaults */
    .stMarkdown, .element-container:has(.stAlert) * {
        font-size: 1.05rem !important;
        color: #012169 !important;
    }

    /* Hide Streamlit footer and menu */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="duke-header">Duke Chatbot</div>', unsafe_allow_html=True)

st.markdown("<h1>Duke Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h3>Ask Me Anything About Duke</h3>", unsafe_allow_html=True)

user_input = st.text_input("Ask me a question:")

if user_input:
    with st.spinner("Thinking..."):
        full_response = run_bot(user_input)

        match = re.search(r'Final Answer.*?:\s*(.*)', full_response, re.DOTALL)
        if match:
            response = match.group(1).strip()
        else:
            obs_match = re.search(r'Observation:\s*(.*?)(?:\n[A-Z]|$)', full_response, re.DOTALL)
            response = obs_match.group(1).strip() if obs_match else full_response.strip()

        st.success(response)

if st.button("Reset"):
    st.session_state.clear()
    st.experimental_rerun()
