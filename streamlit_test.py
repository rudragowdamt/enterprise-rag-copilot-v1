
import time

import streamlit as st

from src.rag_pipeline import ask_rag


# =========================================================
# CONFIGURATION
# =========================================================

MAX_REQUESTS = 10
REQUEST_COOLDOWN_SECONDS = 5
MAX_QUESTION_LENGTH = 500


# =========================================================
# EXAMPLE INVESTIGATION QUESTIONS
# =========================================================

EXAMPLE_QUESTIONS = {
    "Axway | HTTP 504 — Previous Incident": (
        "PaymentService through Axway is returning HTTP 504. "
        "What should I investigate and have we seen this before?"
    ),
    "Axway | HTTP 504 — Root Cause and Resolution": (
        "What caused incident INC003, and how was it resolved?"
    ),
    "Boomi | SFTP Authentication Failure": (
        "How can I diagnose a Boomi SFTP authentication failure?"
    ),
    "Boomi | SSH Key Authentication": (
        "What should I verify when SSH key authentication "
        "fails in a Boomi SFTP connection?"
    ),
    "Axway | HTTP 401 Unauthorized": (
        "How do I troubleshoot HTTP 401 Unauthorized "
        "errors in Axway API Gateway?"
    ),
    "Axway | HTTP 403 Forbidden": (
        "What should I investigate when Axway API Gateway "
        "returns HTTP 403 Forbidden?"
    ),
    "Axway | HTTP 429 Too Many Requests": (
        "How should I investigate HTTP 429 Too Many Requests "
        "errors in Axway API Gateway?"
    ),
    "Boomi | SFTP Connection Configuration": (
        "Which Boomi SFTP connection settings should I "
        "verify when a connection fails?"
    ),
    "Custom Question": "",
}


SCENARIO_DESCRIPTIONS = {
    "Axway | HTTP 504 — Previous Incident": (
        "Find a similar historical incident, its root cause, "
        "and documented resolution."
    ),
    "Axway | HTTP 504 — Root Cause and Resolution": (
        "Retrieve root cause analysis and resolution details "
        "from an incident record."
    ),
    "Boomi | SFTP Authentication Failure": (
        "Retrieve runbook-based troubleshooting steps."
    ),
    "Boomi | SSH Key Authentication": (
        "Investigate SSH key configuration and authentication."
    ),
    "Axway | HTTP 401 Unauthorized": (
        "Investigate an API authentication failure."
    ),
    "Axway | HTTP 403 Forbidden": (
        "Investigate an API authorization failure."
    ),
    "Axway | HTTP 429 Too Many Requests": (
        "Investigate API rate-limiting behavior."
    ),
    "Boomi | SFTP Connection Configuration": (
        "Review SFTP connector configuration checks."
    ),
    "Custom Question": (
        "Enter your own enterprise integration support question."
    ),
}


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Enterprise Integration AI Copilot",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# SESSION STATE
# =========================================================

if "request_count" not in st.session_state:
    st.session_state.request_count = 0

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0.0

if "selected_scenario" not in st.session_state:
    st.session_state.selected_scenario = next(
        iter(EXAMPLE_QUESTIONS)
    )

if "question_input" not in st.session_state:
    st.session_state.question_input = EXAMPLE_QUESTIONS[
        st.session_state.selected_scenario
    ]

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""


# =========================================================
# QUESTION SELECTION CALLBACK
# =========================================================

def update_selected_question():
    """
    Update the editable question when the scenario changes.
    """

    selected = st.session_state.selected_scenario

    st.session_state.question_input = (
        EXAMPLE_QUESTIONS[selected]
    )

    st.session_state.last_result = None


# =========================================================
# BRANDING
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
    'RAG-powered incident investigation, troubleshooting '
    'and enterprise knowledge retrieval'
    '</div>',
    unsafe_allow_html=True,
)


