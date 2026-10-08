\# 🤖 Enterprise Integration Knowledge \& Incident Resolution RAG Copilot



An enterprise-focused \*\*Retrieval-Augmented Generation (RAG)\*\* application that helps support teams investigate integration incidents using runbooks, architecture documents, operational procedures, policies, and historical incident knowledge.



The project demonstrates an end-to-end RAG workflow using \*\*Amazon Bedrock, Titan Text Embeddings V2, Claude Haiku, Python, FastAPI, Streamlit, automated testing, and quantitative retrieval evaluation\*\*.



> \*\*Portfolio Project:\*\* All enterprise documents, incidents, systems, and operational data in this repository are synthetic and created specifically for demonstration and learning.



\---



\## 🎯 Business Problem



Enterprise integration support teams often troubleshoot production issues across platforms such as:



\- Boomi

\- Axway API Gateway

\- Layer7 API Gateway

\- SFTP integrations

\- Databases

\- APIs and backend services



Useful troubleshooting knowledge may be distributed across runbooks, architecture documents, SOPs, policies, and historical incident records.



During a production incident, engineers may need to manually search multiple sources before determining:



\- What failed?

\- What should be investigated?

\- Has this happened before?

\- What was the previous root cause?

\- What remediation steps are recommended?

\- Which operational policy applies?



This project explores how \*\*RAG can turn distributed operational knowledge into a searchable AI-assisted troubleshooting experience.\*\*



\---



\## 💡 Example Use Case



A support engineer asks:



> \*\*PaymentService through Axway is returning HTTP 504. What should I investigate and have we seen this before?\*\*



The application:



1\. Converts the question into an embedding.

2\. Searches the enterprise knowledge chunks using semantic similarity.

3\. Retrieves the most relevant runbooks and historical incidents.

4\. Builds grounded context from the retrieved evidence.

5\. Sends only that context and the question to the LLM.

6\. Generates an operationally useful answer.

7\. Displays the supporting sources and retrieval scores.



This allows the engineer to investigate the issue using both \*\*documented troubleshooting guidance and historical incident knowledge\*\*.



\---



\## 🏗️ Architecture



```text

&#x20;                   ┌─────────────────────────────┐

&#x20;                   │       Streamlit UI          │

&#x20;                   │ Enterprise Integration      │

&#x20;                   │       AI Copilot            │

&#x20;                   └──────────────┬──────────────┘

&#x20;                                  │

&#x20;                                  ▼

&#x20;                   ┌─────────────────────────────┐

&#x20;                   │       RAG Pipeline          │

&#x20;                   │         ask\_rag()           │

&#x20;                   └──────────────┬──────────────┘

&#x20;                                  │

&#x20;                                  ▼

&#x20;                   ┌─────────────────────────────┐

&#x20;                   │ Amazon Titan Text           │

&#x20;                   │ Embeddings V2               │

&#x20;                   │ Query → 1024-d Vector       │

&#x20;                   └──────────────┬──────────────┘

&#x20;                                  │

&#x20;                                  ▼

&#x20;                   ┌─────────────────────────────┐

&#x20;                   │ Semantic Retrieval          │

&#x20;                   │ Cosine Similarity           │

&#x20;                   │ Top-K Knowledge Chunks      │

&#x20;                   └──────────────┬──────────────┘

&#x20;                                  │

&#x20;                                  ▼

&#x20;                   ┌─────────────────────────────┐

&#x20;                   │ Grounded Context Builder    │

&#x20;                   │ Retrieved Evidence          │

&#x20;                   └──────────────┬──────────────┘

&#x20;                                  │

&#x20;                                  ▼

&#x20;                   ┌─────────────────────────────┐

&#x20;                   │ Amazon Bedrock              │

&#x20;                   │ Claude Haiku                │

&#x20;                   │ Grounded Generation         │

&#x20;                   └──────────────┬──────────────┘

&#x20;                                  │

&#x20;                                  ▼

&#x20;                   ┌─────────────────────────────┐

&#x20;                   │ Answer + Source Citations   │

&#x20;                   │ + Retrieval Evidence        │

&#x20;                   └─────────────────────────────┘

```



The repository also includes a \*\*FastAPI REST interface\*\*, allowing the same reusable RAG pipeline to be consumed by applications other than Streamlit.



\---



\## 🧠 RAG Pipeline



```text

Enterprise Knowledge

&#x20;       ↓

Document Loading

&#x20;       ↓

Structure-Aware Chunking

&#x20;       ↓

Titan Embeddings

&#x20;       ↓

Persisted Chunk Vectors

&#x20;       ↓

User Question

&#x20;       ↓

Query Embedding

&#x20;       ↓

Cosine Similarity Search

&#x20;       ↓

Top-K Retrieval

&#x20;       ↓

Grounded Context

&#x20;       ↓

Claude Haiku

&#x20;       ↓

Answer + Citations

```



