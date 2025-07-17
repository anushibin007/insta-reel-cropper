from mcp.server.fastmcp import FastMCP
from image_utils import create_vertical_image
from PIL import Image
import io
import base64

mcp = FastMCP("Instagram Reel Vertical Image MCP Tool")


@mcp.tool()
def make_vertical(canvas_image_base64: str) -> str:
    """
    Given a base64 PNG/JPG image, returns a base64 PNG with the screenshot centered
    on a vertical 1080x1920 background matching the most common pixel.
    """
    image_bytes = base64.b64decode(canvas_image_base64)
    screenshot = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    result_img = create_vertical_image(screenshot)
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


if __name__ == "__main__":
    mcp.run()
