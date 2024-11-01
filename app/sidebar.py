import streamlit as st
import requests
from pathlib import Path
from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    # Construct the absolute path to the image
    image_path = Path(__file__).parent / "logo-white.svg"

    # Display the image in the sidebar
    st.sidebar.image(str(image_path), use_column_width=True)

    model_options = ["gpt-3.5-turbo-0125", "babbage-002","gpt-3.5-turbo-instruct"]
    st.sidebar.selectbox("Model seç", options = model_options, key="model")

    st.sidebar.header("Doküman Yükle")
    uploaded_file = st.sidebar.file_uploader("", type=["pdf","docx","txt"])
    if uploaded_file is not None:
        if st.sidebar.button("Yükle"):
            with st.spinner("Yükleniyor..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(f"Doküman {uploaded_file} başarıyla yüklendi!")
                    st.session_state.documents = list_documents()

    st.sidebar.header("Yüklenen Dokümanlar")
    if st.sidebar.button("Yenile"):
        with st.spinner("Dokümanlar yeniden yükleniyor..."):
            st.session_state.documents = list_documents()