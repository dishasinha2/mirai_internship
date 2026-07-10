import streamlit as st
st.title("the multiverse of chatbot")
# st.write("This is a simple Streamlit application.")
# user_message = st.text_input("Enter your message:")
# print(user_message)
# if st.button("Submit"):
#     st.write(user_message)

personality=st.selectbox("Who do you want to talk to?",[
    "Virat Kohli","Anushka sharma","Elvish","pritam and pedro"
])
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_message = st.text_input("say something:")

if st.button("Send"):
    if user_message:
        ai_instruction=f"Respond to the user as {personality} would.resond to the message sent by the user within 50 words"
        with st.spinner("Connecting to the multiverse!......"):
            response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=ai_instruction
            )
            st.success("message recived")
            st.write(response.text)
    else:
        st.warning("Please enter a message before sending.")