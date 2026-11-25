import os
import streamlit as st
from openai import OpenAI

# Page setup
st.set_page_config(page_title="RoastBot 🔥", page_icon="🔥")
st.title("🔥 RoastBot")
st.caption("Say something. Anything. I dare you.")

# Connect to GitHub Models
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

system_prompt = (
    "You are a witty, sarcastic stand-up comedian whose job is to playfully roast "
    "whatever the user says. Keep your roasts clever, punchy, and lighthearted—never "
    "cross the line into genuine cruelty, hate speech, or personal attacks."
)

# Remember chat history on the webpage
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Display previous chat bubbles
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input box at the bottom of the screen
if prompt := st.chat_input("Type something to get roasted..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI roast
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            temperature=0.9,
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
