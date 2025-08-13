import streamlit as st
from pathlib import Path
from utils import ask_openai
from promp import ROLE_PROMPT
from message import Message
from utils import load_user_log, save_user_log, get_today_key, can_ask_today, increment_user_count

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "should_clear_input" not in st.session_state:
        st.session_state.should_clear_input = False
   
DATA_FILE = Path("data/user_log.json")
MAX_QUESTIONS_PER_DAY = 5

user_id = "local_user"
user_log = load_user_log(DATA_FILE)
can_ask = can_ask_today(user_id, user_log, MAX_QUESTIONS_PER_DAY)
user_count = user_log.get(user_id, {}).get(get_today_key(), 0)
remain = MAX_QUESTIONS_PER_DAY - user_count

init_session_state()

st.set_page_config(
    page_title="Chat with OpenAI", 
    page_icon="🤖",
    layout="centered")

st.title("Chat with OpenAI")
st.markdown("Welcome to the OpenAI Chatbot! Ask me anything and I'll do my best to provide a helpful response.")
role = st.selectbox("Select Role", list(ROLE_PROMPT.keys()))
system_prompt = ROLE_PROMPT[role]

st.markdown("----------------")
st.markdown("### Chat History")

for msg in st.session_state.messages:
    message = msg.message
    if message["role"] == "user":
        st.write(f"**[{msg.system_prompt}] You Ask:** {message['content']}")
    else:
        st.write(f"**[{msg.system_prompt}] OpenAI Responds:** {message['content']}")
    
st.markdown("----------------")

st.info(f"The question limit for today is {MAX_QUESTIONS_PER_DAY}. You have {remain} questions left for today.")

if not can_ask:
    st.warning(f"You have reached the daily limit of {MAX_QUESTIONS_PER_DAY} questions. Please try again tomorrow.")

question = st.text_input("Ask a question to OpenAI:", 
                         key="input_text", 
                         value="" if st.session_state.should_clear_input else st.session_state.get("input_text", ""),
                         placeholder="Type your question here...", 
                         disabled=not can_ask)

if st.session_state.should_clear_input:
    st.session_state.should_clear_input = False

submit = st.button("Submit", disabled = not can_ask or not st.session_state.input_text.strip())
if submit and question.strip():
    question = st.session_state.input_text.strip()
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

    increment_user_count(user_id, user_log)
    save_user_log(DATA_FILE, user_log)
    
    st.session_state.should_clear_input = True
    st.rerun()  # Rerun to update the chat history

if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.session_state.should_clear_input = True
    st.rerun()  # Rerun to clear the chat history display
            
