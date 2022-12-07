import streamlit as st
from PIL import Image
import requests as rq
import os
from streamlit_extras.app_logo import add_logo
from streamlit_extras.let_it_rain import rain
import base64

home = os.environ['HOME']
abs_path = f"{home}/code/fitfranck/movies/images_raw/Action/save_6935.jpg"

st.set_page_config(
    page_title="IMAGE-IN", page_icon="📸", initial_sidebar_state="expanded", layout="centered"
)

# st.sidebar.markdown(
#     "My Logo (sidebar) should be on top of the Navigation within the sidebar"
# )



#app.py

# PAGES = {
#     "app1": f"{paths['streamlit']}/ pages/app1",
#     "app2": f"{paths['streamlit']}/ pages/app2"
#                          }
# st.sidebar.title('Navigation')
# selection = st.sidebar.radio("Go to", list(PAGES.keys()))
# page = PAGES[selection]



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

add_logo(f'{home}/code/fitfranck/movies/images_train/logo/image_in.png')

# with st.sidebar.container():

#     st.sidebar.title("Sidebar")
#     add_logo(f'{home}/code/fitfranck/movies/images_train/logo/image_in.png')

# PAGES = {
#     "Home": os.path.join(paths['streamlit'], 'streamlit_app' )   ,
#     "Project": os.path.join(paths['streamlit'],' pages1')

# }

# def add_logo(logo_path, width, height):
#     """Read and return a resized logo"""
#     logo = Image.open(logo_path)
#     modified_logo = logo.resize((width, height))
#     return modified_logo

# my_logo = add_logo(f'{home}/code/fitfranck/movies/images_train/logo/image_in.png', 125, 125)
# st.sidebar.image(my_logo)



# st.sidebar.title("Navigation")

# selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# page = PAGES[selection]

# with st.spinner(f"Loading {selection} ..."):
#     ast.shared.components.write_page(page)
# st.sidebar.title("Contribute")
# st.sidebar.info(
#     "This an open source project and you are very welcome to **contribute** your awesome "
#     "comments, questions, resources and apps as "
#     "[issues](https://github.com/MarcSkovMadsen/awesome-streamlit/issues) of or "
#     "[pull requests](https://github.com/MarcSkovMadsen/awesome-streamlit/pulls) "
#     "to the [source code](https://github.com/MarcSkovMadsen/awesome-streamlit). "
# )
# st.sidebar.title("About")
# st.sidebar.info(
#     """
#     This app is maintained by Marc Skov Madsen. You can learn more about me at
#     [datamodelsanalytics.com](https://datamodelsanalytics.com).
# """
# )





st.title("""
         📸 IMAGE-IN
         """)
st.header("*What's on the bill tonight guys  ?*")




uploaded_files = st.file_uploader("drag and drop movies'posters",type=['jpg','jpeg','png'],help="Charger une image au format jpg,jpeg,png", accept_multiple_files=True,)
url = 'http://localhost:8000'

use_example_pictures = st.checkbox(
    "Use example pictures", False, help="Use in-built example pictures to demo the app"
)
if use_example_pictures:
    img= Image.open(abs_path)
    img= img.resize((400,600))
    st.image(img, caption="Here's the image exemple ❇️")
    img_bytes = open(abs_path,'rb')

if uploaded_files:
    for uploaded_file in uploaded_files:
        # st.write(uploaded_file)
        image = Image.open(uploaded_file)
        image = image.resize((400,600))

        st.image(image, caption="Here's the image you uploaded ☝️")
        img_bytes = uploaded_file.getvalue()



clik = st.button('what is the prediction ?')
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
            st.write("drap and drog une photo avant ")


if st.button("it's true "):
    st.balloons()
