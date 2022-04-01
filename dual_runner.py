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


def psnr(img1, img2):  # 这里输入的是（0,255）的灰度或彩色图像，如果是彩色图像，则numpy.mean相当于对三个通道计算的结果再求均值
    MSE = numpy.mean((img1 / 255. - img2 / 255.) ** 2)

    if MSE < 1.0e-10:  # 如果两图片差距过小代表完美重合
        return 100
    PIXEL_MAX = 255
    return 20 * math.log10(PIXEL_MAX / math.sqrt(MSE))  # 将对数中pixel_max的平方放了下来

def ssim(img1, img2):
    return measure.compare_ssim(img1, img2, multichannel=True)


class Ui_SteganoGAN(object):
    Picture_Address = ''
    Save_Address = ''

    def setupUi(self, SteganoGAN):
        SteganoGAN.setObjectName("SteganoGAN")
        SteganoGAN.resize(1114, 637)
        SteganoGAN.setMinimumSize(1114,800)
        SteganoGAN.setMaximumSize(1114,800)
        #GAN.setSizeGripEnabled(False)


        self.picture_address = QtWidgets.QPushButton(SteganoGAN)
        self.picture_address.setGeometry(QtCore.QRect(183.5, 20, 190, 50))
        self.picture_address.setObjectName("picture_address")

        self.save_address = QtWidgets.QPushButton(SteganoGAN)
        self.save_address.setGeometry(QtCore.QRect(740.5, 20, 190, 50))
        self.save_address.setObjectName("save_address")

        self.picture_text = QtWidgets.QPushButton(SteganoGAN)
        self.picture_text.setGeometry(QtCore.QRect(118.5, 110, 320, 30))
        self.picture_text.setText("")
        self.picture_text.setObjectName("picture_text")

        self.save_text = QtWidgets.QPushButton(SteganoGAN)
        self.save_text.setGeometry(QtCore.QRect(675.5, 110, 320, 30))
        self.save_text.setText("")
        self.save_text.setObjectName("save_text")

        self.information_input_label = QtWidgets.QLabel(SteganoGAN)
        self.information_input_label.setGeometry(QtCore.QRect(114, 180,200, 50))
        self.information_input_label.setText("待隐藏信息: ")
        self.information_input_label.setObjectName("information_input_label")

        self.information_input_text = QtWidgets.QLineEdit(SteganoGAN)
        self.information_input_text.setGeometry(QtCore.QRect(264, 180, 700, 50))
        self.information_input_text.setText("")
        self.information_input_text.setObjectName("information_input_text")

        self.output = QtWidgets.QLabel(SteganoGAN)
        self.output.setGeometry(QtCore.QRect(594, 250, 500, 303))
        self.output.setText("")
        self.output.setObjectName("output")

        self.input = QtWidgets.QLabel(SteganoGAN)
        self.input.setGeometry(QtCore.QRect(19, 250, 500, 303))
        self.input.setText("")
        self.input.setObjectName("input")

        self.PSNR_text = QtWidgets.QLabel(SteganoGAN)
        self.PSNR_text.setGeometry(QtCore.QRect(178.5, 570, 200, 60))
        self.PSNR_text.setText("")
        self.PSNR_text.setObjectName("PSNR_text")

        self.SSIM_text = QtWidgets.QLabel(SteganoGAN)
        self.SSIM_text.setGeometry(QtCore.QRect(735.5, 570, 200, 60))
        self.SSIM_text.setText("")
        self.SSIM_text.setObjectName("SSIM_text")

        self.information_output_label = QtWidgets.QLabel(SteganoGAN)
        self.information_output_label.setGeometry(QtCore.QRect(114, 640, 200, 50))
        self.information_output_label.setText("解码信息: ")
        self.information_output_label.setObjectName("information_output_label")

        self.information_output_text = QtWidgets.QLineEdit(SteganoGAN)
        self.information_output_text.setGeometry(QtCore.QRect(264, 640, 700, 50))
        self.information_output_text.setText("")
        self.information_output_text.setObjectName("information_output_text")

        self.create = QtWidgets.QPushButton(SteganoGAN)
        self.create.setGeometry(QtCore.QRect(460, 720, 190, 60))
        self.create.setObjectName("create")

        self.retranslateUi(SteganoGAN)
        QtCore.QMetaObject.connectSlotsByName(SteganoGAN)

    def retranslateUi(self, SteganoGAN):
        _translate = QtCore.QCoreApplication.translate
        SteganoGAN.setWindowTitle(_translate("GAN", "SteganoGAN-图像编码和解码"))
        self.create.setText(_translate("GAN", "生成结果"))
        self.picture_address.setText(_translate("GAN", "原图地址"))
        self.save_address.setText(_translate("GAN", "保存地址"))

    def get_picture(self):
        picture_address = QtWidgets.QFileDialog.getOpenFileName(None, "选取图片地址", 'd:/')
        picture_address = picture_address[0]
        # global Picture_Address
        # Picture_Address = picture_address
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

        self.input.setAlignment(Qt.AlignVCenter)
        self.input.setPixmap(picture)


    def get_save(self):
        save_address = QtWidgets.QFileDialog.getExistingDirectory(None, "选取生成图片保存地址", 'd:/')
        self.Save_Address=save_address
        self.save_text.setText(save_address)


    def get_output(self):
        ok=True
        if self.Picture_Address=='':
            ok=False
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '没有选择原图地址!')
            msg_box.exec_()
        elif self.Save_Address=='':
            ok=False
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '没有选择结果保存地址!')
            msg_box.exec_()
        elif self.information_input_text.text()=="":
            ok = False
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '没有输入待隐藏信息!')
            msg_box.exec_()

        if ok:
            steganogan = SteganoGAN.load(architecture=None, path='steg/final.steg', cuda=True, verbose=True)
            steganogan.encode(self.Picture_Address, self.Save_Address+'/output.png', self.information_input_text.text())
            # print(steganogan.decode('output.png'))
            # main(self.Picture_Address, self.Mask_Address, self.Save_Address)
            if os.path.exists(self.Save_Address + '/output.png'):
                picture = QPixmap(self.Save_Address + '/output.png')
                # wsize = picture.width()
                # hsize = picture.height()
                # picture = picture.scaled(wsize * 2, hsize * 2)
                output_w=self.output.width()
                output_h=self.output.height()
                picture = picture.scaled(output_w, output_h)

                self.output.setAlignment(Qt.AlignVCenter)
                self.output.setPixmap(picture)

                img1 = cv2.imread(self.Picture_Address)
                img2 = cv2.imread(self.Save_Address+'/output.png')
                self.SSIM_text.setText("SSIM: "+str(ssim(img1,img2)))
                self.PSNR_text.setText("PSNR: "+str(psnr(img1, img2)))

                # #输出解码后信息
                # self.information_output_text.setText(steganogan.decode(self.Save_Address + '/output.png'))


                msg_box = QMessageBox(QMessageBox.Information, '成功!', '已生成结果!')
                msg_box.exec_()



                # self.setScaledContents (True)
            else:
                msg_box = QMessageBox(QMessageBox.Warning, '失败', '结果生成失败!')
                msg_box.exec_()
