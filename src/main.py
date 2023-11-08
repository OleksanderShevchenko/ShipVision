import base64
import sys
from io import BytesIO
from PIL import Image, ImageQt
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from main_dialog import MainDialog


_app = QtWidgets.QApplication(sys.argv)   
QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
window = MainDialog(app_=_app)
window.show()
sys.exit(_app.exec_())
