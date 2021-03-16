import requests
import plotly.graph_objects as go
from util import ImageUtils
from util.ParamsCache import ParamsCache

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
                    <img src='data:image/png;base64,{ImageUtils.load_image(temp_image)}'>
                </div>
            </div>
            """

def uploadpic_css():
    return f'''
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
                .css-4kisie {{
                    flex: 1 1 30% !important;
                    width: 2px;
                    padding-left: 0px;
                    }}
            </style>
            '''

def canvas_css():
    return f'''
            <style>
                .css-2trqyj {{
                    background-color: #F93822;
                    color : #FFF;
                    }}
                .css-4kisie {{
                    flex: 1 1 30% !important;
                    width: 2px;
                    padding-left: 0px;
                    }}
                .css-3mnucz {{
                    font-size : x-large !important;
                    }}
                h2 {{
                    font-weight: 550;
                    margin: 0rem 0rem;
                    padding: 0em 9em;
                    line-height: 1;
                    font-size: calc(1.3rem + .6vw);
                    }}
                #MainMenu {{
                    visibility: hidden;
                    }}
                footer {{
                    visibility: hidden;
                    }}
            </style>
            '''

def get_multipart_form_data(temp_image):
    return {
                "inputImage" : (open(temp_image, "rb"))
            }

def get_form_data(model_name, num_class):
    return {
                "modelName" : model_name,
                "numClass" : num_class
            }

def post_(data, files):
    response = requests.post(
        ParamsCache.getInstance().getUrl(),
        data = data, 
        files = files, 
        verify=False
        )

    return response.status_code, response.json()['prediction']
  
def post(model_name, num_class, temp_image):
    return post_(get_form_data(model_name, num_class), get_multipart_form_data(temp_image))

def get_pred_labels_and_values(prediction):
    values = prediction.values()
    keys = prediction.keys()
    keys = [key for key in keys]
    values = [int(val)/100 for val in values]
    return keys, values

def build_graph(keys, values):
    fig = ig = go.Figure(data=[go.Pie(labels=keys, values=values, pull=[0.2, 0, 0, 0])])
    fig.update_traces(hole=.4, hoverinfo="label+percent")
    fig.update_layout(annotations=[dict(text=' ', x=0.18, y=0.5, font_size=20, showarrow=False)])
    return fig
