from PIL import Image
import os

def resize_image(image_dir,target_size=(400,600)):

    for genre in genre_liste :
        path_images = (f'../movies/raw_images/{genre}')

        files = os.listdir(path_images)

        for img in files:
            new_image = Image.open(f'raw_images/{genre}/{img}')
            new_image = new_image.resize(target_size)
            new_image.save(f'images_resized/{genre}/{img}')
