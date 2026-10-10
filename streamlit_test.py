
import json
from pathlib import Path
from urllib.parse import quote

import streamlit as st


# =========================================================
# CONFIGURATION — NO AWS OR BEDROCK IMPORTS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

CACHE_FILE = (
    BASE_DIR / "data" / "demo_cache" / "demo_answers.json"
)

KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"

GITHUB_REPOSITORY = (
    "rudragowdamt/enterprise-rag-copilot-v1"
)

GITHUB_BRANCH = "v2-demo-cache-only"


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Enterprise Integration RAG Copilot",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# LOAD PRE-GENERATED RAG RESULTS
# =========================================================

@st.cache_data
def load_demo_data():
    """
    Read a local JSON file only.

    This function never connects to AWS.
    """

    if not CACHE_FILE.is_file():
        return []

    try:
        with CACHE_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            payload = json.load(file)

        if payload.get("demo_mode") != "cache_only":
            return []

        questions = payload.get("questions", [])

        if not isinstance(questions, list):
            return []

        return [
            item
            for item in questions
            if isinstance(item, dict)
            and item.get("question")
            and item.get("answer")
        ]

    except (OSError, ValueError, TypeError):
        return []


# =========================================================
# SAFE DOCUMENT LINKS
# =========================================================

def find_original_document(source):
    """
    Locate a document inside data/knowledge.

    Only known local Markdown files are eligible.
    The file must have a unique matching path or name.
    """

    if not KNOWLEDGE_DIR.is_dir():
        return None

    raw_path = str(
        source.get("source") or ""
    ).replace("\\", "/").strip()

    if not raw_path:
        return None

    knowledge_root = KNOWLEDGE_DIR.resolve()

    # First try a repository-relative source path.
    candidate = (BASE_DIR / raw_path).resolve()

    if (
        candidate.is_file()
        and candidate.suffix.lower() == ".md"
        and candidate.is_relative_to(knowledge_root)
    ):
        return candidate

    # Some cached sources store only a filename.
    # Match only when that filename is unique.
    filename = raw_path.split("/")[-1]

    if not filename.lower().endswith(".md"):
        return None

    matches = [
        path.resolve()
        for path in KNOWLEDGE_DIR.rglob("*.md")
        if path.name.lower() == filename.lower()
    ]

    if len(matches) == 1:
        return matches[0]

    return None


def get_github_document_url(source):
    """
    Create a GitHub URL only for a verified local file.
    """

    document_path = find_original_document(source)

    if document_path is None:
        return None

    relative_path = document_path.relative_to(
        BASE_DIR.resolve()
    )

    encoded_path = quote(
        relative_path.as_posix(),
        safe="/",
    )

    return (
        f"https://github.com/"
        f"{GITHUB_REPOSITORY}/blob/"
        f"{GITHUB_BRANCH}/{encoded_path}"
    )


# =========================================================
# STYLING
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
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🤖 Enterprise Integration RAG Copilot'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Enterprise incident investigation, troubleshooting '
    'and knowledge retrieval'
    '</div>',
    unsafe_allow_html=True,
)

