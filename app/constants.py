class Prompts:
    BULLET_POINT_PROMPT = """
    Describe this JSON file in a bullet-point list without losing any information, keeping the description within {num_chars} characters.
    """

    PARAGRAPH_PROMPT = """
    Generate a detailed and accurate paragraph summary of maximum {num_chars} characters limit based on the user's input. Ensure precision and conciseness to deliver a focused and insightful summary without losing any information from the input. Avoid any suggestions or misconceptions not presented in the input.
    """


REFERENCE_DESCRIPTION_FIRST_LAST_LINE = [
    "Here's a compact bullet",
    "Here's a comprehensive yet",
    "This overview covers all",
    "Here's a bullet-point summary",
    "This summary covers all",
    "This JSON file describes",
    "Here's a detailed description",
    "This bid is focused"
]


class Messages:
    BLANK_PDF = "It seems that the json data you provided is blank. Unfortunately, I can't generate a description from empty content. Please upload a json with readable text."
