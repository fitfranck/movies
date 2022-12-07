import streamlit as st
from PIL import Image
import requests as rq
from collections import Counter
import os
from streamlit_extras.app_logo import add_logo
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.let_it_rain import rain
import base64
from moviespred.references import paths
import awesome_streamlit as ast
# app1.py
import streamlit as st
def app():
    st.title('APP1')
    st.write('Welcome to app1')

st.title("""
         📸 IMAGE-IN
         """)
st.header("*What's on the bill tonight guys  ?*")
