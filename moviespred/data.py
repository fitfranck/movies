# from pathlib import Path
# from google.cloud import storage
# import os


# images_path =Path('raw_images')
# images_list = list(images_path.glob('*/*.jpg'))

# images_files = [str(path) for path in images_list]


# def upload_blob(bucket_name, source_file_name, destination_blob_name):
#     """Uploads a file to the bucket."""
#     # The ID of your GCS bucket
#     # bucket_name = "your-bucket-name"
#     # The path to your file to upload
#     # source_file_name = "local/path/to/file"
#     # The ID of your GCS object
#     # destination_blob_name = "storage-object-name"

#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)

#     blob.upload_from_filename(source_file_name)

#     print(
#         f"File {source_file_name} uploaded to {destination_blob_name}."
#     )


# if __name__ == "__main__":
#     BUCKET = os.getenv('GCP_BUCKET')
#     for img in images_files:
#         image_name = img.split('/')[-1]#margaux explique
#         path_to_image = os.path.join(
#         os.path.dirname(
#             os.path.abspath(__file__)),'raw_images','Fantasy', f'{image_name}')
#         print( f'{image_name}')
#         upload_blob(BUCKET, path_to_image, f'test_images/{image_name}')
from pathlib import Path
from google.cloud import storage
import os


path_project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_images = os.path.join(path_project, 'raw_images')

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

def upload_images(genre):

    images_list = list(Path(path_images).glob(f'{genre.capitalize()}/*.jpg'))

    images_files = [str(path) for path in images_list]

    for img in images_files:
        image_name = img.split('/')[-1]
        path_to_image = os.path.join(path_images, f'{genre.capitalize()}', f'{image_name}')

        upload_blob(BUCKET, path_to_image, f'test_images/{genre.capitalize()}/{image_name}')
