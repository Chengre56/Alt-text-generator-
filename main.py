import streamlit as st
import pandas as pd
from PIL import Image
from google import genai
import time
import os

# Page configuration
st.set_page_config(page_title="Bulk Alt-Text Generator", page_icon="🖼️", layout="wide")

# --- IMPACT CONTENT VERIFICATION ---
st.write("Impact-Site-Verification: fe779ce7-c525-4db0-87d4-bc40ff9351d6")
# -----------------------------------

st.title("🖼️ Bulk Alt-Text Generator for E-Commerce")
st.write("Upload product images and generate SEO-friendly alt text automatically.")

# ----------------- SIDEBAR AFFILIATE PROMOTION -----------------
# We can keep some simple text-based promos in the sidebar, but the main page is clean
st.sidebar.title("Recommended Tools")
st.sidebar.info("💡 **Building an Online Store?**\nGet a fast, SEO-ready store built for online sales.")

shopify_url = "https://shopify.pxf.io/YOUR_AFFILIATE_ID" 
st.sidebar.link_button("🚀 Start Shopify for $1/month", shopify_url)
# ---------------------------------------------------------------

# Initialize Gemini Client using secrets
try:
    client = genai.Client(api_key=st.secrets["gemini_api_key"])
except Exception as e:
    st.error("API Key missing or invalid. Please check your Streamlit secrets.")

# ===============================================================
# PART 1: CORE APPLICATION LOGIC (The stuff users came to do)
# ===============================================================

# 1. Multi-file uploader (Capped at 10 images)
uploaded_files = st.file_uploader(
    "Upload product images (up to 10 at once)", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

# 2. Process images
if uploaded_files:
    if len(uploaded_files) > 10:
        st.error("Free limit reached! Please upload up to 10 images per batch.")
    else:
        st.write(f"**Total images uploaded:** {len(uploaded_files)}")
        
        if st.button("Generate Alt-Text for All", type="primary"):
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for index, file in enumerate(uploaded_files):
                img = Image.open(file)
                status_text.text(f"Processing image {index + 1}/{len(uploaded_files)}: {file.name}...")
                
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[img, "Write a concise, SEO-friendly alt text for this product image."]
                    )
                    alt_text = response.text.strip()
                except Exception as err:
                    if "429" in str(err) or "EXHAUSTED" in str(err):
                        alt_text = "Error: Daily API quota reached. Please try again later."
                    else:
                        alt_text = f"Error generating text: {str(err)}"

                results.append({
                    "File Name": file.name,
                    "Generated Alt-Text": alt_text
                })
                
                progress_bar.progress((index + 1) / len(uploaded_files))
                # Slight delay to avoid hammering the free tier API
                time.sleep(0.5)
            
            st.success("Processing Complete!")
            # Save results to session state so they persist across interactions
            st.session_state["results_df"] = pd.DataFrame(results)

# 3. Display and Download CSV
if "results_df" in st.session_state:
    df = st.session_state["results_df"]
    st.subheader("📊 Results")
    st.dataframe(df, use_container_width=True)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV Results",
        data=csv_data,
        file_name="product_alt_texts.csv",
        mime="text/csv"
    )

st.divider() # Simple separator between the app and the footer ad

# ===============================================================
# PART 2: MAIN PAGE BOTTOM ADVERTISEMENT (The high-conversion card)
# ===============================================================

promo_url = "https://vel.academy/course-square-d24#aff=bhattavishesh69f3c8"

# Styled high-converting card using custom CSS for attractive formatting
# We use the native `st.container` with `border=True` for a clean look
with st.container(border=True):
    col_img, col_text = st.columns([1, 2]) # 1/3 image, 2/3 text
    
    with col_img:
        # Load and display the exact image you provided (saved as nails_image.png in media folder)
        image_path = os.path.join("media", "nails_image.png")
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning("⚠️ Image file not found at media/nails_image.png.")
    
    with col_text:
        # We use styled HTML here within st.markdown for maximum attractiveness.
        st.markdown(
            f"""
            <div style="background-color: #f0fdf4; border-radius: 10px; padding: 15px; border: 1px solid #c3e6cb; margin-bottom: 20px;">
                <span style="background-color: #166534; color: white; padding: 4px 10px; border-radius: 50px; text-transform: uppercase; font-size: 0.7rem; font-weight: bold; letter-spacing: 1px;">🔥 Unlock Your Best Self</span>
                <h3 style="color: #111827; margin-top: 10px;">Master Real-World Productivity & Mindset Growth</h3>
                <p style="color: #4b5563; font-size: 1rem; margin-bottom: 15px; line-height: 1.5;">
                    Level up your professional and personal life. Access expert-led masterclasses 
                    designed specifically for ambitious creators, students, and modern learners. 
                    From mindset shifts to technical mastery—get lifetime access now.
                </p>
                <div style="margin-bottom: 20px;">
                    <span style="background-color: #d1fae5; color: #065f46; padding: 5px 12px; border-radius: 50px; font-size: 0.8rem; margin-right: 10px;">✨ Self-Paced Learning</span>
                    <span style="background-color: #d1fae5; color: #065f46; padding: 5px 12px; border-radius: 50px; font-size: 0.8rem;">🚀 High-Impact Modules</span>
                </div>
                <a href="{promo_url}" target="_blank" style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block; box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4);">
                    👉 Claim Your Seat & Get Started
                </a>
                <p style="font-size: 0.75rem; color: #6b7280; margin-top: 20px;">
                    ⚠️ *Disclosure: We may earn a commission if you purchase through this link.*
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
# ===============================================================
