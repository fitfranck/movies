import streamlit as st
import pandas as pd
import io
from PIL import Image
import requests as rq



st.markdown("""
                #**IMAGE-IN**

        ## *What's on the bill tonight guys  ?*


""")


uploaded_files = st.file_uploader("drag and drop movies'posters",type=['jpg','jpeg','png'],help="Charger une image au format jpg,jpeg,png", accept_multiple_files=True,)

for uploaded_file in uploaded_files:
     bytes_data = uploaded_file.read()
     image = Image.open(io.BytesIO(bytes_data))
    #  st.write("filename:", uploaded_file.name)
     st.image(image)




image_in_api_url = 'http://127.0.0.1:8000/predict'

response = rq.get(image_in_api_url)

prediction = response.json()

pred = prediction['genre']

st.header(f"the movie's genre: ${round(pred, 2)}")


if st.button("it's true "):
    st.balloons()








# from moviespred.references import paths


# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })

# df
# st.write("WHAT's on the bill tonight guys ?")



# st.write("how it's work ?")

# st.write("just drag and drop movies'posters and click on them for know their genres")



# if st.checkbox('Show content'):
#     st.write('''
#         This code will only be executed when the check box is checked

#         Streamlit elements injected inside of this block of code will \
#         not get displayed unless it is checked
#         ''')









# @st.cache
# def load_image(path):
#     with open(path, 'rb') as f:
#         data = f.read()
#     encoded = base64.b64encode(data).decode()
#     return encoded

# def image_tag(path):
#     encoded = load_image(path)
#     tag = f'<img src="data:image/png;base64,{encoded}">'
#     return tag

# def background_image_style(path):
#     encoded = load_image(path)
#     style = f'''
#     <style>
#     .stApp {{
#         background-image: url("data:image/png;base64,{encoded}");
#         background-size: cover;
#     }}
#     </style>
#     '''
#     return style

# file_jpg = st.file_uploader("Upload a PNG image", type=([".jpg"]))

# if file_jpg:
#     file_jpg_bytes = st.file_reader(file_jpg)
#     st.image(file_jpg_bytes)



# image_path = paths['image_train']/'Action'/'1008779.jpg'
# # image_link = 'https://docs.python.org/3/'

# st.write('*Hey*, click me I\'m a button!')

# st.write(f'<a href="{image_tag(image_path)}</a>', unsafe_allow_html=True)

# if st.checkbox('Show background image', False):
#     st.write(background_image_style(image_path), unsafe_allow_html=True)
