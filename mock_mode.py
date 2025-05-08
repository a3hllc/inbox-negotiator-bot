# mock_mode.py
"""
Inbox Negotiator Bot v1.0.0 (Mock Mode with Gmail Search + Real Send)
Copyright (c) 2025 A3H LLC. All rights reserved.
Licensed for personal use only.
"""

import streamlit as st
from gmail_reader import get_latest_email, search_emails_by_query, send_email

st.set_page_config(page_title="Inbox Negotiator Bot", page_icon="💬")
st.title("📬 Inbox Negotiator Bot")
st.caption("Smart replies for freelancers — local + Gmail mode (Mock AI + Send)")

# Upgrade toggle
upgrade_mode = st.checkbox("✨ Enable Gmail Search Upgrade")

if "email_text" not in st.session_state:
    st.session_state.email_text = ""

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "selected_reply" not in st.session_state:
    st.session_state.selected_reply = ""

st.subheader("1. Paste Client Email or Fetch from Gmail")

if upgrade_mode:
    search_query = st.text_input("Search Gmail (e.g. from:john@example.com project after:2025/01/01)")
    if st.button("🔍 Search Emails"):
        try:
            st.session_state.search_results = search_emails_by_query(search_query)
        except Exception as e:
            st.error(f"Search failed: {e}")

    for i, item in enumerate(st.session_state.search_results):
        with st.expander(f"📨 {item['date']} — {item['subject']}"):
            st.write(item['snippet'])
            if st.button(f"Use this email", key=f"select_{i}"):
                st.session_state.email_text = item['snippet']
                st.success("Email selected and loaded into input field")
                st.rerun()
else:
    if st.button("📬 Fetch from Gmail"):
        try:
            st.session_state.email_text = get_latest_email()
            st.success("Latest email fetched!")
        except Exception as e:
            st.error(f"Failed to fetch email: {e}")

st.text_area("Client Email", value=st.session_state.email_text, height=200, key="email_input")

st.subheader("2. Choose Response Tone")
tone = st.selectbox("Tone", ["Polite", "Assertive", "Chill"])

st.subheader("3. Generate Reply Options")

def generate_reply_options(email: str, tone: str):
    base = f"Thanks for reaching out! Based on your message, I'd love to learn more about the project."
    if tone == "Polite":
        return [
            base + " Could you please share more about the timeline and expectations?",
            base + " I look forward to hearing the full brief when you're ready."
        ]
    elif tone == "Assertive":
        return [
            base + " Please provide a clear scope and timeline so I can evaluate next steps.",
            base + " Let's clarify deliverables and expectations before proceeding."
        ]
    else:  # Chill
        return [
            base + " Shoot me the details and let’s get rolling!",
            base + " Just send over the brief and we’ll kick it off."
        ]

if st.button("✉️ Generate Reply"):
    replies = generate_reply_options(st.session_state.email_text, tone)
    for idx, r in enumerate(replies):
        if st.button(f"✏️ Use Option {idx+1}", key=f"use_reply_{idx}"):
            st.session_state.selected_reply = r
    for idx, r in enumerate(replies):
        st.text_area(f"Option {idx+1}", value=r, height=150, key=f"reply_{idx}")

st.subheader("4. Send Email")
recipient = st.text_input("Recipient Email")
subject = st.text_input("Email Subject", value="Re: Your Inquiry")
body = st.text_area("Reply to Send", value=st.session_state.selected_reply, height=200, key="final_reply")

if st.button("📤 Send Email"):
    if recipient and body:
        result = send_email(recipient, subject, body)
        if isinstance(result, dict) and result.get('id'):
            st.success(f"Email sent to {recipient} with subject '{subject}'")
        else:
            st.error(result)
    else:
        st.error("Please fill in recipient and message.")

st.markdown("---")
st.caption("© 2025 A3H LLC · Inbox Negotiator Bot v1.0.0 · Co-Founder: SS")
