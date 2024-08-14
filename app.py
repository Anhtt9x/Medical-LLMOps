import streamlit as st
import base64
import os
from dotenv import load_dotenv 
import tempfile
from openai import OpenAI
from src.help import *


load_dotenv()

huggingface_key = os.getenv("HUGGING_FACE_API_TOKEN")
openai_key = os.getenv("OPEN_AI_KEY")

client = OpenAI(api_key=openai_key)

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "result" not in st.session_state:
    st.session_state.result = None


def encode_image(image_path):
    with open(image_path, "rb") as image:
        return base64.b64encode(image.read()).decode("utf-8")
    

def chat_eli(query):
    eli_prompt = "you have to explain the below piece of infomation to a five year old \n" +query
    

    prompt = [
        {
            "role":"user",
            "content":eli_prompt
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=1500
    )
    return response.choices[0].message.content


def call_gpt4_model_analis(file_name:str, sample_prompt=sample_prompt):
    base64_image = encode_image(file_name)

    message = [
        {
            "role":"user",
            "content":[
                {
                    "type": "text", "text":sample_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail":"high"
                    }
                }
            ]
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=message,
        max_tokens=1500
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content


st.title("Medical Diseases")

with st.expander("About this Application"):
    st.write("Upload image to GPT-4-vision")


upload_file = st.file_uploader("Upload image",type=["png","jpg","jpeg"])

if upload_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(upload_file.name)[1]) as tmp_file:
        tmp_file.write(upload_file.getvalue())
        st.session_state['filename'] = tmp_file.name

    st.image(upload_file,caption="Uploaded image")


if st.button("Analysis Image"):
    if "filename" in st.session_state or os.path.exists(st.session_state['filename']):
        st.session_state['result'] = call_gpt4_model_analis(st.session_state['filename'])
        st.markdown(st.session_state['result'], unsafe_allow_html=True)
        os.unlink(st.session_state['filename'])


