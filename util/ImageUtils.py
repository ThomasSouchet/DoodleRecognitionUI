import base64
import os
import time
import numpy as np
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
    temp_image = get_temp_image_name()
    img.save(temp_image)
    return temp_image, image_size

def save_temp_image_from_canvas(output):
    output3= np.delete(output,np.where(~output.any(axis=1))[0], axis=0)
    output3= np.delete(output3,np.where(~output3.any(axis=0))[0], axis=1)
    output2 = Image.fromarray(np.uint8(output3[:, :, 0]))
    temp_image = get_temp_image_name()
    output2.save(temp_image)
    return temp_image

def get_temp_image_name():
    return f'{str(int(time.time()))}_img.jpg'