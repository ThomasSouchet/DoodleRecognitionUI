
import streamlit as st
import numpy as np
import requests
from util.ParamsCache import ParamsCache
from util.WebUtils import image_css, image_html
from util.ImageUtils import save_temp_image, delete_temp_image
from pylab import array
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

page_bg_img = f'''
            <style>
                .uploadedFile {{
                    display: none;
                }}
            </style>
            '''

st.markdown(page_bg_img, unsafe_allow_html=True)

st.write("# Doodle Recognition: Let’s play Pictionary !")

st.text("")

model = st.radio('Select a model', ('25K_NCLass_190', '45K_NCLass_150', '120K_NCLass_50', '60K_NCLass_345', 
                                    '20K_NCLass_80','100K_NCLass_100'))

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
elif model == '20K_NCLass_80':
    model_name = 'models_model_V1_DPoint_20K_NCLass_80.h5'
    num_class = 80
else:
    model_name = 'models_model_V1_DPoint_120K_NCLass_50.h5'
    num_class = 50

file_data = st.file_uploader("Select an image", type=["jpg", "jpeg", "png"])

st.text("")

if file_data is not None:
    try:
        temp_image, image_size = save_temp_image(file_data)

        with st.spinner('Checking...'):        
            
            multipart_form_data = {
                "inputImage" : (open(temp_image, "rb"))
            }

            form_data = {
                "modelName" : model_name,
                "numClass" : num_class
            }

            response = requests.post(
                        ParamsCache.getInstance().getLocalUrl(),
                        data = form_data, 
                        files = multipart_form_data, 
                        verify=False
                        )

        response_status = response.status_code
        prediction = response.json()['prediction']

        if response_status == 200:
            values = prediction.values()
            keys = prediction.keys()
            keys = [key for key in keys]
            values = [int(val)/100 for val in values]

            c1, c2 = st.beta_columns(2)

            with c1:
                st.markdown(image_html(image_size, temp_image), unsafe_allow_html=True)

            with c2:
                #st.image()
                
                plt.figure(figsize = (4, 4))
                plt.pie(values, labels = keys,
                        colors = ['blue','orange','red', 'green', 'yellow'],
                        pctdistance = 0.7, labeldistance = 1.4,
                        shadow = True, normalize=False)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
        else:
            st.error(prediction)
   
    except Exception as e:
        st.error(f"An unexpected error occured, please check Streamlit's logs!  \n\n{str(e)}")

    finally:
        delete_temp_image(temp_image)
