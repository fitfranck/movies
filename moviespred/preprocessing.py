import os
import numpy as np
from PIL import Image
from tensorflow.keras.utils import image_dataset_from_directory
from moviespred import paths, genres_list


def resize_image(genre, target_size=(400, 600)):
    """For a given genre, resize all posters to a given size"""
    dir_ = f'{paths["images_raw"]}/{genre}'
    files = os.listdir(dir_)
    print(f'--> START Resize of {genre} ---' )

    for img in files:
        save_path = f'{paths["images_train"]}/{genre}/{img}'
        if not os.path.isfile(save_path):
            new_image = Image.open(f'{dir_}/{img}')
            new_image = new_image.resize(target_size)
            new_image.save(save_path)
    print(f'--> END Resize of {genre} ---' )


def to_rgb(genre):
    """For a given genre, add a third dimension to B&W images"""
    files = os.listdir(f'{paths["images_train"]}/{genre}')
    for i in range(len(files)):
        img = np.array(
            Image.open(f'{paths["images_train"]}/{genre}/{files[i]}'))
        if len(img.shape) == 2:
            img = np.repeat(img[:, :, None], 3, axis=2)
            im = Image.fromarray(img)
            im.save(f'{paths["images_train"]}/{genre}/{files[i]}')


def get_dataset(batch_size=32,
                validation_split=0.2,
                image_size=(600, 400)):
    """Get train/val set"""
    data_dir = paths['images_train']
    seed = np.random.randint(1, 200)
    train_ds = image_dataset_from_directory(data_dir,
                                            validation_split=validation_split,
                                            subset='training',
                                            shuffle=True,
                                            seed=seed,
                                            image_size=image_size,
                                            batch_size=batch_size)

    val_ds = image_dataset_from_directory(data_dir,
                                          validation_split=validation_split,
                                          subset="validation",
                                          shuffle=True,
                                          seed=seed,
                                          image_size=image_size,
                                          batch_size=batch_size)

    return train_ds, val_ds


if __name__ == "__main__":
    for genre in genres_list:
        to_rgb(genre)
