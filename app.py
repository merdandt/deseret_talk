import streamlit as st
import json
import requests
from typing import Optional
import warnings

# Set page configuration
st.set_page_config(page_title="Speaking with the Book Of Mormon", layout="wide")

# Define constants from st.secrets
BASE_API_URL = st.secrets['BASE_API_URL']
LANGFLOW_ID = st.secrets['LANGFLOW_ID']
FLOW_ID = st.secrets['FLOW_ID']
APPLICATION_TOKEN = st.secrets['APPLICATION_TOKEN']
ENDPOINT = st.secrets['ENDPOINT']

# Tweaks dictionary (if any tweaks are needed)
TWEAKS = {
  "ChatInput-n1xIr": {},
  "ParseData-pD6xT": {},
  "Prompt-a84Ga": {},
  "SplitText-XK9Yk": {},
  "OpenAIModel-C6urm": {},
  "ChatOutput-G0vf4": {},
  "AstraDB-fJck3": {},
  "OpenAIEmbeddings-37lct": {},
  "AstraDB-kMQFM": {},
  "OpenAIEmbeddings-RMxPJ": {},
  "File-w0ZcX": {}
}

def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if APPLICATION_TOKEN:
        headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


# Main interface
st.title("Speaking with the Book Of Mormon")

message = st.text_area("I want to learn more about...", "")

# Example questions to display
example_questions = [
    "What is the Book of Mormon?",
    "What is the significance of the plates of brass?",
    "How does the Book of Mormon use the allegory of the olive tree?",
    "Who wrote the Book of Mormon?", 
]
# Display example questions
st.write("Example Questions:")
for question in example_questions:
    st.write(f"- {question}")

if st.button("   Ask   "):
    error_flag = False
    if not message:
        st.error("Please enter a message.")
        error_flag = True
    if not APPLICATION_TOKEN:
        st.error("Application token is missing.")
        error_flag = True
    if not LANGFLOW_ID:
        st.error("Langflow ID is missing.")
        error_flag = True
    if not BASE_API_URL:
        st.error("Base API URL is missing.")
        error_flag = True

    if not error_flag:
        with st.spinner("Thinking..."):
            response = run_flow(
                message=message,
                output_type="chat",
                input_type="chat",
                tweaks=TWEAKS,
             )
        st.write("Response:")
        try:
            print(json.dumps(response, indent=2))
            # Navigate the JSON structure to find the text
            answer = response['outputs'][0]['outputs'][0]['results']['message']['data']['text']
            # Display the text to the user
            st.markdown(answer)
        except (KeyError, IndexError, TypeError) as e:
            st.error("Could not parse the response.")
            st.json(response)