import io
import pandas as pd
from PIL import Image
import streamlit as st
from google import genai

# 1. Page Setup & Configuration
st.set_page_config(
    page_title="Bulk Alt-Text Generator & AI Tools",
    page_icon="✨",
    layout="wide"
)

# 2. Main Header
st.title("✨ Bulk Alt-Text Generator")
st.caption("Generate high-converting, SEO-friendly alt text for image batches instantly.")

# 3. Sidebar API Configuration
st.sidebar.header("🔑 API Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.sidebar.divider()

# Sidebar Secondary Promo
st.sidebar.header("🎓 Master New Skills")
st.sidebar.markdown(
    """
    **Ready to level up your mindset and career?**  
    Explore world-class masterclasses designed for rapid personal and professional growth.
    
    👉 [**Explore the Academy Deals**](https://vel.academy/course-square-d24#aff=bhattavishesh69f3c8)
    """
)
st.sidebar.caption("⚠️ *Disclosure: We may earn an affiliate commission if you enroll through links on this page.*")

# 4. HIGH-CONVERTING HERO PROMOTIONAL CARD
affiliate_link = "https://vel.academy/course-square-d24#aff=bhattavishesh69f3c8"

st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        border: 2px solid #6366f1;
        border-radius: 16px;
        padding: 30px;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
        margin-bottom: 30px;
        text-align: center;
    ">
        <span style="
            background-color: #4f46e5;
            color: #e0e7ff;
            font-size: 0.85rem;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 50px;
            text-transform: uppercase;
            letter-spacing: 1px;
        ">🔥 Exclusive Student & Creator Offer</span>
        
        <h2 style="color: #ffffff; margin-top: 15px; font-weight: 800; font-size: 1.8rem;">
            Unlock Your Full Potential & Transform Your Life
        </h2>
        
        <p style="color: #c7d2fe; font-size: 1.1rem; max-width: 750px; margin: 0 auto 20px auto; line-height: 1.6;">
            Access expert-led courses on productivity, high-value skill-building, personal empowerment, and financial mastery. Join thousands of ambitious learners today.
        </p>
        
        <div style="margin-bottom: 25px;">
            <span style="margin: 0 10px; color: #a5b4fc;">✨ Self-Paced Learning</span> • 
            <span style="margin: 0 10px; color: #a5b4fc;">💎 High-Impact Modules</span> • 
            <span style="margin: 0 10px; color: #a5b4fc;">🚀 Lifetime Access</span>
        </div>
        
        <a href="{affiliate_link}" target="_blank" style="
            background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%);
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: bold;
            padding: 14px 32px;
            text-decoration: none;
            border-radius: 50px;
            display: inline-block;
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
            transition: all 0.3s ease;
        ">
            👉 Claim Your Exclusive Discount Here
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Core Application Logic
if not api_key:
    st.info("👈 Please enter your Gemini API Key in the sidebar to begin processing images.", icon="🔑")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize Gemini Client: {e}")
    st.stop()

# 6. File Uploader
uploaded_files = st.file_uploader(
    "Upload images (JPG, PNG, WEBP)",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True
)

if uploaded_files and st.button("🚀 Generate Alt-Text in Bulk", type="primary"):
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing image {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}...")
        
        try:
            image = Image.open(uploaded_file)
            prompt = "Provide a concise, accurate, and SEO-friendly alt-text description for this image. Output only the alt-text."
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[image, prompt]
            )
            
            results.append({
                "Filename": uploaded_file.name,
                "Alt Text": response.text.strip(),
                "Status": "Success"
            })
        except Exception as e:
            results.append({
                "Filename": uploaded_file.name,
                "Alt Text": f"Error: {str(e)}",
                "Status": "Failed"
            })
            
        progress_bar.progress((idx + 1) / len(uploaded_files))

    status_text.text("Processing complete!")
    
    if results:
        df = pd.DataFrame(results)
        st.subheader("📊 Generated Alt-Text Results")
        st.dataframe(df, use_container_width=True)
        
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv_buffer.getvalue(),
            file_name="bulk_alt_text_results.csv",
            mime="text/csv"
        )
