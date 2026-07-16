import streamlit as st
import pickle
import numpy as np

# ------------------------------------------------------------------
# Page setup
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🎣",
    layout="centered"
)

# ------------------------------------------------------------------
# Load trained model
# ------------------------------------------------------------------
@st.cache_resource
def load_model():
    with open("phishing_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ------------------------------------------------------------------
# Sidebar — About / Tech Stack / Disclaimer
# ------------------------------------------------------------------
with st.sidebar:
    st.title("ℹ️ About This App")
    st.markdown(
        "This app is a **machine learning mini-project** that predicts "
        "whether a website is likely **phishing** or **legitimate**, "
        "based on 15 key URL and website characteristics."
    )

    st.subheader("🛠️ Built With")
    st.markdown(
        "- **Model:** Random Forest Classifier\n"
        "- **Library:** scikit-learn\n"
        "- **UI:** Streamlit\n"
        "- **Trained on:** UCI-style phishing website dataset (30+ engineered features)\n"
        "- **Feature selection:** Top 15 features chosen via Random Forest "
        "feature importance analysis"
    )

    st.subheader("📊 Model Performance")
    st.markdown(
        "Achieved **~94% accuracy** on held-out test data using the reduced "
        "15-feature set — a small trade-off from the full 30-feature model "
        "(~97%), made for a simpler, more user-friendly input form."
    )

    st.divider()
    st.warning(
        "⚠️ **Disclaimer:** This tool was built for **academic and learning "
        "purposes** as part of a supervised machine learning mini-project. "
        "It is **not** a real-world security product and should never be "
        "solely relied on to judge whether a website is actually safe. "
        "Always use your browser's built-in security warnings, antivirus "
        "software, or official verification methods for real decisions."
    )

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.title("🎣 Phishing Website Detector")
st.markdown(
    "Answer a few questions about a website's URL and behavior, "
    "and this Random Forest model will predict whether it's **legitimate** or **phishing**."
)
st.divider()

# ------------------------------------------------------------------
# Helper: 3-way question widget mapped to -1 / 0 / 1
# Also records a human-readable "flag" description for the insights section
# ------------------------------------------------------------------
answer_log = []  # (label, value, description-if-flagged)

def question(label, help_text, safe_label, suspicious_label, phishing_label, key,
             suspicious_flag_text, phishing_flag_text):
    choice = st.selectbox(
        label,
        options=[safe_label, suspicious_label, phishing_label],
        help=help_text,
        key=key
    )
    if choice == safe_label:
        value = 1
    elif choice == suspicious_label:
        value = 0
        answer_log.append((label, value, suspicious_flag_text))
    else:
        value = -1
        answer_log.append((label, value, phishing_flag_text))
    return value

# ------------------------------------------------------------------
# Input form, grouped into two columns for compactness
# ------------------------------------------------------------------
st.subheader("Website Details")

col1, col2 = st.columns(2)

with col1:
    using_ip = question(
        "Domain type",
        "Does the site use a raw IP address instead of a domain name?",
        "Uses a normal domain name", "Not sure", "Uses a raw IP address (e.g. 192.168.1.1)",
        "using_ip",
        "Uncertain whether a domain name or IP address is used",
        "Uses a raw IP address instead of a domain name"
    )
    long_url = question(
        "URL length",
        "Very long URLs are a common phishing tactic.",
        "Short / normal length", "Medium length", "Very long URL",
        "long_url",
        "Medium-length URL",
        "Unusually long URL"
    )
    short_url = question(
        "URL shortener",
        "Is a shortener like bit.ly or tinyurl used?",
        "No shortener used", "Not sure", "Uses a URL shortener",
        "short_url",
        "Unsure if a shortener is used",
        "Uses a URL shortening service"
    )
    symbol_at = question(
        "'@' symbol in URL",
        "The '@' symbol can hide the real destination of a link.",
        "No '@' symbol present", "Not sure", "Contains '@' symbol",
        "symbol_at",
        "Unsure about '@' symbol presence",
        "Contains a suspicious '@' symbol"
    )
    redirecting = question(
        "Redirect trick ('//')",
        "A '//' appearing later in the URL path can indicate a sneaky redirect.",
        "No suspicious '//' redirect", "Not sure", "Suspicious '//' redirect present",
        "redirecting",
        "Unsure about redirect pattern",
        "Suspicious '//' redirect detected in URL path"
    )
    prefix_suffix = question(
        "Dash in domain",
        "Phishing domains often add a dash, e.g. paypal-secure.com.",
        "No dash in domain", "Not sure", "Dash present in domain",
        "prefix_suffix",
        "Unsure about dash in domain",
        "Domain contains a dash (e.g. paypal-secure.com style)"
    )
    subdomains = question(
        "Subdomains",
        "Multiple subdomains can be a phishing red flag.",
        "Few or no subdomains", "One subdomain", "Multiple subdomains",
        "subdomains",
        "Has one subdomain",
        "Has multiple subdomains"
    )
    https = question(
        "HTTPS certificate",
        "Is HTTPS properly used with a trusted certificate?",
        "Valid, trusted HTTPS", "Present but not ideal", "Missing or fake HTTPS",
        "https",
        "HTTPS present but certificate isn't ideal",
        "Missing or fake HTTPS certificate"
    )

with col2:
    domain_reg_len = question(
        "Domain registration length",
        "Phishing domains are often registered for very short periods.",
        "Registered for a long period", "Not sure", "Registered for a very short period",
        "domain_reg_len",
        "Unsure about domain registration length",
        "Domain registered for a very short period"
    )
    favicon = question(
        "Favicon source",
        "Is the site icon (favicon) loaded from the same domain?",
        "Loaded from same domain", "Not sure", "Loaded from an external domain",
        "favicon",
        "Unsure where favicon is loaded from",
        "Favicon loaded from an external domain"
    )
    non_std_port = question(
        "Port number",
        "Phishing sites sometimes use non-standard ports.",
        "Uses standard port", "Not sure", "Uses a non-standard port",
        "non_std_port",
        "Unsure about port usage",
        "Uses a non-standard port"
    )
    https_domain_url = question(
        "'HTTPS' as text in domain",
        "Some phishing sites add the word 'https' into the domain name itself to look trustworthy.",
        "Not used as fake trust trick", "Not sure", "'https' appears as text in domain name",
        "https_domain_url",
        "Unsure about 'https' text trick",
        "The word 'https' appears as text within the domain name itself"
    )
    request_url = question(
        "Media source (images, etc.)",
        "Do most images/media on the page load from the same domain?",
        "Mostly loaded from same domain", "Mixed sources", "Mostly loaded from external domains",
        "request_url",
        "Media loaded from a mix of sources",
        "Most media loaded from external domains"
    )
    anchor_url = question(
        "Link destinations",
        "Do most links on the page point to the same domain?",
        "Mostly point to same domain", "Mixed", "Mostly point elsewhere",
        "anchor_url",
        "Links point to a mix of domains",
        "Most links point away from the site's own domain"
    )
    links_in_script = question(
        "Script/meta tag links",
        "Do script and meta tags mostly reference the same domain?",
        "Mostly same domain", "Mixed", "Mostly external domains",
        "links_in_script",
        "Script/meta tags reference a mix of domains",
        "Script/meta tags mostly reference external domains"
    )

st.divider()

# ------------------------------------------------------------------
# Predict button
# ------------------------------------------------------------------
if st.button("🔍 Analyze Website", use_container_width=True):
    features = np.array([[
        using_ip, long_url, short_url, symbol_at, redirecting, prefix_suffix,
        subdomains, https, domain_reg_len, favicon, non_std_port,
        https_domain_url, request_url, anchor_url, links_in_script
    ]])

    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    classes = list(model.classes_)
    legit_idx = classes.index(1) if 1 in classes else None
    phishing_idx = classes.index(-1) if -1 in classes else None

    confidence = proba[legit_idx] if prediction == 1 else proba[phishing_idx]

    st.divider()
    if prediction == 1:
        st.success("✅ This website looks **Legitimate**")
    else:
        st.error("⚠️ This website looks like **Phishing**")

    st.metric("Model Confidence", f"{confidence * 100:.1f}%")
    st.progress(float(confidence))

    with st.expander("See full probability breakdown"):
        st.write(f"Legitimate probability: {proba[legit_idx]*100:.2f}%")
        st.write(f"Phishing probability: {proba[phishing_idx]*100:.2f}%")

    # ------------------------------------------------------------------
    # Insights — what did we discover from the user's answers?
    # ------------------------------------------------------------------
    st.subheader("🔎 What We Found In Your Answers")
    if not answer_log:
        st.info("No suspicious or phishing-style signals were detected in any of your answers — every response matched a safe/legitimate pattern.")
    else:
        phishing_flags = [desc for _, val, desc in answer_log if val == -1]
        suspicious_flags = [desc for _, val, desc in answer_log if val == 0]

        if phishing_flags:
            st.markdown("**🚩 Phishing-style signals detected:**")
            for flag in phishing_flags:
                st.markdown(f"- {flag}")

        if suspicious_flags:
            st.markdown("**🤔 Ambiguous / uncertain signals:**")
            for flag in suspicious_flags:
                st.markdown(f"- {flag}")

        st.caption(
            f"{len(phishing_flags)} phishing-style signal(s) and "
            f"{len(suspicious_flags)} ambiguous signal(s) out of 15 total features."
        )

st.divider()
st.caption("Built with a Random Forest classifier , as part of an academic ML mini-project.")
