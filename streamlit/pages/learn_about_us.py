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
from moviespred.references import paths


IMAGE_SIZE = (600, 400)

st.title('Our team')

image = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'end.png'))
image = image.resize(IMAGE_SIZE)
st.image(image)
# img_bytes = uploaded_file.getvalue()

st.title('Merci Vincent, notre réalisateur !')
