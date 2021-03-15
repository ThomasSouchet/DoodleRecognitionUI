import base64
import os
import time
from PIL import Image

def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    return encoded

def delete_temp_image(temp_image):
    if os.path.exists(temp_image):
        os.remove(temp_image)

def save_temp_image(file_data):
    img = Image.open(file_data)
    image_size = img.size
    temp_image = str(int(time.time())) + "_" + 'img.png'
    img.save(temp_image)
    return temp_image, image_size