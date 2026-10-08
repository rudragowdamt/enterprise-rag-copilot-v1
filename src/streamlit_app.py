import streamlit as st

from src.rag_pipeline import ask_rag


st.set_page_config(
    page_title="Enterprise Integration AI Copilot",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 Enterprise Integration AI Copilot")

st.write(
    "RAG-powered assistant for enterprise integration "
    "support and incident resolution."
)

st.info(
    "This portfolio demonstration uses synthetic enterprise "
    "runbooks, architecture documents and historical incidents."
)


question = st.text_area(
    "Describe the integration issue",
    value=(
        "PaymentService through Axway is returning HTTP 504. "
        "What should I investigate and have we seen this before?"
    ),
    height=120,
)


if st.button(
    "🔍 Investigate Issue",
    type="primary",
):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner(
                "Searching enterprise knowledge..."
            ):

                result = ask_rag(
                    question.strip()
                )

            st.success(
                "Analysis completed successfully."
            )

            st.subheader(
                "🤖 Copilot Response"
            )

            st.markdown(
                result.get(
                    "answer",
                    "No answer returned.",
                )
            )

            st.subheader(
                "📚 Retrieved Evidence"
            )

            sources = result.get(
                "sources",
                [],
            )

            for index, source in enumerate(
                sources,
                start=1,
            ):

                score = float(
                    source.get(
                        "similarity_score",
                        0,
                    )
                )

                with st.expander(
                    f"Source {index}: "
                    f"{source.get('title', 'Document')} "
                    f"({score:.4f})"
                ):

                    st.write(
                        "**Document:**",
                        source.get(
                            "document_id",
                            "N/A",
                        ),
                    )

                    st.write(
                        "**Section:**",
                        source.get(
                            "section",
                            "N/A",
                        ),
                    )

                    st.write(
                        "**Source:**",
                        source.get(
                            "source",
                            "N/A",
                        ),
                    )


            if result.get("cache_hit"):

                st.caption(
                    "⚡ Response served from cache."
                )

            else:

                st.caption(
                    "🧠 Response generated using Amazon Bedrock."
                )


        except Exception as error:

            st.error(
                "The RAG request failed."
            )

            st.exception(error)


st.divider()

st.caption(
    "Amazon Bedrock • Titan Embeddings V2 • "
    "Claude Haiku 4.5 • RAG • Streamlit"
)