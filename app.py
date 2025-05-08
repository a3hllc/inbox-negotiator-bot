# app.py
"""
Inbox Negotiator Bot v1.0.0 (OpenAI API Mode)
Copyright (c) 2025 A3H LLC. All rights reserved.
Licensed for personal use only.
"""

import streamlit as st
import openai
import os
from gmail_reader import get_latest_email

st.set_page_config(page_title="Inbox Negotiator Bot", page_icon="💬")
st.title("📬 Inbox Negotiator Bot")
st.caption("Smart replies for freelancers — local + Gmail + AI mode")

# Set your OpenAI API key securely here or via environment variable
API_KEY = os.getenv("OPENAI_API_KEY") or "sk-proj-your-real-key-here"

st.subheader("1. Paste Client Email or Fetch from Gmail")

if "email_text" not in st.session_state:
    st.session_state.email_text = ""

col1, col2 = st.columns([3, 1])

with col1:
    st.text_area("Client Email", value=st.session_state.email_text, height=200, key="email_input")

with col2:
    if st.button("📬 Fetch from Gmail"):
        try:
            st.session_state.email_text = get_latest_email()
            st.success("Latest email fetched!")
        except Exception as e:
            st.error(f"Failed to fetch email: {e}")

st.subheader("2. Choose Response Tone")
tone = st.selectbox("Tone", ["Polite", "Assertive", "Chill"])

st.subheader("3. Generate Reply")

def generate_reply(email: str, tone: str) -> str:
    prompt = (
        f"You're a helpful freelance assistant. A client sent this email:\n\n"
        f"{email}\n\n"
        f"Write a {tone.lower()} reply as a professional freelancer."
    )
    try:
        client = openai.OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error generating reply: {e}]"

if st.button("✉️ Generate Reply"):
    reply = generate_reply(st.session_state.email_text, tone)
    st.text_area("Suggested Reply", value=reply, height=200)

st.markdown("---")
st.caption("© 2025 A3H LLC · Inbox Negotiator Bot v1.0.0 · Co