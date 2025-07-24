# RAG LLM App in Local Directory
---
#### Structure of the Project
```
rag-system/
├── venv/
├── docs/
│   ├── ...
├── vectorstore/
│   └── ...
├── ingest.py
├── app.py          <-- Flask application
└── templates/
    └── index.html  <-- HTML in templates folder
```
---
1. ```mkdir rag-system``` (run on WSL)

2. ```cd rag-system```

3. Create a virtual environment with venv
   ```python -m venv venv```

4. Activate the virtual environment
    ##### On Windows:
    ```.\venv\Scripts\activate```
    ##### On macOS/Linux:
    ```source venv/bin/activate ```
   
6. Install requirements.txt
   ``` pip install -r requirements.txt ```

7. ```mkdir docs```

8. Install Ollama Locally
``` sudo snap install ollama ```

9. Download a model with ollama
``` ollama pull deepseek-r1:1.5b ``` **Downloading deepseek-r1:1.5b which is just 1.1GB See here for a list of models: https://ollama.com/search

10. ```ollama pull nomic-embed-text```

11. Flask uses a templates folder by default to find HTML files. Create this folder in your project root

    ```mkdir templates```

12. , and inside it, create index.html.
13. run ```ollama serve```
14. run ```python ingest.py```
15. run ```python app.py```
   
