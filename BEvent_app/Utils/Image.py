import io
from PIL import Image


def convert_image_to_byte_array(image_content):
    image = Image.open(io.BytesIO(image_content))
    byte_array = io.BytesIO()
    image.save(byte_array, format="JPEG")
    return byte_array.getvalue()


def convert_byte_array_to_image(byte_array_byte):
    #il byte_array_byte corrisponde agli attributi nel db che sono foto
    immagini = [Image.open(io.BytesIO(byte_array)) for byte_array in byte_array_byte]
    return immagini
