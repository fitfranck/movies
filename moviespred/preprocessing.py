from PIL import Image
import numpy as np
from moviespred.references import genres
from moviespred import paths
import os

def resize_image(genre,target_size=(400,600)):

    # for genre in image_dir :
    # path_images_resize = paths['resize_images']
    dir_ = f'{paths["raw_images"]}/{genre}'
    files = os.listdir(dir_)
    print(f'The resize of the {genre} movie posters are finished' )

    for img in files:
        new_image = Image.open(f'{dir_}/{img}')
        new_image = new_image.resize(target_size)
        new_image.save(f'{paths["resize_images"]}/{genre}/{img}')


def to_rgb(genre):
    files = os.listdir(f'{paths["resize_images"]}/{genre}')
    for i in range(len(files)):
        img = np.array(Image.open(f'{paths["resize_images"]}/{genre}/{files[i]}'))
        if len(img.shape) == 2:
            img = np.repeat(img[:,:,None], 3, axis=2)
            im = Image.fromarray(img)
            im.save(f'{paths["resize_images"]}/{genre}/{files[i]}')
