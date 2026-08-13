import io
import pandas as pd
from PIL import Image
import streamlit as st
from google import genai

# 1. Page Configuration
st.set_page_config(
    page_title="Bulk Alt-Text Generator",
    page_icon="🖼️",
    layout="wide"
)

# 2. Page Title & Description
st.title("🖼️ Bulk Alt-Text Generator")
st.caption("Powered by Streamlit, Pandas, and Google Gemini AI")

# 3. Initialize Gemini Client via Environment/Secrets
try:
    # Client automatically picks up GEMINI_API_KEY from environment or st.secrets
    client = genai.Client()
except Exception as e:
    st.error(f"Failed to initialize Gemini Client: {e}. Ensure GEMINI_API_KEY is configured.")
    st.stop()

# 4. Image Upload Section
uploaded_files = st.file_uploader(
    "Upload images (JPG, PNG, WEBP)",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True
)

# 5. Processing & Generation Logic
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
            
            alt_text = response.text.strip()
            
            results.append({
                "Filename": uploaded_file.name,
                "Alt Text": alt_text,
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
    
    # 6. Pandas Data Display & Export
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
