import streamlit as st
from utils import ask_openai

st.set_page_config(
    page_title="Chat with OpenAI", 
    page_icon="🤖",
    layout="centered")

st.title("Chat with OpenAI")

st.markdown("Welcome to the OpenAI Chatbot! Ask me anything and I'll do my best to provide a helpful response.")

if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("----------------")
st.markdown("### Chat History")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(f"**You Ask:** {msg['content']}")
    else:
        st.write(f"**OpenAI Responds:** {msg['content']}")
    
st.markdown("----------------")

question = st.text_input("Ask a question to OpenAI:", placeholder="Type your question here...")

if st.button("Submit") and question.strip() != "":
    st.session_state.messages.append({
        "role": "user",
        "content": question
        })
    
    with st.spinner("Getting response from OpenAI..."):
        response = ask_openai(st.session_state.messages)
        st.write("Response from OpenAI:")
        st.markdown(response, unsafe_allow_html=False
                    )
        st.session_state.messages.append({
        "role": "assistant",
        "content": response
        })

    st.rerun()

