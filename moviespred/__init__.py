import os


paths = dict(project= os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
paths["raw_images"]=os.path.join(paths["project"], 'raw_images')
paths["resize_images"]=os.path.join(paths["project"], 'images_resized')
paths["ref"]=os.path.join(paths["project"], 'raw_data')
