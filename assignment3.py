import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# ---------------------------------------
# Load Environment Variables
# ---------------------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# ---------------------------------------
# Page Config
# ---------------------------------------
st.set_page_config(
    page_title="🌌 Multiverse AI",
    page_icon="🌌",
    layout="wide"
)

# ---------------------------------------
# Custom CSS
# ---------------------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#334155);
}

h1{
    color:white;
    text-align:center;
}

.stMarkdown{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Memory Vault (Assignment Requirement)
# ---------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------
# Character Prompts
# ---------------------------------------
characters = {

"Virat Kohli":
"""
You are Virat Kohli.

Be confident.
Motivational.
Talk like Virat.
Never say you are AI.
""",

"Anushka Sharma":
"""
You are Anushka Sharma.

Be kind.
Positive.
Friendly.
""",

"Elvish":
"""
You are Elvish Yadav.

Use funny Hindi-English.

Keep responses entertaining.
""",

"Pritam & Pedro":
"""
You are two best friends.

Reply together.

Be funny.
""",

"Albert Einstein":
"""
You are Albert Einstein.

Explain things simply.

Be intelligent.
""",

"Iron Man":
"""
You are Tony Stark.

Funny.

Sarcastic.

Genius.
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

# ---------------------------------------
# Sidebar
# ---------------------------------------
st.sidebar.title("⚙️ Settings")

personality = st.sidebar.selectbox(
    "Choose Personality",
    list(characters.keys())
)

style = st.sidebar.selectbox(
    "Response Style",
    [
        "Normal",
        "Funny",
        "Motivational",
        "Serious"
    ]
)

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------------------------------
# Main Title
# ---------------------------------------
st.title("🌌 Multiverse AI")

st.write("Chat with your favorite personality.")

# ---------------------------------------
# Display Chat History
# (Assignment Requirement)
# ---------------------------------------
for message in st.session_state.messages:

    avatar = None

    if message["role"] == "assistant":
        avatar = avatars[personality]

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------------------------------
# Chat Input
# (Assignment Requirement)
# ---------------------------------------
if user_message := st.chat_input("Say something..."):

    # Save User Message
    st.session_state.messages.append({
        "role":"user",
        "content":user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    # Build Conversation History
    history = ""

    for msg in st.session_state.messages:

        history += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
{characters[personality]}

You must remain in character.

Conversation History:

{history}

Reply in a {style} style.

Keep answers under 80 words.
"""

    with st.chat_message(
        "assistant",
        avatar=avatars[personality]
    ):

        with st.spinner("Connecting to the Multiverse..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                reply = response.text

            except Exception as e:

                reply = f"Error: {e}"

        st.markdown(reply)

    # Save AI Response
    st.session_state.messages.append({
        "role":"assistant",
        "content":reply
    })

    # Token Estimator
    total_characters = len(user_message)

    token_count = total_characters / 4

    st.info(
        f"🧠 Estimated Tokens Used: {token_count:.2f}"
    )

# ---------------------------------------
# Download Chat
# ---------------------------------------
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

# ---------------------------------------
# Footer
# ---------------------------------------
st.markdown("---")

st.caption("Built with ❤️ using Streamlit + Google Gemini")