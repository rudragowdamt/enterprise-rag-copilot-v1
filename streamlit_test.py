import streamlit as st

st.set_page_config(
    page_title="Streamlit Test",
    page_icon="🧪",
)

st.title("Streamlit Cloud Test")

if "question" not in st.session_state:
    st.session_state.question = ""

if st.button("Axway 504"):
    st.session_state.question = (
        "PaymentService through Axway is returning HTTP 504."
    )

st.text_area(
    "Question",
    key="question",
)

st.success("Streamlit is working.")