import os
import base64
import pandas as pd
from PIL import Image
import requests as rq
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_extras.app_logo import add_logo
from streamlit_extras.let_it_rain import rain
import plotly.express as px
import seaborn as sns

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
    """"

    """
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

COLOR_BLUE = "#1C83E1"

if uploaded_files:
    col1, col2 = st.columns(2)
    with col1:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image = image.resize(IMAGE_SIZE)
            st.image(image, caption="Here's the image you uploaded ☝️")
            img_bytes = uploaded_file.getvalue()

    with col2:
        clik = st.button('What is the prediction?')
        if clik:
            res = rq.post(url + "/predict", files={'img': img_bytes})
            res_num = {k: float(v.replace('%', '')) for k, v in res.json().items()}
            df = pd.DataFrame(res_num, index=['score']).T
            df = df.sort_values(by='score', ascending=False)

            # df = df.reset_index(drop=False)
            # df.columns = ['genre', 'score']
            print(df)
            # fig = plt.figure(figsize=(14, 25))
            # sns.barplot(data=df, x='score', y='genre')
            # plt.xlabel(''); plt.ylabel('')
            # plt.xticks(fontsize=30); plt.yticks(fontsize=30)
            # st.pyplot(fig)
            fig = px.bar(df, orientation='h',title= "prediction")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True,facet_row=df['score'])
