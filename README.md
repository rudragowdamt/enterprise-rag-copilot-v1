# 🤖 Enterprise Integration Knowledge & Incident Resolution RAG Copilot

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-Bedrock-orange)](https://aws.amazon.com/bedrock/)
[![RAG](https://img.shields.io/badge/AI-RAG-purple)](#)
[![Tests](https://img.shields.io/badge/Tests-23%20Passed-brightgreen)](#)
[![Recall](https://img.shields.io/badge/Recall%405-90.28%25-brightgreen)](#)
[![Demo](https://img.shields.io/badge/Live-Demo-success)](https://enterprise-rag-copilot-v1-38ekag5apcyv6vjwsa6x4a.streamlit.app/)

> **Live Demo:**  
> https://enterprise-rag-copilot-v1-38ekag5apcyv6vjwsa6x4a.streamlit.app/

An enterprise-focused **Retrieval-Augmented Generation (RAG)** application that helps support teams investigate integration incidents using runbooks, architecture documents, operational procedures, policies, and historical incident knowledge.

The project demonstrates an end-to-end AI engineering workflow using **Amazon Bedrock, Titan Text Embeddings V2, Claude Haiku 4.5, Python, FastAPI, Streamlit, caching, automated testing, retrieval evaluation, security controls, and public cloud deployment**.

> **Portfolio Project:** All enterprise documents, incidents, systems, runbooks, and operational data in this repository are synthetic and were created specifically for demonstration and learning.

---

## 🚀 Live Application

The Enterprise Integration AI Copilot is publicly deployed using Streamlit Community Cloud.

### 👉 [Launch the Enterprise Integration AI Copilot](https://enterprise-rag-copilot-v1-38ekag5apcyv6vjwsa6x4a.streamlit.app/)

The live application allows users to:

- Ask enterprise integration support questions
- Try predefined troubleshooting scenarios
- Retrieve semantically relevant enterprise knowledge
- Generate grounded AI responses using Amazon Bedrock
- Inspect retrieved evidence
- View source metadata and similarity scores
- Observe whether a response was generated fresh or served from cache

The public demo also includes basic usage guardrails such as request limits, cooldown controls, and input-length validation.

---

## 🎯 Business Problem

Enterprise integration support teams frequently troubleshoot production issues across platforms such as:

- Boomi
- Axway API Gateway
- Layer7 API Gateway
- SFTP integrations
- Databases
- APIs
- Backend services

Operational knowledge is often distributed across:

- Runbooks
- Architecture documents
- Standard operating procedures
- Policies
- Historical incident records
- Troubleshooting documentation

During a production incident, engineers may need to manually search multiple sources before determining:

- What failed?
- What should be investigated?
- Has this happened before?
- What was the previous root cause?
- What remediation steps are recommended?
- Which operational policy applies?

This project demonstrates how **RAG can convert distributed operational knowledge into an AI-assisted incident investigation experience**.

---

## 💡 Example Use Case

A support engineer asks:

> **PaymentService through Axway is returning HTTP 504. What should I investigate and have we seen this before?**

The application:

1. Normalizes and checks the request cache.
2. Converts a new question into an embedding using Amazon Titan.
3. Searches enterprise knowledge chunks using semantic similarity.
4. Retrieves the most relevant runbooks and historical incidents.
5. Builds grounded context from the retrieved evidence.
6. Sends the context and question to Claude through Amazon Bedrock.
7. Generates an operational troubleshooting response.
8. Displays supporting sources and similarity scores.
9. Stores the completed result in the cache for repeated requests.

This allows an engineer to investigate an issue using both **documented troubleshooting guidance and historical incident knowledge**.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────────────┐
                    │       Streamlit UI          │
                    │ Enterprise Integration      │
                    │       AI Copilot            │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │      Request Guardrails     │
                    │ Limit / Cooldown / Length   │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       RAG Pipeline          │
                    │         ask_rag()           │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       Result Cache          │
                    │     HIT          MISS       │
                    └──────┬────────────┬─────────┘
                           │            │
                      HIT  │            │ MISS
                           │            ▼
                           │  ┌──────────────────────────┐
                           │  │ Titan Text Embeddings V2 │
                           │  │ Query → 1024-d Vector    │
                           │  └────────────┬─────────────┘
                           │               │
                           │               ▼
                           │  ┌──────────────────────────┐
                           │  │ Semantic Retrieval       │
                           │  │ Cosine Similarity        │
                           │  │ Top-K Knowledge Chunks   │
                           │  └────────────┬─────────────┘
                           │               │
                           │               ▼
                           │  ┌──────────────────────────┐
                           │  │ Grounded Context Builder │
                           │  │ Retrieved Evidence       │
                           │  └────────────┬─────────────┘
                           │               │
                           │               ▼
                           │  ┌──────────────────────────┐
                           │  │ Amazon Bedrock           │
                           │  │ Claude Haiku 4.5         │
                           │  │ Grounded Generation      │
                           │  └────────────┬─────────────┘
                           │               │
                           └───────────────┤
                                           ▼
                              ┌──────────────────────────┐
                              │ Answer + Evidence        │
                              │ + Source Metadata        │
                              └──────────────────────────┘
```

The same reusable RAG pipeline is also exposed through a **FastAPI REST interface**, allowing the AI capability to be consumed independently of the Streamlit UI.

---

## 🧠 End-to-End RAG Pipeline

```text
Synthetic Enterprise Knowledge
          ↓
Document Loading
          ↓
Structure-Aware Chunking
          ↓
Titan Text Embeddings V2
          ↓
Persisted Chunk Vectors
          ↓
User Question
          ↓
Cache Lookup
     ↙          ↘
 Cache HIT     Cache MISS
     ↓             ↓
Return Saved    Query Embedding
Result             ↓
              Cosine Similarity
                    ↓
              Top-K Retrieval
                    ↓
              Grounded Context
                    ↓
              Claude Haiku 4.5
                    ↓
              Answer + Evidence
                    ↓
                 Cache
```

The LLM is explicitly instructed to answer using the supplied context and indicate when the available evidence is insufficient.

---

## 📚 Synthetic Enterprise Knowledge Base

The knowledge corpus contains **24 synthetic enterprise documents** across multiple operational knowledge categories.

| Knowledge Type | Examples |
|---|---|
| Runbooks | Axway 504, Boomi failures, Layer7 OAuth, SFTP, certificates, database pools |
| Historical Incidents | Payment API 504, certificate expiry, database connectivity, SFTP failures |
| Architecture | Enterprise integration architecture, payment integration flow, middleware overview |
| Procedures | Production deployment, certificate rotation, disaster recovery, health checks |
| Policies | P1 escalation and change management |

The documents are transformed into:

**76 metadata-rich retrieval chunks**

Metadata is preserved so retrieved evidence remains traceable to its original document and section.

---

## 🔢 Embeddings

The project uses:

**Amazon Titan Text Embeddings V2**

Configuration:

```text
Model: amazon.titan-embed-text-v2:0
Dimensions: 1024
Normalization: Enabled
AWS Region: ap-south-1
```

The same embedding model is used for:

- Enterprise knowledge chunks
- User questions

This places both representations in the same vector space for semantic comparison.

---

## 🔎 Semantic Retrieval

The current learning baseline intentionally implements retrieval transparently using:

- Persisted JSON embedding records
- In-memory vector comparison
- Cosine similarity
- Top-K ranking

This makes the underlying RAG mechanics easy to inspect and understand before introducing a managed vector database.

> **Important:** The current implementation is intentionally a learning baseline and should not be interpreted as a production-scale vector database architecture.

Future iterations can compare this implementation with technologies such as Amazon OpenSearch Serverless or other vector stores.

---

## 📊 Quantitative RAG Evaluation

RAG quality is not evaluated only by whether an answer appears reasonable.

The project includes a **golden evaluation dataset containing 12 enterprise support questions** and expected source documents.

### Retrieval V1 Baseline

| Metric | Result |
|---|---:|
| Knowledge Documents | 24 |
| Retrieval Chunks | 76 |
| Golden Questions | 12 |
| Top-K | 5 |
| **Average Recall@5** | **90.28%** |

The Retrieval V1 baseline is intentionally preserved so future retrieval changes can be compared objectively.

Future experiments can evaluate:

- Improved chunking
- Metadata filtering
- Hybrid search
- Reranking
- Retrieval V2
- Production vector-store alternatives

---

## 💬 Grounded Generation

Retrieved evidence is assembled into structured context before generation.

The generation prompt instructs the LLM to:

- Use supplied context
- Avoid inventing unsupported information
- Provide practical troubleshooting guidance
- Mention relevant historical incidents when available
- Cite retrieved sources
- State when available evidence is insufficient

Generation uses **Claude Haiku 4.5 through Amazon Bedrock**.

The application uses a Bedrock inference profile to invoke the generation model.

---

## ⚡ Persistent RAG Cache

The application includes a lightweight file-based result cache.

The flow is:

```text
Question
   ↓
Normalize
   ↓
Create Cache Key
   ↓
Cache Lookup
   ↓
 ┌───────────────┐
 │               │
HIT             MISS
 │               │
 ▼               ▼
Return       Titan Embedding
Saved             ↓
Result         Retrieval
                  ↓
               Claude
                  ↓
             Save Result
                  ↓
             Return Result
```

Question normalization includes:

- Lowercasing
- Leading/trailing whitespace removal
- Collapsing repeated whitespace

Therefore semantically identical input formatting can reuse the same cached result.

### Why caching matters

A cache hit bypasses both:

- Titan query embedding invocation
- Claude generation invocation

This reduces:

- Repeated AWS model calls
- Response latency
- Demo operating cost
- Unnecessary model consumption

Embedding vectors are removed before the completed RAG result is stored in the response cache.

This reduced the size of one tested cached response from approximately **164 KB to 4.7 KB**, a reduction of roughly **97%**.

> The current file-based cache is appropriate for this portfolio demonstration. A production architecture would use a shared and durable caching mechanism.

---

## 🎨 Interactive Streamlit Application

The project includes a publicly deployed **Enterprise Integration AI Copilot**.

### Example scenarios

Users can immediately test scenarios including:

- Axway HTTP 504
- Boomi post-deployment failure
- Layer7 HTTP 401 after an IdP change
- SFTP host-key change

### UI capabilities

The application displays:

- Natural-language support question
- Grounded AI response
- Cache HIT/FRESH status
- Retrieved evidence
- Source document ID
- Chunk ID
- Document section
- Similarity score
- Knowledge-base statistics
- Recall@5 evaluation metric
- Synthetic-data disclosure

### Public Demo Guardrails

The public application includes lightweight controls:

```text
Maximum requests per session: 10
Request cooldown: 5 seconds
Maximum question length: 500 characters
```

These controls complement AWS-side cost and permission controls.

> Session-based limits are demonstration safeguards and are not equivalent to production identity-based rate limiting.

---

## ⚡ FastAPI Interface

The reusable RAG pipeline is also exposed through a REST API.

Available endpoints:

```text
GET  /health
POST /ask
```

Example request:

```json
{
  "question": "Why is Axway returning HTTP 504?"
}
```

The API returns:

- Original question
- Grounded answer
- Retrieved source metadata
- Similarity scores
- Cache status

Internal **1024-dimensional embedding vectors are intentionally not exposed through the API response**.

This keeps internal vector representations behind the application boundary.

---

## 🧪 Automated Testing

The project currently contains **23 automated tests**.

Coverage includes:

- Corpus validation
- Document metadata
- Chunk generation
- Chunk uniqueness
- Embedding input validation
- Grounding prompt construction
- Context generation
- RAG pipeline validation
- Cache normalization
- Cache-key generation
- Cache HIT behavior
- Verification that cached responses bypass model calls
- FastAPI health endpoint
- FastAPI question endpoint
- API response contract

Current regression status:

```text
23 passed
```

External AI calls are mocked where appropriate to:

- Keep unit tests deterministic
- Avoid unnecessary Amazon Bedrock calls
- Reduce test execution cost
- Isolate application logic from external services

A known non-blocking Starlette/httpx deprecation warning is currently retained for dependency compatibility and can be addressed in a future dependency upgrade.

---

## 🔐 Security Design

The project applies several security practices appropriate for a public portfolio demonstration.

### Repository Security

- AWS credentials are not committed
- `.env` is excluded
- Streamlit secrets are excluded
- Runtime cache files are excluded
- Account-specific IAM policy files are excluded
- Synthetic enterprise data is used
- Internal embedding vectors are not exposed through API responses

### AWS Access

A dedicated AWS IAM identity is used for the public demonstration rather than broad administrator permissions.

The identity is restricted to the Amazon Bedrock resources required for:

- Titan embedding invocation
- Claude inference-profile invocation

Broad permissions such as `AmazonBedrockFullAccess` are intentionally avoided for the demo identity.

### Streamlit Secrets

AWS credentials required by the hosted demonstration are stored using Streamlit's secret-management mechanism rather than source code or GitHub.

> For production AWS hosting, IAM roles and temporary credentials would be preferred over long-lived static access keys.

---

## 💰 Cost Controls

The application was designed with cost-conscious AI engineering in mind.

Controls include:

- Small synthetic knowledge corpus
- Pre-generated document embeddings
- Lightweight Top-K retrieval
- Claude Haiku 4.5 for generation
- Persistent RAG result caching
- Cache HIT bypass of Titan and Claude calls
- Mocked external AI calls during unit tests
- 10-request Streamlit session limit
- 5-second request cooldown
- 500-character question limit
- Dedicated least-privilege IAM identity
- AWS Budget monitoring

An AWS monthly budget is configured with cost notifications.

> AWS Budget alerts provide monitoring and notifications; they are **not a hard spending cap**.

---

## 🛠️ Technology Stack

| Area | Technology |
|---|---|
| Programming | Python 3.12 |
| Cloud | AWS |
| AI Platform | Amazon Bedrock |
| Embeddings | Amazon Titan Text Embeddings V2 |
| Embedding Dimension | 1024 |
| Generative AI | Claude Haiku 4.5 |
| Retrieval | Cosine similarity / Top-K semantic search |
| Orchestration | Custom Python RAG pipeline |
| Cache | File-based normalized-question cache |
| API | FastAPI |
| UI | Streamlit |
| Deployment | Streamlit Community Cloud |
| Testing | Pytest |
| AWS SDK | Boto3 |
| Version Control | Git / GitHub |

---

## 📁 Repository Structure

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
│   ├── embed_corpus.py
│   ├── evaluate_retrieval.py
│   ├── evaluate_retrieval_full.py
│   ├── inspect_chunks.py
│   └── rag_generation_demo.py
│
├── src/
│   ├── api.py
│   ├── cache.py
│   ├── chunking.py
│   ├── documents.py
│   ├── embeddings.py
│   ├── generation.py
│   ├── rag_pipeline.py
│   └── retrieval.py
│
├── tests/
│
├── streamlit_test.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Running Locally

### 1. Clone the repository

```powershell
git clone https://github.com/rudragowdamt/enterprise-rag-copilot-v1.git
cd enterprise-rag-copilot-v1
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Configure AWS access

The application uses Boto3's AWS credential provider mechanism.

**Never store AWS access keys in this repository.**

The AWS identity used to run the application must have permission to invoke the required Amazon Bedrock embedding and generation resources.

### 6. Run automated tests

```powershell
python -m pytest -q
```

Expected regression result:

```text
23 passed
```

### 7. Start the Streamlit application

```powershell
python -m streamlit run .\streamlit_test.py
```

### 8. Start the FastAPI service

```powershell
python -m uvicorn src.api:app --reload
```

FastAPI documentation is then available through the local `/docs` endpoint.

---

## 🌐 Public Deployment

The portfolio application is deployed using **Streamlit Community Cloud**.

Deployment configuration:

```text
Repository:
rudragowdamt/enterprise-rag-copilot-v1

Branch:
main

Application entry point:
streamlit_test.py

Python:
3.12
```

Sensitive AWS configuration is supplied through Streamlit Secrets and is not stored in GitHub.

### Live Application

👉 **https://enterprise-rag-copilot-v1-38ekag5apcyv6vjwsa6x4a.streamlit.app/**

---

## 🛡️ Defense in Depth for the Public Demo

The demo does not rely on a single cost or security mechanism.

```text
User
 ↓
Streamlit Input Validation
 ↓
500 Character Limit
 ↓
5 Second Cooldown
 ↓
10 Request Session Limit
 ↓
RAG Cache
 ↓
Least-Privilege AWS IAM
 ↓
Amazon Bedrock
 ↓
AWS Budget Monitoring
```

Each layer addresses a different concern:

| Control | Purpose |
|---|---|
| Input length | Limits oversized requests |
| Cooldown | Reduces rapid repeated submission |
| Session quota | Limits casual demo usage |
| Cache | Avoids duplicate Bedrock work |
| IAM | Restricts AWS capabilities |
| Budget | Provides cost visibility and alerts |

---

## 🗺️ Project Status

### Completed

- [x] Synthetic enterprise knowledge corpus
- [x] Document ingestion
- [x] Structure-aware chunking
- [x] Amazon Titan embeddings
- [x] 1024-dimensional vector representations
- [x] Persisted embeddings
- [x] Semantic retrieval
- [x] Golden-question evaluation dataset
- [x] Retrieval Recall@5 baseline
- [x] 90.28% average Recall@5
- [x] Grounded Bedrock generation
- [x] Source attribution
- [x] Reusable RAG orchestration
- [x] FastAPI REST interface
- [x] Interactive Streamlit UI
- [x] Persistent RAG cache
- [x] Automated cache tests
- [x] 23-test regression suite
- [x] Public Streamlit deployment
- [x] Public demo request guardrails
- [x] Dedicated least-privilege AWS identity
- [x] Streamlit secret management
- [x] AWS Budget monitoring
- [x] GitHub security cleanup

### Potential Next Iterations

- [ ] Metadata filtering
- [ ] Hybrid retrieval
- [ ] Reranking
- [ ] Retrieval V2 evaluation
- [ ] Managed vector-store comparison
- [ ] Application authentication
- [ ] Production-grade rate limiting
- [ ] Centralized observability
- [ ] IAM-role-based AWS deployment
- [ ] Optional ServiceNow workflow integration

---

## 🎓 Key Engineering Learnings

This project was intentionally built in stages rather than hiding the RAG mechanics behind a fully managed abstraction.

Key areas explored include:

- Enterprise document ingestion
- Metadata preservation
- Structure-aware chunking
- Embedding generation
- Vector similarity
- Semantic retrieval
- Grounded generation
- Prompt construction
- Source attribution
- Retrieval evaluation
- Cache design
- API design
- AI application testing
- AWS Bedrock integration
- IAM least privilege
- Secret management
- Public AI application guardrails
- Cost-conscious AI engineering
- Separation of reusable AI logic from UI/API layers
- Cloud deployment troubleshooting

A central engineering lesson from the project is that a useful enterprise RAG solution is not simply:

```text
Documents → LLM
```

It is an engineered system:

```text
Knowledge
   ↓
Chunking
   ↓
Embeddings
   ↓
Retrieval
   ↓
Evaluation
   ↓
Grounding
   ↓
Generation
   ↓
Caching
   ↓
API / UI
   ↓
Testing
   ↓
Security
   ↓
Cost Controls
   ↓
Deployment
```

The goal was therefore not only to build an AI chatbot, but to understand **how an enterprise RAG system retrieves, evaluates, grounds, exposes, secures, caches, and governs knowledge**.

---

## 🧩 Why This Project Matters

Enterprise AI solutions need more than LLM access.

A production-oriented RAG solution requires thinking about:

- Knowledge quality
- Retrieval accuracy
- Grounding
- Hallucination reduction
- Traceability
- Testing
- Security
- Cost
- API boundaries
- Deployment
- Operational controls

This project applies those concepts to a realistic enterprise integration and production-support domain.

---

## ⚠️ Disclaimer

This repository is a **learning and portfolio project**.

All company names, incidents, runbooks, architectures, operational scenarios, and support records used by the project are synthetic or fictitious.

The public application is intended for demonstration purposes only.

A production deployment would require additional capabilities including:

- Authentication
- Authorization
- Identity-based rate limiting
- Durable distributed caching
- Scalable vector storage
- Centralized monitoring
- Audit logging
- Data governance
- Resilience
- Secrets rotation
- Production IAM roles
- Operational support

---

## 👤 Project Focus

**Enterprise Integration + Production Support + AI/ML + Retrieval-Augmented Generation + AWS**

Designed to demonstrate how deep enterprise integration and production-support knowledge can be combined with modern AI engineering techniques to build practical operational copilots.

---

## 🔗 Links

**Live Demo:**  
https://enterprise-rag-copilot-v1-38ekag5apcyv6vjwsa6x4a.streamlit.app/

**GitHub Repository:**  
https://github.com/rudragowdamt/enterprise-rag-copilot-v1

---

⭐ If you find this enterprise RAG implementation useful, feel free to explore the repository and live demonstration.