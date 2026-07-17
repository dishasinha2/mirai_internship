import streamlit as st
from google import genai
from google.genai import types
import requests
import json
import os
import re
import tempfile
import uuid
from gtts import gTTS

# --------------------------------------------------------------------------
# PHASE 1: THE DIRECTOR'S CUT (UI & CONFIGURATION)
# --------------------------------------------------------------------------

st.set_page_config(page_title="AI Visual Novel Engine", page_icon="📖", layout="wide")


@st.cache_resource
def get_gemini_client(api_key: str):
    """Create and cache the Gemini client so we don't re-init on every rerun."""
    return genai.Client(api_key=api_key)


# --- Sidebar: Story Settings -------------------------------------------------

# Look for the key in the environment first (e.g. GEMINI_API_KEY set in your shell,
# a .env file, or your deployment platform's secrets manager). Fall back to a manual
# text input only if it isn't found, so this still works for anyone without the env var.
env_api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

with st.sidebar:
    st.title("📖 Story Settings")

    if env_api_key:
        api_key = env_api_key
        st.success("Gemini API key loaded from environment ✅")
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get a free key at https://aistudio.google.com/apikey",
        )

    genre = st.selectbox(
        "Story Genre",
        ["Fantasy Adventure", "Sci-Fi Thriller", "Mystery/Noir", "Horror", "Slice of Life", "Cyberpunk"],
    )

    art_style = st.selectbox(
        "Art Style",
        ["Studio Ghibli anime", "Watercolor painting", "Dark graphic novel", "Pixel art", "Photorealistic cinematic"],
    )

    st.divider()
    if st.button("🔄 Restart Story", use_container_width=True):
        for key in ["chat", "history", "current_story", "current_image_prompt", "current_options", "current_audio"]:
            st.session_state.pop(key, None)
        st.rerun()

# --- Session State Initialization -------------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = None
if "history" not in st.session_state:
    st.session_state.history = []          # list of {"role": ..., "content": ...} for display
if "current_story" not in st.session_state:
    st.session_state.current_story = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None   # bytes of the last generated image
if "current_options" not in st.session_state:
    st.session_state.current_options = []
if "current_audio" not in st.session_state:
    st.session_state.current_audio = None   # path to last generated mp3

st.title("🎭 AI Multi-Modal Visual Novel")
st.caption(f"Genre: **{genre}** | Art Style: **{art_style}**")

if not api_key:
    st.info("👈 Enter your Gemini API key in the sidebar to begin your story.")
    st.stop()

client = get_gemini_client(api_key)

# --------------------------------------------------------------------------
# PHASE 2: THE STRUCTURED JSON ENGINE
# --------------------------------------------------------------------------

SYSTEM_PROMPT = f"""
You are the narrative engine for an interactive visual novel.

Genre: {genre}
Art style for all image prompts: {art_style}

RULES:
1. You must respond with ONLY a valid JSON object — no markdown fences, no commentary,
   no text before or after the JSON.
2. The JSON object must have EXACTLY these three keys:
   - "story_text": a vivid narrative paragraph (4-8 sentences) continuing the story.
   - "image_prompt": a heavily detailed, descriptive prompt (setting, subject, mood,
     lighting, composition) written for an AI image generator, styled as "{art_style}".
   - "options": a JSON list of 2 to 3 short, distinct strings describing what the
     protagonist could do next.

Example of the exact shape required:
{{
  "story_text": "...",
  "image_prompt": "...",
  "options": ["Option A", "Option B", "Option C"]
}}

Never break character. Never include text outside the JSON object.
"""


def extract_json(raw_text: str) -> dict:
    """
    Gemini sometimes wraps JSON in ```json fences or adds stray text.
    This strips fences and pulls out the first {...} block, then parses it.
    """
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    # Fallback: grab the outermost { ... } block if there's stray text around it
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)

    return json.loads(cleaned)  # import json is used here


