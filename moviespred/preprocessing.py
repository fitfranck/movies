from PIL import Image
import os
from moviespred import paths

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
