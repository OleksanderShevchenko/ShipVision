import os
import shutil

_TARGET_FOLDER = "valid"
_PATH_IMAGE = f"Ships dataset/{_TARGET_FOLDER}/images"
_DATASET_FOLDER = f"Ships dataset/{_TARGET_FOLDER}/"
_PATH_LABELS = f"Ships dataset/{_TARGET_FOLDER}/labels"
_CLASSES = ['Aircraft Carrier', 'Bulkers', 'Car Carrier', 'Container Ship', 'Cruise', 'DDG', 'Recreational', 'Sailboat', 'Submarine', 'Tug']


def convert_dataset_to_tensorflow_ogranizing():
    working_dir = os.path.dirname(os.path.realpath(__file__))
    dataset_path = os.path.join(working_dir, *os.path.split(_DATASET_FOLDER))
    errors = 0

    i = 0
    for dir in _CLASSES:
        class_dir_name = os.path.join(dataset_path, dir)
        if not os.path.exists(class_dir_name):
            os.makedirs(class_dir_name)

    files_img = os.listdir(_PATH_IMAGE)
    print(f"Totally found {len(files_img)} image files!")
    counter = 0
    for file in files_img:
        name, ext = os.path.splitext(file)
        label_file_name = name + ".txt"
        label_file = os.path.join(_PATH_LABELS, label_file_name)
        if os.path.isfile(label_file):
            with open(label_file, "rt") as fp:
                data = fp.readlines()
                idx = int(data[0].strip().split()[0])
                class_name = _CLASSES[idx]
                class_dir_name = os.path.join(dataset_path, class_name)
                source_file = os.path.join(_PATH_IMAGE, file)
                destination_file = os.path.join(class_dir_name, file)
                shutil.copyfile(source_file, destination_file)
                counter += 1
        else:
            print(f'File - {label_file} could not be found! Image file {file} will not be copied')
            errors += 1
    print(f"--- Done!!! --- Total errors = {errors} Totally copied {counter} files")

if __name__ == "__main__":
    convert_dataset_to_tensorflow_ogranizing()
