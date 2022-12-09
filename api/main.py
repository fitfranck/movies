import os
import io
import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import  CORSMiddleware
from tensorflow.keras.models import load_model
from api.helpers import macro_f1


# from tensorflow.keras import  models
GENRES = ['action',
 'adventure',
 'animation',
 'comedy',
 'crime',
 'documentary',
 'family',
 'horror',
 'romance']

IMAGE_SIZE = (224, 224)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.model = load_model(os.path.join(MODEL_PATH, 'full_model'),
                custom_objects={"macro_f1": macro_f1})

@app.get("/")
async def root():
    return {"status": "UP"}

@app.post('/predict')
async def predict(img: UploadFile=File(...)):

    contents = await img.read()
    if contents:
        image = Image.open(io.BytesIO(contents))
        image = image.resize(IMAGE_SIZE)
        image = np.array(image)
        image = image.reshape((1, *IMAGE_SIZE, 3))

        preds_raw = app.state.model.predict(image).reshape(len(GENRES))

        order = np.argsort(preds_raw)[::-1][:5]
        mask = preds_raw >= preds_raw[order][-1]
        preds_probas = preds_raw[mask]
        preds_genres = np.array(GENRES)[mask]
        result={}
        for k,v in zip(preds_genres, preds_probas):
            result[k]= f"{v:.2%}"
        return result
    else:
        return {"error": "image could not be read"}
