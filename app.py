
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

# def load_image(path):
#     with open(path, 'rb') as f:
#         data = f.read()
#         encoded = base64.b64encode(data).decode()
#     return encoded

# encoded = load_image('images/preview.jpg')

# page_bg_img = f'''
#             <style>
#                 body {{
#                     background-image: url("data:image/jpeg;base64,{encoded}");
#                     background-size: cover;
#                 }}
#             </style>
#             '''

#st.markdown(page_bg_img, unsafe_allow_html=True)

st.write("# Doodle Recognition: Let’s play Pictionary !")

st.text("")

# enter here the address of your api
#url = 'https://doodle-recognition-api-x4dwwwxida-ew.a.run.app/predict/'
url = 'http://127.0.0.1:8000/predict'

st.write("Real-time Doodle Recognition with Quick, Draw !")
with st.beta_expander("Click here for more info about the model"):
    st.markdown("""
        <p>What is “Quick, Draw !”</p>
        
        <p>=> Google Open Source Dataset</p>
        <p>=> Collection of 50 million drawings across 345 categories</p>
        <p>=> Ready to use images (already, preprocessed)</p>
    """, unsafe_allow_html=True)

st.text("")

model = st.radio('Select a model', ('25K_NCLass_190', '45K_NCLass_150', '120K_NCLass_50', '60K_NCLass_345', '100K_NCLass_100'))

st.write(model)

model_name = ''
num_class = 0

if model == '25K_NCLass_190':
    model_name = 'models_model_V1_DPoint_25K_NCLass_190.h5'
    num_class = 190
elif model == '45K_NCLass_150':
    model_name = 'models_model_V1_DPoint_45K_NCLass_150.h5'
    num_class = 150
elif model == '100K_NCLass_100':
    model_name = 'models_model_V1_DPoint_100K_NCLass_100.h5'
    num_class = 100
elif model == '60K_NCLass_345':
    model_name = 'models_model_V1_DPoint_60K_NCLass_345.h5'
    num_class = 345
else:
    model_name = 'models_model_V1_DPoint_120K_NCLass_50.h5'
    num_class = 50

file_data = st.file_uploader("Select an image", type=["jpg", "jpeg", "png"])

st.text("")

if file_data is not None:
    with st.spinner('Checking...'):
        # load the image from uploader; fix rotation for iOS devices if necessary
        
        img = Image.open(file_data)
                
        temp_image = str(int(time.time())) + "_" + 'img.png'
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

        c1, c2 = st.beta_columns(2)

        with c1:
            st.image(img)

        with c2:     
            plt.figure(figsize = (4, 4))
            plt.pie(values, labels = keys,
                    colors = ['blue','orange','red', 'green', 'yellow'],
                    pctdistance = 0.7, labeldistance = 1.4,
                    shadow = False, normalize=False)
            plt.legend()
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
