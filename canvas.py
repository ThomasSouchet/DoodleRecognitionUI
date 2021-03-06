import time, sys
import streamlit as st
from util import WebUtils, ImageUtils, ExceptionUtils
from streamlit_drawable_canvas import st_canvas

def canvas() :

    ALL_CAT_KEY = '🎲 All categories' 
    ANIMALS_KEY = '🐒 Animals'
    FOODS_KEY = '🍕 Foods'
    TRANSPORTS_KEY = '🚍 Means of transport'
    OBJECT_KEY = '🌂 Object'
    EMPTY_SPACE_KEY = ''

    temp_image = EMPTY_SPACE_KEY
    prediction = {}

    try:

        st.markdown(WebUtils.canvas_css(), unsafe_allow_html=True)

        st.image(ImageUtils.get_title_img())

        st.text(EMPTY_SPACE_KEY)

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

        model_name = EMPTY_SPACE_KEY
        num_class = EMPTY_SPACE_KEY

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
            model_name = 'models_model_V1_DPoint_20K_NCLass_80.h5'
            num_class = '80'

        st.text(EMPTY_SPACE_KEY)

        c1, c2 = st.beta_columns(2)
        with c1:
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
                
                temp_image = ImageUtils.save_temp_image_from_canvas(canvas_result.image_data)

                st.write(temp_image)

        with c2:
            if guess:
                
                response_status, prediction = WebUtils.post(model_name, num_class, temp_image) 

                if response_status == 200:

                    keys, values = WebUtils.get_pred_labels_and_values(prediction)

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

                    st.write(WebUtils.build_graph(keys, values))

                else:
                    st.error(prediction)

            else:
                st.title(EMPTY_SPACE_KEY)
                st.title(EMPTY_SPACE_KEY)

                st.markdown("<img src='https://media.giphy.com/media/IzitAtI5TJQEwWohcc/giphy.gif' width='400px' border='0px'/>", unsafe_allow_html=True)
                st.header("Start drawing here")

    except Exception as e:
        st.error(ExceptionUtils.exception_process_display(sys.exc_info()))

    finally:
        ImageUtils.delete_temp_image(temp_image)
