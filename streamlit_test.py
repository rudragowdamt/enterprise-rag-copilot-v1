
import re
import time
from pathlib import Path
from urllib.parse import quote

import streamlit as st

from src.rag_pipeline import ask_rag


# =========================================================
# CONFIGURATION
# =========================================================

MAX_REQUESTS = 10
REQUEST_COOLDOWN_SECONDS = 5
MAX_QUESTION_LENGTH = 500

REPO_ROOT = Path(__file__).resolve().parent

GITHUB_REPOSITORY = (
    "rudragowdamt/enterprise-rag-copilot-v1"
)

GITHUB_BRANCH = (
    "feature/enterprise-rag-security-reliability"
)


# =========================================================
# ORIGINAL FOUR DEMO QUESTIONS
# =========================================================

EXAMPLE_QUESTIONS = {
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
    "Custom Question": "",
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

if "selected_example" not in st.session_state:
    st.session_state.selected_example = (
        "Axway 504 Gateway Timeout"
    )

if "question_input" not in st.session_state:
    st.session_state.question_input = EXAMPLE_QUESTIONS[
        st.session_state.selected_example
    ]

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""


# =========================================================
# HELPERS
# =========================================================

def update_question():
    """Populate the question when the dropdown changes."""

    selection = st.session_state.selected_example

    st.session_state.question_input = (
        EXAMPLE_QUESTIONS[selection]
    )

    st.session_state.last_result = None


def get_source_content(source):
    """Return the retrieved source text."""

    return str(source.get("content") or "").strip()


def get_document_url(source):
    """
    Create a GitHub link only when the source file
    actually exists inside the deployed repository.

    Never construct links for missing or external files.
    """

    source_name = source.get("source")

    if not source_name:
        return None

    try:
        source_path = Path(str(source_name))

        if not source_path.is_absolute():
            source_path = REPO_ROOT / source_path

        source_path = source_path.resolve()

        relative_path = source_path.relative_to(
            REPO_ROOT
        )

        if not source_path.is_file():
            return None

        encoded_path = quote(
            relative_path.as_posix(),
            safe="/",
        )

        return (
            f"https://github.com/"
            f"{GITHUB_REPOSITORY}/blob/"
            f"{GITHUB_BRANCH}/{encoded_path}"
        )

    except (OSError, ValueError):
        return None


def find_sections(sources, keywords):
    """
    Find retrieved evidence by section name.

    Do not infer missing root causes or resolutions.
    """

    matches = []

    for index, source in enumerate(
        sources,
        start=1,
    ):
        section = str(
            source.get("section") or ""
        ).lower()

        if any(
            keyword in section
            for keyword in keywords
        ):
            matches.append((index, source))

    return matches


def show_section_evidence(matches, empty_message):
    """Show factual excerpts with matching source numbers."""

    if not matches:
        st.info(empty_message)
        return

    for index, source in matches[:3]:

        title = source.get(
            "title",
            "Enterprise Document",
        )

        section = source.get(
            "section",
            "Unknown Section",
        )

        st.markdown(
            f"**[SOURCE {index}] — {title}**"
        )

        st.caption(f"Section: {section}")

        content = get_source_content(source)

        if content:
            st.text(content)
        else:
            st.caption(
                "No passage text available."
            )


def get_historical_incidents(sources):
    """Identify retrieved historical incident records."""

    incidents = []
    seen = set()

    for index, source in enumerate(
        sources,
        start=1,
    ):
        title = str(
            source.get("title") or ""
        )

        document_id = str(
            source.get("document_id") or ""
        )

        if not (
            re.search(
                r"\bINC[-_ ]?\d+\b",
                title,
                flags=re.IGNORECASE,
            )
            or re.search(
                r"\bINC[-_ ]?\d+\b",
                document_id,
                flags=re.IGNORECASE,
            )
        ):
            continue

        if document_id in seen:
            continue

        seen.add(document_id)

        incidents.append(
            (index, source)
        )

    return incidents


def is_rejected_answer(answer):
    """
    Recognize the existing pipeline's known
    safety and insufficient-evidence responses.
    """

    normalized = answer.lower()

    rejection_phrases = [
        "the generated answer could not be verified",
        "could not find sufficiently relevant information",
        "violates the assistant's security policy",
    ]

    return any(
        phrase in normalized
        for phrase in rejection_phrases
    )


# =========================================================
# BRANDING
# =========================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        font-weight: 700;
        color: #6C3FC5;
    }

    .subtitle {
        font-size: 18px;
        color: #777777;
        margin-bottom: 18px;
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
    'AI-powered incident investigation and '
    'enterprise knowledge retrieval'
    '</div>',
    unsafe_allow_html=True,
)

