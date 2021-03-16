
import streamlit as st
import numpy as np
import requests
from util.ParamsCache import ParamsCache
from util.WebUtils import image_css, image_html, get_multipart_form_data, get_form_data
from util.ImageUtils import save_temp_image, delete_temp_image, save_temp_image_from_canvas
from streamlit_drawable_canvas import st_canvas
from pylab import array
import matplotlib.pyplot as plt

from PIL import Image
import time
import matplotlib as mpl

st.set_page_config(layout="wide")

hide_streamlit_style = f'''
            <style>
                #MainMenu {{
                    visibility: hidden;
                    }}
                footer {{
                    visibility: hidden;
                    }}
                .uploadedFile {{
                    display: none;
                    }}
            </style>
            '''

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

c1, c2 = st.beta_columns(2)

with c1:
    if st.button("Doodle Recognition"):
        ParamsCache.getInstance().setCurrentPage(True, False)

with c2:
    if st.button("Let’s play Pictionary !"):
        ParamsCache.getInstance().setCurrentPage(False, True)

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

st.text("")

temp_image = ''
form_data = ''
multipart_form_data = ''
prediction = {}

try:
    if ParamsCache.getInstance().getIsDoodle():
        
        file_data = st.file_uploader("Select an image", type=["jpg", "jpeg", "png"])

        if file_data is not None:

            temp_image, image_size = save_temp_image(file_data)

            with st.spinner('Checking...'):        

                response = requests.post(
                            ParamsCache.getInstance().getUrl(),
                            data = get_form_data(model_name, num_class), 
                            files = get_multipart_form_data(temp_image), 
                            verify=False
                            )

                response_status = response.status_code
                prediction = response.json()['prediction']

                if response_status == 200:
                    values = prediction.values()
                    keys = prediction.keys()
                    keys = [key for key in keys]
                    values = [int(val)/100 for val in values]

                    c3, c4 = st.beta_columns(2)

                    with c3:
                        st.markdown(image_html(image_size, temp_image), unsafe_allow_html=True)

                    with c4:
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

    elif ParamsCache.getInstance().getIsPictionary():
        
        st.title(":sparkles: Let's draw :")

        c5, c6 = st.beta_columns(2)
        guess = False
        
        with c5:
            canvas_result = st_canvas(
                stroke_width = 6,
                stroke_color = "#fff",
                background_color = "#000",
                height = 400,
                width = 400,
                drawing_mode = "freedraw",
                key = "canvas",
            )
            
            result = st.button("Guess")

            guess = canvas_result.image_data is not None and result
            
            if guess:
                temp_image = save_temp_image_from_canvas(canvas_result.image_data)

                st.write(temp_image)

        with c6:
            if guess:
                response = requests.post(
                                ParamsCache.getInstance().getUrl(), 
                                data = get_form_data(model_name, num_class), 
                                files = get_multipart_form_data(temp_image), 
                                verify = False
                                )

                response_status = response.status_code
                prediction = response.json()['prediction']
                
                if response_status == 200:
                    values = prediction.values()
                    keys = prediction.keys()
                    keys = [key for key in keys]
                    values = [int(val)/100 for val in values]

                    with st.spinner('Hmmm... Let me think :thinking_face:'):
                        time.sleep(1)
                    with st.spinner(':hamburger:'):
                        time.sleep(0.7)
                    with st.spinner(':heart: , maybe ?'):
                        time.sleep(0.9)
                    with st.spinner(':dog:'):
                        time.sleep(0.5)
                    with st.spinner('Almost there...'):
                        time.sleep(1.5)
                    with st.spinner(':fire:'):
                        time.sleep(0.3)
                    with st.spinner(':cat:'):
                        time.sleep(0.2)
                    with st.spinner(':basketball:'):
                        time.sleep(0.2)
                    with st.spinner(':koala:'):
                        time.sleep(0.2)
                    with st.spinner(':kiwi_fruit:'):
                        time.sleep(0.1)
                    with st.spinner(" Got it ! :raised_hands: :raised_hands:"):
                        time.sleep(1.5)
                    plt.figure(figsize = (1, 1))
                    cmap = plt.get_cmap("tab20c")
                    outer_colors = cmap(np.arange(5)*4)
                    mpl.rcParams['font.size'] = 3
                    plt.pie(values, labels = keys,radius=1, colors=outer_colors,
                            wedgeprops=dict(width=0.2, edgecolor='w'))
                    st.set_option('deprecation.showPyplotGlobalUse', False)
                    st.pyplot()

                else:
                    st.error(prediction)

except Exception as e:
    print(e)
    st.error(f"An unexpected error occured, please check Streamlit's logs!  \n\n{str(e)}")

finally:
    delete_temp_image(temp_image)
