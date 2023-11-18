import os
import uuid

from errors_messages import Errors

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            return folder_path
        except OSError as e:
            # print(f"Error creating folder: {folder_path}\n{e}")
            # Handle the error as needed
            return Errors.FOLDER_NOT_CREATED

    return folder_path


# Function to check if a filename has an allowed extension
def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def save_image(folder_path, file):
    parent_folder = create_folder_if_not_exists(folder_path)
    if parent_folder == Errors.FOLDER_NOT_CREATED:
        return Errors.FOLDER_NOT_CREATED

    if not allowed_image_file(file.filename):
        return Errors.INVALID_FILE_TYPE
    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file.save(os.path.join(parent_folder, unique_filename))
    return os.path.join(parent_folder, unique_filename)


def commify(value):
    return "{:,}".format(value)