The LLM is explicitly instructed to answer using the retrieved context and to indicate when the supplied evidence is insufficient.



\---



\## 📚 Synthetic Enterprise Knowledge Base



The current knowledge corpus contains \*\*24 synthetic enterprise documents\*\* across five categories:



| Knowledge Type | Examples |

|---|---|

| Runbooks | Axway 504, Boomi failures, Layer7 OAuth, SFTP, certificates, database pools |

| Historical Incidents | Payment API 504, certificate expiry, database connectivity, SFTP failures |

| Architecture | Enterprise integration architecture, payment integration flow, middleware overview |

| Procedures | Production deployment, certificate rotation, disaster recovery, health checks |

| Policies | P1 escalation and change management |



The documents are transformed into:



\*\*76 metadata-rich retrieval chunks\*\*



Metadata is preserved so retrieved evidence remains traceable to its original document and section.



\---



\## 🔢 Embeddings



The project uses:



\*\*Amazon Titan Text Embeddings V2\*\*



Current configuration:



```text

Model: amazon.titan-embed-text-v2:0

Dimensions: 1024

Normalization: Enabled

AWS Region: ap-south-1

```



The same embedding model is used for both:



\- Enterprise knowledge chunks

\- User queries



This places both representations in the same vector space for semantic comparison.



\---



\## 🔎 Semantic Retrieval



The current learning baseline intentionally implements retrieval transparently using:



\- Persisted JSON embedding records

\- In-memory vector comparison

\- Cosine similarity

\- Top-K ranking



This makes the underlying RAG mechanics easy to inspect and understand before introducing a production-scale vector database.



> \*\*Important:\*\* The current implementation should not be interpreted as a production vector database architecture.



Future iterations can compare this baseline with technologies such as \*\*Amazon OpenSearch Serverless\*\* or other vector stores.



\---



\## 📊 RAG Evaluation



RAG quality is not evaluated only by whether an answer "looks good."



The project contains a \*\*golden evaluation dataset with 12 enterprise support questions\*\* and expected source documents.



\### Retrieval V1 Baseline



| Metric | Result |

|---|---:|

| Knowledge Documents | 24 |

| Retrieval Chunks | 76 |

| Golden Questions | 12 |

| Top-K | 5 |

| Average Recall@5 | \*\*90.28%\*\* |



This baseline is intentionally preserved so future changes can be measured objectively.



Planned experiments include:



\- Improved chunking

\- Metadata filtering

\- Hybrid search

\- Reranking

\- Retrieval quality comparison



\---



\## 💬 Grounded Generation



Retrieved evidence is assembled into structured context before generation.



The prompt instructs the LLM to:



\- Use only supplied context

\- Avoid inventing unsupported information

\- Provide practical troubleshooting steps

\- Mention relevant historical incidents when available

\- Cite retrieved sources

\- State when the available evidence is insufficient



Generation currently uses \*\*Claude Haiku through Amazon Bedrock\*\*.



\---



\## 🎨 Interactive Streamlit Application



The project includes an interactive \*\*Enterprise Integration AI Copilot\*\* interface.



Features include:



\- Natural-language incident questions

\- Example troubleshooting scenarios

\- AI-generated operational responses

\- Retrieved evidence

\- Expandable source information

\- Similarity scores

\- Knowledge-base statistics

\- Retrieval evaluation metrics

\- Synthetic-data disclosure



Example scenarios include:



\- Axway HTTP 504

\- Boomi post-deployment failure

\- Layer7 HTTP 401 after an IdP change

\- SFTP host-key change



\---



\## ⚡ FastAPI Interface



The RAG pipeline is also exposed through a REST API.



Available endpoints:



```text

GET  /health

POST /ask

```



Example request:



```json

{

&#x20; "question": "Why is Axway returning HTTP 504?"

}

```



The API returns:



\- Original question

\- Grounded answer

\- Retrieved source metadata

\- Similarity scores



Internal 1024-dimensional embedding vectors are intentionally \*\*not exposed through the API response\*\*.



\---



\## 🧪 Automated Testing



The project currently contains \*\*20 automated tests\*\* covering:



\- Corpus validation

\- Document metadata

\- Chunk generation

\- Chunk uniqueness

\- Embedding input validation

\- Grounding prompt construction

\- Context generation

\- RAG pipeline validation

\- FastAPI health endpoint

\- FastAPI question endpoint

\- API response contract



Current regression status:



```text

20 passed

```



External AI calls are mocked where appropriate in API unit tests to keep testing deterministic and avoid unnecessary model invocation costs.



\---



\## 🛠️ Technology Stack



| Area | Technology |

|---|---|

| Programming | Python 3.12 |

| Cloud | AWS |

| Embeddings | Amazon Titan Text Embeddings V2 |

| Generative AI | Claude Haiku via Amazon Bedrock |

| Retrieval | Cosine similarity / Top-K semantic search |

| API | FastAPI |

| UI | Streamlit |

