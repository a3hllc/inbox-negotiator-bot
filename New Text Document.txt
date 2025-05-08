"""
Inbox Negotiator Bot v1.0.0
Copyright (c) 2025 A3H LLC. All rights reserved.
Licensed for personal use only.
"""

import streamlit as st

# ----------------------------
# App Setup
# ----------------------------
st.set_page_config(page_title="Inbox Negotiator Bot", page_icon="💬")
st.title("📬 Inbox Negotiator Bot")
st.caption("Smart replies for freelancers — local mode")

# ----------------------------
# Mock Email Input
# ----------------------------
mock_email = """
Hi there,

I found your profile on LinkedIn and I'm wondering if you're available for a quick project.
It's a small design job. Budget is a bit tight but should be quick.
Let me know if you're interested.

Best,
John
"""

st.subheader("1. Paste Client Email")
email_text = st.text_area("Client Email", value=mock_email, height=200)

# ----------------------------
# Tone Selection
# ----------------------------
tone = st.selectbox("2. Choose Response Tone", ["Polite", "Assertive", "Chill"])

# ----------------------------
# Generate Reply (Mock Mode)
# ----------------------------
def generate_reply(email: str, tone: str) -> str:
    if tone == "Polite":
        return ("Hi John,\n\nThanks so much for reaching out! I'd love to hear more about the project scope "
                "and timeline. Feel free to share the details and your budget expectations.\n\nBest,\n[Your Name]")
    elif tone == "Assertive":
        return ("Hi John,\n\nThanks for getting in touch. To evaluate this properly, I'd need a clear scope and "
                "your target budget. I typically take on design projects with clear timelines and compensation.\n\nBest,\n[Your Name]")
    else:
        return ("Hey John,\n\nAppreciate you reaching out. Happy to chat more — just shoot over the brief and "
                "let me know what you’ve got in mind budget-wise.\n\nCheers,\n[Your Name]")

if st.button("3. Generate Reply"):
    reply = generate_reply(email_text, tone)
    st.text_area("Suggested Reply", value=reply, height=200)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("© 2025 A3H LLC · Inbox Negotiator Bot v1.0.0")
