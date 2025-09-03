import streamlit as st
from db import init_db
st.set_page_config(page_title="AI Q&A Assistant", page_icon="🤖")
st.write("Welcome to AI Q&A Assistant，请通过左侧导航进入各功能页面。")

init_db()