| Testing | Pytest |

| AWS SDK | Boto3 |

| Version Control | Git / GitHub |



\---



\## 📁 Repository Structure



```text

enterprise-rag-copilot-v1/

│

├── data/

│   ├── knowledge/

│   ├── evaluation/

│   └── embeddings/

│

├── docs/

│

├── scripts/

│   ├── embed\_corpus.py

│   ├── evaluate\_retrieval.py

│   ├── evaluate\_retrieval\_full.py

│   ├── inspect\_chunks.py

│   └── rag\_generation\_demo.py

│

├── src/

│   ├── api.py

│   ├── chunking.py

│   ├── documents.py

│   ├── embeddings.py

│   ├── generation.py

│   ├── rag\_pipeline.py

│   ├── retrieval.py

│   └── streamlit\_app.py

│

├── tests/

│

├── requirements.txt

└── README.md

```



\---



\## 🚀 Running Locally



\### 1. Create a virtual environment



```powershell

python -m venv .venv

```



\### 2. Activate it



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```powershell

python -m pip install -r requirements.txt

```



\### 4. Configure AWS access



The application uses the standard AWS credential provider chain through Boto3.



\*\*Never store AWS access keys in this repository.\*\*



The AWS identity used to run the application must have the required Amazon Bedrock permissions.



\### 5. Run automated tests



```powershell

python -m pytest -v

```



\### 6. Start the Streamlit application



```powershell

python -m streamlit run .\\src\\streamlit\_app.py

```



\### 7. Start the FastAPI service



```powershell

python -m uvicorn src.api:app --reload

```



FastAPI documentation is then available through the local `/docs` endpoint.



\---



\## 🔐 Security Principles



This portfolio project follows several basic security practices:



\- No AWS credentials are committed to the repository

\- `.env` is excluded through `.gitignore`

\- Synthetic data is used instead of confidential enterprise information

\- Internal embedding vectors are not exposed through the API

\- AWS access is handled through the standard credential provider mechanism



Additional controls will be required before exposing the application as a public production service.



\---



\## 💰 Cost Awareness



The project was designed with cost-conscious experimentation in mind.



Examples include:



\- Lightweight synthetic corpus

\- Pre-generated knowledge embeddings

\- Top-K retrieval

\- Claude Haiku for generation

\- Mocked AI calls during API unit testing

\- Avoiding repeated embedding generation during normal question answering



A public deployment should additionally implement usage controls, monitoring, and safeguards against uncontrolled model invocation.



\---



\## 🗺️ Roadmap



\### Completed



\- \[x] Synthetic enterprise knowledge corpus

\- \[x] Document ingestion

\- \[x] Structure-aware chunking

\- \[x] Amazon Titan embeddings

\- \[x] Persisted vector representations

\- \[x] Semantic retrieval

\- \[x] Golden-question evaluation dataset

\- \[x] Retrieval Recall@5 baseline

\- \[x] Grounded Bedrock generation

\- \[x] Source citations

\- \[x] Reusable RAG orchestration

\- \[x] FastAPI REST interface

\- \[x] Interactive Streamlit UI

\- \[x] Automated regression testing

\- \[x] GitHub version control



\### Next



\- \[ ] Public demo deployment with security and cost controls

\- \[ ] Metadata filtering

\- \[ ] Hybrid retrieval

\- \[ ] Reranking

\- \[ ] Retrieval V2 evaluation

\- \[ ] Production vector-store comparison

\- \[ ] Observability and monitoring

\- \[ ] IAM hardening

\- \[ ] Optional ServiceNow workflow integration



\---



\## 🎓 Key Engineering Learnings



This project is intentionally built in stages rather than hiding the RAG mechanics behind a fully managed abstraction.



Key areas explored include:



\- Enterprise document ingestion

\- Metadata preservation

\- Chunking strategy

\- Embedding generation

\- Vector similarity

\- Semantic retrieval

\- Grounding

\- Prompt construction

\- Source attribution

\- Retrieval evaluation

\- API design

\- AI application testing

\- AWS Bedrock integration

\- Cost-conscious AI engineering

\- Separation of reusable AI logic from UI/API layers



The goal is not only to build an AI chatbot, but to understand \*\*how an enterprise RAG system retrieves, evaluates, grounds, exposes, and governs knowledge.\*\*



\---



\## ⚠️ Disclaimer



This repository is a \*\*learning and portfolio project\*\*.



All company names, incidents, runbooks, architectures, operational scenarios, and support records used by the project are synthetic or fictitious.



The application should not be considered production-ready without additional work around authentication, authorization, scalable vector storage, rate limiting, monitoring, data governance, security controls, resilience, and operational support.



\---



\## 👤 Project Focus



\*\*Enterprise Integration + AI/ML + Retrieval-Augmented Generation + AWS\*\*



Designed to demonstrate how enterprise integration and production-support experience can be combined with modern AI engineering techniques to build practical operational copilots.

