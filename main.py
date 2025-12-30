import streamlit as st

st.set_page_config(page_title="AI Prompt Spark", page_icon="✨")

st.title("✨ My First AI App")
st.write("هذا التطبيق يحول أفكارك إلى أوامر احترافية")

option = st.selectbox("اختر نوع النظام:", ["Payment", "E-commerce", "AI Art"])
user_task = st.text_input("ماذا تريد أن تفعل؟", "Write your idea here")

if st.button("Generate ✨"):
    st.success("إليك البرومبت الخاص بك:")
    st.code(f"Act as an expert in {option}. Task: {user_task}. Ensure high integrity.")
