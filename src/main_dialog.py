import base64
import os
from io import BytesIO
from os import path as os_path
import tensorflow as tf

from PIL import Image, ImageQt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QAction, QToolButton, QLabel, QComboBox, QVBoxLayout, QMenu, QFileDialog, QInputDialog, \
    QLineEdit, QMessageBox, QApplication


class MainDialog(QtWidgets.QDialog):
    """
    This class implements main window appearance and behaviour
    """
    __class_names = ['Aircraft Carrier', 'Bulkers', 'Car Carrier', 'Container Ship', 'Cruise', 'DDG', 'Recreational', 'Sailboat', 'Submarine', 'Tug']

    # <editor-fold desc="Constructor, Destructor, redefined methods">
    def __init__(self, parent = None, app_: QApplication = None):
        
        super().__init__(parent)
        self.__app: QApplication = app_
        uic.loadUi(os_path.dirname(__file__) + '/ui/main.ui', self)
        self.pbBrows.clicked.connect(self.__load_picture)
        self.bpClassify.clicked.connect(self.__classify)
        self._model = tf.keras.models.load_model(os_path.dirname(__file__) + "\model\ship_vision_effisientnet_b0.h5")
        self.previousPath = "C:/"
        self.__last_file: str = None

    def __load_picture(self):
        title = "Open picture"
        file_type = "Picture Files "
        extension = ".jpeg"
        file_name = self.__open_standard_save_open_dialogue(title, file_type, extension, True)

        if not os.path.isfile(file_name):
            return
        
        self.__last_file = file_name
        try:
            with open(file_name, 'rb') as pic:
                pixmap_image = self.__pixmap_from_binary_string(base64.b64encode(pic.read()))
                self.lblImage.setPixmap(pixmap_image)
        except Exception as err:
            print(f"Error occur: {err}")
            
    
    def __classify(self):
        if not os.path.isfile(self.__last_file):
            return
        img = self.__load_and_prepare_image(self.__last_file)
        pred_prob = self._model.predict(tf.expand_dims(img, axis=0))
        pred_class = self.__class_names[pred_prob.argmax()]
        self.lblClass.setText(pred_class)


    def __open_standard_save_open_dialogue(self, title, file_type, extension, is_open=True):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        default_path = self.previousPath
        if not os.path.isdir(default_path):
            default_path = 'C:\\'

        if is_open:
            file_name, val = QFileDialog.getOpenFileName(self, title, default_path,
                                                         file_type + '(*' + extension + ')', options=options)
        else:
            file_name, val = QFileDialog.getSaveFileName(self, title, default_path,
                                                         file_type + '(*' + extension + ')', options=options)
        if len(file_name) > 1:  # if file has been pointed
            if not file_name.endswith(extension):  # check if extension has not been included
                file_name = file_name + extension
            print(file_name)
        return file_name
    
    def __pixmap_from_binary_string(self, image: str) -> QPixmap:
        img_byte_data = base64.b64decode(image)
        image_data = BytesIO(img_byte_data)
        image = Image.open(image_data)
        qImage = ImageQt.ImageQt(image)
        pixmap_image = QtGui.QPixmap.fromImage(qImage)
        return pixmap_image
    
    # create a function to load nad prepare image
    def __load_and_prepare_image(self, filename, image_size=224, scale=True):
        # read image
        img = tf.io.read_file(filename)
        # Decode image into tensor
        img = tf.io.decode_image(img, channels=3)
        # Resize the image
        img = tf.image.resize(img, [image_size, image_size])
        #  Scale Yes/No?
        if scale:
            return img/255.
        else:
            return img