st.info(
    "Investigate enterprise integration failures using "
    "synthetic runbooks and historical incident records. "
    "The Copilot retrieves relevant evidence and uses "
    "Amazon Bedrock to generate a source-cited answer."
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

    st.subheader("Technology")

    st.write("🧠 Amazon Bedrock")
    st.write("🔢 Titan Text Embeddings V2")
    st.write("💬 Claude Haiku 4.5")
    st.write("🔎 Semantic Retrieval")
    st.write("🎨 Streamlit")

    st.divider()

    st.subheader("Knowledge Base")

    st.write("📄 28 documents")
    st.write("🧩 106 chunks")

    st.divider()

    st.subheader("Reliability Controls")

    st.write("🛡️ AWS Bedrock Guardrails")
    st.write("✅ Contextual Grounding")
    st.write("🔐 Retrieval Confidence")
    st.write("📚 Citation Validation")

    st.divider()

    st.caption(
        "Portfolio demonstration using synthetic data."
    )

    st.caption(
        "Grounding threshold is configured for a demo "
        "and is not production calibrated."
    )


# =========================================================
# INVESTIGATION SCENARIOS
# =========================================================

st.subheader("🔍 Investigate an Integration Issue")

st.write(
    "Choose a realistic investigation scenario or "
    "enter your own question."
)


selected_example = st.selectbox(
    "Select an investigation scenario",
    options=list(EXAMPLE_QUESTIONS.keys()),
    key="selected_scenario",
    on_change=update_selected_question,
)


st.caption(
    SCENARIO_DESCRIPTIONS[selected_example]
)


question = st.text_area(
    "Investigation question",
    key="question_input",
    height=115,
    max_chars=MAX_QUESTION_LENGTH,
    placeholder=(
        "Describe the integration error, affected service, "
        "platform, or incident number..."
    ),
)


# =========================================================
# INVESTIGATION CAPABILITIES
# =========================================================

with st.expander(
    "What can this Copilot demonstrate?",
    expanded=False,
):

    st.markdown(
        """
        - **Incident correlation:** Find similar historical failures.
        - **Root cause analysis:** Retrieve documented causes.
        - **Troubleshooting:** Follow relevant operational runbooks.
        - **Resolution knowledge:** Find previously documented fixes.
        - **Evidence:** Inspect retrieved source passages.
        - **Guardrails:** Reject prohibited requests and check grounding.

        Responses depend on the available knowledge-base evidence.
        """
    )


# =========================================================
# REQUEST STATUS
# =========================================================

remaining_requests = max(
    MAX_REQUESTS - st.session_state.request_count,
    0,
)

st.caption(
    f"Demo requests remaining: "
    f"{remaining_requests}/{MAX_REQUESTS}"
)


# =========================================================
# INVESTIGATE BUTTON
# =========================================================

investigate_clicked = st.button(
    "🔍 Investigate Issue",
    type="primary",
    use_container_width=True,
)


# =========================================================
# RAG EXECUTION
# =========================================================

if investigate_clicked:

    cleaned_question = question.strip()

    # -----------------------------------------------------
    # INPUT VALIDATION
    # -----------------------------------------------------

    if not cleaned_question:

        st.warning(
            "Please enter an integration support question."
        )

    elif len(cleaned_question) > MAX_QUESTION_LENGTH:

        st.warning(
            "The question exceeds the allowed length."
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
            "Please wait a few seconds before submitting "
            "another request."
        )

    else:

        # -------------------------------------------------
        # VALID REQUEST
        # -------------------------------------------------

        st.session_state.request_count += 1
        st.session_state.last_request_time = time.time()

        st.session_state.last_result = None
        st.session_state.last_question = cleaned_question

        try:

            with st.spinner(
                "Retrieving enterprise knowledge and "
                "validating the generated response..."
            ):

                result = ask_rag(
                    cleaned_question
                )

            st.session_state.last_result = result

        except Exception:

            # Keep internal exception details out of
            # the public demonstration interface.
            st.error(
                "The Copilot encountered a processing error. "
                "Please try again or contact the demo owner."
            )


# =========================================================
# DISPLAY THE LATEST RESULT
# =========================================================

result = st.session_state.last_result

if result is not None:

    st.divider()

    st.subheader("🤖 Copilot Response")

    st.caption(
        "Question: "
        + st.session_state.last_question
    )

    answer = result.get(
        "answer",
        "No answer returned.",
    )

    st.markdown(answer)

    if result.get("cache_hit", False):

        st.caption(
            "⚡ Response served from cache."
        )

    else:

        st.caption(
            "🧠 RAG analysis using Amazon Bedrock."
        )


    # =====================================================
    # RETRIEVED EVIDENCE
    # =====================================================

    st.subheader("📚 Retrieved Evidence")

    st.caption(
        "Explore the source passages retrieved from "
        "the knowledge base. A retrieved passage is not "
        "necessarily cited or used in the final answer."
    )

    sources = result.get(
        "sources",
        [],
    )

    if not sources:

        st.info(
            "No retrieval evidence was returned."
        )

    else:

        st.write(
            f"**{len(sources)} knowledge chunks retrieved**"
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

            source_label = (
                f"[SOURCE {index}] "
                f"{title} — {section}"
            )

            with st.expander(
                source_label,
                expanded=False,
            ):

                st.write(
                    "**Document:**",
                    title,
                )

                st.write(
                    "**Section:**",
                    section,
                )

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
                    "**Source file:**",
                    source.get(
                        "source",
                        "N/A",
                    ),
                )

                st.write(
                    "**Semantic similarity:**",
                    f"{score:.4f}",
                )

                source_content = source.get(
                    "content",
                    "",
                )

                if source_content:

                    st.markdown(
                        "**Retrieved knowledge passage:**"
                    )

                    # Render as plain text, not HTML.
                    st.text(source_content)

                else:

                    st.caption(
                        "Passage text was not included "
                        "in the result."
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

remaining_requests = max(
    MAX_REQUESTS - st.session_state.request_count,
    0,
)

st.caption(
    f"Demo requests remaining: "
    f"{remaining_requests}/{MAX_REQUESTS}"
)

st.caption(
    "Enterprise Integration Knowledge & Incident Resolution "
    "RAG Copilot | Portfolio Project | Synthetic Data"
)
