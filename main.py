import io
from google import genai
from PIL import Image
import streamlit as st

def generate_alt_text(image_path: str) -> str:
    # 1. Initialize the Google Gemini Client using secrets
    client = genai.Client(api_key=st.secrets["gemini_api_key"])
    
    # 2. Open the image using Pillow and save to bytes
    image = Image.open(image_path)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format or 'JPEG')
    image_bytes = img_byte_arr.getvalue()
    
    # 3. Define the prompt
    prompt = (
        "Write a concise, accurate Alt Text description (1-2 sentences) for this product image. "
        "It will be used by screen readers for visually impaired users and for Google SEO. "
        "Focus on colors, material, key features, and product type. "
        "Do not start with 'Image of' or 'Picture of'."
    )
    
    # 4. Generate content using the stable vision model
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=[
            {"mime_type": f"image/{image.format.lower() if image.format else 'jpeg'}", "data": image_bytes},
            prompt
        ]
    )
    
    return response.text

# --- Example Usage in Streamlit ---
if __name__ == "__main__":
    IMAGE_FILE = "images.jpg" 
    
    try:
        alt_text = generate_alt_text(IMAGE_FILE)
        st.write("--- Generated Alt Text ---")
        st.write(alt_text)
    except Exception as e:
        st.error(f"Error generating alt text: {e}")
