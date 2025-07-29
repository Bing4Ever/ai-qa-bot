import streamlit as st
from utils import ask_openai
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Chat with OpenAI", page_icon=":robot_face:")
st.title("Chat with OpenAI")

question = st.text_input("Ask a question to OpenAI:")

if question:
    with st.spinner("Getting response from OpenAI..."):
        response = ask_openai(question)
        st.write("Response from OpenAI:")
        st.write(response)