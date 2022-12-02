from fastapi import FastAPI
from tensorflow.keras.models import load_model
from moviespred import paths
import os
import numpy as np
# from tensorflow.keras import  models

app = FastAPI()

app.state.model = load_model(os.path.join(paths['models'], 'full_model'))

@app.get("/")
async def root():
    return {"status": "UP"}

@app.get('/predict')
def predict():
    # Fake image to test model load and predict
    image = np.ones(shape=(1, 600, 400, 3))
    # yet to to code, remaining question : are we going with a recording or an image directly?
    pred = app.state.model.predict(image)
    return {"prediction": str(pred)}  #transform np arry et que je reshape
