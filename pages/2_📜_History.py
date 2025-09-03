import streamlit as st
from db import get_user_chat_logs

st.title("📜 我的历史记录")

# 初始化 user_id
if "user_id" not in st.session_state:
    st.stop()

user_id = st.session_state.user_id

# 分页参数
PAGE_SIZE = 5
if "history_page" not in st.session_state:
    st.session_state.history_page = 0

# 获取数据
logs = get_user_chat_logs(user_id, limit=PAGE_SIZE, offset=st.session_state.history_page * PAGE_SIZE)

# 展示记录
if logs:
    for timestamp, role, question, answer in logs:
        st.markdown(f"🕒 **{timestamp}** | 🎭 **{role}**")
        st.markdown(f"**你：** {question}")
        st.markdown(f"**AI：** {answer}")
        st.markdown("---")
else:
    st.info("No chat history available.")

# 分页按钮
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Previous") and st.session_state.history_page > 0:
        st.session_state.history_page -= 1
        st.rerun()
with col2:
    st.caption(f"Page：{st.session_state.history_page + 1}")
with col3:
    if len(logs) == PAGE_SIZE:
        if st.button("➡️ Next"):
            st.session_state.history_page += 1
            st.rerun()
