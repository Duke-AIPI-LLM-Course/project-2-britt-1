import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import re
from agent.agent import run_bot
import streamlit as st


st.set_page_config(page_title="Duke Chatbot", layout="wide")
st.title("Ask Me Anything About Duke!")

st.markdown("""
    <style>
    body {
        background-color: #e8edf4;
        color: #000000;
        font-family: 'Georgia', serif;
    }
    .stApp {
        background-color: #e8edf4;
    }
    .stTextInput input {
        background-color: #ffffff;
        color: #000000;
        border-radius: 8px;
        padding: 10px;
    }
    .stTextInput label {
        color: #000000;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #012169;
        color: white;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2541a2;
        color: white;
    }
    .stMarkdown, .stSuccess {
        color: #000000;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

user_input = st.text_input("Ask me a question:")

if user_input:
    with st.spinner("Thinking..."):
        full_response = run_bot(user_input)

        final_answer_match = re.search(
            r'Action:\s*\{\s*"action"\s*:\s*"Final Answer"\s*,\s*"action_input"\s*:\s*"([^"]+)"\s*\}',
            full_response,
            re.DOTALL
        )

        if final_answer_match:
            response = final_answer_match.group(1).strip()
        elif "Final Answer:" in full_response:
            response = full_response.split("Final Answer:")[-1].strip()
        else:
            response = full_response.strip()

        st.success(response)

if st.button("Reset"):
    st.session_state.clear()
    st.experimental_rerun()