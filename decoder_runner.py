import numpy as np
from steganogan import SteganoGAN
from steganogan.loader import DataLoader
from steganogan.encoders import BasicEncoder, DenseEncoder
from steganogan.decoders import BasicDecoder, DenseDecoder
from steganogan.critics import BasicCritic

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

import numpy
import math
import cv2
from skimage import measure


class Ui_SteganoGAN(object):
    Picture_Address = ''
    Save_Address = ''

    def setupUi(self, SteganoGAN):
        SteganoGAN.setObjectName("SteganoGAN")
        SteganoGAN.resize(1114, 700)
        SteganoGAN.setMinimumSize(1114,700)
        SteganoGAN.setMaximumSize(1114,700)
        #GAN.setSizeGripEnabled(False)

        self.picture_address = QtWidgets.QPushButton(SteganoGAN)
        self.picture_address.setGeometry(QtCore.QRect(432, 20, 250, 50))
        self.picture_address.setObjectName("picture_address")

        self.picture_text = QtWidgets.QPushButton(SteganoGAN)
        self.picture_text.setGeometry(QtCore.QRect(397, 80, 320, 30))
        self.picture_text.setText("")
        self.picture_text.setObjectName("picture_text")

        self.output = QtWidgets.QLabel(SteganoGAN)
        self.output.setGeometry(QtCore.QRect(257, 120, 600, 400))
        self.output.setText("")
        self.output.setObjectName("output")

        self.information_output_label = QtWidgets.QLabel(SteganoGAN)
        self.information_output_label.setGeometry(QtCore.QRect(100, 540, 200, 50))
        self.information_output_label.setText("解密信息: ")
        self.information_output_label.setObjectName("information_output_label")

        self.information_output_text = QtWidgets.QLineEdit(SteganoGAN)
        self.information_output_text.setGeometry(QtCore.QRect(207, 540, 700, 50))
        self.information_output_text.setText("")
        self.information_output_text.setObjectName("information_output_text")

        self.create = QtWidgets.QPushButton(SteganoGAN)
        self.create.setGeometry(QtCore.QRect(460, 600, 190, 60))
        self.create.setObjectName("create")

        self.retranslateUi(SteganoGAN)
        QtCore.QMetaObject.connectSlotsByName(SteganoGAN)

    def retranslateUi(self, SteganoGAN):
        _translate = QtCore.QCoreApplication.translate
        SteganoGAN.setWindowTitle(_translate("SteganoGAN", "Steg图像-图片文字解密"))
        self.create.setText(_translate("SteganoGAN", "解密图像"))
        self.picture_address.setText(_translate("SteganoGAN", "待解密图像地址"))


    def get_picture(self):
        picture_address = QtWidgets.QFileDialog.getOpenFileName(None, "选取图片地址", 'd:/')
        picture_address = picture_address[0]
        self.Picture_Address=picture_address
        temp=picture_address.split('/')
        temp=temp[-1]
        self.picture_text.setText(temp)

        picture = QPixmap(self.Picture_Address)
        # wsize = picture.width()
        # hsize = picture.height()
        # picture = picture.scaled(wsize * 2, hsize * 2)
        output_w = self.output.width()
        output_h = self.output.height()
        picture = picture.scaled(output_w, output_h)

        self.output.setAlignment(Qt.AlignVCenter)
        self.output.setPixmap(picture)


    def get_output(self):
        ok=True
        if self.Picture_Address=='':
            ok=False
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '没有待解密图像地址!')
            msg_box.exec_()

        if ok:
            steganogan = SteganoGAN.load(architecture=None, path='steg/final.steg', cuda=True, verbose=True)
            # 输出解码后信息
            self.information_output_text.setText(steganogan.decode(self.Picture_Address))
            msg_box = QMessageBox(QMessageBox.Information, '成功!', '已输出解密结果!')
            msg_box.exec_()
