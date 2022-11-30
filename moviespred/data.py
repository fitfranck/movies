from pathlib import Path
from google.cloud import storage
import os
from moviespred import paths
from moviespred.preprocessing import resize_image
import pandas as pd
import requests as rq
from PIL import Image
import io
from moviespred import paths

genre_liste =['action',
 'adventure',
 'animation',
 'comedy',
 'crime',
 'documentary',
 'drama',
 'family',
 'fantasy',
 'history',
 'horror',
 'music',
 'mystery',
 'romance',
 'science-fiction',
 'thriller',
 'war',
 'western']

BUCKET = os.getenv('GCP_BUCKET')

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

def upload_images(genre, source_dir, target_blob):
    #genre : genre_name
    #source_dir : source de l'upload
    #target_blob : où les mettre
    images_list = list(Path(source_dir).glob(f'{genre.lower()}/*.jpg'))
    images_files = [str(path) for path in images_list]

    for img in images_files:
        image_name = img.split('/')[-1]
        path_to_image = os.path.join(source_dir, f'{genre.lower()}', f'{image_name}')

        upload_blob(BUCKET, path_to_image, f'{target_blob}/{genre.lower()}/{image_name}')



def movies_pred(genre):

    genres_raw = [
    {'id': 28, 'name': 'action'},
    {'id': 12, 'name': 'adventure'},
    {'id': 16, 'name': 'animation'},
    {'id': 35, 'name': 'comedy'},
    {'id': 80, 'name': 'crime'},
    {'id': 99, 'name': 'documentary'},
    {'id': 18, 'name': 'drama'},
    {'id': 10751, 'name': 'family'},
    {'id': 14, 'name': 'fantasy'},
    {'id': 36, 'name': 'history'},
    {'id': 27, 'name': 'horror'},
    {'id': 10402, 'name': 'music'},
    {'id': 9648, 'name': 'mystery'},
    {'id': 10749, 'name': 'romance'},
    {'id': 878, 'name': 'science-fiction'},
    {'id': 10770, 'name': 'tv-movie'},
    {'id': 53, 'name': 'thriller'},
    {'id': 10752, 'name': 'war'},
    {'id': 37, 'name': 'western'}
]

    df = pd.read_csv(f'{paths["ref"]}/references.csv')

    df = df.drop(columns = 'Unnamed: 0')
    df = df.drop_duplicates()
    df = df.dropna(subset=['overview','poster_path'])
    df = df[df.is_principal != 10770]
    df['id'] = df['id'].apply(lambda x: '{0:0>7}'.format(x))

    df['poster_url'] = 'https://www.themoviedb.org/t/p/original/' + df['poster_path']

    non_num_values = []

    for i in df['id']:
        if i.isdigit() == False:
            non_num_values.append(i)

    for i in non_num_values:
        indexNames = df[ df['id'] == i ].index
        df = df.drop(indexNames)

    df = df.sort_values(by = 'popularity', ascending = False)

    df_genre = df[df['is_principal'] == [x['id'] for x in genres_raw if x['name']==genre][0]]
    df_genre = df_genre.sort_values(by = 'popularity', ascending = False)
    df_len = len(df_genre)

    list_address = df_genre['poster_url'].to_list()
    list_names = df_genre['id'].to_list()

    c = 1
    for content, save_name in zip(list_address, list_names):
        res = rq.get(content)
        save_path = f"{paths['raw_images']}/{genre}/{save_name}.jpg"
        with open(save_path, 'w') as f:
            image = Image.open(io.BytesIO(res.content))
            image.save(f)
            print(f'{c}/{df_len} downloaded image of {genre}')
            c = c + 1

def remove(genre,dir_):
    directory = os.path.join(dir_, genre)
    files = os.listdir(directory)
    for img in files:
        os.remove(f'{dir_}/{genre}/{img}')


def download_images(genre):

    movies_pred(genre)

        # fct telecharger
    resize_image(genre)
        # fct resized
    upload_images(genre, paths['raw_images'],'test_images/')
    upload_images(genre, paths['resize_images'],'images_train/')
        # fct uload BUCKET
    remove(genre,paths['raw_images'])
    remove(genre,paths['resize_images'])
