import requests
import streamlit as st


def get_api_response(question, session_id, model):
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json'}
    
    data = {"question":question,
            "model":model}
    
    if session_id:
        data["session_id"]=session_id

    try:
        response = requests.post("https://fasih-ai-bot.onrender.com/chat", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get response from the API. Error: {response.status_code} - {response.text}")
            return None
        
    except Exception as e:
        st.error(f"An error occured while fetching the response from the API: {str(e)}")
        return None
    
def upload_document(file):
    print("Uploading file...")
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post("https://fasih-ai-bot.onrender.com/upload-doc", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to upload file. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occured while uploading the file: {str(e)}")
        return None
    
def list_documents():
    try:
        response = requests.get("https://fasih-ai-bot.onrender.com/list-docs")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to list documents. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occured while fetching the document list: {str(e)}")
        return None
    
def delete_document(file_id):
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json'}
    
    data = {"file_id": file_id}
    
    try:
        response = requests.post("https://fasih-ai-bot.onrender.com/delete-doc", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to delete document. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occured while deleting the document: {str(e)}")
        return None