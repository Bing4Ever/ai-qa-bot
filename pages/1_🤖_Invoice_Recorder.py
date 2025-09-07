import streamlit as st
from utils.llm import analyze_invoice_image_bytes
from utils.func import save_image_local
from utils.auth import get_user_id
from db.invoice_records import save_invoice_record
import pandas as pd

st.set_page_config(page_title="Invoice Analyzer", page_icon="🧾")
st.title("🧾 Smart Invoice Analyzer")

st.markdown("Upload an invoice image to extract and categorize its contents automatically.")

# 文件上传
uploaded_file = st.file_uploader("Upload Invoice Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # 显示上传的图片缩略图
    st.image(uploaded_file, width=300, caption="Uploaded Invoice")

    # 分析按钮
    if st.button("📊 Analyze Invoice"):
        with st.spinner("Analyzing the invoice..."):
            try:
                # 保存文件
                file_path = save_image_local(uploaded_file)
                file_name = uploaded_file.name
                image_bytes = uploaded_file.getvalue()

                # 调用 GPT
                result = analyze_invoice_image_bytes(image_bytes)

                # 展示结构化数据（用户友好）
                if "error" in result:
                    st.error("❌ GPT parsing failed.")
                    st.code(result.get("raw_response", ""), language="json")
                else:
                    st.subheader("📄 Invoice Summary")

                    st.markdown(f"**🛍️ Issuer:** {result.get('issuer', 'N/A')}")
                    st.markdown(f"**📅 Date:** {result.get('invoice_date', 'N/A')}")
                    st.markdown(f"**💰 Total:** ${result.get('total_amount', 'N/A')}")

                    # 展示明细项目
                    items = result.get("items", [])
                    if items:
                        st.subheader("📦 Itemized List")
                        df = pd.DataFrame(items)
                        st.table(df)
                    else:
                        st.info("No item details detected.")

                    # 保存入数据库
                    user_id = get_user_id()  # 你可以替换为真实用户 ID
                    save_invoice_record(user_id, file_path, file_name, result)
                    st.success("✅ Invoice saved successfully!")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

