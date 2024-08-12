import re
import json
import asyncio
import pandas as pd
import streamlit as st

from app.helper.generate_description import DescriptionGenerator


def display_sample_jsons():
    sample_json_files = ["app/static/1.json", "app/static/2.json", "app/static/3.json", "app/static/4.json",
                         "app/static/5.json"]

    sample_json_number = pd.DataFrame(
        {'first column': ["Sample - 1", "Sample - 2", "Sample - 3", "Sample - 4", "Sample - 5"]})

    sample_number = st.selectbox(
        "Select Sample Number",
        options=sample_json_number['first column']
    )

    num = re.findall(r'\d+', sample_number)
    index_num = int(num[0])
    document_path = sample_json_files[index_num - 1]
    print(f"Sample {num} is processed!")
    with open(document_path, "r") as f:
        json_data = f.read()

    json_data = json.loads(json_data)
    return json_data


def get_json_file():
    uploaded_file = st.file_uploader("Select JSON File", type=['json'])
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        data = json.loads(file_content)
        return data
    else:
        return None


def get_char_limit():
    chars_number = pd.DataFrame({'first column': ["2000 Characters", "1500 Characters", "500 Characters"]})
    char_limit = st.selectbox(
        'Select Character Limit',
        chars_number['first column']
    )

    return char_limit


def display_descriptions(formatted_data, paragraph_description):
    col1, col2 = st.columns(2)

    with col1:
        with st.container(height=600):
            st.subheader('Instant Bid API JSON Response', divider='red')
            st.code(formatted_data)
    with col2:
        with st.container(height=600):
            st.subheader('Description', divider='red')
            st.write(paragraph_description)


async def main():
    st.set_page_config(
        page_title="Instant Bid - Description Generator PoC",
        page_icon=":car:",
        layout="wide"
    )

    st.title("Instant Bid - Description Generator PoC")
    st.divider()
    st.subheader("Provide your Instant Bid ID to generate description\n "
                 "(Sample IDs: 682095, 682096, 682097, 682101, 682102)")

    data = """"""

    description_generator = DescriptionGenerator()

    instant_bid_id = st.text_input("Instant Bid ID", label_visibility="collapsed")

    if st.button("Generate"):
        print("data")
        # with st.spinner("Generating Description..."):
        #     paragraph_description = await description_generator.get_paragraph_description("json_data", "char_limit")
        # display_descriptions(data, paragraph_description)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
