from pathlib import Path
from google.cloud import storage
import os
from moviespred import paths
from moviespred.preprocessing import resize_image
import pandas as pd

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

    images_list = list(Path(source_dir).glob(f'{genre.lower()}/*.jpg'))

    images_files = [str(path) for path in images_list]

    for img in images_files:
        image_name = img.split('/')[-1]
        path_to_image = os.path.join(source_dir, f'{genre.lower()}', f'{image_name}')

        upload_blob(BUCKET, path_to_image, f'{target_blob}/{genre.lower()}/{image_name}')


def download_images(genre, nbr):
    for i in range nbr:
        if not i%10:
        fct telecharger
        fct resized
        fct uload BUCKET
        rm
