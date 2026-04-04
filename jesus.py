import streamlit as st
import google.generativeai as genai
import os

# --- Config ---
# Read API key securely from Streamlit Secrets
API_KEY = os.getenv("GEMINI_API_KEY")  # <- make sure you added this in Streamlit Secrets
MODEL = "gemini-2.5-flash"

# Configure the Gemini client
genai.configure(api_key=API_KEY)

# --- Load knowledge base ---
with open("chatbot.txt", "r") as f:
    kb = f.read()

# --- System prompt ---
system_prompt = f"""
You are the Bread of Life AG Church chatbot.
Your job is to provide church member details,
and also give details about the church.
Always respond politely.
{kb}
"""

# --- Initialize chat ---
if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=system_prompt
    )
    st.session_state.chat = model.start_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Streamlit UI ---
st.title("Bread of Life AG Church")
st.caption("Church Information Chatbot")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask something about the church or members...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get AI response
    response = st.session_state.chat.send_message(user_input)
    reply = response.text

    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
