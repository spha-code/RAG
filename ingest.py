# ingest.py
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings # Updated import
from langchain_chroma import Chroma          # <<< NEW Updated import

# Define the path to your documents
DATA_PATH = "docs"
# Define the path where the Chroma vector store will be persisted
DB_FAISS_PATH = "vectorstore/db_chroma"

def create_vector_db():
    print("Loading documents...")
    # Load documents from the specified directory. You can extend this to other loaders.
    # For now, we use DirectoryLoader to load all supported document types (e.g., PDFs, TXT).
    # You might need specific loaders if you have other file types.
    loader = DirectoryLoader(DATA_PATH, glob="**/*",
                             loader_cls=PyPDFLoader, # Use PyPDFLoader for PDFs.
                                                     # For other file types, you might need to specify/add more loaders.
                             recursive=True) # Recursively load from subdirectories
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    # Split documents into chunks
    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50) # [2, 5, 13, 14, 15]
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")

    # Create embeddings using OllamaEmbeddings (using the model you pulled)
    print("Generating embeddings with OllamaEmbeddings...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text") # Use the embedding model you pulled [11, 22]

    # Create a Chroma vector store and persist it locally [25]
    print("Creating Chroma vector store and persisting it...")
    db = Chroma.from_documents(texts, embeddings, persist_directory=DB_FAISS_PATH)
    #db.persist()
    print("Vector database created and persisted successfully!")

if __name__ == "__main__":
    create_vector_db()