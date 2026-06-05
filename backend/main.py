# Part 1 — Imports

from fastapi import FastAPI, UploadFile, File
# FastAPI ⟶ it is the main class that creates the app
# UploadFile ⟶ a special FastAPI type for handling file uploads
# File ⟶ a function that marks a parameter as a file upload field

from fastapi.middleware.cors import CORSMiddleware
# The CORS middleware class. Every request/response passes through this middleware while communicating between frontend and backend.

from pydantic import BaseModel
# Pydantic is a data validation library(it make the data validation easy)
# BaseModel lets you define the exact shape of data you expect.

from rag import get_answer
# This basically imports the get_answer function from rag.py file

from ingest import ingest_pdf
# Import the ingest_pdf function from the ingest.py file.

import shutil
# Built-in Python module for file operations to copies file contents from the uploaded stream to a local file on disk. More reliable than reading/writing manually.

import os
# We use it here to creates docs/ folder if it doesn't exist


# Part 2 — Creating the App
# This is the main application object
# Everything gets attached to this
app = FastAPI()


# Part 3 — CORS Middleware
# Middleware runs on EVERY request before it
# reaches your endpoint functions
# This one adds CORS headers to allow React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",           # local development
        "https://your-app.vercel.app",     # replace after Vercel deploy
        "*"                                # temporary — allows all origins
    ],
    allow_methods=["*"],    # allow GET, POST, PUT, DELETE etc
    allow_headers=["*"]     # allow all headers
)


# Part 4 — Request Body Model
# Pydantic BaseModel defines the shape of data we expect from the frontend
# FastAPI uses this to:
# 1. Validate incoming data automatically
# 2. Show correct docs in /docs page
class QuestionRequest(BaseModel):
    question: str   # we expect a field called "question"
                    # that is a string



#  Part 5 — Health Check Endpoint
# GET /
# Just to verify the server is running
@app.get("/")
def root():
    return {"status": "RAG Chatbot API is running!"}



# Part 6 — Upload Endpoint
# POST /upload
# Receives a PDF file from React frontend
# Saves it to docs/ folder
# Runs ingest_pdf() to process it
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # UploadFile = FastAPI's file upload type
    # File(...) = this field is required (... means required)

    print(f"Received file: {file.filename}")

    # Make sure docs/ folder exists
    # exist_ok=True means don't error if it already exists
    os.makedirs("docs", exist_ok=True)

    # Build the save path
    file_path = f"docs/{file.filename}"

     # Save the uploaded file to disk
    # shutil.copyfileobj copies file contents
    # from upload stream to our local file
    with open(file_path, "wb") as f:
        # "wb" = write binary mode (for PDFs)
        shutil.copyfileobj(file.file, f)

    print(f"File saved to: {file_path}")

    # Run the ingestion pipeline
    # This chunks, embeds and stores in ChromaDB
    ingest_pdf(file_path)

    # Return success message to frontend
    return {
        "message": f"{file.filename} uploaded and ingested successfully!"
    }


# Part 7 — Ask Endpoint
# POST /ask
# Receives a question from React frontend
# Runs get_answer() from rag.py
# Returns the answer
@app.post("/ask")
async def ask_question(body: QuestionRequest):
    # body is automatically parsed from JSON
    # FastAPI validates it matches QuestionRequest shape
    # If frontend sends wrong data → FastAPI returns error automatically

    print(f"Question received: {body.question}")

    # Call our RAG pipeline
    answer = get_answer(body.question)

    print(f"Answer generated: {answer[:100]}...")

    # Return answer to frontend
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)