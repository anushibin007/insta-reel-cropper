from PIL import Image
import numpy as np
from collections import Counter
import io


def create_vertical_image(
    input_image: Image.Image, canvas_size=(1080, 1920)
) -> Image.Image:
    img_array = np.array(input_image)
    pixels = img_array.reshape(-1, 3)
    pixels_tuples = [tuple(pixel) for pixel in pixels]
    color_counts = Counter(pixels_tuples)
    dominant_color = color_counts.most_common(1)[0][0]

    canvas = Image.new("RGB", canvas_size, dominant_color)
    img = input_image.copy()
    img.thumbnail(canvas_size, Image.Resampling.LANCZOS)
    x = (canvas_size[0] - img.width) // 2
    y = (canvas_size[1] - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas


def image_to_bytes(image: Image.Image) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
