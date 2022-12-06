import os

import numpy as np
import pandas as pd

from tensorflow.data import Dataset, AUTOTUNE
from tensorflow.io import read_file, decode_jpeg
from tensorflow import strings
from tensorflow import int32

import matplotlib.pyplot as plt

from moviespred import paths

refs = pd.read_csv(paths['references'] + '/references_mlt_label.csv')
refs = refs.query("is_tv_movie == 0").copy()
refs.drop('is_tv_movie', axis=1, inplace=True)
refs['images_file'] = refs['image_path'].str.split('/').apply(
    lambda x: os.sep.join(x[-2:]))
classes = refs[[c for c in refs.columns if 'is_' in c]]
refs['classes_vector'] = [
    '-'.join(list(row)) for row in classes.to_numpy().astype(np.str_)
]

genres = np.array([g.replace('is_', '') for g in classes.columns])

dataset = refs[['images_file', 'classes_vector']]

dataset = dataset.sample(frac=1.).reset_index(drop=True)
index_val = int(.7 * dataset.shape[0])

dataset_train = dataset.loc[:index_val, :]
dataset_val = dataset.loc[index_val + 1:, :]

ds_train = Dataset.from_tensor_slices(dataset_train)
ds_test = Dataset.from_tensor_slices(dataset_val)


def get_label(sample):
    lab = sample[1]
    label = strings.to_number(strings.split(lab, sep='-'), out_type=int32)
    return label


def get_image(sample):
    file_path = strings.join([paths['images_train'], os.sep, sample[0]])
    img = read_file(file_path)
    img = decode_jpeg(img, channels=3)
    return img


def load_sample(sample):
    image = get_image(sample)
    label = get_label(sample)
    return image, label


ds_train = ds_train.map(load_sample, num_parallel_calls=AUTOTUNE).batch(32)

im, la = next(iter(ds_train))

plt.imshow(im)
plt.title('-'.join(genres[la.numpy().astype(np.bool_)]))
