from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from image_utils import create_vertical_image

app = FastAPI()


@app.post("/generate")
async def generate_image(file: UploadFile = File(...)):
    contents = await file.read()
    screenshot = Image.open(io.BytesIO(contents)).convert("RGB")
    result_img = create_vertical_image(screenshot)
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
