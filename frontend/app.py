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

st.set_page_config(page_title="Duke Chatbot", layout="wide")

st.markdown("""
    <style>
    body, .stApp {
        background-color: #e8edf4;
        color: #000000;
        font-family: 'Georgia', serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stTextInput label {
        color: #000000 !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #012169 !important;
        color: white !important;
        border-radius: 6px;
        font-weight: bold;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #2541a2 !important;
    }
    .stMarkdown p {
        color: #000000 !important;
    }
    .stSpinner {
        background-color: #012169 !important;
    }
    .stSpinner::after {
        border-color: #012169 transparent transparent !important;
    }
""", unsafe_allow_html=True)


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
            # fallback to show first observation if parsing fails
            obs_match = re.search(r'Observation:\s*(.*?)(?:\n[A-Z]|$)', full_response, re.DOTALL)
            response = obs_match.group(1).strip() if obs_match else full_response.strip()

        st.success(response)

if st.button("Reset"):
    st.session_state.clear()
    st.experimental_rerun()
