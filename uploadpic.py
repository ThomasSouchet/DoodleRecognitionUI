
import streamlit as st
from util import WebUtils, ImageUtils

def uploadpic():

    temp_image = ''
    prediction = {}

    try:

        st.markdown(WebUtils.uploadpic_css(), unsafe_allow_html=True)

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
        st.error(f"An unexpected error occured, please check Streamlit's logs!  \n\n{str(e)}")

    finally:
        ImageUtils.delete_temp_image(temp_image)
