import streamlit as st
from PIL import Image
import numpy as np
from collections import Counter
import io


def clean_image_corners(img, corner_size=50, brightness_threshold=1):
    """
    Replaces bright/noise pixels in each corner with the dominant background color.
    """
    img_np = np.array(img)
    h, w, _ = img_np.shape

    # Find dominant color (most common pixel)
    pixels = img_np.reshape(-1, 3)
    pixels_tuples = [tuple(pixel) for pixel in pixels]
    color_counts = Counter(pixels_tuples)
    dominant_color = color_counts.most_common(1)[0][0]

    # Define four image corner areas
    corners = [
        (0, corner_size, 0, corner_size),  # top-left
        (0, corner_size, w - corner_size, w),  # top-right
        (h - corner_size, h, 0, corner_size),  # bottom-left
        (h - corner_size, h, w - corner_size, w),  # bottom-right
    ]

    def is_bright(pixel):
        return (
            np.mean(pixel) > brightness_threshold
        )  # You can adjust 200 for stricter/softer cleaning

    for r_start, r_end, c_start, c_end in corners:
        subregion = img_np[r_start:r_end, c_start:c_end]
        bright_mask = np.apply_along_axis(is_bright, 2, subregion)
        subregion[bright_mask] = dominant_color
        img_np[r_start:r_end, c_start:c_end] = subregion

    return Image.fromarray(img_np)


st.title("Instagram Reel Vertical Image Generator")
st.write(
    "Upload your screenshot and get a Reel-ready vertical image with a matching background."
)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    screenshot = Image.open(uploaded_file).convert("RGB")

    # Clean noise in image corners
    screenshot = clean_image_corners(screenshot)

    # Extract new dominant color after cleaning
    img_array = np.array(screenshot)
    pixels = img_array.reshape(-1, 3)
    pixels_tuples = [tuple(pixel) for pixel in pixels]
    color_counts = Counter(pixels_tuples)
    dominant_color = color_counts.most_common(1)[0][0]  # (R, G, B) tuple

    # Create vertical canvas
    canvas_size = (1080, 1920)
    canvas = Image.new("RGB", canvas_size, dominant_color)

    # Resize and center
    screenshot.thumbnail((canvas_size[0], canvas_size[1]), Image.Resampling.LANCZOS)
    x = (canvas_size[0] - screenshot.width) // 2
    y = (canvas_size[1] - screenshot.height) // 2
    canvas.paste(screenshot, (x, y))

    st.image(canvas, caption="Generated Image", use_container_width=True)

    # Download button
    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="Download Image",
        data=byte_im,
        file_name="reel_ready_image.png",
        mime="image/png",
    )