def advance_story(user_action: str | None):
    """Send the user's action (or a 'begin' kickoff) to Gemini and parse the JSON reply."""
    if st.session_state.chat is None:
        st.session_state.chat = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        prompt = "Begin the story now with an opening scene."
    else:
        prompt = f"The player chose: \"{user_action}\"\n\nContinue the story from here, following the same JSON format and rules as before."

    with st.spinner("The story is being written..."):
        try:
            response = st.session_state.chat.send_message(prompt)
            raw_text = response.text
        except Exception as e:
            st.toast(f"⚠️ Story engine error: {e}", icon="⚠️")
            return

    try:
        data = extract_json(raw_text)
        story_text = data["story_text"]
        image_prompt = data["image_prompt"]
        options = data["options"]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        st.toast("⚠️ Couldn't parse the AI's response as JSON. Try again.", icon="⚠️")
        return

    # ----------------------------------------------------------------------
    # PHASE 4: MULTI-MEDIA RENDERING (IMAGE)
    # ----------------------------------------------------------------------
    image_bytes = generate_image(image_prompt)

    # ----------------------------------------------------------------------
    # PHASE 4: MULTI-MEDIA RENDERING (TTS AUDIO)
    # ----------------------------------------------------------------------
    audio_path = generate_narration(story_text)

    # Save everything into session_state so it persists across reruns
    st.session_state.current_story = story_text
    st.session_state.current_image = image_bytes
    st.session_state.current_options = options
    st.session_state.current_audio = audio_path

    st.session_state.history.append({"role": "narrator", "content": story_text})


# --------------------------------------------------------------------------
# PHASE 4 HELPERS: IMAGE + TTS GENERATION (WRAPPED FOR GRACEFUL FAILURE)
# --------------------------------------------------------------------------

def generate_image(image_prompt: str):
    """Call the Pollinations API and return raw image bytes, or None on failure."""
    try:
        encoded_prompt = requests.utils.quote(image_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=512&nologo=true"
        resp = requests.get(url, timeout=25)
        resp.raise_for_status()
        return resp.content
    except Exception:
        st.toast("🖼️ Image server is busy, skipping visual...", icon="🖼️")
        return None


def generate_narration(story_text: str):
    """Convert story_text to speech with gTTS and return the mp3 file path, or None on failure."""
    try:
        tts = gTTS(text=story_text, lang="en")
        audio_path = os.path.join(tempfile.gettempdir(), f"narration_{uuid.uuid4().hex}.mp3")
        tts.save(audio_path)
        return audio_path
    except Exception:
        st.toast("🔊 Narration engine is busy, skipping audio...", icon="🔊")
        return None


# --------------------------------------------------------------------------
# PHASE 3: DYNAMIC UI GENERATION + RENDERING
# --------------------------------------------------------------------------

# Kick off the story if this is a fresh session
if st.session_state.current_story is None:
    advance_story(None)

col_img, col_story = st.columns([1, 1.3])

with col_img:
    if st.session_state.current_image:
        st.image(st.session_state.current_image, use_container_width=True)
    else:
        st.markdown(
            "<div style='padding:2rem;text-align:center;border:1px dashed #999;border-radius:8px;'>"
            "🖼️ No image available for this scene</div>",
            unsafe_allow_html=True,
        )

with col_story:
    if st.session_state.current_story:
        st.markdown(f"### {st.session_state.current_story}")

    if st.session_state.current_audio:
        st.audio(st.session_state.current_audio, format="audio/mp3")

    st.divider()
    st.markdown("#### What do you do?")

    # Dynamically generate one button per option returned by the AI
    for i, option in enumerate(st.session_state.current_options):
        if st.button(option, key=f"option_{i}_{len(st.session_state.history)}", use_container_width=True):
            advance_story(option)
            st.rerun()

# --- Story log (collapsible) -------------------------------------------------
with st.expander("📜 Story so far"):
    for entry in st.session_state.history:
        st.write(entry["content"])
        st.markdown("---")
