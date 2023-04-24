import os

def get_image_filenames(directory):
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            filenames.append(filename)
    return filenames

def get_image(image_id):
    directory = './outputs'  # replace with your directory path
    image_path = os.path.join(directory, f"{image_id}")

    if os.path.isfile(image_path):
        return image_path
    else:
        return None
