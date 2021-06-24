#coding=utf-8
#@Time:2021/4/23 15:06
#@Author:csdn@hijacklei
#@File:videocatch.py
#@Software:PyCharm
from PyQt5.QtGui import QPixmap,QPainter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from PyQt5.QtWidgets import *
import cv2
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageusetool_rc
class VideoCatch(QMainWindow):
    def __init__(self):
        super(VideoCatch, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("视频数据采集")
        self.resize(500,550)
        self.setWindowIcon(QIcon(r":/11.ico"))
        _translate = QtCore.QCoreApplication.translate

        self.videoshow=QLabel("Video Show",self)
        self.videoshow.setAlignment(Qt.AlignCenter)
        self.videoshow.move(50,30)
        self.videoshow.resize(400,400)
        self.videoshow.setStyleSheet("QLabel{background:gray;}"
                                 "QLabel{color:rgb(0,0,0,120);font-size:30px;font-weight:bold;font-family:宋体;}"
                                 )

        self.selectlujing = QPushButton("点击选择保存路径",self)
        self.selectlujing.move(50, 450)
        self.selectlujing.resize(140,30)
        self.selectlujing.clicked.connect(self.select)


        self.savelujing=QLineEdit(self)
        self.savelujing.move(200,450)
        self.savelujing.resize(250, 30)
        self.savelujing.setPlaceholderText(_translate("MainWindow", "保存地址路径"))


        self.zhenlv=QLineEdit(self)
        self.zhenlv.resize(140,30)
        self.zhenlv.move(50,490)
        self.zhenlv.setPlaceholderText(_translate("MainWindow", "输入帧率，例如：10"))


        self.begincatch = QPushButton("开始采集", self)
        self.begincatch.move(200, 490)
        self.begincatch.resize(125, 30)
        self.begincatch.clicked.connect(self.begin)

        self.stopcatch = QPushButton("点击退出", self)
        self.stopcatch.move(325, 490)
        self.stopcatch.resize(125, 30)
        self.stopcatch.clicked.connect(self.stop)

    def select(self):
        text1 = QFileDialog.getExistingDirectory(self,
                                                 "保存文件",
                                                 "")
        self.savelujing.setText(text1)

    def begin(self):
        cap = cv2.VideoCapture(0)
        i = 0
        def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
            if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
                img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            # 创建一个可以在给定图像上绘图的对象
            draw = ImageDraw.Draw(img)
            # 字体的格式
            fontStyle = ImageFont.truetype(
                "simsun.ttc", textSize, encoding="utf-8")
            # 绘制文本
            draw.text(position, text, textColor, font=fontStyle)
            # 转换回OpenCV格式
            return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

        while (1):
            ret, frame = cap.read()
            # 展示图片
            frame = cv2AddChineseText(frame, '正在抓取第' + str(i) + "张图片", (360, 20), (0, 255, 0), 30)
            show = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                     QtGui.QImage.Format_RGB888)
            self.videoshow.setScaledContents(True)
            self.videoshow.setPixmap(QtGui.QPixmap.fromImage(showImage))
            # 保存图片
            cv2.imwrite(str(self.savelujing.text())+"\\" + str(i) + ".jpg", frame)
            i = i + 1
            if cv2.waitKey(int(self.zhenlv.text())) & 0xFF == ord('q'):
                break
        # 释放对象和销毁窗口
        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        try:
            os._exit(5)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    main=VideoCatch()
    main.show()
    sys.exit(app.exec_())