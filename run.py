import json
import asyncio
import pandas as pd
import streamlit as st

from app.helper.generate_description import DescriptionGenerator


def set_custom_css():
    st.markdown(
        """
        <style>
        .code-block-container {
            height: 250px;
            width: 100%; /* Set width to 100% for full-width columns */
            overflow: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def display_json_data(json_data):
    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            st.write(f'Sample {i + 1}')
            json_string = json.dumps(json.loads(json_data), indent=2)
            st.markdown(f'<div class="code-block-container"><pre><code>{json_string}</code></pre></div>',
                        unsafe_allow_html=True)


def display_select_boxes(df1, df2):
    col1, col2, col3 = st.columns(3)
    with col1:
        sample_number = st.selectbox(
            'Select Sample Number',
            df1['first column']
        )
    with col2:
        char_limit = st.selectbox(
            'Select Character Limit',
            df2['first column']
        )
    with col3:
        if st.button("Generate Description"):
            st.write("Response")
    return sample_number, char_limit


def display_file_uploader():
    uploaded_file = st.file_uploader("Select JSON File", type=['json'])
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        data = json.loads(file_content)
        return data
    else:
        return None


def display_code_columns(bullet_points_description, paragraph_description):
    col1, col2 = st.columns(2)
    with col1:
        st.code(bullet_points_description)
    with col2:
        st.code(paragraph_description)


async def main():
    description_generator = DescriptionGenerator()
    set_custom_css()
    json_data = ""
    # display_json_data(json_data)
    df1 = pd.DataFrame({'first column': [1, 2, 3, 4]})
    df2 = pd.DataFrame({'first column': [500, 1500, 2000]})
    sample_number, char_limit = display_select_boxes(df1, df2)
    data = display_file_uploader()
    if data:
        paragraph_description = await description_generator.get_paragraph_description(data, char_limit)
        bullet_points_description = await description_generator.get_bullet_point_description(data, char_limit)
        display_code_columns(bullet_points_description, paragraph_description)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
