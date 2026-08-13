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

# ----------------- SIDEBAR AFFILIATE PROMOTION -----------------
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
# PART 1: CORE APPLICATION LOGIC
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
    st.subheader("📊 Results")
    st.dataframe(df, use_container_width=True)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV Results",
        data=csv_data,
        file_name="product_alt_texts.csv",
        mime="text/csv"
    )

st.divider()

# ===============================================================
# PART 2: MATCHED BEAUTY & STYLE ADVERTISEMENT
# ===============================================================

promo_url = "https://vel.academy/course-square-d24#aff=bhattavishesh69f3c8"
# Direct public web image link so Streamlit loads it everywhere without local file errors
nail_image_url = "https://images.unsplash.com/photo-1604654894610-df63bc536371?q=80&w=800&auto=format&fit=crop"

with st.container(border=True):
    col_img, col_text = st.columns([1, 2])
    
    with col_img:
        st.image(nail_image_url, use_container_width=True, caption="Matte Black Luxury Press-On Nails")
    
    with col_text:
        st.markdown(
            f"""
            <div style="background-color: #0f172a; color: #ffffff; border-radius: 12px; padding: 20px; border: 1px solid #334155;">
                <span style="background-color: #ec4899; color: white; padding: 4px 12px; border-radius: 50px; text-transform: uppercase; font-size: 0.75rem; font-weight: bold; letter-spacing: 1px;">💅 Beauty & E-Commerce Spotlight</span>
                <h3 style="color: #f472b6; margin-top: 12px; font-size: 1.4rem;">Upgrade Your Beauty Store & Personal Brand</h3>
                <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6; margin-bottom: 15px;">
                    Selling press-on nails, beauty products, or lifestyle accessories? Master high-converting social media marketing, aesthetic photo branding, and client retention strategies to scale your sales automatically.
                </p>
                <div style="margin-bottom: 20px;">
                    <span style="background-color: #831843; color: #fbcfe8; padding: 5px 12px; border-radius: 50px; font-size: 0.8rem; margin-right: 8px;">✨ Premium Aesthetic Guides</span>
                    <span style="background-color: #831843; color: #fbcfe8; padding: 5px 12px; border-radius: 50px; font-size: 0.8rem;">🚀 Brand Scaling Strategies</span>
                </div>
                <a href="{promo_url}" target="_blank" style="background: linear-gradient(135deg, #ec4899 0%, #be185d 100%); color: white; padding: 12px 28px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block; box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);">
                    👉 Check Out Special Beauty & Creator Offers
                </a>
                <p style="font-size: 0.75rem; color: #94a3b8; margin-top: 15px;">
                    *Disclosure: We may earn an affiliate commission if you make a purchase through this link.*
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