st.info(
    "Select an integration issue to see how RAG "
    "retrieves historical incidents, troubleshooting "
    "runbooks and supporting evidence."
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("Enterprise RAG Copilot")

    st.write("🧠 Amazon Bedrock")
    st.write("🔢 Titan Embeddings V2")
    st.write("💬 Claude Haiku 4.5")
    st.write("🔎 Knowledge Retrieval")
    st.write("🎨 Streamlit")

    st.divider()

    st.subheader("Knowledge Base")

    st.write("📄 28 documents")
    st.write("🧩 106 chunks")

    st.divider()

    st.subheader("Reliability Controls")

    st.write("🛡️ Bedrock Guardrails")
    st.write("✅ Contextual Grounding")
    st.write("📚 Citation Validation")
    st.write("🔐 Retrieval Confidence")

    st.divider()

    st.caption(
        "Portfolio demonstration with synthetic data."
    )

    st.caption(
        "Grounding threshold: 0.50 "
        "(temporary demo configuration)."
    )


# =========================================================
# QUESTION INPUT
# =========================================================

st.subheader("🔍 Investigate an Integration Issue")

st.selectbox(
    "Choose a demonstration scenario",
    options=list(EXAMPLE_QUESTIONS.keys()),
    key="selected_example",
    on_change=update_question,
)

question = st.text_area(
    "Describe the integration issue",
    key="question_input",
    height=115,
    max_chars=MAX_QUESTION_LENGTH,
    placeholder=(
        "Enter an integration support question..."
    ),
)

remaining = max(
    MAX_REQUESTS - st.session_state.request_count,
    0,
)

st.caption(
    f"Demo requests remaining: {remaining}/{MAX_REQUESTS}"
)


# =========================================================
# EXECUTE RAG
# =========================================================

if st.button(
    "🔍 Investigate Issue",
    type="primary",
    use_container_width=True,
):

    cleaned_question = question.strip()

    if not cleaned_question:

        st.warning(
            "Please enter an integration support question."
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

        st.session_state.request_count += 1

        st.session_state.last_request_time = (
            time.time()
        )

        st.session_state.last_result = None

        st.session_state.last_question = (
            cleaned_question
        )

        try:

            with st.spinner(
                "Retrieving historical incidents "
                "and troubleshooting knowledge..."
            ):

                # Existing RAG backend.
                # No pipeline changes.
                result = ask_rag(
                    cleaned_question
                )

            st.session_state.last_result = result

        except Exception:

            st.error(
                "The Copilot could not process "
                "this request. Please try again."
            )


# =========================================================
# DISPLAY SIX-SECTION INVESTIGATION REPORT
# =========================================================

result = st.session_state.last_result

if result is not None:

    answer = str(
        result.get(
            "answer",
            "No answer returned.",
        )
    )

    sources = result.get(
        "sources",
        [],
    ) or []

    rejected = is_rejected_answer(answer)

    st.divider()

    st.header("🤖 AI Incident Investigation Report")

    st.caption(
        f"Question: {st.session_state.last_question}"
    )

    if rejected:

        st.warning(
            "The Copilot could not provide a validated "
            "answer for this question."
        )

        st.markdown(answer)

    else:

        st.success(
            "The RAG pipeline returned an investigation "
            "answer with supporting knowledge."
        )

    # =====================================================
    # 1. INCIDENT CORRELATION
    # =====================================================

    st.subheader("🔎 1. Incident Correlation")

    historical_incidents = get_historical_incidents(
        sources
    )

    if historical_incidents:

        st.write(
            "Historical incident records were retrieved "
            "from the knowledge base:"
        )

        for index, source in historical_incidents:

            st.markdown(
                f"**{source.get('title', 'Incident')}** "
                f"— [SOURCE {index}]"
            )

            st.caption(
                "Retrieved historical evidence; "
                "not confirmation of the current root cause."
            )

    else:

        st.info(
            "No matching historical incident record "
            "was retrieved for this question."
        )

    # =====================================================
    # 2. ROOT CAUSE ANALYSIS
    # =====================================================

    st.subheader("🎯 2. Root Cause Analysis")

    root_cause_sources = find_sections(
        sources,
        ["root cause", "causes"],
    )

    show_section_evidence(
        root_cause_sources,
        (
            "No dedicated root-cause section was "
            "retrieved. Review the investigation answer "
            "for any documented diagnostic findings."
        ),
    )

    # =====================================================
    # 3. TROUBLESHOOTING GUIDANCE
    # =====================================================

    st.subheader("🛠️ 3. Troubleshooting Guidance")

    if rejected:

        st.info(
            "Troubleshooting guidance was not returned "
            "because the pipeline did not provide "
            "a validated answer."
        )

    else:

        st.markdown(answer)

        st.caption(
            "Generated from retrieved knowledge. "
            "Follow operational change controls "
            "before making production changes."
        )

    # =====================================================
    # 4. RESOLUTION KNOWLEDGE
    # =====================================================

    st.subheader("✅ 4. Resolution Knowledge")

    resolution_sources = find_sections(
        sources,
        [
            "resolution",
            "remediation",
            "fix",
            "recovery",
        ],
    )

    show_section_evidence(
        resolution_sources,
        (
            "No dedicated resolution section was "
            "retrieved for this question. "
            "The knowledge base may contain "
            "investigation guidance without a "
            "documented previous fix."
        ),
    )

    # =====================================================
    # 5. SUPPORTING EVIDENCE
    # =====================================================

    st.subheader("📚 5. Supporting Evidence")

    st.caption(
        "Open each source to cross-check the retrieved "
        "information. Source numbers correspond to "
        "the citations in the Copilot response."
    )

    if not sources:

        st.info(
            "No source evidence was returned."
        )

    else:

        for index, source in enumerate(
            sources,
            start=1,
        ):

            title = source.get(
                "title",
                "Enterprise Document",
            )

            section = source.get(
                "section",
                "N/A",
            )

            with st.expander(
                f"[SOURCE {index}] "
                f"{title} — {section}"
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

                content = get_source_content(
                    source
                )

                if content:

                    st.markdown(
                        "**Retrieved passage:**"
                    )

                    st.text(content)

                else:

                    st.caption(
                        "Source content is unavailable."
                    )

                # Link only to a verified repository file.
                document_url = get_document_url(
                    source
                )

                if document_url:

                    st.link_button(
                        "🔗 View original document on GitHub",
                        document_url,
                    )

                else:

                    st.caption(
                        "Original document link unavailable. "
                        "Use the retrieved passage above "
                        "to cross-check this source."
                    )

    # =====================================================
    # 6. SECURITY & GROUNDING
    # =====================================================

    st.subheader("🛡️ 6. Security & Grounding")

    if rejected:

        st.warning(
            "The Copilot withheld an answer because "
            "a safety, grounding, or evidence check "
            "did not produce an acceptable response."
        )

    else:

        st.write(
            "The response was returned by the "
            "configured RAG pipeline."
        )

    st.write(
        "The application uses Bedrock Guardrails, "
        "retrieval confidence checks, contextual "
        "grounding, and citation validation."
    )

    if result.get("cache_hit", False):

        st.caption(
            "⚡ This response was served from cache."
        )

    st.caption(
        "The current grounding threshold is 0.50 "
        "for demonstration. This does not guarantee "
        "that every statement is correct or that "
        "the application is production ready."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

remaining = max(
    MAX_REQUESTS - st.session_state.request_count,
    0,
)

st.caption(
    f"Demo requests remaining: {remaining}/{MAX_REQUESTS}"
)

st.caption(
    "Enterprise Integration Knowledge & Incident Resolution "
    "RAG Copilot | Portfolio Project | Synthetic Data"
)
