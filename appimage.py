import streamlit as st

import requests

 

st.title("MY AI IMAGE GENERATOR")

 

st.sidebar.header("SETTINGS")

art_style=st.sidebar.selectbox(

    "Select desired Art Style",

    ["Photorealistic","Anime","Vintage Victorian","Sketch","3D Render"]

)

 

width=st.sidebar.slider("Image width",min_value=256,max_value=1024,value=768)

height=st.sidebar.slider("Image height",min_value=256,max_value=1024,value=768)

 

user_prompt=st.text_input("Decribe the image you want to generate")
if st.button("Generate Image"):

    if user_prompt:

        with st.spinner("Rendering the image"):

            # Include the height and width on your own

            full_prompt=f"{user_prompt}, make the art style: {art_style}"

            url=f"https://image.pollinations.ai/prompt/{full_prompt}"

            response=requests.get(url)

 

            if response.status_code==200:

                st.success("Image Generated")

                # st.write(response)

                # Convert the binary into pixels or an actual image

                st.image(response.content,caption=full_prompt)
                st.download_button("Download Image",data=response.content,file_name="image.png",mime="image/png")

            else:

                st.error("API is not working")