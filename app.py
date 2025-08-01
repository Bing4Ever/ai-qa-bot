import streamlit as st
from pathlib import Path
from utils import ask_openai
from promp import ROLE_PROMPT
from message import Message

DATA_FILE = Path("data/user_log.json")
MAX_QUESTIONS_PER_DAY = 5

st.set_page_config(
    page_title="Chat with OpenAI", 
    page_icon="🤖",
    layout="centered")

st.title("Chat with OpenAI")
st.markdown("Welcome to the OpenAI Chatbot! Ask me anything and I'll do my best to provide a helpful response.")
role = st.selectbox("Select Role", list(ROLE_PROMPT.keys()))
system_prompt = ROLE_PROMPT[role]

if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("----------------")
st.markdown("### Chat History")

for msg in st.session_state.messages:
    message = msg.message
    if message["role"] == "user":
        st.write(f"**[{msg.system_prompt}] You Ask:** {message['content']}")
    else:
        st.write(f"**[{msg.system_prompt}] OpenAI Responds:** {message['content']}")
    
st.markdown("----------------")

question = st.text_input("Ask a question to OpenAI:", placeholder="Type your question here...")

if st.button("Submit") and question.strip() != "":
    st.session_state.messages.append(Message({
            "role": "user",
            "content": question
        }, role))
    
    with st.spinner("Getting response from OpenAI..."):
        response = ask_openai(list(map(lambda p: p.message, st.session_state.messages)), system_prompt=system_prompt)

    st.write("Response from OpenAI:")
    st.markdown(response, unsafe_allow_html=False)
    st.session_state.messages.append(Message({
            "role": "assistant",
            "content": response
        }, role))

    st.rerun()

