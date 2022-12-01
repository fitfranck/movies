from PIL import Image
import numpy as np
from moviespred.references import genres
from moviespred import paths
import os

def resize_image(genre, target_size=(400,600)):
    """For a given genre, resize all posters to a given size"""
    dir_ = f'{paths["images_raw"]}/{genre}'
    files = os.listdir(dir_)
    print(f'The resize of the {genre} movie posters are finished' )

    for img in files:
        new_image = Image.open(f'{dir_}/{img}')
        new_image = new_image.resize(target_size)
        new_image.save(f'{paths["images_train"]}/{genre}/{img}')


def to_rgb(genre):
    """For a given genre, add a third dimension to B&W images"""
    files = os.listdir(f'{paths["images_train"]}/{genre}')
    for i in range(len(files)):
        img = np.array(Image.open(f'{paths["images_train"]}/{genre}/{files[i]}'))
        if len(img.shape) == 2:
            img = np.repeat(img[:,:,None], 3, axis=2)
            im = Image.fromarray(img)
            im.save(f'{paths["images_train"]}/{genre}/{files[i]}')
