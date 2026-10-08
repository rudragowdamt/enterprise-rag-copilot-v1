import streamlit as st

from src.rag_pipeline import ask_rag


st.set_page_config(
    page_title="Enterprise Integration RAG Copilot",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 Enterprise Integration RAG Copilot")

st.write(
    "AI-powered knowledge assistant for enterprise "
    "integration support and incident resolution."
)


question = st.text_area(
    "Ask an integration support question",
    placeholder=(
        "Example: PaymentService through Axway is returning "
        "HTTP 504. What should I investigate?"
    ),
)


if st.button("Ask Copilot"):
    if not question.strip():
        st.warning(
            "Please enter a question."
        )
    else:
        with st.spinner(
            "Searching enterprise knowledge..."
        ):
            result = ask_rag(question)

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Retrieved Sources")

        for index, source in enumerate(
            result["sources"],
            start=1,
        ):
            st.write(
                f"{index}. "
                f"{source['title']} — "
                f"{source['section']} "
                f"(Similarity: "
                f"{source['similarity_score']:.4f})"
            )