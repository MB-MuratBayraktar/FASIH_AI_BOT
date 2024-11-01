import streamlit as st
import requests

from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    st.sidebar.image("./logo-white.svg", use_column_width=True)

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

    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
             st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})")
        selected_file_id = st.sidebar.selectbox("Select a document to delete", options=[doc['id'] for doc in documents],
        format_func = lambda x: next(doc['filename'] for doc in documents if doc['id'] == x))
        if st.sidebar.button("Sil"):
            with st.spinner("Siliniyor..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(f"Doküman {selected_file_id} başarıyla silindi!")
                    st.session_state.documents = list_documents()
                else:
                    st.sidebar.error(f"Doküman silinemedi! {selected_file_id}")


def upload_document(file):
    print("Uploading file...")
    try:
        files = {"file": (file.name,file,file.type)}
        response = requests.post("http://localhost:8000/upload-doc", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to upload file. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occured while uplloading the file: {str(e)}")
        return None
    

def list_documents():
    try:
        response = requests.get("http://localhost:8000/list-docs")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to list documents. Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"an error occured while fetching the document list: {str(e)}")
        return []

def delete_document(file_id):
    headers = {'accept' : 'application/json',
               'Content_Type': 'application/json'}
    data = {"file_id":file_id}
    try:
        response = requests.post("http://localhost:8000/delete-doc", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to delete document. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occured while deleting the document: {str(e)}")
        return None        
    