import asyncio
import streamlit as st

from app.helper.invoke_api import InvokeAPI
from app.helper.generate_description import DescriptionGenerator


def display_descriptions(api_response, paragraph_description):
    col1, col2 = st.columns(2)

    with col1:
        with st.container(height=600):
            st.subheader('Instant Bid API JSON Response', divider='red')
            st.json(api_response)
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
                 "(Sample IDs: 756335, 756336, 756337, 756338, 756339)")

    invoke_api = InvokeAPI()
    description_generator = DescriptionGenerator()

    is_button_clicked = False
    api_response, paragraph_description = None, None

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        instant_bid_id = st.text_input("Instant Bid ID", label_visibility="collapsed",
                                       placeholder="Enter Instant Bid ID")

    with col2:
        if st.button("Generate"):
            is_button_clicked = True

    with col3:
        print()

    with col4:
        print()

    if is_button_clicked:
        with st.spinner("Fetching Instant Bid Data..."):
            api_response = invoke_api.invoke_instant_bid_api(instant_bid_id)

        with st.spinner("Generating Description..."):
            paragraph_description = await description_generator.get_paragraph_description(api_response, 2000)

        display_descriptions(api_response, paragraph_description)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
