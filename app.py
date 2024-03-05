from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import streamlit as st
import os 
import google.generativeai as genai 

load_dotenv() ## loading all the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded") 
	
## Initialize streamlit app
st.set_page_config(page_title="Image Caption Generator App")
st.header('Gemini LLM Image Caption Generator Application')
uploaded_file=st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button('Give me Image Captions')


input_prompt="""
You are an expert in analyzing image. You have to look into image and analyze the image.
You have to give list of top 5 Image caption that can be analyzed from image. Caption should be in maximum 
10 words.
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt, image_data) 
    st.header("The Response is")
    st.write(response) 

