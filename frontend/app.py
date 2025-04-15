import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Duke Chatbot", layout="wide")
st.title("Ask Me Anything About Duke!")

st.markdown("""
<style>
    .main {
        background-color: #e6edf5;
    }
    .stButton>button {
        background-color: #012169;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

user_input = st.text_input("Ask me a question:")

if user_input:
    with st.spinner("Thinking..."):
        response = run_bot(user_input)
        st.success(response)
if st.button("Reset"):
    st.session_state.clear()
    st.experimental_rerun()
