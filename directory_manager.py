import os

def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True, f"Directory '{path}' created successfully."
    except OSError as e:
        return False, f"Failed to create directory: {e}"

def directory_exists(path):
    return os.path.exists(path)
