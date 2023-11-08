import os
from PIL import Image

_DATASET_FOLDER = "Ships dataset"
_DIRS = ["train", "test", "valid"]
_CLASSES = ['Aircraft Carrier', 'Bulkers', 'Car Carrier', 'Container Ship', 'Cruise', 'DDG', 'Recreational', 'Sailboat', 'Submarine', 'Tug']

def correct_dataset():

    def _convert_image(image_file, class_name, counter) -> bool:
        try:
            image = Image.open(image_file)
            image_rgb = image.convert("RGB")
            new_file = os.path.join(os.path.dirname(image_file), class_name + "_" + str(counter) + ".jpeg")
            image_rgb.save(new_file)
        except Exception as err:
            print(f"Errror of convertation file {image_file} to jpg: \n{err}")
            return False
        else:
            return True

    for dir in _DIRS:
        for class_name in _CLASSES:
            counter = 0
            target_files_path = os.path.join(_DATASET_FOLDER, dir, class_name)
            files = os.listdir(target_files_path)
            for file in files:
                full_file_name = os.path.join(target_files_path, file)
                counter += 1
                seccess = _convert_image(full_file_name, class_name, counter)
                if seccess:
                    try:
                        os.remove(full_file_name)
                    except OSError:
                        pass
                    except Exception as err:
                        print(f"Error of deletion of file {full_file_name}: \n{err}")
                    

if __name__ == "__main__":
    correct_dataset()