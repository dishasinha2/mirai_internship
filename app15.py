import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
st.title("AI chat with chat history")
@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GENAI_API_KEY"))
client=get_client() #get ai client is a function , onces the connection is establish even if it will rerun it will not change the session , mtlb history store rhegi
if "messages" not in st.session_state:
    st.session_state.messages=[] #make emplty list , it is there to check if there is any message or not
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat=client.chats.create(model="gemini-2.5-flash") #this is the model we are using

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"] )

if user_message:=st.chat_input("Type your message here"):
    with st.chat_message("user"):
        st.write(user_message)
    st.session_state.messages.append({"role":"user","content":user_message})
    with st.spinner("Thinking..."):
        response=st.session_state.gemini_chat.send_message(user_message)
    with st.chat_message("AI"):
        st.write(response.text)
    st.session_state.messages.append({"role":"AI","content":response.text})
    #create a new string
    output="Chat History: "
    for msg in st.session_state.messages:
        output+=f"{msg['role']}\n"
    st.sidebar.download_button("Download Chat History",data=str(st.session_state.messages),file_name="chat_history.txt",mime="text/plain")