import os
from PIL import Image

_TARGET_FOLDER = "AdditionToTrain"
_CLASSES = ['Aircraft Carrier', 'Bulkers', 'Car Carrier', 'Container Ship', 'Cruise', 'DDG', 'Recreational', 'Sailboat', 'Submarine', 'Tug']


def create_empty_folders():
    if not os.path.exists(_TARGET_FOLDER):
            os.makedirs(_TARGET_FOLDER)

    for class_name in _CLASSES:
        target_files_path = os.path.join(_TARGET_FOLDER, class_name)
        os.makedirs(target_files_path)
                

if __name__ == "__main__":
    create_empty_folders()