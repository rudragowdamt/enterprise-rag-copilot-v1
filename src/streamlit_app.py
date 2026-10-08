import time
import streamlit as st

from src.rag_pipeline import ask_rag


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Enterprise Integration AI Copilot",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# SETTINGS
# =========================================================

MAX_REQUESTS = 10
MAX_QUESTION_LENGTH = 500
REQUEST_COOLDOWN_SECONDS = 5


# =========================================================
# SESSION STATE
# =========================================================

if "request_count" not in st.session_state:
    st.session_state.request_count = 0

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0.0


# =========================================================
# STYLING
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #6C3FC5;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #777777;
        margin-bottom: 22px;
    }

    .info-box {
        background-color: rgba(108, 63, 197, 0.08);
        border-left: 5px solid #6C3FC5;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 22px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🤖 Enterprise Integration AI Copilot
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        RAG-powered knowledge assistant for enterprise
        integration support and incident resolution
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="info-box">
        <b>How it works:</b>
        Ask an enterprise integration support question.
        The Copilot retrieves relevant information from
        synthetic runbooks, architecture documents and
        historical incidents, then generates a grounded
        response using Amazon Bedrock.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("About the Copilot")

    st.write(
        "Enterprise integration support assistant built "
        "using Retrieval-Augmented Generation (RAG)."
    )

    st.divider()

    st.markdown("### AI Stack")

    st.write("🧠 Amazon Bedrock")
    st.write("🔢 Titan Text Embeddings V2")
    st.write("💬 Claude Haiku 4.5")
    st.write("🔎 Semantic Retrieval")
    st.write("🎨 Streamlit")

    st.divider()

    st.markdown("### Knowledge Base")

    st.write("📄 24 enterprise documents")
    st.write("🧩 76 retrieval chunks")
    st.write("🧪 12 golden evaluation questions")
    st.write("🎯 Recall@5: 90.28%")

    st.divider()

    st.caption(
        "Portfolio demonstration using synthetic "
        "enterprise integration data."
    )


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.subheader("Try an example")

example_questions = {
    "Axway 504": (
        "PaymentService through Axway is returning HTTP 504. "
        "What should I investigate and have we seen this before?"
    ),
    "Boomi Failure": (
        "A Boomi production process started failing immediately "
        "after deployment. What should support check?"
    ),
    "Layer7 401": (
        "Layer7 suddenly returns 401 for many clients after "
        "an IdP change. What is a likely cause?"
    ),
    "SFTP Issue": (
        "Our partner SFTP host key changed. Can we bypass "
        "validation to restore service?"
    ),
}


# =========================================================
# EXAMPLE SELECTOR
# =========================================================

selected_example = st.selectbox(
    "Choose an example or enter your own question below",
    options=[
        "Custom question",
        "Axway 504",
        "Boomi Failure",
        "Layer7 401",
        "SFTP Issue",
    ],
)


if selected_example == "Custom question":

    default_question = ""

else:

    default_question = example_questions[
        selected_example
    ]


# =========================================================
# QUESTION INPUT
# =========================================================

question = st.text_area(
    "Describe the integration issue",
    value=default_question,
    height=120,
    max_chars=MAX_QUESTION_LENGTH,
    placeholder=(
        "Example: PaymentService through Axway is "
        "returning HTTP 504..."
    ),
)


# =========================================================
# REQUEST INFORMATION
# =========================================================

remaining_requests = max(
    MAX_REQUESTS
    - st.session_state.request_count,
    0,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Documents",
        "24",
    )

with col2:
    st.metric(
        "Retrieval Chunks",
        "76",
    )

with col3:
    st.metric(
        "Demo Requests Remaining",
        remaining_requests,
    )


# =========================================================
# INVESTIGATE
# =========================================================

if st.button(
    "🔍 Investigate Issue",
    type="primary",
    use_container_width=True,
):

    clean_question = question.strip()

    if not clean_question:

        st.warning(
            "Please enter an integration support question."
        )

    elif len(clean_question) > MAX_QUESTION_LENGTH:

        st.warning(
            f"Please keep the question under "
            f"{MAX_QUESTION_LENGTH} characters."
        )

    elif st.session_state.request_count >= MAX_REQUESTS:

        st.error(
            "Demo request limit reached for this session."
        )

    elif (
        time.time()
        - st.session_state.last_request_time
        < REQUEST_COOLDOWN_SECONDS
    ):

        st.warning(
            "Please wait a few seconds before "
            "submitting another request."
        )

    else:

        # Count only valid requests
        st.session_state.request_count += 1

        st.session_state.last_request_time = time.time()

        st.write(
            "Searching enterprise knowledge..."
        )

        try:

            with st.spinner(
                "Running RAG retrieval and generating "
                "a grounded response..."
            ):

                result = ask_rag(
                    clean_question
                )

            # =============================================
            # SUCCESS
            # =============================================

            st.success(
                "Analysis completed successfully."
            )


            # =============================================
            # CACHE STATUS
            # =============================================

            if result.get(
                "cache_hit",
                False,
            ):

                st.info(
                    "⚡ Response served from RAG cache."
                )

            else:

                st.info(
                    "🧠 Fresh RAG analysis completed "
                    "using Amazon Bedrock."
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
            # RETRIEVED EVIDENCE
            # =============================================

            st.subheader(
                "📚 Retrieved Evidence"
            )

            st.caption(
                "Knowledge chunks retrieved before "
                "the AI generated its response."
            )

            sources = result.get(
                "sources",
                [],
            )

            if not sources:

                st.warning(
                    "No retrieval evidence was returned."
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
                    "Unknown Document",
                )

                section = source.get(
                    "section",
                    "Unknown Section",
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
                        "**Chunk ID:**",
                        source.get(
                            "chunk_id",
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

                    safe_score = min(
                        max(
                            score,
                            0.0,
                        ),
                        1.0,
                    )

                    st.progress(
                        safe_score
                    )


        except Exception as error:

            st.error(
                "RAG execution failed."
            )

            st.exception(
                error
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

remaining_requests = max(
    MAX_REQUESTS
    - st.session_state.request_count,
    0,
)

st.caption(
    f"Demo requests remaining: "
    f"{remaining_requests}/{MAX_REQUESTS}"
)

st.caption(
    "Enterprise Integration Knowledge & Incident Resolution "
    "RAG Copilot | Portfolio Project | "
    "Synthetic demonstration data"
)