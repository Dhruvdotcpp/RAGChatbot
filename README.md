# RAG Chatbot

A document Q&A chatbot powered by 
Retrieval-Augmented Generation (RAG).

## ✨ Features
- Upload any PDF and chat with it
- Answers strictly from document content
- Fast responses via LLaMA 3 (Groq)
- Semantic search with ChromaDB

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Frontend | React + Tailwind CSS |
| Backend | FastAPI + Python |
| Embeddings | Sentence Transformers |
| Vector DB | ChromaDB |
| LLM | LLaMA 3 via Groq API |
| RAG Framework | LangChain |

## ⚙️ How RAG Works

<img width="1162" height="565" alt="image" src="https://github.com/user-attachments/assets/f69d1958-f6a8-430e-937d-0a4a481019c6" />

PDF → Chunk text → Embed → Store in ChromaDB

Question → Embed → Find similar chunks → Send to LLM → Answer

## 🚀 Run Locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
