import streamlit as st
import google.generativeai as genai

API_KEY = "AIzaSyCzw1A20CqsWtm7-IGJNFoFv8eHEvwmMEw"
MODEL = "gemini-2.5-flash"

genai.configure(api_key=API_KEY)

# Load knowledge base
with open("chatbot.txt", "r") as f:
    kb = f.read()

system_prompt = f"""
you are bread of life ag church chatbot...
{kb}
"""

# Init chat
if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=system_prompt
    )
    st.session_state.chat = model.start_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Bread of Life AG Church")

# Chat UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    response = st.session_state.chat.send_message(user_input)
    reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)
