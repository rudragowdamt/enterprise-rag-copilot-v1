import streamlit as st

st.set_page_config(
    page_title="Streamlit RAG Test",
    page_icon="🧪",
)

st.title("Streamlit RAG Import Test")

st.write("Step 1: Streamlit loaded successfully.")

try:
    from src.rag_pipeline import ask_rag

    st.success("Step 2: RAG pipeline imported successfully.")

except Exception as error:
    st.error("RAG pipeline import failed.")
    st.exception(error)
    st.stop()


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


st.success("Step 3: Application completed successfully.")