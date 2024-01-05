import io
from PIL import Image


def convert_image_to_byte_array(image_content):
    image = Image.open(io.BytesIO(image_content))
    byte_array = io.BytesIO()
    image.save(byte_array, format="JPEG")
    return byte_array.getvalue()
