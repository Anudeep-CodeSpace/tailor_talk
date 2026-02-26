import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# --- Configuration ---
# This looks for a secret in Streamlit Cloud. 
# If it doesn't find it (like when running locally), it defaults to your local FastAPI server.
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000/chat")

# --- UI Setup ---
st.set_page_config(page_title="TailorTalk Titanic Agent", page_icon="🚢", layout="centered")
st.title("🚢 TailorTalk: Titanic Data Assistant")
st.markdown("Ask me anything about the Titanic dataset! Try asking for a histogram or average fares.")
st.warning('Backend uses a free tier llm, can hit rate limit quickly.', icon='⚠️')

# --- Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"]:
            try:
                image_bytes = base64.b64decode(message["image"])
                image = Image.open(BytesIO(image_bytes))
                st.image(image)
            except Exception as e:
                st.error("Failed to load visualization.")

# --- User Input ---
if prompt := st.chat_input("E.g., What percentage of passengers were male?"):
    # 1. Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Call FastAPI Backend
    with st.chat_message("assistant"):
        # Added a helpful note for the free-tier Render "cold start" delay
        with st.spinner("Analyzing data... (If this is the first request in a while, the server might take 30-50s to wake up)"):
            try:
                response = requests.post(BACKEND_URL, json={"query": prompt}, timeout=120)
                response.raise_for_status()
                data = response.json()
                
                answer = data.get("answer", "No text response provided.")
                image_base64 = data.get("image")

                # Display text
                st.markdown(answer)
                
                # Display image if present
                if image_base64:
                    try:
                        image_bytes = base64.b64decode(image_base64)
                        image = Image.open(BytesIO(image_bytes))
                        st.image(image)
                    except Exception as e:
                        st.error("Generated an image, but failed to display it.")
                
                # Save to session state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "image": image_base64
                })

            except requests.exceptions.Timeout:
                error_msg = "Request timed out. The Render server might still be waking up. Please try again!"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except requests.exceptions.RequestException as e:
                error_msg = f"Error connecting to backend: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})