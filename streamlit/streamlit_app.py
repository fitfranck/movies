import streamlit as st
from PIL import Image
import requests as rq


url = 'http://localhost:8000'



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


# st.write    ("""
#                 # **IMAGE-IN**

#         ## *What's on the bill tonight guys  ?*


# """)

# original_title = '<p style="font-family:Courier; color:Pink; font-size: 50px;"> IMAGE-IN</p>'
# st.write(original_title, unsafe_allow_html=True)



# CSS = """
# h1 {
#     color: red;
# }
# .stApp {
#     background-image: url(https://avatars1.githubusercontent.com/u/9978111?v=4);
#     background-size: cover;
# }
# """


# st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)


st.write    ("""
                # **IMAGE-IN**

        ## *What's on the bill tonight guys  ?*


""")

uploaded_files = st.file_uploader("drag and drop movies'posters",type=['jpg','jpeg','png'],help="Charger une image au format jpg,jpeg,png", accept_multiple_files=True,)



for uploaded_file in uploaded_files:
    image = Image.open(uploaded_file)
    image = image.resize((400,600))

    st.image(image, caption="Here's the image you uploaded ☝️")
    img_bytes = uploaded_file.getvalue()

# if uploaded_files:

clik = st.button('click')
if clik:
    st.write('coucou')
    res = rq.post(url + "/predict", files={'img': img_bytes})
    st.write(res.json())
if uploaded_files:
    res = rq.post(url + "/predict", files={'img': img_bytes})
    st.write('predict!')
    st.write(res.status_code)
    if res.status_code=='200':
        st.write(f'<a href="{url}">{res}</a>', unsafe_allow_html=True)
    else:
        pass

# if st.checkbox("Show the movies' genre", False):
#     predict(image: UploadFile=File(f"{url}+/predict"))


if st.button("it's true "):
    st.balloons()
# if res.status_code == 200:
#     ### Display the image returned by the API
#     st.image(res.content, caption="Image returned from API ☝️")
# else:
#     st.markdown("**Oops**, something went wrong 😓 Please try again.")
#     print(res.status_code, res.content)
# image_in_api_url = 'http://localhost:8000/predict'

# response = rq.get(image_in_api_url)

# prediction = response.json()

# pred = prediction['genre']

# st.header(f"the movie's genre: ${round(pred, 2)}")





# image_path = 'images/python.png'
