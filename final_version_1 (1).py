# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'version1.3.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import SimpleITK as sitk
from myshow import myshow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider
import itk
import vtk
import Masks
import math
from PIL import Image
import numpy as np
import data_transforms
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from ipywidgets import interact, interactive
import predict

class Ui_uygulamaPrototip(QWidget):
    def __init__(self):
        super(Ui_uygulamaPrototip, self).__init__()
        self.fileName = 'xyz'
    def render(self,vtk_img):
        colors = vtk.vtkNamedColors()
        
        colors.SetColor("BkgColor", [0, 0, 0, 0])
        #51, 77, 102, 255
        
        
        # Create the renderer, the render window, and the interactor. The renderer
        # draws into the render window, the interactor enables mouse- and
        # keyboard-based interaction with the scene.
        ren = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)
        
        # The following reader is used to read a series of 2D slices (images)
        # that compose the volume. The slice dimensions are set, and the
        # pixel spacing. The data Endianness must also be specified. The reader
        # uses the FilePrefix in combination with the slice number to construct
        # filenames using the format FilePrefix.%d. (In this case the FilePrefix
        # is the root name of the file: quarter.)
        
        # The volume will be displayed by ray-cast alpha compositing.
        # A ray-cast mapper is needed to do the ray-casting.
        volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
        volumeMapper.SetInputData(vtk_img)
        
        # The color transfer function maps voxel intensities to colors.
        # It is modality-specific, and often anatomy-specific as well.
        # The goal is to one color for flesh (between 500 and 1000)
        # and another color for bone (1150 and over).
        volumeColor = vtk.vtkColorTransferFunction()
        volumeColor.AddRGBPoint(0, 127.0, 0.0, 0.0) #akciğer
        volumeColor.AddRGBPoint(500, 20.0, 20.5, 20.3) #bronşlar
        volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
        volumeColor.AddRGBPoint(1150, 1.0, 0.0, 0.9)
        
        # The opacity transfer function is used to control the opacity
        # of different tissue types.
        volumeScalarOpacity = vtk.vtkPiecewiseFunction()
        volumeScalarOpacity.AddPoint(0, 0.05)
        volumeScalarOpacity.AddPoint(500, 1.0)
        volumeScalarOpacity.AddPoint(1000, 1.0)
        volumeScalarOpacity.AddPoint(1150, 1.0)
        
        # The gradient opacity function is used to decrease the opacity
        # in the "flat" regions of the volume while maintaining the opacity
        # at the boundaries between tissue types.  The gradient is measured
        # as the amount by which the intensity changes over unit distance.
        # For most medical data, the unit distance is 1mm.
        volumeGradientOpacity = vtk.vtkPiecewiseFunction()
        volumeGradientOpacity.AddPoint(0, 0.0)
        volumeGradientOpacity.AddPoint(90, 0.5)
        volumeGradientOpacity.AddPoint(100, 1.0)
        
        # The VolumeProperty attaches the color and opacity functions to the
        # volume, and sets other volume properties.  The interpolation should
        # be set to linear to do a high-quality rendering.  The ShadeOn option
        # turns on directional lighting, which will usually enhance the
        # appearance of the volume and make it look more "3D".  However,
        # the quality of the shading depends on how accurately the gradient
        # of the volume can be calculated, and for noisy data the gradient
        # estimation will be very poor.  The impact of the shading can be
        # decreased by increasing the Ambient coefficient while decreasing
        # the Diffuse and Specular coefficient.  To increase the impact
        # of shading, decrease the Ambient and increase the Diffuse and Specular.
        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(volumeColor)
        volumeProperty.SetScalarOpacity(volumeScalarOpacity)
        volumeProperty.SetGradientOpacity(volumeGradientOpacity)
        volumeProperty.SetInterpolationTypeToLinear()
        volumeProperty.ShadeOn()
        volumeProperty.SetAmbient(0.2)
        volumeProperty.SetDiffuse(1.0)
        volumeProperty.SetSpecular(1.0)
        
        # The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
        # and orientation of the volume in world coordinates.
        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volumeProperty)
        
        # Finally, add the volume to the renderer
        ren.AddViewProp(volume)
        
        # Set up an initial view of the volume.  The focal point will be the
        # center of the volume, and the camera position will be 400mm to the
        # patient's left (which is our right).
        camera = ren.GetActiveCamera()
        c = volume.GetCenter()
        camera.SetViewUp(0, 0, -1)
        camera.SetPosition(c[0], c[1] - 400, c[2])
        camera.SetFocalPoint(c[0], c[1], c[2])
        camera.Azimuth(30.0)
        camera.Elevation(30.0)
        
        # Set a background color for the renderer
        ren.SetBackground(colors.GetColor3d("BkgColor"))
        
        # Increase the size of the render window
        renWin.SetSize(640, 480)
        
        # Interact with the data.
        iren.Start()
        
    def sliderChanged(self):
        value=self.horizontalSlider.value()
        image_interact = QtGui.QImage(self.image_np[value], self.image_np[value].shape[1],self.image_np[value].shape[0], self.image_np[value].shape[1] ,QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap(image_interact)
        scene = QtWidgets.QGraphicsScene(self) 
        scene.addPixmap(pix)
        self.dicomViewer.setScene(scene)
        self.dicomViewer.show()
        self.lblSliceValue.setText(str(value))
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Dosya Yükle", "","Nrrd Files (*.nrrd)", options=options)
        self.fileName = fileName
        scene = QtWidgets.QGraphicsScene(self) 
        image = sitk.ReadImage(self.fileName)
        image = Masks.reScaleas255(image)
        image_np = sitk.GetArrayFromImage(image)
        self.image_np=image_np
        midPoint=math.floor((len(self.image_np)-1)/2)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(len(self.image_np)-1)
        self.horizontalSlider.setValue(midPoint)
        self.lblSliceValue.setText(str(midPoint))

        image_interact = QtGui.QImage(self.image_np[midPoint], self.image_np[midPoint].shape[1],self.image_np[midPoint].shape[0], self.image_np[midPoint].shape[1] ,QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap(image_interact)
        scene.addPixmap(pix)
        self.dicomViewer.setScene(scene)
        self.dicomViewer.show()
        self.horizontalSlider.valueChanged.connect(self.sliderChanged)
        
    def buttonClicked(self):
        temp=self.fileName
        image = sitk.ReadImage(self.fileName)
        sitk_masks = predict.predict_nrrd(image)
        sitk_masks = Masks.reScaleas255(sitk_masks)
        mask_np = sitk.GetArrayFromImage(sitk_masks)
        self.mask_np=mask_np
        self.masked_image=self.mask_np*self.image_np
        sitk_masked_image = sitk.GetImageFromArray(self.masked_image)
        image_dimension=3
        index=[15]*image_dimension
        itk_image = data_transforms.sitk_to_itk(sitk_masked_image, image_dimension, index)

        # Rendering
        vtk_img = data_transforms.vtk_image_from_image(itk_image)
        self.render(vtk_img)
    
    
    def setupUi(self, uygulamaPrototip):
        uygulamaPrototip.setObjectName("uygulamaPrototip")
        uygulamaPrototip.resize(955, 856)
        uygulamaPrototip.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(uygulamaPrototip)
        self.centralwidget.setObjectName("centralwidget")
        self.dicomViewer = QtWidgets.QGraphicsView(self.centralwidget)
        self.dicomViewer.setGeometry(QtCore.QRect(210, 15, 550, 550))
        self.dicomViewer.setMaximumSize(QtCore.QSize(550, 550))
        self.dicomViewer.setObjectName("dicomViewer")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 690, 251, 111))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(340, 710, 581, 91))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 650, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(340, 680, 581, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(70, 650, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(290, 570, 381, 31))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(340, 610, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lblSliceValue = QtWidgets.QLabel(self.centralwidget)
        self.lblSliceValue.setGeometry(QtCore.QRect(400, 610, 55, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.lblSliceValue.setFont(font)
        self.lblSliceValue.setObjectName("lblSliceValue")
        uygulamaPrototip.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(uygulamaPrototip)
        self.statusbar.setObjectName("statusbar")
        uygulamaPrototip.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(uygulamaPrototip)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 955, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuDosya = QtWidgets.QMenu(self.menuBar)
        self.menuDosya.setObjectName("menuDosya")
        self.menu_lemler = QtWidgets.QMenu(self.menuBar)
        self.menu_lemler.setObjectName("menu_lemler")
        uygulamaPrototip.setMenuBar(self.menuBar)
        self.actionYeni = QtWidgets.QAction(uygulamaPrototip)
        self.actionYeni.setObjectName("actionYeni")
        self.actionDosya_A = QtWidgets.QAction(uygulamaPrototip)
        self.actionDosya_A.setObjectName("actionDosya_A")
        self.actionKaydet = QtWidgets.QAction(uygulamaPrototip)
        self.actionKaydet.setObjectName("actionKaydet")
        self.action_k = QtWidgets.QAction(uygulamaPrototip)
        self.action_k.setObjectName("action_k")
        self.action3_Boyutlu_G_r_nt_le = QtWidgets.QAction(uygulamaPrototip)
        self.action3_Boyutlu_G_r_nt_le.setObjectName("action3_Boyutlu_G_r_nt_le")
        self.actionAday_Nod_l_Tespiti_A_Kapa = QtWidgets.QAction(uygulamaPrototip)
        self.actionAday_Nod_l_Tespiti_A_Kapa.setObjectName("actionAday_Nod_l_Tespiti_A_Kapa")
        self.actionYard_m = QtWidgets.QAction(uygulamaPrototip)
        self.actionYard_m.setObjectName("actionYard_m")
        self.menuDosya.addSeparator()
        self.menuDosya.addAction(self.actionDosya_A)
        self.menuDosya.addSeparator()
        self.menuDosya.addAction(self.action_k)
        self.menu_lemler.addAction(self.action3_Boyutlu_G_r_nt_le)
        self.menu_lemler.addAction(self.actionAday_Nod_l_Tespiti_A_Kapa)
        self.menu_lemler.addSeparator()
        self.menu_lemler.addAction(self.actionYard_m)
        self.menuBar.addAction(self.menuDosya.menuAction())
        self.menuBar.addAction(self.menu_lemler.menuAction())
        self.actionDosya_A.triggered.connect(self.openFileNameDialog)
        self.pushButton.clicked.connect(self.buttonClicked)
        
        self.retranslateUi(uygulamaPrototip)
        self.pushButton.clicked.connect(self.dicomViewer.close)
        QtCore.QMetaObject.connectSlotsByName(uygulamaPrototip)
        uygulamaPrototip.setTabOrder(self.dicomViewer, self.checkBox)
        uygulamaPrototip.setTabOrder(self.checkBox, self.pushButton)
        uygulamaPrototip.setTabOrder(self.pushButton, self.textEdit)

    def retranslateUi(self, uygulamaPrototip):
        _translate = QtCore.QCoreApplication.translate
        uygulamaPrototip.setWindowTitle(_translate("uygulamaPrototip", "Uygulama Prototipi"))
        self.pushButton.setText(_translate("uygulamaPrototip", "3 BOYUTLU GÖRÜNTÜLE"))
        self.label.setText(_translate("uygulamaPrototip", "Programın güncel durumu"))
        self.checkBox.setText(_translate("uygulamaPrototip", "Aday Nodül Tespiti"))
        self.label_2.setText(_translate("uygulamaPrototip", "Kesit :"))
        self.lblSliceValue.setText(_translate("uygulamaPrototip", "0"))
        self.menuDosya.setTitle(_translate("uygulamaPrototip", "Dosya"))
        self.menu_lemler.setTitle(_translate("uygulamaPrototip", "İşlemler"))
        self.actionYeni.setText(_translate("uygulamaPrototip", "Yeni"))
        self.actionDosya_A.setText(_translate("uygulamaPrototip", "Dosya Aç"))
        self.actionKaydet.setText(_translate("uygulamaPrototip", "Kaydet"))
        self.action_k.setText(_translate("uygulamaPrototip", "Çıkış"))
        self.action3_Boyutlu_G_r_nt_le.setText(_translate("uygulamaPrototip", "3 Boyutlu Görüntüle"))
        self.actionAday_Nod_l_Tespiti_A_Kapa.setText(_translate("uygulamaPrototip", "Aday Nodül Tespiti Aç/Kapa"))
        self.actionYard_m.setText(_translate("uygulamaPrototip", "Yardım"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    uygulamaPrototip = QtWidgets.QMainWindow()
    ui = Ui_uygulamaPrototip()
    ui.setupUi(uygulamaPrototip)
    uygulamaPrototip.show()
    sys.exit(app.exec_())

