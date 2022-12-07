from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from moviespred import paths
import os
import numpy as np

import io
from PIL import Image

# from tensorflow.keras import  models
genre_list = ['action','animation','horror', 'drame', 'science-fiction', 'comedy']
genre_sample = ['action','animation','horror']
app = FastAPI()

app.state.model = load_model(os.path.join(paths['models'], 'full_model'))



@app.get("/")
async def root():
    return {"status": "UP"}

@app.post('/predict')
async def predict(img: UploadFile=File(...)):

    contents = await img.read()
    if contents:

        image = Image.open(io.BytesIO(contents))
        image = image.resize((400,600))
        image = np.array(image)
        image = image.reshape((1,600,400,3))


    else:
        # Fake image to test model load and predict
        # home = os.environ['HOME']
        # image= Image.open(f"{home}/code/fitfranck/movies/images_raw/Action/save_6935.jpg")
        # image= image.resize((400,600))
        pass
    # yet to to code, remaining question : are we going with a recording or an image directly?
    preds_raw = app.state.model.predict(image).reshape(3)


    mask = preds_raw > 0.02

    preds_probas = preds_raw[mask]
    preds_genres = np.array(genre_sample)[mask]
    # pred_genres = np.array(genre_sample)[probas]

    json_dict={}
    for k,v in zip(preds_genres, preds_probas):
        json_dict[k]= f"{v:.2%}"

    return json_dict
