import streamlit as st
from PIL import Image
import requests as rq
import os
from streamlit_extras.app_logo import add_logo
from streamlit_extras.let_it_rain import rain
import base64


st.set_page_config(
    page_title="IMAGE-IN", page_icon="📸", initial_sidebar_state="expanded", layout="centered"
)

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def build_markup_for_logo(
    png_file,
    background_position="10% 10%",
    margin_top="0.10%",
    image_width="30%",
    image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )

def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

IMAGE_SIZE = (400, 600)
LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'image_in.png')

add_logo(LOGO_PATH)

st.title("""
         📸 IMAGE-IN
         """)
st.header("*What's on the bill tonight guys  ?*")


uploaded_files = st.file_uploader("drag and drop movies'posters",type=['jpg','jpeg','png'],help="Charger une image au format jpg,jpeg,png", accept_multiple_files=True,)
url = 'https://movies-7pwb73wneq-od.a.run.app'
# url = 'http://localhost:8000'

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        image = image.resize(IMAGE_SIZE)
        st.image(image, caption="Here's the image you uploaded ☝️")
        img_bytes = uploaded_file.getvalue()

clik = st.button('What is the prediction?')
if clik:
    try:
        res = rq.post(url + "/predict", files={'img': img_bytes})
        st.write(res.json())
        rain(
            emoji="🎈",
            font_size=54,
            falling_speed=5,
            animation_length="1",
        )
    except:
        st.write("Please load a movie poster")
