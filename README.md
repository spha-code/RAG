# RAG ollama LLM App in Flask Backend Local Directory
---
![Screenshot](https://raw.githubusercontent.com/spha-code/RAG-system/main/Screenshot.png)
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

7. ```mkdir docs``` and upload files (.pdf, .txt) manually in the directory

8. Install Ollama Locally
``` sudo snap install ollama ```

9. Download a model with ollama
``` ollama pull deepseek-r1:1.5b ```

    Downloaded deepseek-r1:1.5b which is 1.1GB 
    
    See here for a list of models: https://ollama.com/search

11. ```ollama pull nomic-embed-text```

12. Flask uses a templates folder by default to find HTML files. Create this folder in your project root

    ```mkdir templates```

13. Inside the templates folder, create ```index.html```

14. Open a new terminal and run ```ollama serve```
    This command starts the Ollama server, do not close this terminal
    
15. run ```python ingest.py```
    
16. run ```python app.py```
   
