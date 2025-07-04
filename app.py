import os
import streamlit as st
import tempfile

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile

import chromadb
from chromadb.api.types import EmbeddingFunction
from langchain_ollama import OllamaEmbeddings
from typing import List
from httpx import HTTPStatusError
import json

from prompt import system_prompt
import ollama

from sentence_transformers import CrossEncoder

def call_llm(context:str, prompt:str):
    response = ollama.chat(
        model="llama3.2:latest",
        stream=True,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}, Question: {prompt}"},
        ],
    )

    for chunk in response:
        if chunk["done"] is False:
            yield chunk["message"]["content"]
        else:
            break

def re_rank_cross_encoder(prompt: str, documents: list[str]) -> tuple[str, list[int]]:
    relevant_text = ""
    relevant_text_ids = []

    encoder_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    ranks = encoder_model.rank(prompt, documents, top_k=3)

    for rank in ranks:
        relevant_text += documents[rank["corpus_id"]]
        relevant_text_ids.append(rank["corpus_id"])
    
    return relevant_text, relevant_text_ids
# Custom Embedding Wrapper for ChromaDB
class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model: str):
        self.embedding_model = OllamaEmbeddings(model=model)

    def __call__(self, input: List[str]) -> List[List[float]]:
        return [self.embedding_model.embed_query(text) for text in input]

# Process the Uploaded Document
def process_document(uploaded_file: UploadedFile) -> list[Document]:
    # Determine file extension and set suffix accordingly
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    if file_ext in [".pdf", ".docx", ".txt", ".csv", ".xlsx"]:
        temp_file = tempfile.NamedTemporaryFile("wb", suffix=file_ext, delete=False)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")
    temp_file.write(uploaded_file.read())
    temp_file.close()

    loader = PyMuPDFLoader(temp_file.name)
    docs = loader.load()
    os.unlink(temp_file.name)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", "\t", "\r", ".", ",", ";", "!", "?", ""]
    )

    return text_splitter.split_documents(docs)

# Get or Create Vector Collection in ChromaDB
def get_vector_collection() -> chromadb.Collection:
    ollama_embedding = OllamaEmbeddingFunction(model="nomic-embed-text")

    chroma_client = chromadb.PersistentClient(path="./rag-chroma")
    return chroma_client.get_or_create_collection(
        name="rag-qa",
        embedding_function=ollama_embedding,
        metadata={"hnsw:space": "cosine"}
    )

# Add Processed Document Splits to Collection
def add_to_collection(all_splits: list[Document], file_name: str):
    collection = get_vector_collection()
    documents, metadatas, ids = [], [], []

    for i, split in enumerate(all_splits):
        documents.append(split.page_content)
        metadatas.append(split.metadata)
        ids.append(f"{file_name}_{i}")

    try:
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )
    except json.JSONDecodeError as e:
        st.error(f"JSON decode error: {e}")
    except HTTPStatusError as e:
        st.error(f"HTTP error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

def query_collection(prompt: str, n_results: int = 10):
    collection = get_vector_collection()
    results = collection.query(query_texts=[prompt], n_results=n_results)
    return results

# Streamlit App UI
def main():
    st.set_page_config(page_title="RAG Q&A", page_icon="🧠")
    st.sidebar.header("RAG Q&A")

    st.sidebar.info(
        """
        **Upload your documents**
        
        Supported formats: PDF, DOCX, TXT, CSV, XLSX
        
        You can select multiple files.
        
        _Need support for another format? Let us know!_
        """
    )

    uploaded_files = st.sidebar.file_uploader(
        "Upload File(s)", type=["pdf","docx","csv","txt","xlsx"], accept_multiple_files=True
    )

    process = st.sidebar.button("Process Document(s)")

    if process and uploaded_files:
        for uploaded_file in uploaded_files:
            normalized_file_name = uploaded_file.name.translate(
                str.maketrans({"-": "_", " ": "_", ".": "_", "(": "_", ")": "_"})
            )
            with st.spinner(f"Processing {uploaded_file.name}..."):
                all_splits = process_document(uploaded_file)
                add_to_collection(all_splits, normalized_file_name)
        st.sidebar.success("All documents processed!")

    st.title("RAG Q&A Document Assistant")
    st.info(
        """
        **How to use:**
        1. Upload one or more documents using the sidebar.
        2. Click **Process Document(s)**.
        3. Ask questions about your documents below.
        
        Supported formats: PDF, DOCX, TXT, CSV, XLSX
        
        _Need another format? Request it in the feedback!_
        """
    )

    st.header("Ask a Question")
    prompt = st.text_area("Ask a question related to your documents")
    ask = st.button("Ask")

    if ask and prompt:
        results = query_collection(prompt)
        context = results.get("documents")[0]
        relevant_text, relevant_text_ids = re_rank_cross_encoder(prompt, context)
        response = call_llm(context=relevant_text, prompt=prompt)
        st.write_stream(response)
    
        with st.expander("See retrieved documents"):
            st.write(results)
        
        with st.expander("See relevant text"):
            st.write(relevant_text)
            st.write(relevant_text_ids)

if __name__ == "__main__":
    main()