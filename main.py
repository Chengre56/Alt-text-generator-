import streamlit as st
import pandas as pd
from PIL import Image
from google import genai
import time

st.title("Bulk Alt-Text Generator")

# Initialize Gemini Client using secrets
client = genai.Client(api_key=st.secrets["gemini_api_key"])

# 1. Multi-file uploader
uploaded_files = st.file_uploader(
    "Upload product images", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

# 2. Process images with rate-limiting delay
if uploaded_files:
    st.write(f"**Total images uploaded:** {len(uploaded_files)}")
    
    if st.button("Generate Alt-Text for All"):
        results = []
        progress_bar = st.progress(0)
        
        for index, file in enumerate(uploaded_files):
            img = Image.open(file)
            
            # Request alt-text generation
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[img, "Write a concise, SEO-friendly alt text for this product image."]
            )
            
            alt_text = response.text.strip()
            
            results.append({
                "File Name": file.name,
                "Generated Alt-Text": alt_text
            })
            
            # Update progress bar
            progress_bar.progress((index + 1) / len(uploaded_files))
            
            # 1-second delay between API calls to prevent 429 rate limit errors
            time.sleep(1)
        
        st.success("Done!")
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
