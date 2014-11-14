#!/usr/bin/python 

# script by Jordi Binefa | http://binefa.com/blog/2013/10/webcam-viewer-using-python-pyqt-pygame/
import sys
import pygame.image
import pygame.camera
from PyQt4 import Qt, QtCore, QtGui
from time import sleep

def funcioTemporitzada():
	global webcamImage,cam
	img = cam.get_image()
	pygame.image.save(img, "photo.jpg")	
	webcamPixmap = QtGui.QPixmap('photo.jpg')
	webcamImage.setPixmap(webcamPixmap)

pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
cam.start()

a = Qt.QApplication(sys.argv)
webcamImage = Qt.QLabel()
funcioTemporitzada()
widget = Qt.QWidget()
verticalBox = Qt.QVBoxLayout()
verticalBox.addWidget(webcamImage)
widget.setLayout(verticalBox)
widget.show()
temporitzador = QtCore.QTimer()
a.connect(temporitzador, Qt.SIGNAL("timeout()"), funcioTemporitzada)
temporitzador.start(250)
a.exec_()

pygame.camera.quit()
