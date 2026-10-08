import streamlit as st

from src.rag_pipeline import ask_rag


st.set_page_config(
    page_title="RAG Cloud Test",
    page_icon="🧪",
)

st.title("RAG Cloud Test")


question = (
    "PaymentService through Axway is returning HTTP 504. "
    "What should I investigate and have we seen this before?"
)


st.write("Test question:")

st.info(question)


if st.button("Run RAG Test"):

    st.write("Starting RAG pipeline...")

    try:

        with st.spinner("Running RAG..."):

            result = ask_rag(question)

        st.success("RAG completed successfully.")

        st.subheader("Answer")

        st.write(
            result.get(
                "answer",
                "No answer returned",
            )
        )

        st.subheader("Sources")

        st.write(
            len(
                result.get(
                    "sources",
                    [],
                )
            )
        )

        st.write(
            "Cache hit:",
            result.get(
                "cache_hit",
                False,
            ),
        )

    except Exception as error:

        st.error("RAG execution failed.")

        st.exception(error)