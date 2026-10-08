import streamlit as st

from src.rag_pipeline import ask_rag


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Enterprise Integration AI Copilot",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# SIMPLE PURPLE BRANDING
# =========================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #6C3FC5;
    }

    .subtitle {
        font-size: 18px;
        color: #777777;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="main-title">'
    '🤖 Enterprise Integration AI Copilot'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'RAG-powered assistant for enterprise integration '
    'support and incident resolution'
    '</div>',
    unsafe_allow_html=True,
)


st.info(
    "Ask an enterprise integration support question. "
    "The Copilot retrieves relevant information from "
    "synthetic runbooks, architecture documents and "
    "historical incidents before generating a grounded answer."
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("AI Copilot")

    st.write(
        "Enterprise Integration Knowledge & "
        "Incident Resolution"
    )

    st.divider()

    st.write("🧠 Amazon Bedrock")
    st.write("🔢 Titan Text Embeddings V2")
    st.write("💬 Claude Haiku 4.5")
    st.write("🔎 Semantic Retrieval")
    st.write("🎨 Streamlit")

    st.divider()

    st.write("📄 24 documents")
    st.write("🧩 76 chunks")
    st.write("🎯 Recall@5: 90.28%")

    st.divider()

    st.caption(
        "Portfolio demonstration using synthetic data."
    )


# =========================================================
# QUESTION
# =========================================================

st.subheader("Ask the Copilot")
example_questions = {
    "Axway 504 Gateway Timeout": (
        "PaymentService through Axway is returning HTTP 504. "
        "What should I investigate and have we seen this before?"
    ),
    "Boomi Deployment Failure": (
        "A Boomi production process started failing immediately "
        "after deployment. What should support check?"
    ),
    "Layer7 Authentication Issue": (
        "Layer7 suddenly returns 401 for many clients after "
        "an IdP change. What is a likely cause?"
    ),
    "SFTP Host Key Change": (
        "Our partner SFTP host key changed. Can we bypass "
        "validation to restore service?"
    ),
}

selected_example = st.selectbox(
    "Try an example",
    [
        "Axway 504 Gateway Timeout",
        "Boomi Deployment Failure",
        "Layer7 Authentication Issue",
        "SFTP Host Key Change",
    ],
)

default_question = example_questions[selected_example]
question = st.text_area(
    "Describe the integration issue",
    value=default_question,
    height=120,
    max_chars=500,
)


# =========================================================
# RAG
# =========================================================

if st.button(
    "🔍 Investigate Issue",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning(
            "Please enter an integration support question."
        )

    else:

        try:

            with st.spinner(
                "Searching enterprise knowledge and "
                "generating a grounded response..."
            ):

                result = ask_rag(
                    question.strip()
                )

            st.success(
                "Analysis completed successfully."
            )


            # =============================================
            # CACHE
            # =============================================

            if result.get(
                "cache_hit",
                False,
            ):

                st.caption(
                    "⚡ Response served from cache."
                )

            else:

                st.caption(
                    "🧠 Fresh RAG analysis using Amazon Bedrock."
                )


            # =============================================
            # ANSWER
            # =============================================

            st.subheader(
                "🤖 Copilot Response"
            )

            st.markdown(
                result.get(
                    "answer",
                    "No answer returned.",
                )
            )


            # =============================================
            # EVIDENCE
            # =============================================

            st.subheader(
                "📚 Retrieved Evidence"
            )

            st.caption(
                "These knowledge chunks were retrieved "
                "before generating the response."
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
                        0.0,
                    )
                )

                title = source.get(
                    "title",
                    "Enterprise Document",
                )

                section = source.get(
                    "section",
                    "N/A",
                )

                with st.expander(
                    f"Source {index} — "
                    f"{title} | "
                    f"Score {score:.4f}"
                ):

                    st.write(
                        "**Document ID:**",
                        source.get(
                            "document_id",
                            "N/A",
                        ),
                    )

                    st.write(
                        "**Section:**",
                        section,
                    )

                    st.write(
                        "**Source:**",
                        source.get(
                            "source",
                            "N/A",
                        ),
                    )

                    st.write(
                        "**Similarity Score:**",
                        f"{score:.4f}",
                    )


        except Exception as error:

            st.error(
                "The Copilot could not process the request."
            )

            st.exception(error)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Enterprise Integration Knowledge & Incident Resolution "
    "RAG Copilot | Portfolio Project | Synthetic Data"
)