import streamlit as st
from PIL import Image
from image_utils import create_vertical_image, image_to_bytes

st.title("Instagram Reel Vertical Image Generator")
st.write(
    "Upload your screenshot and get a Reel-ready vertical image with a matching background."
)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    screenshot = Image.open(uploaded_file).convert("RGB")
    result_img = create_vertical_image(screenshot)

    st.image(result_img, caption="Generated Image", use_container_width=True)

    byte_im = image_to_bytes(result_img)
    st.download_button(
        label="Download Image",
        data=byte_im,
        file_name="reel_ready_image.png",
        mime="image/png",
    )
