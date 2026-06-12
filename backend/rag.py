import os
# built in python module, no installation needed.
# Use it as os.getenv("GOOGLE_API_KEY")
# This helps in reading the value of the api key from the environment variable (which load_dotemv() loads from .env file) 

from dotenv import load_dotenv
# Read .env file and load everything into environment variable 
# load_dotenv()
# os.getenv("GOOGLE_API_KEY") 
# The dotenv and os together helps in getting the storing the api response in the variable and read it. 

# .env file → load_dotenv() loads it → os.getenv() reads it

from langchain_huggingface import HuggingFaceEmbeddings
# These models is need here too, to convert user's question into vector

# from langchain_community.vectorstores import Chroma
# New:-
from langchain_chroma import Chroma
# This is ChromaDB wrapper from langchain
# Here, we connect our existing ChromaDB database and run similarity searches.

# from langchain_google_genai import ChatGoogleGenerativeAI
# The gemini wrapper from langchain 
# Let us talk to gemini api. Without this we'd have to write complex http requests manually.

# Since gemini not working we shift to grok
from langchain_groq import ChatGroq


# from langchain.schema import HumanMessage, SystemMessage
# New:-
from langchain_core.messages import HumanMessage, SystemMessage
# Special message obj langchain uses to structure conversation with LLMs
# SystemMessage --> instructions for the AI (how to behave)
# HumanMessage --> the actual user question

import chromadb
# Use to create PersistentClient which connects to our saved database on disk.


load_dotenv()
# This line runs immediately when the file is imported. It reads .env file and loads
# Now os.getenv() can access it anywhere needed


# This function will take question as str and return answer as str
def get_answer(question: str) -> str:

    print(f"\nQuestion received: {question}")

    # STEP 1: Load the same embedding model
    # print("Loading embedding model...")
    # embeddings = HuggingFaceEmbeddings(
    #     model_name="all-MiniLM-L6-v2"
    # )
    # The model used here must be same that was used in ingest.py 

    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    # Replace HuggingFaceEmbeddings with:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # STEP 2: Connect to ChromaDB
    print("Connecting to ChromaDB...")

    client = chromadb.PersistentClient(path="./chroma_db")
    # Opens the ChromaDB saved on disk at the given path 
    # Persistent means it reads from the disk not any temp in memory database. So the chunks stored in ingest.py are still there. 

    vectorstore = Chroma(
        client=client,
        collection_name="pdf_collection",  # same name as ingest.py
        embedding_function=embeddings
    )
    # Chroma() wraps the ChromaDB client with langchain so that we can use .similarity_search() 
    # Collection name should match with the one used in ingest.py 
    # embedding_function=embeddings --> tells chroma how to convert question to a vector for search.


    # STEP 3: Similarity Search
    print("Searching for relevant chunks...")

    docs = vectorstore.similarity_search(question, k=3)
    # This is where the question is matched with similar chunks. This happens in the following way:
    # Your question gets embedded(i.e gets converted to vector)
    # ChromaDB compares this vector against all the stored chunk vectors
    # The top 3(cause k=3) most similar chunks as document object are returned.

    print(f"Found {len(docs)} relevant chunks")

    # Print what chunks were found (helpful for debugging)
    for i, doc in enumerate(docs):
        print(f"\nChunk {i+1} preview: {doc.page_content[:100]}...")



    # STEP 4: Build Context

    context = "\n\n".join([doc.page_content for doc in docs])
    # "\n\n" --> puts two blank lines between each chunks
    # .join([doc.page_content for doc in docs]) --> loops through each chunk and combines it before sending the combined chunks(aka context) to gemini 


    # STEP 5: Initialize Gemini

    print("Sending to Groq...")

    # llm = ChatGoogleGenerativeAI(
    #     # model="gemini-1.5-flash" ---> Old
    #     model="gemini-2.0-flash",  # --> New
    #     google_api_key=os.getenv("GOOGLE_API_KEY"),
    #     temperature=0.3
    # )

    # gemini-1.5-flash --> Gemini model we will be using. Flash = fast and free.

    # google_api_key=os.getenv("GOOGLE_API_KEY") -->
    # os reads the api key from .env file(which was earlier been loaded using load_dotenv() ). Using os keeps the key hidden.

    # temperature=0.3 --> Controls how creative vs factual the response is. 0.3 is optimal. Mostly factual, slight variation

    # Shifting to groq
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )


    # STEP 6: Build Prompt and Get Answer

    messages = [
        SystemMessage(content=f"""You are a helpful assistant that answers 
            questions based on the provided document context.

            IMPORTANT RULES:
            - Answer ONLY using the context provided below
            - If the answer is not in the context, say "I don't know based on the document"
            - Give a detailed answer, But do not add infomation outside the data given
            - Don't make up information
            - If user is greeting. Greet back and ask Hi! Upload a PDF on the left and ask me anything about it.

            Context from document:
            {context}"""),

                    HumanMessage(content=question)
    ]

    # Two messages SystemMessage and Human message are used here 
    # SystemMessage --> sets the rule and gives context.
    # HumanMessage --> the actual question 

    # f before the string means it's an f-string — you can embed variables inside {}
    # {context} gets replaced with the actual chunk text before sending to Gemini

    response = llm.invoke(messages)
    # Send messages to Gemini and get response

    print("✅ Got answer from Groq!")

    # response.content contains the actual answer text
    return response.content




# Temporary test — remove after testing
# if __name__ == "__main__":
#     answer = get_answer("What are the assignment questions about?")
#     print("\n" + "="*50)
#     print("ANSWER:")
#     print(answer)
#     print("="*50)