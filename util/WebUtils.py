from util.ImageUtils import load_image

def image_css(image_size):
    return f"""
            #teachers {{
                display: flex;
                flex-wrap: wrap;
            }}
            .teacher-card {{
                display: flex;
                flex-direction: column;
            }}
            .teacher-card img {{
                width: {image_size}px;
                height: {image_size}px;
                padding: 4px;
                margin: 10px;
                box-shadow: 0 0 4px #eee;
            }}
            .teacher-card span {{
                text-align: center;
            }}
            """

def image_html(image_size, temp_image):
    return f"""
            <style>
                {image_css(image_size)}
            </style>
            <div id="teachers">
                <div class="teacher-card">
                    <img src='data:image/png;base64,{load_image(temp_image)}'>
                </div>
            </div>
            """

def get_multipart_form_data(temp_image):
    return {
                "inputImage" : (open(temp_image, "rb"))
            }

def get_form_data(model_name, num_class):
    return {
                "modelName" : model_name,
                "numClass" : num_class
            }
