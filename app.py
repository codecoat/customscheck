import streamlit as st
import requests

# 1. App Configuration
st.set_page_config(page_title="AU Border Scan", page_icon="🦘")
HF_TOKEN = "PASTE_YOUR_HUGGING_FACE_TOKEN_HERE" # Put your token here!
API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 2. Australia 2026 Biosecurity Rules
AU_RULES = {
    "apple": {"status": "🔴 PROHIBITED", "note": "Fresh fruit is banned. Discard in amnesty bins."},
    "banana": {"status": "🔴 PROHIBITED", "note": "High risk to AU crops. Do not bring in."},
    "meat": {"status": "🔴 PROHIBITED", "note": "Jerky, salami, and uncanned meats are banned (FMD risk)."},
    "wood": {"status": "🟡 MUST DECLARE", "note": "Wooden items must be inspected for bark or borers."},
    "boots": {"status": "🟡 MUST DECLARE", "note": "Must be free of mud/soil. Soil carries diseases."},
    "honey": {"status": "🟡 MUST DECLARE", "note": "Banned in WA. Must be inspected elsewhere."},
    "chocolate": {"status": "🟢 ALLOWED", "note": "Commercial confectionery is generally fine."},
}

# 3. User Interface
st.title("🦘 AU Border Checker")
st.write("Snap a photo to check Australia's 2026 biosecurity rules.")

img_file = st.camera_input("Scan your item")

if img_file:
    with st.spinner('AI is analyzing...'):
        # Send image to Hugging Face AI
        response = requests.post(API_URL, headers=headers, data=img_file.getvalue())
        data = response.json()
        
        if response.status_code == 200:
            top_label = data[0]['label'].lower()
            st.write(f"AI Detection: **{top_label}**")
            
            # Match AI label to AU Rules
            match = next((k for k in AU_RULES if k in top_label), None)
            
            if match:
                rule = AU_RULES[match]
                if "🔴" in rule['status']: st.error(rule['status'])
                elif "🟡" in rule['status']: st.warning(rule['status'])
                else: st.success(rule['status'])
                st.info(rule['note'])
            else:
                st.warning("### 🟡 UNKNOWN - MUST DECLARE")
                st.write("If you can eat it, wear it (outdoors), or it's made of wood: **Declare it.**")
