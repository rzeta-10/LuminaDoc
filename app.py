import os
import streamlit as st
import tempfile
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile




def process_document(uploaded_file: UploadedFile) -> list[Document]:
    temp_file = tempfile.NamedTemporaryFile("wb", suffix=".pdf", delete=False)
    temp_file.write(uploaded_file.read())

    loader = PyMuPDFLoader(temp_file.name)
    docs = loader.load()
    os.unlink(temp_file.name)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, 
        chunk_overlap=100, 
        separators=["\n\n", "\n", " ", "\t", "\r", ".", ",", ";", "!", "?", ""]
    )

    return text_splitter.split_documents(docs)

if __name__ == "__main__":
    with st.sidebar:
        st.set_page_config(page_title="RAG Q&A", page_icon="🧠")
        st.header("RAG Q&A")
        uploaded_file = st.file_uploader(
            "Upload PDF File", type=["pdf"], accept_multiple_files=False
        )

        process = st.button(
            "Process",
        )

    if uploaded_file and process:
        all_splits = process_document(uploaded_file)
        st.write(all_splits)
