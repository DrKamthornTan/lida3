import streamlit as st
import pandas as pd

st.header("DHV AI Startup Demo to Chat with Excel")

# Load the dataframe from the saved filename.csv
dataframe = pd.read_csv("filename.csv")

# Display the dataframe
st.dataframe(dataframe)

# Rest of your code...
from lida import Manager, TextGenerationConfig, llm
import os
import openai
from PIL import Image
from io import BytesIO
import base64

openai.api_key = os.getenv('OPENAI_API_KEY')

lida = Manager(text_gen=llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)

    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))



st.subheader("Generate Graph from File")


text_area = st.text_area("Query your Data to Generate Graph", height=200)
if st.button("Generate Graph"):
    if len(text_area) > 0:
        st.info("Your Query: " + text_area)
        lida = Manager(text_gen=llm("openai"))
        textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)

        summary = lida.summarize("filename1.csv", summary_method="default", textgen_config=textgen_config)
        user_query = text_area

        charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config)
        image_base64 = charts[0].raster
        img = base64_to_image(image_base64)
        st.image(img)