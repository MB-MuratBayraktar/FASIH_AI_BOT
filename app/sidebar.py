import streamlit as st
import requests
from pathlib import Path
from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    # Construct the absolute path to the image
    image_path = Path(__file__).parent / "logo-white.svg"

    # Display the image in the sidebar
    st.sidebar.image(str(image_path), use_column_width=True)

    model_options = ["gpt-3.5-turbo-0125", "babbage-002", "gpt-3.5-turbo-instruct"]
    st.sidebar.selectbox("Select model", options=model_options, key="model")

    st.sidebar.header("Upload a document")
    uploaded_file = st.sidebar.file_uploader("Choose a document", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    if uploaded_file is not None:
        if st.sidebar.button("Upload", key="upload_button"):
            with st.spinner("Uploading..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(f"File {uploaded_file.name} uploaded successfully!")
                    st.session_state.documents = list_documents()

    st.sidebar.header("Uploaded documents")
    if st.sidebar.button("Refresh", key="refresh_button"):
        with st.spinner("Refreshing uploaded documents..."):
            st.session_state.documents = list_documents()

    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(doc["filename"])

