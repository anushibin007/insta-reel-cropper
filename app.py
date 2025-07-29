import streamlit as st
from PIL import Image
from image_utils import create_vertical_image, image_to_bytes

st.title("Instagram Reel Vertical Image Generator")
st.write(
    "Upload your screenshot and get a Reel-ready vertical image with a matching background."
)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        screenshot = Image.open(uploaded_file).convert("RGB")

        result_img = create_vertical_image(screenshot)

        byte_im = image_to_bytes(result_img)

        # Try to show image (if fails, catch exception)
        try:
            st.image(result_img, caption="Generated Image", use_container_width=True)
        except Exception:
            st.warning(
                "Image preview could not be displayed, but the download is available below."
            )

        # Always show download button
        st.download_button(
            label="Download Image",
            data=byte_im,
            file_name="reel_ready_image.png",
            mime="image/png",
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
