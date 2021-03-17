import sys
import streamlit as st
from util import WebUtils, ImageUtils, ExceptionUtils

def uploadpic():

    temp_image = ''
    prediction = {}
    
    ALL_CAT_KEY = '🎲 All categories' 
    ANIMALS_KEY = '🐒 Animals'
    FOODS_KEY = '🍕 Foods'
    TRANSPORTS_KEY = '🚍 Means of transport'
    OBJECT_KEY = '🌂 Object'
    
    try:

        st.markdown(WebUtils.uploadpic_css(), unsafe_allow_html=True)

        st.text("")

        model = st.radio(
                            "Let's play with :", 
                            ( 
                                ALL_CAT_KEY, 
                                ANIMALS_KEY,
                                FOODS_KEY,
                                TRANSPORTS_KEY,
                                OBJECT_KEY
                            )
                        )
        st.write(model)

        model_name = ''
        num_class = ''

        if model == ANIMALS_KEY:
            model_name = 'models_Animal_model.h5'
            num_class = 'animals'
        elif model == FOODS_KEY:
            model_name = 'models_Food_model.h5'
            num_class = 'food'
        elif model == TRANSPORTS_KEY:
            model_name = 'models_Transport_model.h5'
            num_class = 'transport'
        elif model == OBJECT_KEY:
            model_name = 'models_Object_model.h5'
            num_class = 'object'
        else:
            model_name = 'models_model_V1_DPoint_60K_NCLass_345.h5'
            num_class = '345'

        st.text("")

        file_data = st.file_uploader("Select an image", type=["jpg", "jpeg", "png"])

        if file_data is not None:

            temp_image, image_size = ImageUtils.save_temp_image(file_data)

            with st.spinner('Checking...'):        

                response_status, prediction = WebUtils.post(model_name, num_class, temp_image)

                if response_status == 200:
                        
                    keys, values = WebUtils.get_pred_labels_and_values(prediction)
                        
                    c1, c2 = st.beta_columns(2)

                    with c1:
                        st.markdown(WebUtils.image_html(image_size, temp_image), unsafe_allow_html=True)

                    with c2:
                        st.write(WebUtils.build_graph(keys, values))
                else:
                    st.error(prediction)

    except Exception as e:
        st.error(ExceptionUtils.exception_process_display(sys.exc_info()))

    finally:
        ImageUtils.delete_temp_image(temp_image)
