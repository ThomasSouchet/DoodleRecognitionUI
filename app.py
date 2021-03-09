
import streamlit as st
import requests
import os
import time
from PIL import ExifTags
from fastai.vision.core import PILImage

st.set_page_config(layout="wide")

st.write("# Doodle Recognition: Let’s play Pictionary !")

st.text("")

# enter here the address of your api
url = 'http://127.0.0.1:8000/predict/'

st.write("Real-time Doodle Recognition with Quick, Draw !")
with st.beta_expander("Click here for more info about the model"):
    st.markdown("""
        <p>What is “Quick, Draw !”</p>
        
        <p>=> Google Open Source Dataset</p>
        <p>=> Collection of 50 million drawings across 345 categories</p>
        <p>=> Ready to use images (already, preprocessed)</p>
    """, unsafe_allow_html=True)

st.text("")

file_data = st.file_uploader("Select an image", type=["jpg", "jpeg", "png"])

st.text("")

def fix_rotation(file_data):
    # check EXIF data to see if has rotation data from iOS. If so, fix it.
    try:
        image = PILImage.create(file_data)
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
            # This step is necessary because image.rotate returns a PIL.Image, not PILImage, the fastai derived class.
            image.__class__ = PILImage

    except (AttributeError, KeyError, IndexError):
        pass  # image didn't have EXIF data

    return image

if file_data is not None:
    with st.spinner('Checking...'):
        # load the image from uploader; fix rotation for iOS devices if necessary
        
        time.sleep(2)

        img = fix_rotation(file_data)
        
        st.image(img, width=200)
        
        params = {} #dict()

        response = requests.get(url, params=params)

        prediction = response.json()

        pred = prediction['Prediction']

        st.write(pred)
