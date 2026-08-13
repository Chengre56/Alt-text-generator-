from PIL import Image
from google import genai
import streamlit as st

# Set up Streamlit app UI
st.title("Alt-Text Generator")

# Initialize Gemini Client using Streamlit secrets
client = genai.Client(api_key=st.secrets["gemini_api_key"])

# File uploader in Streamlit
uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    if st.button("Generate Alt-Text"):
        with st.spinner("Generating..."):
            # Call Gemini API using PIL image directly in contents
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[img, "Write a concise alt text for this image."],
            )

            # Display the result
            st.subheader("Generated Alt-Text:")
            st.write(response.text)
