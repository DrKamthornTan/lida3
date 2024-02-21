import streamlit as st
from lida import Manager, TextGenerationConfig, llm
import os
import openai
from PIL import Image
from io import BytesIO
import base64
import pandas as pd

openai.api_key = os.getenv('OPENAI_API_KEY')

lida = Manager(text_gen=llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)

    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

def convert_to_csv(file):
    if isinstance(file, str):
        # File is already in CSV format
        return file

    if file.name.endswith('.xlsx'):
        # Read the XLSX file
        df = pd.read_excel(file, engine='openpyxl')
    elif file.name.endswith('.csv'):
        # Read the CSV file
        df = pd.read_csv(file)
    else:
        raise ValueError("Unsupported file format. Only XLSX and CSV files are supported.")

    # Convert to CSV
    csv_file = file.name.replace(".xlsx", ".csv")
    df.to_csv(csv_file, index=False)

    return csv_file

st.header("DHV AI Startup Demo to Chat with Excel")

st.subheader("Summarization of your Data")
file_uploader = st.file_uploader("Upload your XLSX or CSV", type=["xlsx", "csv"])
if file_uploader is not None:
    file_type = file_uploader.name.split(".")[-1]

    if file_type == "xlsx":
        # Convert Excel to CSV
        csv_file_path = convert_to_csv(file_uploader)

        summary = lida.summarize(csv_file_path, summary_method="default", textgen_config=textgen_config)
        # st.write(summary)

        goals = lida.goals(summary, n=2, textgen_config=textgen_config)
        for goal in goals:
            st.write(goal)

        i = 0
        library = "seaborn"
        textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)

        charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)
        img_base64_string = charts[0].raster
        img = base64_to_image(img_base64_string)
        st.image(img)

        if len(goals) > 1:
            second_goal_charts = lida.visualize(summary=summary, goal=goals[1], textgen_config=textgen_config, library=library)
            second_goal_img_base64_string = second_goal_charts[0].raster
            second_goal_img = base64_to_image(second_goal_img_base64_string)
            st.image(second_goal_img)

    elif file_type == "csv":
        csv_file_path = convert_to_csv(file_uploader)

        summary = lida.summarize(csv_file_path, summary_method="default", textgen_config=textgen_config)
        # st.write(summary)

        goals = lida.goals(summary, n=2, textgen_config=textgen_config)
        for goal in goals:
            st.write(goal)

        i = 0
        library = "seaborn"
        textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)

        charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)
        img_base64_string = charts[0].raster
        img = base64_to_image(img_base64_string)
        st.image(img)

        if len(goals) > 1:
            second_goal_charts = lida.visualize(summary=summary, goal=goals[1], textgen_config=textgen_config, library=library)
            second_goal_img_base64_string = second_goal_charts[0].raster
            second_goal_img = base64_to_image(second_goal_img_base64_string)
            st.image(second_goal_img)

    else:
        st.error("Invalid file format. Please upload an Excel or CSV file.")
