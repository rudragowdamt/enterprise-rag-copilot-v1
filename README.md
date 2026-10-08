# Enterprise Knowledge & Incident Resolution RAG Copilot

A staged portfolio project for learning and demonstrating enterprise Retrieval-Augmented Generation (RAG), AWS, AI/ML, evaluation, and production engineering.

## Business problem
Enterprise support teams lose time searching runbooks, SOPs, architecture notes, policies, knowledge articles, and historical incidents. This copilot retrieves approved internal knowledge and generates grounded answers with evidence.

## Stage roadmap
1. Foundation & corpus (this package)
2. Chunking + local baseline retrieval
3. AWS Bedrock embeddings + vector search
4. RAG generation + citations + guardrails
5. Retrieval evaluation + ML relevance experiments
6. Advanced RAG: metadata filters, hybrid retrieval, reranking
7. FastAPI + Streamlit enterprise UI
8. AWS deployment, observability, security and cost controls
9. Optional ServiceNow/action integration

## Stage 1 objective
Understand the enterprise use case, data model and repository before invoking an LLM.

## Quick start (Windows PowerShell)
```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
python scripts\inspect_corpus.py
```

Expected: tests pass and the script lists 8 synthetic enterprise documents.

## Important
All documents and incidents are synthetic. Do not put real confidential company information, credentials, tokens, PII, or secrets into this repository.
