
import streamlit as st
import numpy as np
import requests
import os
import base64
import time
import json
from pylab import array
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ExifTags

st.set_page_config(layout="wide")

def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    return encoded

encoded = load_image('images/preview.jpg')

page_bg_img = f'''
            <style>
                body {{
                    background-image: url("data:image/jpeg;base64,{encoded}");
                    background-size: cover;
                }}
            </style>
            '''

#st.markdown(page_bg_img, unsafe_allow_html=True)

st.write("# Doodle Recognition: Let’s play Pictionary !")

st.text("")

# enter here the address of your api
url = 'https://doodle-recognition-api-x4dwwwxida-ew.a.run.app/predict/'

st.write("Real-time Doodle Recognition with Quick, Draw !")
with st.beta_expander("Click here for more info about the model"):
    st.markdown("""
        <p>What is “Quick, Draw !”</p>
        
        <p>=> Google Open Source Dataset</p>
        <p>=> Collection of 50 million drawings across 345 categories</p>
        <p>=> Ready to use images (already, preprocessed)</p>
    """, unsafe_allow_html=True)

st.text("")

model = st.radio('Select a model', ('20K_NCLass_345', '25K_NCLass_190', '45K_NCLass_150', '120K_NCLass_50'))

st.write(model)

model_name = ''
num_class = 0

if model == '20K_NCLass_345':
    model_name = 'models_model_V1_DPoint_20K_NCLass_345.h5'
    num_class = 345
elif model == '25K_NCLass_190':
    model_name = 'models_model_V1_DPoint_25K_NCLass_190.h5'
    num_class = 190
elif model == '45K_NCLass_150':
    model_name = 'models_model_V1_DPoint_45K_NCLass_150.h5'
    num_class = 150
else:
    model_name = 'models_model_V1_DPoint_120K_NCLass_50.h5'
    num_class = 50

file_data = st.file_uploader("Select an image", type=["jpg", "jpeg", "png"])

st.text("")

def fix_rotation(file_data):
    # check EXIF data to see if has rotation data from iOS. If so, fix it.
    try:
        image = Image.open(file_data)
        image = image.convert("RGB")
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break

        exif = dict(image.getexif().items())

        rot = 0
        if exif[orientation] == 3:
            rot = 180
        elif exif[orientation] == 6:
            rot = 270
        elif exif[orientation] == 8:
            rot = 90

        if rot != 0:
            st.write(f"Rotating image {rot} degrees (you're probably on iOS)...")
            image = image.rotate(rot, expand=True)

    except (AttributeError, KeyError, IndexError):
        pass  # image didn't have EXIF data

    return image

if file_data is not None:
    with st.spinner('Checking...'):
        # load the image from uploader; fix rotation for iOS devices if necessary
        
        img = fix_rotation(file_data)
        
        st.image(img)
        
        temp_image = str(int(time.time())) + "_" + 'img.jpg'
        img.save(temp_image)

        multipart_form_data = {
            "inputImage" : (open(temp_image, "rb"))
        }

        form_data = {
            "modelName" : model_name,
            "numClass" : num_class
        }
        
        response = requests.post(url, data = form_data, files = multipart_form_data, verify=False)

        if os.path.exists(temp_image):
            os.remove(temp_image)

        prediction = response.json()['prediction']
        values = prediction.values()
        keys = prediction.keys()
        keys = [key for key in keys]
        values = [int(val)/100 for val in values]
        
        plt.figure(figsize = (8, 8))
        plt.pie(values, labels = keys,
                colors = ['red', 'green', 'yellow','blue','orange'],
                pctdistance = 0.7, labeldistance = 1.4,
                shadow = False, normalize=False)
        plt.legend()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
