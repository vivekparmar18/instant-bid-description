import re
import json
import asyncio
import pandas as pd
import streamlit as st

from app.helper.generate_description import DescriptionGenerator


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def display_sample_jsons():
    sample_json_files = ["app/static/1.json", "app/static/2.json", "app/static/3.json"]
    col1, col2, col3 = st.columns(3, gap="small")

    with col1:
        with st.container(height=300):
            st.markdown(
                """
                <div style="text-align: center; font-weight: bold; font-size:20px; padding-bottom:10px">
                    Sample 1
                </div>
                """,
                unsafe_allow_html=True
            )

            with open(sample_json_files[0], "r") as f:
                json_data = f.read()

            json_string = json.dumps(json.loads(json_data), indent=2)
            st.code(json_string, language="json")

    with col2:
        with st.container(height=300):
            st.markdown(
                """
                <div style="text-align: center; font-weight: bold; font-size:20px; padding-bottom:10px">
                    Sample 2
                </div>
                """,
                unsafe_allow_html=True
            )

            with open(sample_json_files[1], 'r') as f:
                data = json.load(f)

            flat_data = flatten_json(data)
            st.table(flat_data)

    with col3:
        with st.container(height=300):
            st.markdown(
                """
                <div style="text-align: center; font-weight: bold; font-size:20px; padding-bottom:10px">
                    Sample 3
                </div>
                """,
                unsafe_allow_html=True
            )
            with open(sample_json_files[2], "r") as f:
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
                bullet_points_description = await description_generator.get_bullet_point_description(json_data,
                                                                                                     char_limit)
                paragraph_description = await description_generator.get_paragraph_description(json_data, char_limit)
        display_descriptions(bullet_points_description, paragraph_description)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