st.info(
    "Explore previously generated RAG investigations "
    "using synthetic enterprise integration knowledge. "
    "Each answer was generated during preparation and "
    "saved with its retrieved source evidence."
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("RAG Copilot V2")

    st.write("🧠 Amazon Bedrock")
    st.write("🔢 Titan Text Embeddings V2")
    st.write("💬 Claude Haiku 4.5")
    st.write("🔎 Knowledge Retrieval")
    st.write("🎨 Streamlit")

    st.divider()

    st.subheader("Demonstration Mode")

    st.success("Cache-only mode")

    st.write(
        "No live AI inference or AWS requests "
        "are performed by this application."
    )

    st.divider()

    st.write("📄 24 knowledge documents")
    st.write("🎯 Pre-generated RAG responses")

    st.divider()

    st.caption(
        "Portfolio demonstration using synthetic data."
    )


# =========================================================
# LOAD QUESTION BANK
# =========================================================

questions = load_demo_data()

if not questions:

    st.error(
        "The demonstration question bank is unavailable. "
        "Check data/demo_cache/demo_answers.json."
    )

    st.stop()


# =========================================================
# QUESTION DROPDOWN
# =========================================================

st.subheader("🔍 Investigate an Integration Issue")

st.write(
    "Choose an investigation scenario to explore "
    "how RAG uses enterprise knowledge."
)

question_labels = [
    item.get(
        "label",
        item["question"],
    )
    for item in questions
]

selected_index = st.selectbox(
    "Select an investigation scenario",
    options=range(len(questions)),
    format_func=lambda index: question_labels[index],
)

selected_item = questions[selected_index]

question = selected_item["question"]
answer = str(selected_item["answer"])

sources = selected_item.get(
    "sources",
    [],
)

if not isinstance(sources, list):
    sources = []


st.text_area(
    "Investigation question",
    value=question,
    height=105,
    disabled=True,
)

st.caption(
    f"{len(questions)} predefined investigation questions "
    "available."
)


# =========================================================
# SHOW CACHED ANSWER
# =========================================================

if st.button(
    "🔍 View Investigation",
    type="primary",
    use_container_width=True,
):

    st.session_state["show_demo_answer"] = True
    st.session_state["selected_demo_index"] = selected_index


# Do not display an old answer after changing the question.
show_answer = (
    st.session_state.get("show_demo_answer", False)
    and st.session_state.get(
        "selected_demo_index"
    ) == selected_index
)


if show_answer:

    st.divider()

    st.success(
        "Previously generated RAG investigation retrieved "
        "from the local demonstration cache."
    )

    # =====================================================
    # COPILOT RESPONSE
    # =====================================================

    st.header("🤖 Copilot Investigation")

    st.markdown(answer)

    st.caption(
        "This response was generated previously using "
        "the RAG pipeline. No AI model was called "
        "to display this answer."
    )


    # =====================================================
    # EVIDENCE
    # =====================================================

    st.divider()

    st.subheader("📚 Supporting Evidence")

    st.write(
        "Review the knowledge passages retrieved "
        "during the original RAG execution."
    )

    st.caption(
        "Source numbers correspond to citations "
        "in the saved answer."
    )

    if not sources:

        st.warning(
            "No supporting sources were stored "
            "for this response."
        )

    else:

        st.write(
            f"**{len(sources)} retrieved knowledge chunks**"
        )

        for index, source in enumerate(
            sources,
            start=1,
        ):

            title = str(
                source.get(
                    "title",
                    "Enterprise Document",
                )
            )

            section = str(
                source.get(
                    "section",
                    "Unknown Section",
                )
            )

            with st.expander(
                f"[SOURCE {index}] "
                f"{title} — {section}"
            ):

                st.markdown(
                    f"**Document:** {title}"
                )

                st.markdown(
                    f"**Section:** {section}"
                )

                st.write(
                    "**Document ID:**",
                    source.get(
                        "document_id",
                        "N/A",
                    ),
                )

                content = source.get(
                    "content",
                    "",
                )

                if content:

                    st.markdown(
                        "**Retrieved source passage:**"
                    )

                    st.text(str(content))

                else:

                    st.caption(
                        "The original passage was not "
                        "included in the saved response."
                    )

                score = source.get(
                    "similarity_score",
                )

                if score is not None:

                    try:
                        st.caption(
                            "Semantic similarity: "
                            f"{float(score):.4f}"
                        )
                    except (TypeError, ValueError):
                        pass

                github_url = get_github_document_url(
                    source
                )

                if github_url:

                    st.link_button(
                        "🔗 View original document on GitHub",
                        github_url,
                    )

                else:

                    st.caption(
                        "Original document link unavailable; "
                        "review the saved source passage above."
                    )


    # =====================================================
    # RAG CONCEPT
    # =====================================================

    st.divider()

    st.subheader("🧠 How RAG Produced This Answer")

    st.markdown(
        """
        **1. Knowledge base:** Enterprise integration
        documents and historical incident runbooks.

        **2. Retrieval:** Vector embeddings were used
        to find relevant document passages.

        **3. Generation:** Amazon Bedrock and Claude
        generated an answer using the retrieved context.

        **4. Evidence:** Retrieved passages were saved
        alongside the answer for cross-checking.

        **5. Demonstration:** The previously generated
        answer is displayed directly from local JSON,
        without any live AWS calls.
        """
    )

    st.warning(
        "This is a pre-generated demonstration, "
        "not a live AI chatbot. The presence of citations "
        "does not independently guarantee every claim "
        "is correct."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Enterprise Integration Knowledge & Incident Resolution "
    "RAG Copilot | V2 Cached Demonstration"
)

st.caption(
    "Synthetic data | Pre-generated answers | "
    "No live AWS inference"
)
