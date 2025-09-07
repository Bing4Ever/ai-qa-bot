from streamlit_cookies_controller import CookieController
import streamlit as st
from datetime import datetime

cookie_manager = CookieController()

def get_user_id():
    cookie_manager.set("user_id", "demo-user")
    return cookie_manager.get("user_id") or "anonymous"
