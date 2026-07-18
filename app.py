import streamlit as st
import requests

# Page UI configurations
st.set_page_config(page_title="AgriHelp Universal Platform", layout="wide")

API_URL = "http://127.0.0.1:8000/api"

# Initialize Global App States
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_name = ""

# CSS Injection for Theme Color Consistency (AgroBot Green Palette)
st.markdown("""
<style>
    .stButton>button { background-color: #3B8256 !important; color: white !important; width: 100%; border-radius:8px;}
    .kpi-card { background-color: #F4FBF7; border: 1px solid #E1EFE7; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 1px 1px 5px rgba(0,0,0,0.05); }
    .kpi-val { font-size: 28px; font-weight: bold; color: #2C5E3B; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SCREEN 1: SIGN IN MODULE (Image 51862.jpg)
# -------------------------------------------------------------
if not st.session_state.authenticated:
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        # Left branding block stylized layout
        st.markdown("""
        <div style='background: linear-gradient(135deg, #3B8256, #224D32); padding: 45px; border-radius: 15px; color: white; min-height: 420px;'>
            <h2>🌱 AgriHelp</h2>
            <p style='font-size: 16px; opacity: 0.9;'>Your AI-powered agricultural companion for plant disease detection and farming guidance</p>
            <hr style='opacity: 0.3;'>
            <p>✅ <b>AI-based disease detection</b></p>
            <p>✅ <b>Multilingual support (English / Hindi / Hinglish)</b></p>
            <p>✅ <b>Real-time farming advice</b></p>
            <p>✅ <b>Expert treatment recommendations</b></p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("## Welcome Back!")
        st.caption("Sign in to continue to AgriHelp")
        
        email_input = st.text_input("Email Address", value="user@gmail.com")
        pass_input = st.text_input("Password", type="password", value="user123")
        
        if st.button("Sign In"):
            try:
                res = requests.post(f"{API_URL}/auth/login", json={"email": email_input, "password": pass_input}).json()
                if "status" in res and res["status"] == "success":
                    st.session_state.authenticated = True
                    st.session_state.user_role = res["user"]["role"]
                    st.session_state.user_name = res["user"]["name"]
                    st.rerun()
            except Exception:
                st.error("Authentication server down or incorrect credentials typed.")
    st.stop()

# -------------------------------------------------------------
# HEADER CONTROLS NAVIGATION SYSTEM
# -------------------------------------------------------------
st.markdown(f"""
<div style='background-color: #3B8256; padding: 15px; border-radius: 8px; color: white; display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;'>
    <h3 style='margin:0;'>🚜 AgriHelp Universal Ecosystem</h3>
    <div style='font-weight: 500;'>👤 Workspace: {st.session_state.user_name} ({st.session_state.user_role.upper()})</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout Systems"):
    st.session_state.authenticated = False
    st.rerun()

# -------------------------------------------------------------
# SCREEN 2: FARMER CORE ENGINE DASHBOARD (Image 51864.jpg)
# -------------------------------------------------------------
if st.session_state.user_role == "farmer":
    col_dash1, col_dash2 = st.columns(2, gap="large")
    
    with col_dash1:
        st.markdown("#### 🔍 Plant Disease Detection Canvas")
        uploaded_img = st.file_uploader("Upload Leaf File Specimen", type=["jpg", "jpeg", "png"])
        
        if uploaded_img: 
            st.image(uploaded_img, width=280)
    
            if st.button("Analyze Image Specimen"):
        # Convert the Streamlit upload file memory pointer back to standard bytes
                file_bytes = uploaded_img.getvalue()
                files = {"file": (uploaded_img.name, file_bytes, uploaded_img.type)}
        
                with st.spinner("Analyzing leaf scan with TensorFlow engine..."):
                    try:
                # Dispatch POST network request directly to the FastAPI server endpoint
                        response = requests.post(f"{API_URL}/predict", files=files)
                
                        if response.status_code == 200:
                            result = response.json()
                            st.success("Analysis Complete!")
                            st.markdown(f"### 🎯 Results")
                            st.markdown(f"* **Disease Identified:** `{result['disease']}`")
                            st.markdown(f"* **Model Certainty:** `{result['confidence']}`")
                        else:
                            st.error("Error received from prediction server engine.")
                    except Exception as e:
                        st.error(f"Could not connect to backend server: {e}")
                
    with col_dash2:
        st.markdown("#### 💬 Ask Me Anything Assistant")
        st.chat_message("assistant").write("Hello! I'm your agricultural assistant. Ask me about crop diseases, pests, or farming practices!")
        user_msg = st.chat_input("Type your farming question here...")
        if user_msg:
            st.chat_message("user").write(user_msg)
            st.chat_message("assistant").write(f"Processing query via localized LangChain engine. Regarding your query: '{user_msg}', ensure soil moisture remains balanced.")

# -------------------------------------------------------------
# SCREEN 3: ADMINISTRATIVE PRIVILEGES PORTAL (Images 51866, 51868, 51870)
# -------------------------------------------------------------
elif st.session_state.user_role == "admin":
    # 5-Metric Counter Cards Layout
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1: st.markdown("<div class='kpi-card'><p>Farmers</p><p class='kpi-val'>2</p></div>", unsafe_allow_html=True)
    with kpi2: st.markdown("<div class='kpi-card'><p>Admins</p><p class='kpi-val'>1</p></div>", unsafe_allow_html=True)
    with kpi3: st.markdown("<div class='kpi-card'><p>Total Scans</p><p class='kpi-val'>15</p></div>", unsafe_allow_html=True)
    with kpi4: st.markdown("<div class='kpi-card'><p>Scans Today</p><p class='kpi-val'>2</p></div>", unsafe_allow_html=True)
    with kpi5: st.markdown("<div class='kpi-card'><p>Messages</p><p class='kpi-val'>11</p></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User Management Console Sub-block
    st.markdown("### 👥 User Management Console")
    users = requests.get(f"{API_URL}/users").json()
    st.table(users)
    
    # Recent Predictions Columns Layout
    st.markdown("### 📊 Live Traffic Stream Matrix")
    pred_col1, pred_col2, pred_col3 = st.columns(3)
    preds = requests.get(f"{API_URL}/predictions").json()
    
    with pred_col1:
        st.info("📷 Image Queries")
        st.write([p for p in preds if p['type'] == 'Image'])
    with pred_col2:
        st.success("📝 Text Inquiries")
        st.write([p for p in preds if p['type'] == 'Text'])
    with pred_col3:
        st.warning("🎙️ Voice Signals")
        st.write([p for p in preds if p['type'] == 'Voice'])
        
    st.markdown("---")
    
    # Disease Treatment Base Dictionary Table
    st.markdown("### 🗄️ Master Plant Disease Treatment Dictionary")
    diseases = requests.get(f"{API_URL}/diseases").json()
    st.dataframe(diseases, use_container_width=True)

    