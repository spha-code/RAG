# app.py
from flask import Flask, render_template, request, jsonify
from langchain_ollama import OllamaEmbeddings # Updated import
from langchain_ollama import OllamaLLM      # Updated import
from langchain_chroma import Chroma          # <<< NEW Updated import
from langchain.chains import RetrievalQA
import os
import threading

app = Flask(__name__)

# Define the path where the Chroma vector store is persisted
DB_FAISS_PATH = "vectorstore/db_chroma"

# Global variable to store the QA chain, loaded once
qa_chain = None
qa_chain_lock = threading.Lock() # To prevent race conditions during loading

def load_qa_chain_instance():
    """
    Loads the RAG chain, including embeddings, vector store, and LLM.
    This function is called once when the Flask app starts.
    """
    global qa_chain
    if qa_chain is None:
        with qa_chain_lock:
            if qa_chain is None: # Double-checked locking
                print("Loading QA chain (embeddings, vector store, LLM)...")
                try:
                    # Initialize embeddings
                    embeddings = OllamaEmbeddings(model="nomic-embed-text")

                    # Load the persisted Chroma vector store
                    db = Chroma(persist_directory=DB_FAISS_PATH, embedding_function=embeddings)
                    print("Vector database loaded.")

                    # Initialize the local LLM with Ollama
                    llm = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.7)

                    # Create a retriever from the vector store
                    retriever = db.as_retriever(search_kwargs={"k": 3})

                    # Create the RetrievalQA chain
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=retriever,
                        return_source_documents=True
                    )
                    print("QA chain loaded successfully!")
                except Exception as e:
                    print(f"Error loading QA chain: {e}")
                    qa_chain = None # Reset to None if loading fails

# Route for the home page
@app.route('/')
def index():
    if not os.path.exists(DB_FAISS_PATH):
        return render_template('index.html', error="Vector database not found! Please run `python ingest.py` first to create it.")
    return render_template('index.html')

# Route to handle queries (POST request)
@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('query')
    if not user_query:
        return jsonify({"answer": "Please enter a question.", "sources": []})

    if qa_chain is None:
        return jsonify({"answer": "RAG system not ready. Please check server logs for errors during startup.", "sources": []})

    print(f"Received query: {user_query}")
    try:
        response = qa_chain.invoke({"query": user_query})
        answer = response["result"]
        sources = []
        if response.get("source_documents"):
            for doc in response["source_documents"]:
                source_name = doc.metadata.get('source', 'Unknown Source')
                sources.append(source_name)
        print("Query processed.")
        return jsonify({"answer": answer, "sources": list(set(sources))}) # Use set to get unique sources
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({"answer": f"An error occurred: {e}. Please ensure Ollama server is running and models are pulled.", "sources": []})

if __name__ == '__main__':
    threading.Thread(target=load_qa_chain_instance).start()
    app.run(debug=False) 
