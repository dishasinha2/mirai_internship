import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import time

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="🌌 Multiverse AI",
    page_icon="🌌",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#0f172a,#1e293b,#334155);
color:white;
}

h1{
text-align:center;
color:#ffffff;
}

.block-container{
padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("🌌 Multiverse AI")
st.write("Talk with your favorite personalities powered by Gemini AI.")

# -----------------------------
# Characters
# -----------------------------
characters = {

"Virat Kohli":
"""
You are Virat Kohli.

Be confident.
Motivational.
Talk about discipline, cricket and fitness.

Never say you are an AI.
""",

"Anushka Sharma":
"""
You are Anushka Sharma.

Be calm, positive and intelligent.

Never reveal you are an AI.
""",

"Elvish":
"""
You are Elvish Yadav.

Speak in funny Hindi-English.

Keep replies entertaining.

Never reveal you are AI.
""",

"Pritam & Pedro":
"""
You are two friends.

Reply as both.

Make conversations funny.
""",

"Albert Einstein":
"""
You are Albert Einstein.

Explain things simply.

Be thoughtful.
""",

"Iron Man":
"""
You are Tony Stark.

Funny.

Confident.

Genius.

Sarcastic.
"""
}

avatars = {
"Virat Kohli":"🏏",
"Anushka Sharma":"🎬",
"Elvish":"😎",
"Pritam & Pedro":"😂",
"Albert Einstein":"🧠",
"Iron Man":"🤖"
}

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("⚙ Settings")

personality = st.sidebar.selectbox(
    "Choose Character",
    list(characters.keys())
)

style = st.sidebar.selectbox(
    "Response Style",
    [
        "Normal",
        "Funny",
        "Motivational",
        "Serious",
        "Roast"
    ]
)

max_words = st.sidebar.slider(
    "Maximum Words",
    20,
    200,
    80
)

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:

    avatar = "🙂"

    if message["role"] == "assistant":
        avatar = avatars[personality]

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
user_message = st.chat_input("Type your message...")

if user_message:

    # User Message
    st.session_state.messages.append({
        "role":"user",
        "content":user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    # Build History
    history = ""

    for msg in st.session_state.messages:

        history += f"{msg['role']} : {msg['content']}\n"

    prompt = f"""
{characters[personality]}

Conversation History:

{history}

Respond in a {style} style.

Limit the response to approximately {max_words} words.

Remain completely in character.

Never mention that you are an AI assistant.
"""

    try:

        with st.spinner(f"Connecting to {personality}'s universe..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        reply = response.text

    except Exception as e:

        reply = f"Error: {e}"

    st.session_state.messages.append({
        "role":"assistant",
        "content":reply
    })

    # Assistant Reply
    with st.chat_message(
        "assistant",
        avatar=avatars[personality]
    ):

        placeholder = st.empty()

        typed = ""

        for word in reply.split():

            typed += word + " "

            placeholder.markdown(typed)

            time.sleep(0.03)

    # -----------------------------
    # Token Estimator
    # -----------------------------
    characters_count = len(user_message)

    estimated_tokens = characters_count / 4

    st.info(
        f"🧠 Estimated Tokens Used: {estimated_tokens:.2f}"
    )

# -----------------------------
# Download Chat
# -----------------------------
if st.session_state.messages:

    transcript = ""

    for msg in st.session_state.messages:

        transcript += f"{msg['role'].upper()}:\n"

        transcript += msg["content"]

        transcript += "\n\n"

    st.download_button(
        "📥 Download Chat",
        transcript,
        file_name="multiverse_chat.txt"
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("🌌 Multiverse AI 2.0 | Powered by Google Gemini")