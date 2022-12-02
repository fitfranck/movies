from pathlib import Path
from google.cloud import storage
import os
from moviespred.preprocessing import resize_image
import pandas as pd
import requests as rq
from PIL import Image
import io
from moviespred import paths, genres_raw, genres_list
from google.cloud import storage

BUCKET = os.getenv('GCP_BUCKET')

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

def upload_images(genre, source_dir, target_blob):
    """Upload all images for a given genre"""
    images_list = list(Path(source_dir).glob(f'{genre.lower()}/*.jpg'))
    images_files = [str(path) for path in images_list]

    for img in images_files:
        image_name = img.split('/')[-1]
        path_to_image = os.path.join(source_dir, f'{genre.lower()}', f'{image_name}')

        upload_blob(BUCKET, path_to_image, f'{target_blob}/{genre.lower()}/{image_name}')

def create_table(genre):
    """Create a DataFrame for a given genre"""
    df = pd.read_csv(f'{paths["references"]}/references.csv')

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
    return df_genre

def download_posters(df):
    """Download posters from a DataFrame"""
    df_len = len(df)
    list_address = df['poster_url'].to_list()
    list_names = df['id'].to_list()

    c = 1
    for content, save_name in zip(list_address, list_names):
        save_path = f"{paths['images_raw']}/{genre}/{save_name}.jpg"
        if not os.path.isfile(save_path):
            with open(save_path, 'w') as f:
                res = rq.get(content)
                image = Image.open(io.BytesIO(res.content))
                image.save(f)
                print(f'{c}/{df_len} downloaded image of {genre}')
                c = c + 1

def remove_images(genre, dir_):
    """Remove images for a given genre"""
    directory = os.path.join(dir_, genre)
    files = os.listdir(directory)
    for img in files:
        os.remove(f'{dir_}/{genre}/{img}')

def get_images(genre):
    """For a given genre, get posters, resize them, upload both to bucket
    then remove local files"""
    df = create_table(genre)

    download_posters(df)

    resize_image(genre)

    upload_images(genre, paths['images_raw'], 'images_raw')
    upload_images(genre, paths['images_train'], 'images_train')

    remove_images(genre, paths['images_raw'])
    remove_images(genre, paths['images_train'])


def list_blobs(bucket_name,genre,limit=50):
    """Lists all the blobs in the bucket."""

    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name, prefix=f'images_train/{genre}', max_results=limit)

    return blobs


def save_train_image(blob):
    save_path = os.path.join(paths['project'], blob.name)
    blob.to_filename(save_path)


genres_test = ['animation', 'comedy', 'documentary', 'drama', 'horror']

if __name__ == "__main__":
    for genre in genres_test:
    #     get_images(genre)
        blobs = list_blobs('movies-wagon', genre)
        for blob in blobs:
            save_train_image(blob)
