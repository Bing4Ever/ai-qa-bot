import streamlit as st
from db.init import init_database_from_sql
st.set_page_config(page_title="AI Q&A Assistant", page_icon="🤖")
st.write("Welcome to AI Financial Assistant! Please navigate using the sidebar.")

init_database_from_sql()

st.set_page_config(page_title="Redirecting...", layout="centered")

# 自动跳转到 Upload 页面
st.switch_page("pages/1_🤖_Invoice_Recorder.py")