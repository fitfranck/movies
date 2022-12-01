from PIL import Image
import numpy as np
from references import genres
from moviespred import paths
import os

def resize_image(image_dir,target_size=(400,600)):

    for genre in genres :
        path_images = (f'../movies/raw_images/{genre}')

        files = os.listdir(path_images)

        for img in files:
            new_image = Image.open(f'raw_images/{genre}/{img}')
            new_image = new_image.resize(target_size)
            new_image.save(f'images_resized/{genre}/{img}')


def to_rgb():
    for g in genres:
        files = os.listdir(f'{paths["resize_images"]}/{g}')
        for i in range(len(files)):
            img = np.array(Image.open(f'{paths["resize_images"]}/{g}/{files[i]}'))
            if len(img.shape) == 2:
                img = np.repeat(img[:,:,None], 3, axis=2)
                im = Image.fromarray(img)
                im.save(f'{paths["resize_images"]}/{g}/{files[i]}')
