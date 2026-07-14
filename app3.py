import streamlit as st
st.title("the AI imae stuido")
intensity=st.sidebar.slider("chooseee",min_value=1,max_value=10)
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_message = st.text_input("say something:")
intensity=st.sidebar.slider("weidth",min_value=1,max_value=10)
intensity=st.sidebar.slider("height",min_value=1,max_value=10)
