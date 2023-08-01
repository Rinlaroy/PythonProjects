# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QFileDialog
import os
from keras.models import load_model
from PIL import Image
from keras.preprocessing import image
import numpy as np
import keras
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 700)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(180, 20, 571, 41))
        self.label.setStyleSheet("font: 75 14pt \"Times New Roman\";\n"
"color: rgb(170, 0, 0);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(290, 80, 511, 351))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(230, 580, 100, 21))
        self.label_3.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(320, 580, 251, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(340, 480, 211, 43))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "METAL SURFACE DEFECT DETECTION"))
        self.label_3.setText(_translate("Dialog", "RESULT :"))
        self.pushButton.setText(_translate("Dialog", "UPLOAD IMAGE"))
        self.pushButton.clicked.connect(self.upload)

    def upload(self):
        filename = QFileDialog.getOpenFileName(None, "BROWSE FILE", "", "images (*.*)")
        path = filename[0]
        target_size = (224,224)
        model=load_model('surface.h5')
        print("model loaded")
        pngfile = QPixmap(filename[0])
        pixmap2 = pngfile.scaledToWidth(550)
        pixmap3 = pngfile.scaledToHeight(290)
        self.label_2.setPixmap(pixmap3)
        test_image = image.load_img(path, target_size = (224,224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        test_image = test_image/255
        result = model.predict(test_image)
        print(np.exp(result))
        print(np.argmax(result))
        res = np.argmax(result)
        if res==0:
            self.lineEdit.setText('CRAZING')
        elif res==1:
            self.lineEdit.setText('No defect')
        elif res==2:
            self.lineEdit.setText('PATCHES')
        elif res==3:
            self.lineEdit.setText('PITTED')
        elif res==4:
            self.lineEdit.setText('ROLLED')
        elif res==5:
            self.lineEdit.setText('SCRATCHES')
     


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
