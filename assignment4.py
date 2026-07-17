import streamlit as st
import requests
import random
import urllib.parse

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 AI Image Studio")
st.write("Generate amazing AI images with different art styles!")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("⚙️ Settings")

art_style = st.sidebar.selectbox(
    "Select Art Style",
    [
        "Photorealistic",
        "Anime",
        "Vintage Victorian",
        "Sketch",
        "3D Render"
    ]
)

width = st.sidebar.slider(
    "Image Width",
    min_value=256,
    max_value=1024,
    value=768
)

height = st.sidebar.slider(
    "Image Height",
    min_value=256,
    max_value=1024,
    value=768
)

magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# -------------------------------
# Random Prompts
# -------------------------------
random_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon flying over the Taj Mahal at sunset",
    "A futuristic underwater city",
    "A magical forest with glowing animals"
]

# -------------------------------
# User Prompt
# -------------------------------
user_prompt = st.text_input("Describe the image you want to generate")

generate = st.button("🎨 Generate Image")
surprise = st.button("🎲 Surprise Me!")

# -------------------------------
# Decide Prompt
# -------------------------------
prompt = ""

if generate:
    prompt = user_prompt

elif surprise:
    prompt = random.choice(random_prompts)
    st.info(f"🎲 Surprise Prompt:\n\n**{prompt}**")

# -------------------------------
# Image Generation
# -------------------------------
if prompt:

    full_prompt = f"{prompt}, make the art style: {art_style}"

    # Magic Enhance
    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    encoded_prompt = urllib.parse.quote(full_prompt)

    # Assignment Requirement 1
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}"
    )

    with st.spinner("🎨 Rendering your image..."):

        response = requests.get(url)

    if response.status_code == 200:

        st.success("✅ Image Generated Successfully!")

        st.image(
            response.content,
            caption=full_prompt,
            use_container_width=True
        )

        # Assignment Requirement 2
        filename = f"{art_style.lower().replace(' ', '_')}_image.png"

        st.download_button(
            "📥 Download Image",
            data=response.content,
            file_name=filename,
            mime="image/png"
        )

    else:

        st.error("❌ Failed to generate image. Please try again.")