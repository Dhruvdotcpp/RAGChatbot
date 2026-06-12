# Importing all the neccessary models for pdf processing(read, chunk, embed, and store)

# Importing PyPDFLoader to open and read pdf files
from langchain_community.document_loaders import PyPDFLoader

# Import text spliter to break long text into smaller overlapping chunks
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# New:-
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import embeddings model to convert text into vectors
# from langchain_community.embeddings import SentenceTransformerEmbeddings
# New:-
from langchain_huggingface import HuggingFaceEmbeddings

# Import ChromaDB vector store to store vectors and corresponding texts and to also perform searching operation
from langchain_community.vectorstores import Chroma



# Main Function (call this with any PDF path)
def ingest_pdf(pdf_path: str):
    # pdf_path: str -> means this function expects a string like "docs/myfile.pdf"
    print(f"Starting ingestion for: {pdf_path}")

    # Stage-1 Loading
    # PyPDFLoader reads each page and returns list of document object
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # documents is a list like:
    # [Document(page_content="page 1 text", metadata={page: 0}),
    #  Document(page_content="page 2 text", metadata={page: 1}),
    #  ...]

    print(f"Loaded {len(documents)} pages from PDF")

    # Ṣtage-2 Chunking
    # RecursiveCharacterTextSplitter tries to split on paragraphs first, then sentences, then words — to keep meaning intact
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,   # Each chunk is 500 characters long
        chunk_overlap = 50  # Last 50 characters of a particular chunk are overlap with the first 50 character of the next chunk 
    )

    # split_documents takes our list of pages and splits each page into chunks
    chunks = splitter.split_documents(documents)

    print(f"Split into {len(chunks)} chunks")

    # Printing the first chunk
    print("\n--- Preview of first chunk ---")
    print(chunks[0].page_content)
    print("------------------------------\n")


    # Stage-3 Embedding
    # Load the sentence-transformers model "all-MiniLM-L6-v2" is small, fast, and free
    # First time: downloads the model (~80MB)
    # After that: loads from cache instantly
    print("Loading embedding model...")

    # embeddings = SentenceTransformerEmbeddings(
    #     model_name="all-MiniLM-L6-v2"
    # )
    # New:-
    # embeddings = HuggingFaceEmbeddings(
    #     model_name="all-MiniLM-L6-v2"
    # )
    # print("Embedding model loaded")

    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    # Replace HuggingFaceEmbeddings with:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
)

    # Stage-4 ChromaDB
    # This does two things at once:
    # 1. Converts every chunk into a vector using embeddings
    # 2. Stores the vectors + original text in ChromaDB

    print("Storing chunks in ChromaDB...")

    # vectorstore = Chroma.from_documents(
    #     documents=chunks,               # our text chunks
    #     embedding=embeddings,           # model to embed them
    #     persist_directory="./chroma_db" # folder to save data
    # )
    # persist_directory means ChromaDB saves everything
    # to disk in a folder called chroma_db/
    # So data survives even after you restart the server
    # New:-
    import chromadb
    # Create a persistent ChromaDB client explicitly
    client = chromadb.PersistentClient(path="./chroma_db")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        client=client,
        collection_name="pdf_collection"
    )


    print("All chunks stored in ChromaDB!")
    print(f"Data saved to ./chroma_db folder")
    print("Ingestion complete!")


# Temporary test to check working properly or not
# if __name__ == "__main__":
#     ingest_pdf("docs/test.pdf")

# if __name__ == "__main__"  means: Only run this block if I'm running this file directly, not when it's imported by another file