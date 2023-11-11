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

from ui.main_ui import Ui_Dialog


class MainDialog(QtWidgets.QDialog, Ui_Dialog):
    """
    This class implements main window appearance and behaviour
    """
    __class_names = ['Aircraft Carrier',
                    'Bulkers',
                    'Car Carrier',
                    'Container Ship',
                    'Cruise',
                    'DDG',
                    'Recreational',
                    'Sailboat',
                    'Submarine',
                    'Tug']
    # <editor-fold desc="Constructor, Destructor, redefined methods">
    def __init__(self, parent = None, app_: QApplication = None):
        
        super().__init__(parent)
        self.__app: QApplication = app_
        self.setupUi(self)
        # uic.loadUi(os_path.dirname(__file__) + '/ui/main.ui', self)
        self.pbBrows.clicked.connect(self.__load_picture)
        self.cbModel.currentIndexChanged.connect(self.__select_model)
        self.bpClassify.clicked.connect(self.__classify)
        self.bpClassify.setEnabled(False)
        self._model_path = os.path.join(os_path.dirname(__file__), "model")
        self._model: tf.keras.Model = None
        self.previousPath = "C:/"
        self.__last_file: str = None
        self.__populate_model_files()

    def __populate_model_files(self) -> None:
        items = []
        for _, _, file_name in os.walk(self._model_path):
            items = file_name
        if len(items) > 0:
            self.cbModel.addItems(items)
            self.cbModel.setCurrentIndex(-1)

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
                data = pic.read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.lblImage.setPixmap(pixmap)
                self.lblClass.setText("Unknown")
        except Exception as err:
            print(f"Error occur: {err}")

    def __select_model(self, idx: int) -> None:
        if idx < 0:
            return
        model_name = self.cbModel.currentText()        
        file_name = os.path.join(self._model_path, model_name)

        if not os.path.isfile(file_name):
            self._model = None
            self.showDialog(f"Model file with name {file_name} could not be found!", "Initialize model")
            self.bpClassify.setEnabled(False)
            self.lblClass.setText("Unknown")
            return
        self.lblClass.setText("Loading model ... Please wait.")
        self.repaint()
        self.__app.processEvents()
        self._model = tf.keras.models.load_model(file_name)
        self.bpClassify.setEnabled(True)
        self.lblClass.setText("Unknown")
    
    def __classify(self):
        if not os.path.isfile(self.__last_file) or self._model is None:
            return
        self.lblClass.setText("-----")
        self.repaint()
        self.__app.processEvents()
        img = self.__load_and_prepare_image(self.__last_file, scale=False)
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
        self.previousPath = os.path.dirname(file_name)
        return file_name
    
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
        
    def showDialog(self, msg: str, title: str):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
