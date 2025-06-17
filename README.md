# 🚀 **LuminaDoc: Your Offline Document Intelligence Hub** 🔍

LuminaDoc is a powerful, privacy-focused document analysis tool that brings **RAG (Retrieval-Augmented Generation)** capabilities to your local environment. Process, analyze, and interact with your documents using advanced **LLMs**—all without requiring an internet connection.

---

<div align="center">
  <img src="https://github.com/rzeta-10/LuminaDoc/blob/main/demo.gif" alt="Demo">
</div>

## 📚 **Key Features**  

- **100% Offline Processing:** Your documents never leave your machine.  
- **Built-in RAG Pipeline:** Advanced retrieval and generation workflows.  
- **Local Vector Storage:** Supports **ChromaDB** for efficient retrieval.  
- **Format Support:** PDF, DOCX, TXT, CSV, XLSX.  
- **Intelligent Chunking:** Semantic search with precise document splitting.  
- **Conversational Interface:** Ask questions, get contextual answers.  
- **Custom Knowledge Base:** Build and manage your knowledge repositories.  
- **Multi-file Upload:** Upload and process multiple documents at once.  
- **Simple Streamlit UI:** Clean, native Streamlit interface—no HTML required.  

---

## 💡 **Perfect For:**  

- 📊 **Researchers:** Analyze private datasets securely.  
- ⚖️ **Legal Professionals:** Handle confidential legal documents locally.  
- 💼 **Business Analysts:** Process sensitive data without cloud dependencies.  
- 🧑‍💻 **Developers:** Build offline-first AI-powered applications.  
- 🔐 **Privacy Advocates:** Ensure your data stays secure and private.  

---

## 🛠️ **Tech Stack**  

- **Backend:** Python 3.9+
- **Frontend:** Streamlit 
- **Database:** Local Vector DB (ChromaDB)  
- **Embedding Model:** Ollama (`nomic-embed-text`)  
- **LLM Support:** Local LLMs (e.g., `llama3.2:latest`)  
- **Cross-Encoder:** Sentence Transformers (`ms-marco-MiniLM-L-6-v2`)  

---

## 🔒 **Privacy First**  

- **No Cloud Services:** All processing happens locally.  
- **No API Keys Required:** Run seamlessly without third-party dependencies.  
- **No Data Sharing:** Your documents remain secure on your machine.  

---

# 📦 **Installation Guide**

Follow these steps to install and run **LuminaDoc** locally:

### ✅ **Step 1: Clone the Repository**  
Open your terminal and clone the LuminaDoc repository:  
```bash
git clone https://github.com/yourusername/luminadoc.git
cd luminadoc
```

---

### ✅ **Step 2: Create a Virtual Environment**  
Create an isolated Python environment:  
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/MacOS
venv\Scripts\activate     # On Windows
```

---

### ✅ **Step 3: Install Dependencies**  
Install the required Python packages:  
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Ensure Required Dependencies Include:**  
- `streamlit`  
- `langchain-ollama`  
- `chromadb`  
- `sentence-transformers`  
- `PyMuPDF`  
- `httpx`
- `langchain-community`
- `langchain`
- `ollama`

---

### ✅ **Step 4: Install Ollama and Pull Models**  
If **Ollama** is not installed, run the following commands:

#### **For macOS:**
```bash
brew install ollama
```

#### **For Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### **Verify the installation**:
```bash
ollama --version
```

#### **Pull Required Models:**
Make sure to download the required models:
```bash
ollama pull nomic-embed-text
ollama pull llama3.2:latest
```

Start the Ollama server:
```bash
ollama serve
```

Verify the models:
```bash
curl http://localhost:11434/api/tags
```

Ensure the **`nomic-embed-text`** and **`llama3.2`** models are listed.

---

### ✅ **Step 5: Start LuminaDoc**  
Run the Streamlit app locally:  
```bash
streamlit run app.py
```

The app will start, and you’ll see a URL in your terminal, usually:  
```text
Local URL: http://localhost:8501
```

Open this in your browser.

---

## 🚀 **Using LuminaDoc**

1. **Upload Documents:**  
   - In the sidebar, upload one or more documents (**PDF, DOCX, TXT, CSV, XLSX**).  
   - Click on the **Process Document(s)** button.  
   - Need another format? Request it in the feedback!
   
2. **Ask Questions:**  
   - Enter your question in the **Ask a Question** text area.  
   - Click **Ask** to retrieve relevant information.  

3. **View Results:**  
   - The system will show the **retrieved context** and the **AI-generated answer**.  
   - Explore retrieved documents and relevant text via expandable sections.

---

## ✅ **Environment Variables (Optional)**  
If you want to customize configurations:  

Create a `.env` file:  
```env
OLLAMA_SERVER_URL=http://localhost:11434
VECTOR_DB_PATH=./rag-chroma
```

Update your code to load `.env` using `dotenv` if needed.

---

## ✅ **Troubleshooting**

1. **Port Conflicts:** Ensure Ollama is running on `http://localhost:11434`.  
2. **Dependencies Issues:** Run `pip install -r requirements.txt` again.  
3. **Streamlit Errors:** Clear the cache:  
   ```bash
   streamlit cache clear
   ```

4. **Logs:** Check server logs for errors:
   ```bash
   ollama serve --verbose
   ```

---

## 🧠 **How It Works**

1. **Document Upload & Processing:**  
   - Documents are uploaded and split into smaller semantic chunks.  
   - Chunks are embedded using `nomic-embed-text` and stored in **ChromaDB**.  

2. **User Query:**  
   - Your query searches the vector database for relevant chunks.  
   - Results are re-ranked using **CrossEncoder**.  

3. **LLM Response:**  
   - The context is passed to **LLM (e.g., llama3.2)** for final generation.  
   - The answer is displayed in the Streamlit interface.  

---

## 🔗 **Next Steps**  
- Explore advanced features like **custom pipelines**.  
- Experiment with **different local LLM models**.  
- Contribute to the project on GitHub!  

---

**Illuminate your documents with AI-powered insights—locally and securely.** 🚀📚
