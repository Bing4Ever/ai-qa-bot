import streamlit as st
from prompts import ROLE_PROMPTS

st.title("⚙️ Settings")

st.subheader("🎭 Preset Role Prompts")

# 展示并允许修改提示词（目前仅展示功能）
for role, prompt in ROLE_PROMPTS.items():
    with st.expander(role, expanded=False):
        st.code(prompt, language="markdown")
        st.caption("（To edit, please modify prompts.py）")
