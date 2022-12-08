import os
import base64
import pandas as pd
from PIL import Image
import requests as rq
import streamlit as st
import altair as alt
from streamlit_extras.app_logo import add_logo
from streamlit_extras.let_it_rain import rain
import plotly.express as px


st.title('APP1')
st.write('Welcome to app1')


col1, col2 = st.columns(2)

with col1:

        image = Image.open(uploaded_file)
        image = image.resize(IMAGE_SIZE)
        st.image(image, caption="Here's the image you uploaded ☝️")
        img_bytes = uploaded_file.getvalue()
