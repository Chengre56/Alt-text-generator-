import streamlit as st
import pandas as pd
from PIL import Image
from google import genai
import time

# Page configuration
st.set_page_config(page_title="Bulk Alt-Text Generator", page_icon="🖼️", layout="wide")

# --- IMPACT CONTENT VERIFICATION ---
st.write("Impact-Site-Verification: fe779ce7-c525-4db0-87d4-bc40ff9351d6")
# -----------------------------------

st.title("🖼️ Bulk Alt-Text Generator for E-Commerce")
st.write("Upload product images and generate SEO-friendly alt text automatically.")

# ----------------- MAIN PAGE FEATURED PROMOTION -----------------
promo_url = "https://vel.academy/course-square-d24#aff=bhattavishesh69f3c8"

with st.container(border=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("🔥 Unlock High-Value Skills & Level Up")
        st.write(
            "Access top-rated courses on personal growth, productivity, and skill-building "
            "designed for ambitious creators and students."
        )
    with col2:
        st.write("") # Spacing
        st.link_button("👉 Claim Offer Here", promo_url, type="primary", use_container_width=True)
# ----------------------------------------------------------------

# ----------------- SIDEBAR AFFILIATE PROMOTION -----------------
st.sidebar.title("Recommended Tools")
st.sidebar.info("💡 **Building an Online Store?**\nGet a fast, SEO-ready store built for online sales.")

shopify_url = "https://shopify.pxf.io/YOUR_AFFILIATE_ID" 
st.sidebar.link_button("🚀 Start Shopify for $1/month", shopify_url)

st.sidebar.divider()
st.sidebar.write("🎓 **Featured Masterclass:**")
st.sidebar.link_button("✨ Vel Academy Courses", promo_url)
# ---------------------------------------------------------------

# Initialize Gemini Client using secrets
try:
    client = genai.Client(api_key=st.secrets["gemini_api_key"])
except Exception as e:
    st.error("API Key missing or invalid. Please check your Streamlit secrets.")

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
        
        if st.button("Generate Alt-Text for All"):
            results = []
            progress_bar = st.progress(0)
            
            for index, file in enumerate(uploaded_files):
                img = Image.open(file)
                
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
                time.sleep(1)
            
            st.success("Processing Complete!")
            st.session_state["results_df"] = pd.DataFrame(results)

# 3. Display and Download CSV
if "results_df" in st.session_state:
    df = st.session_state["results_df"]
    st.subheader("Results")
    st.dataframe(df, use_container_width=True)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="alt_texts.csv",
        mime="text/csv"
    )
