import time

import streamlit as st

from src.rag_pipeline import ask_rag


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Enterprise Integration AI Copilot",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #6C3FC5;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #777777;
        margin-bottom: 25px;
    }

    .info-box {
        background-color: rgba(108, 63, 197, 0.08);
        border-left: 5px solid #6C3FC5;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .source-card {
        border: 1px solid rgba(108, 63, 197, 0.30);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">'
    '🤖 Enterprise Integration AI Copilot'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'RAG-powered knowledge assistant for enterprise '
    'integration support and incident resolution'
    '</div>',
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="info-box">
    <b>How it works:</b>
    Ask an enterprise integration support question.
    The Copilot searches synthetic runbooks, architecture
    documents and historical incidents before generating
    a grounded answer with supporting sources.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("About the Copilot")

    st.write(
        "Built using Retrieval-Augmented Generation (RAG) "
        "for enterprise integration operations."
    )

    st.markdown("**AI Stack**")

    st.write("🧠 Amazon Bedrock")
    st.write("🔢 Titan Text Embeddings V2")
    st.write("💬 Claude Haiku")
    st.write("🔎 Semantic Vector Retrieval")
    st.write("⚡ FastAPI")
    st.write("🎨 Streamlit")

    st.divider()

    st.markdown("**Knowledge Base**")

    st.write("📄 24 enterprise documents")
    st.write("🧩 76 retrieval chunks")
    st.write("🧪 12 golden evaluation questions")
    st.write("🎯 Retrieval Recall@5: 90.28%")

    st.divider()

    st.caption(
        "Portfolio demonstration using synthetic "
        "enterprise integration data."
    )


# ---------------------------------------------------------
# EXAMPLE QUESTIONS
# ---------------------------------------------------------

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


if "question" not in st.session_state:
    st.session_state.question = ""
if "request_count" not in st.session_state:
    st.session_state.request_count = 0

MAX_REQUESTS = 10
MAX_QUESTION_LENGTH = 500
REQUEST_COOLDOWN_SECONDS = 5

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0.0
columns = st.columns(4)

for column, (label, example) in zip(
    columns,
    example_questions.items(),
):
    with column:
        if st.button(
            label,
            use_container_width=True,
        ):
            st.session_state.question = example


# ---------------------------------------------------------
# QUESTION
# ---------------------------------------------------------

st.subheader("Ask the Copilot")

question = st.text_area(
    "Describe the integration issue",
    key="question",
    height=120,
    placeholder=(
        "Example: PaymentService through Axway is "
        "returning HTTP 504..."
    ),
)


# ---------------------------------------------------------
# RAG EXECUTION
# ---------------------------------------------------------

if st.button(
    "🔍 Investigate Issue",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning(
            "Please enter an integration support question."
        )
    elif len(question) > MAX_QUESTION_LENGTH:

        st.warning(
            "Question is too long. "
            f"Please keep it under "
            f"{MAX_QUESTION_LENGTH} characters."
        )
    elif (
        time.time()
        - st.session_state.last_request_time
        < REQUEST_COOLDOWN_SECONDS
    ):

        st.warning(
            "Please wait a few seconds "
            "before submitting another request."
        )    
    elif st.session_state.request_count >= MAX_REQUESTS:

        st.error(
            "Demo request limit reached. "
            "This session allows a maximum of "
            f"{MAX_REQUESTS} requests."
        )

    else:

        st.session_state.request_count += 1
        st.session_state.last_request_time = time.time()
        with st.spinner(
            "Searching enterprise knowledge and "
            "generating a grounded response..."
        ):

            try:
                result = ask_rag(question)

            except Exception as error:
                st.error(
                    "The Copilot could not process the request."
                )
                st.exception(error)
                st.stop()


        # -------------------------------------------------
        # ANSWER
        # -------------------------------------------------

        st.success(
            "Analysis completed"
        )

        st.subheader(
            "🤖 Copilot Response"
        )

        st.markdown(
            result["answer"]
        )


        # -------------------------------------------------
        # SOURCES
        # -------------------------------------------------

        st.subheader(
            "📚 Retrieved Evidence"
        )

        st.caption(
            "The following knowledge chunks were retrieved "
            "before the AI generated its response."
        )

        for index, source in enumerate(
            result["sources"],
            start=1,
        ):

            score = source[
                "similarity_score"
            ]

            with st.expander(
                f"Source {index} — "
                f"{source['title']} | "
                f"{source['section']} | "
                f"Score {score:.4f}"
            ):

                st.write(
                    f"**Document ID:** "
                    f"{source['document_id']}"
                )

                st.write(
                    f"**Chunk ID:** "
                    f"{source['chunk_id']}"
                )

                st.write(
                    f"**Section:** "
                    f"{source['section']}"
                )

                st.write(
                    f"**Source:** "
                    f"{source['source']}"
                )

                st.progress(
                    min(
                        max(float(score), 0.0),
                        1.0,
                    )
                )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

remaining_requests = (
    MAX_REQUESTS
    - st.session_state.request_count
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