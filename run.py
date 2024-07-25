import re
import json
import asyncio
import pandas as pd
import streamlit as st

from app.helper.generate_description import DescriptionGenerator


def display_sample_jsons():
    sample_json_files = ["app/static/1.json", "app/static/2.json", "app/static/3.json"]
    columns = st.columns(3, gap="small")

    for i, col in enumerate(columns):
        with col:
            with st.container(height=300):
                st.markdown(
                    f"""
                    <div style="text-align: center; font-weight: bold; font-size:20px; padding-bottom:10px">
                        Sample {i + 1}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                with open(sample_json_files[i], "r") as f:
                    json_data = f.read()

                json_string = json.dumps(json.loads(json_data), indent=2)
                st.code(json_string, language="json")

    sample_json_number = pd.DataFrame({'first column': ["Sample - 1", "Sample - 2", "Sample - 3"]})

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
    chars_number = pd.DataFrame({'first column': ["500 Characters", "1500 Characters", "2000 Characters"]})

    char_limit = st.selectbox(
        'Select Character Limit',
        chars_number['first column']
    )

    return char_limit


def display_descriptions(bullet_points_description, paragraph_description):
    col1, col2 = st.columns(2)

    with col1:
        with st.container(height=600):
            st.subheader('Bullet Point Description', divider='red')
            st.write(bullet_points_description)
    with col2:
        with st.container(height=600):
            st.subheader('Paragraph Description', divider='red')
            st.write(paragraph_description)


async def main():
    st.set_page_config(
        page_title="Instant Bid Description",
        page_icon=":car:",
        layout="wide"
    )

    st.title("Instant Bid Description")
    st.subheader("Generate description from Instant Bids with ease !🚗")

    json_data = display_sample_jsons()
    st.subheader("OR")
    data = get_json_file()

    char_limit = get_char_limit()

    description_generator = DescriptionGenerator()

    if st.button("Generate Description"):
        with st.spinner("Generating Description..."):
            if data:
                bullet_points_description = await description_generator.get_bullet_point_description(data, char_limit)
                paragraph_description = await description_generator.get_paragraph_description(data, char_limit)
            else:
                bullet_points_description = await description_generator.get_bullet_point_description(json_data, char_limit)
                paragraph_description = await description_generator.get_paragraph_description(json_data, char_limit)
        display_descriptions(bullet_points_description, paragraph_description)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
