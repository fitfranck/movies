
import pandas as pd
import os
from PIL import Image
import numpy as np

import matplotlib.pyplot as plt

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import utils
from tensorflow.keras import Model, models
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from moviespred.references import paths

df = pd.read_csv(f"{paths['references']}/'references.csv'")

# https://cloud.google.com/resource-manager/docs/creating-managing-projects


# project_id = 'movies-370013'


# !gcloud config set project {project_id}

# bucket = 'movies-wagon'
# !mkdir images_preprocess
# !gsutil -m cp -r gs://movies-wagon/images_resized/ images_preprocess/


# rm_liste =[
#  'adventure',
#  'comedy',
#  'crime',
#  'documentary',
#  'drama',
#  'family',
#  'fantasy',
#  'history',
#  'music',
#  'mystery',
#  'romance',
#  'science-fiction',
#  'thriller',
#  'war',
#  'western']

# remove_liste = [rm.capitalize() for rm in rm_liste]
# for genre in remove_liste:
#   !rm -rf images_preprocess/images_resized/{genre}

#   genre_liste =['action', 'Animation', 'Horror']


# genres = [g.capitalize() for g in genre_liste]







# list_img = []

# for g in genres:
#   files = os.listdir(f'images_preprocess/images_resized/{g}')
#   for i in range(len(files)):
#     img = np.array(Image.open(f'images_preprocess/images_resized/{g}/{files[i]}'))
#     if len(img.shape) == 2:
#       img = np.repeat(img[:,:,None], 3, axis=2)
#       image = Image.fromarray(img)
#       image.save( f'images_preprocess/images_resized/{g}/{files[i]}')

data_dir = paths/'images_preprocess/images_resized'
batch_size = 32

train_ds = utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size= (600,400),
  batch_size=batch_size)

val_ds = utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(600, 400),
  batch_size=batch_size)

class_names = train_ds.class_names


AUTOTUNE = tensorflow.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


data_augmentation = Sequential(
  [
    layers.RandomFlip("horizontal",
                      input_shape=(600,
                                  400,
                                  3)),
    layers.RandomRotation(0.4),
    layers.RandomZoom(0.4),
  ]
)



num_classes = len(class_names)

def initialize_model(X: np.ndarray) -> Model:

    model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255, input_shape=(600, 400, 3)),
    layers.Conv2D(4, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(8, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.5),
    layers.Flatten(),
    layers.Dense(32, activation='softmax'),
    layers.Dropout(0.3),
    layers.Dense(num_classes)
    ])
    return model

def compile_model(model: Model, learning_rate: float) -> Model:
    model.compile(optimizer='adam',
              loss=tensorflow.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    return model




def train_model(model: Model,
                X: np.ndarray,
                y: np.ndarray,
                batch_size=64,
                patience=2,
                validation_split=0.3,
                validation_data=None) -> Tuple[Model, dict]:

    es = EarlyStopping(patience= 25, monitor='val_loss', restore_best_weights=True)



    epochs=1
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[es]
    )
    return model, history
