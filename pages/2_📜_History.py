import streamlit as st
from db.invoice_records import get_invoice_records_by_user
from dotenv import load_dotenv
from utils.auth import get_user_id  # 你可以封装 cookie 或 session 中取 id

load_dotenv()
st.set_page_config(page_title="📜 Invoice History", page_icon="📜")

st.title("📜 Invoice History")

user_id = get_user_id()
if not user_id:
    st.warning("You need to log in to view your invoice history.")
    st.stop()

# 分页参数
page_size = 5
page = st.number_input("Page", min_value=1, step=1)

records, total_count = get_invoice_records_by_user(user_id, page, page_size)

if not records:
    st.info("No invoice records found.")
else:
    for record in records:
        id, file_name, image_path, invoice_date, issuer, total_amount, created_at = record

        st.markdown(f"### 🧾 {file_name} ({created_at[:10]})")
        st.image(image_path, width=250)

        st.markdown(f"""
        **🛍️ Issuer:** {issuer or 'N/A'}  
        **📅 Date:** {invoice_date or 'N/A'}  
        **💰 Total:** ${total_amount or 'N/A'}
        """)
        st.divider()

    total_pages = (total_count + page_size - 1) // page_size
    st.markdown(f"Page {page} of {total_pages}")
