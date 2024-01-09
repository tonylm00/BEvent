import base64
import io
import os

from PIL import Image

from app import app


def convert_image_to_byte_array(image_content):
    image = Image.open(io.BytesIO(image_content))
    byte_array = io.BytesIO()
    image.save(byte_array, format="JPEG")
    return byte_array.getvalue()


def convert_byte_array_to_image(byte_array):
    return base64.b64encode(byte_array).decode('utf-8')


def convert_path_to_image(tipo_evento):
    path_img = os.path.join(app.root_path, 'static', 'images', tipo_evento + '.jpg')
    with open(path_img, 'rb') as img_file:
        image_content = img_file.read()
    return image_content

#implementare design pattern proxy