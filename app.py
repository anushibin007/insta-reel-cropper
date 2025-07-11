import streamlit as st
from PIL import Image
import numpy as np
from collections import Counter
import io

st.title("Instagram Reel Vertical Image Generator")
st.write("Upload your screenshot and get a Reel-ready vertical image with a matching background.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    screenshot = Image.open(uploaded_file).convert('RGB')

    # Extract dominant color (most common pixel)
    img_array = np.array(screenshot)
    pixels = img_array.reshape(-1, 3)
    pixels_tuples = [tuple(pixel) for pixel in pixels]
    color_counts = Counter(pixels_tuples)
    dominant_color = color_counts.most_common(1)[0][0]  # (R, G, B) tuple

    # Create vertical canvas
    canvas_size = (1080, 1920)
    canvas = Image.new('RGB', canvas_size, dominant_color)

    # Resize and center the screenshot
    screenshot.thumbnail((canvas_size[0], canvas_size[1]), Image.Resampling.LANCZOS)
    x = (canvas_size[0] - screenshot.width) // 2
    y = (canvas_size[1] - screenshot.height) // 2
    canvas.paste(screenshot, (x, y))

    st.image(canvas, caption='Generated Image', use_container_width=True)

    # Download button
    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="Download Image",
        data=byte_im,
        file_name="reel_ready_image.png",
        mime="image/png"
    )
