import streamlit as st
from modules.domain_recon import get_whois, get_dns
from modules.ip_recon import get_ip_info
from modules.breach_check import check_breach, check_password
from modules.username_recon import search_username
from modules.report import generate_report
import whois
import dns.resolver
import requests
import subprocess

# Page config
st.set_page_config(
    page_title="ReconX",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { background-color: #0e1117; }
    h1 { color: #00FF41; font-family: monospace; }
    h2, h3 { color: #00BFFF; font-family: monospace; }
    .stButton>button {
        background-color: #00FF41;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
    }
    .stButton>button:hover { background-color: #00cc33; }
    .stTextInput>div>div>input {
        background-color: #1e1e2e;
        color: white;
        border: 1px solid #00FF41;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("# 🕵️ ReconX")
st.sidebar.markdown("### OSINT Automation Tool")
st.sidebar.markdown("---")
tool = st.sidebar.radio("Select Module", [
    "🌐 Domain Recon",
    "📍 IP Intelligence",
    "🔓 Breach Check",
    "🔑 Password Check",
    "👤 Username Search",
    "📄 PDF Report"
])

# Header
st.markdown("# 🕵️ ReconX — OSINT Automation Tool")
st.markdown("---")

# Domain Recon
if tool == "🌐 Domain Recon":
    st.markdown("## 🌐 Domain Recon")
    target = st.text_input("Enter domain (e.g. google.com)")
    if st.button("Run Recon"):
        if target:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### WHOIS")
                try:
                    w = whois.whois(target)
                    st.json({
                        "Domain": str(w.domain_name),
                        "Registrar": str(w.registrar),
                        "Created": str(w.creation_date),
                        "Expires": str(w.expiration_date),
                        "Name Servers": str(w.name_servers)
                    })
                except Exception as e:
                    st.error(f"WHOIS failed: {e}")
            with col2:
                st.markdown("### DNS Records")
                for record in ["A", "MX", "TXT", "NS"]:
                    try:
                        answers = dns.resolver.resolve(target, record)
                        for r in answers:
                            st.code(f"{record}: {r}")
                    except:
                        st.warning(f"{record}: Not found")

# IP Intelligence
elif tool == "📍 IP Intelligence":
    st.markdown("## 📍 IP Intelligence")
    target = st.text_input("Enter IP address (e.g. 8.8.8.8)")
    if st.button("Lookup IP"):
        if target:
            try:
                response = requests.get(f"http://ip-api.com/json/{target}")
                data = response.json()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Country", data.get("country", "N/A"))
                    st.metric("City", data.get("city", "N/A"))
                    st.metric("Region", data.get("regionName", "N/A"))
                with col2:
                    st.metric("ISP", data.get("isp", "N/A"))
                    st.metric("Org", data.get("org", "N/A"))
                    st.metric("Timezone", data.get("timezone", "N/A"))
                st.map(data=[{"lat": data["lat"], "lon": data["lon"]}])
            except Exception as e:
                st.error(f"IP lookup failed: {e}")

# Breach Check
elif tool == "🔓 Breach Check":
    st.markdown("## 🔓 Email Breach Check")
    email = st.text_input("Enter email address")
    if st.button("Check Breaches"):
        if email:
            headers = {"hibp-api-key": "free", "user-agent": "reconx-tool"}
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            response = requests.get(url, headers=headers)
            if response.status_code == 404:
                st.success(f"✅ {email} was NOT found in any known breaches.")
            elif response.status_code == 401:
                st.warning("⚠ HIBP requires a paid API key for email lookup.")
            else:
                breaches = response.json()
                st.error(f"⚠ Found in {len(breaches)} breaches!")
                for b in breaches:
                    with st.expander(f"💀 {b['Name']} — {b['BreachDate']}"):
                        st.write("**Data leaked:**", ", ".join(b.get("DataClasses", [])))

# Password Check
elif tool == "🔑 Password Check":
    st.markdown("## 🔑 Password Leak Check")
    st.info("🔒 Your password is never sent anywhere. Uses k-anonymity.")
    pwd = st.text_input("Enter password", type="password")
    if st.button("Check Password"):
        if pwd:
            import hashlib
            sha1 = hashlib.sha1(pwd.encode()).hexdigest().upper()
            prefix, suffix = sha1[:5], sha1[5:]
            response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
            found = False
            for line in response.text.splitlines():
                h, count = line.split(":")
                if h == suffix:
                    st.error(f"⚠ This password has been leaked **{count} times**! Change it immediately.")
                    found = True
                    break
            if not found:
                st.success("✅ This password was not found in any known leaks.")

# Username Search
elif tool == "👤 Username Search":
    st.markdown("## 👤 Username Search")
    username = st.text_input("Enter username")
    if st.button("Search Platforms"):
        if username:
            with st.spinner("Searching across 300+ platforms..."):
                result = subprocess.run(
                    ["sherlock", username, "--print-found"],
                    capture_output=True, text=True
                )
                lines = result.stdout.splitlines()
                found = [l for l in lines if "[+]" in l]
                st.success(f"✅ Found on {len(found)} platforms")
                for line in found:
                    st.markdown(f"🔗 {line.strip()}")

# PDF Report
elif tool == "📄 PDF Report":
    st.markdown("## 📄 Generate PDF Report")
    target = st.text_input("Enter domain for report")
    if st.button("Generate Report"):
        if target:
            with st.spinner("Generating report..."):
                generate_report(target, "reconx_report.pdf")
            with open("reconx_report.pdf", "rb") as f:
                st.download_button(
                    label="📥 Download Report",
                    data=f,
                    file_name=f"reconx_{target}.pdf",
                    mime="application/pdf"
                )
            st.success("✅ Report ready!")