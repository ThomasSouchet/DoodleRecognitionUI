import streamlit as st
# Local Imports
import canvas
import uploadpic
import home

st.set_page_config(
    layout="wide",
    page_title = "Sketching with DL",
    page_icon = ":fire:",
    initial_sidebar_state="expanded",
    )

# Sidebar Navigation
st.sidebar.title('Sketching with DL')
options = st.sidebar.selectbox(
    "How would you like to play ?",
    ("Homepage", "Upload a file", "Draw something"))

if options == 'Homepage':
    home.home()
elif options == 'Upload a file':
    uploadpic.uploadpic()
elif options == 'Draw something':
    canvas.canvas()
