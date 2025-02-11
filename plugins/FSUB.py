import os

FILE_PATH = "fsub.txt"

def get_fsub():
    """Retrieve FSUB_1 from file."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return file.read().strip()
    return ""

def update_fsub(channel_id):
    """Update FSUB_1 value in file."""
    with open(FILE_PATH, "w") as file:
        file.write(channel_id)
    return True
