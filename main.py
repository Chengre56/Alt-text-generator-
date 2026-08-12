from google import genai
from PIL import Image

def generate_alt_text(image_path: str, api_key: str) -> str:
    """
    Takes an image file path and uses Gemini Vision to write 
    an accessible, SEO-friendly alt text description.
    """
    # 1. Initialize the Google Gemini Client
    client = genai.Client(api_key=api_key)
    
    # 2. Open the image using Pillow
    image = Image.open(image_path)
    
    # 3. Create a strict prompt for clean alt-text output
    prompt = (
        "Write a concise, accurate Alt Text description (1-2 sentences) for this product image. "
        "It will be used by screen readers for visually impaired users and for Google SEO. "
        "Focus on colors, material, key features, and product type. "
        "Do not start with 'Image of' or 'Picture of'."
    )
    
    # 4. Generate content using the vision model
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=[image, prompt]
    )
    
    return response.text

# --- Example Usage ---
if __name__ == "__main__":
    # Get a free API key from Google AI Studio (aistudio.google.com)
    YOUR_API_KEY = "your-gemini-api-key-here"
    
    # Path to any product photo on your computer
    IMAGE_FILE = "images.jpg" 
    
    try:
        alt_text = generate_alt_text(IMAGE_FILE, YOUR_API_KEY)
        print("\n--- Generated Alt Text ---")
        print(alt_text)
    except Exception as e:
        print(f"Error generating alt text: {e}")

