# AI Resume Matcher

An end-to-end AI pipeline designed to ingest unstructured resumes, extract normalized candidate profiles using structured LLM outputs with strict schema validation, and match candidates to job descriptions.

---

## Project Status

> **Current Status:** **Phase 1 Complete (Active Development)**
> Ingestion, LLM-powered structured extraction, schema validation, and relational database storage are implemented. Semantic vector search and the recruiter matching interface are planned next.

- [X] **Phase 1: Resume Ingestion & Structured Storage**
    - [X] Multi-format resume parsing (`.pdf`, `.docx`)
    - [X] LLM extraction with JSON schema enforcement (Groq API)
    - [X] Strict schema validation & type coercion with Pydantic
    - [X] Normalized relational database storage (SQLite) with many-to-many skill mapping
    - [X] Automated retry mechanism with rate-limit backoff
- [ ] **Phase 2: Semantic Matching & Embeddings** *(Next Up)*
    - [ ] Generate dense embeddings for candidates and job descriptions
    - [ ] Vector search index using ChromaDB
    - [ ] Hybrid matching (skills overlap + semantic cosine similarity)
- [ ] **Phase 3: Recruiter Interface & Scoring**
    - [ ] Interactive UI for uploading resumes and job postings
    - [ ] Ranked candidate recommendations with match explanations

---

## Architecture & Ingestion Pipeline

```text
[ Resume File (.pdf / .docx) ]
           ||
           \/
[ Text Extractor (pdfplumber / python-docx) ]
           ||
           \/
[ Groq LLM API (Structured JSON Schema) ]
           ||
           \/
[ Pydantic Validation (Candidate Model) ]
           ||
           \/
[ Normalized Relational DB (SQLite) ]
    |-- Candidate
    |-- ExperienceEntry
    |-- EducationEntry
    |-- Skill
    |-- CandidateSkill (many-to-many)
```

## Tech Stack
- **Language:** Python 3.10+
- **LLM Engine:** [Groq Cloud API](https://groq.com/)
- **Validation:** [Pydantic v2](https://pydantic.dev/docs/)
- **Document Processing:** `pdfplumber`, `python-docx` 
- **Database:** SQLite3 (Normalized relational schema) 
- **Vector Search (Upcoming):** ChromaDB

## Project Structure
```text
ai-resume-matcher/
├── src/
│   ├── resume_reader.py      # PDF & DOCX text extraction
│   ├── resume_extractor.py   # Groq LLM extraction + retry/rate-limit logic
│   ├── validation.py         # Pydantic models for Candidate, Experience, Education
│   └── sqlite_db.py          # SQLite schema creation & insert operations
├── get_random_resumes.py     # Batch sampling utility for testing
├── requirements.txt          # Project dependencies
├── .env.example              # Template for environment variables
└── README.md
```

## Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/SaraKhan-24/AI-Resume-Matcher.git
cd AI-Resume-Matcher
```
### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```
### 5. Run the Extraction Pipeline
```bash
python -m src.resume_extractor
```
Extracted candidate records will be validated and populated directly into `resumes.db`
