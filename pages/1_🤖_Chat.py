import streamlit as st
import base64
from pathlib  import Path
from prompts import ROLE_PROMPTS
from utils import ask_openai_with_role, ask_openai_with_image
from db import insert_chat_log, count_user_queries, count_user_queries_today
import uuid

# 初始化 Session 状态
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_role" not in st.session_state:
    st.session_state.last_role = None

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = ""

user_id = st.session_state.user_id

st.title("🤖 AI Q&A Assistant")

# 角色选择与提示词逻辑
role = st.selectbox("🎭 Choose Role", list(ROLE_PROMPTS.keys()))
default_prompt = ROLE_PROMPTS[role]

if st.session_state.last_role != role:
    st.session_state.system_prompt = default_prompt
    st.session_state.last_role = role

# 可编辑提示词
with st.expander("📝 System Prompt (Editable)", expanded=False):
    new_prompt = st.text_area("System Prompt", value=st.session_state.system_prompt, key="system_prompt_editor", height=120)
    if new_prompt != st.session_state.system_prompt:
        st.session_state.system_prompt = new_prompt
        st.success("✅ Prompt updated")

# 提问进度与限额
DAILY_LIMIT = 20
total = count_user_queries(user_id)
today = count_user_queries_today(user_id)

st.markdown(f"📊 Today's Usage：**{today}/{DAILY_LIMIT}** | Total Usage：**{total}**")
st.progress(min(today / DAILY_LIMIT, 1.0))

if today >= DAILY_LIMIT:
    st.warning("🚫 You have reached the daily free limit. Please come back tomorrow or support the developer.")
    st.stop()

# 聊天 UI 展示历史记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 可选图片上传
uploaded_file = st.file_uploader("📷 Upload an image (optional)", type=["jpg", "jpeg", "png"])

# 输入框与提交按钮
if prompt := st.chat_input("Type your question here"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 获取 AI 回复
    
    if uploaded_file:
        if not prompt:
            st.error("❗ Please enter a question along with the image.")
            st.stop()
            
        with st.spinner("🔍 Processing image..."):
             answer = ask_openai_with_image(
                message=prompt,
                system_prompt=st.session_state.system_prompt,
                image_file=uploaded_file
            )
        # 写入数据库
        # 保存图片到本地
        uploads_dir = Path("data/uploads")
        uploads_dir.mkdir(parents=True, exist_ok=True)

        image_id = str(uuid.uuid4())
        ext = uploaded_file.name.split(".")[-1]
        image_filename = uploads_dir / f"{image_id}.{ext}"
        with open(image_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # 保存路径作为 image_path
        image_path_str = str(image_filename)

        insert_chat_log(user_id, role, st.session_state.system_prompt, prompt, answer, image_path=image_path_str)
    else:
        with st.spinner("🤔 Thinking..."):
            answer = ask_openai_with_role(
            messages=st.session_state.messages,
            system_prompt=st.session_state.system_prompt
            )
        # 写入数据库
        insert_chat_log(user_id, role, st.session_state.system_prompt, prompt, answer)
    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

    
