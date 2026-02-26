import streamlit as st
from app import classify_email
from email_reader import fetch_emails

st.set_page_config(
    page_title="AI Email Classifier",
    page_icon="📧",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    body { background-color: #f5f6fa; }
    .main { background-color: #f5f6fa; }

    .header-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #1e3a8a;
        margin-bottom: 0;
    }
    .header-sub {
        font-size: 0.95rem;
        color: #7f8c8d;
        margin-bottom: 20px;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        margin-bottom: 10px;
    }
    .metric-number {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #7f8c8d;
        margin: 0;
    }
    .email-card {
        background: white;
        padding: 16px;
        border-radius: 10px;
        margin: 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    }
    .badge-spam {
        background: #fdecea;
        color: #c0392b;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-promotions {
        background: #fef9e7;
        color: #b7770d;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-support {
        background: #eaf4fb;
        color: #1a6fa1;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-personal {
        background: #eafaf1;
        color: #1e8449;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .alert-box {
        background: #fdecea;
        border-left: 4px solid #c0392b;
        padding: 12px 16px;
        border-radius: 6px;
        color: #c0392b;
        font-size: 0.9rem;
        margin: 10px 0;
    }
    .info-box {
        background: #eaf4fb;
        border-left: 4px solid #1a6fa1;
        padding: 12px 16px;
        border-radius: 6px;
        color: #1a6fa1;
        font-size: 0.9rem;
        margin: 10px 0;
    }
    .warning-box {
        background: #fef9e7;
        border-left: 4px solid #b7770d;
        padding: 12px 16px;
        border-radius: 6px;
        color: #b7770d;
        font-size: 0.9rem;
        margin: 10px 0;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 8px;
        padding: 8px 24px;
        border: none;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .stButton>button:hover {
        background-color: #1a252f;
        color: white;
    }
    .sidebar-note {
        font-size: 0.78rem;
        color: #95a5a6;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Flaticon SVG icons (monochrome, professional)
ICON_INBOX = '<img src="https://cdn-icons-png.flaticon.com/512/2374/2374335.png" width="22" style="filter:grayscale(100%);opacity:0.7;vertical-align:middle;margin-right:8px">'
ICON_EDIT  = '<img src="https://cdn-icons-png.flaticon.com/512/1827/1827951.png" width="22" style="filter:grayscale(100%);opacity:0.7;vertical-align:middle;margin-right:8px">'
ICON_MAIL  = '<img src="https://cdn-icons-png.flaticon.com/512/561/561127.png" width="22" style="filter:grayscale(100%);opacity:0.7;vertical-align:middle;margin-right:8px">'

BADGE = {
    "Spam":       '<span class="badge-spam">Spam</span>',
    "Promotions": '<span class="badge-promotions">Promotions</span>',
    "Support":    '<span class="badge-support">Support</span>',
    "Personal":   '<span class="badge-personal">Personal</span>',
}

COLORS = {
    "Spam": "#c0392b",
    "Promotions": "#b7770d",
    "Support": "#1a6fa1",
    "Personal": "#1e8449"
}

# ── Header ──
st.markdown('<h1 style="font-size:1.5rem;font-weight:700;color:#1e3a8a;margin-bottom:0;">AI EMAIL CLASSIFIER</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size:0.95rem;color:#7f8c8d;margin-bottom:20px;">Powered by Fine-tuned DistilBERT — 98% Accuracy</p>', unsafe_allow_html=True)
st.divider()

# ── Mode Selection ──
mode = st.radio(
    "Select Mode",
    ["Live Inbox", "Manual Input"],
    horizontal=True,
    label_visibility="collapsed"
)

# ══════════════════════════════════════
# MODE 1: Live Inbox
# ══════════════════════════════════════
if mode == "Live Inbox":
    with st.sidebar:
        st.markdown("### Connect Your Email")
        st.markdown("---")
        host = st.selectbox("Email Provider", [
            "imap.gmail.com",
            "imap.outlook.com",
            "imap.yahoo.com"
        ])
        username = st.text_input("Email Address")
        password = st.text_input("App Password", type="password")
        st.markdown(
            '<p class="sidebar-note">Gmail: Generate App Password from<br>'
            'Google Account → Security → App Passwords</p>',
            unsafe_allow_html=True
        )
        num_emails = st.slider("Number of Emails", 5, 30, 10)
        fetch_btn = st.button("Fetch & Classify", use_container_width=True)

    if fetch_btn:
        if not username or not password:
            st.markdown(
                '<div class="warning-box">Please enter your email address and app password to continue.</div>',
                unsafe_allow_html=True
            )
        else:
            with st.spinner("Connecting to inbox and classifying emails..."):
                try:
                    emails = fetch_emails(host, username, password, num_emails)

                    if not emails:
                        st.markdown(
                            '<div class="alert-box">No emails were fetched. '
                            'Please check your credentials and try again.</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        # Classify
                        results = []
                        for e in emails:
                            category, confidence = classify_email(
                                e["body"],
                                sender=e["from"],
                                subject=e["subject"]
                            )
                            results.append({**e, "category": category, "confidence": confidence})

                        # Summary
                        st.subheader("Classification Summary")
                        col1, col2, col3, col4 = st.columns(4)
                        for col, label in zip(
                            [col1, col2, col3, col4],
                            ["Personal", "Spam", "Promotions", "Support"]
                        ):
                            count = sum(1 for r in results if r["category"] == label)
                            col.markdown(f"""
                            <div class="metric-card">
                                <p class="metric-number" style="color:{COLORS[label]}">{count}</p>
                                <p class="metric-label">{label}</p>
                            </div>
                            """, unsafe_allow_html=True)

                        st.divider()

                        # Email list
                        st.subheader("Email Results")
                        for r in results:
                            with st.expander(f"{r['subject']} — {r['from']}"):
                                col1, col2 = st.columns([1, 2])
                                col1.markdown(
                                    f"**Category:** {BADGE[r['category']]}",
                                    unsafe_allow_html=True
                                )
                                col2.markdown(f"**Confidence:** `{r['confidence']:.1f}%`")
                                st.progress(int(r['confidence']))
                                st.markdown(f"**Preview:** {r['body'][:200]}...")

                except Exception as e:
                    error = str(e)
                    if "AUTHENTICATIONFAILED" in error or "Invalid credentials" in error:
                        st.markdown(
                            '<div class="alert-box">Authentication failed. '
                            'Please check your email and app password.<br><br>'
                            'Gmail users: Make sure you are using an App Password, '
                            'not your regular Gmail password.</div>',
                            unsafe_allow_html=True
                        )
                    elif "Application-specific password" in error:
                        st.markdown(
                            '<div class="alert-box">Gmail requires an App Password.<br><br>'
                            'Go to: Google Account → Security → 2-Step Verification → App Passwords<br>'
                            'Generate a password for "Mail" and use it here.</div>',
                            unsafe_allow_html=True
                        )
                    elif "IMAP" in error or "connect" in error.lower():
                        st.markdown(
                            '<div class="alert-box">Could not connect to email server. '
                            'Please check your internet connection and try again.</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="alert-box">Something went wrong: {error}</div>',
                            unsafe_allow_html=True
                        )

# ══════════════════════════════════════
# MODE 2: Manual Input
# ══════════════════════════════════════
else:
    st.subheader("Test Any Email Manually")
    col1, col2 = st.columns([1, 2])

    with col1:
        subject = st.text_input("Subject")
        sender  = st.text_input("Sender (optional)")

    with col2:
        body = st.text_area("Email Body", height=200)

    if st.button("Classify Email"):
        if not body:
            st.markdown(
                '<div class="warning-box">Please enter the email body to classify.</div>',
                unsafe_allow_html=True
            )
        else:
            try:
                category, confidence = classify_email(body, sender=sender, subject=subject)
                st.divider()

                col1, col2, col3 = st.columns(3)
                col1.markdown(f"""
                <div class="metric-card">
                    <p class="metric-number" style="color:{COLORS[category]}">{category}</p>
                    <p class="metric-label">Category</p>
                </div>
                """, unsafe_allow_html=True)

                col2.markdown(f"""
                <div class="metric-card">
                    <p class="metric-number" style="color:#2c3e50">{confidence:.1f}%</p>
                    <p class="metric-label">Confidence</p>
                </div>
                """, unsafe_allow_html=True)

                col3.markdown(f"""
                <div class="metric-card">
                    <p class="metric-number" style="color:#2c3e50;font-size:1rem">DistilBERT</p>
                    <p class="metric-label">Model</p>
                </div>
                """, unsafe_allow_html=True)

                st.progress(int(confidence))

            except Exception as e:
                st.markdown(
                    f'<div class="alert-box">Classification failed. Please try again.<br>{str(e)}</div>',
                    unsafe_allow_html=True
                )