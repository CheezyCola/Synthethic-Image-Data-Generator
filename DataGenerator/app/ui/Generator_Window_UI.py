# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Generator_Window_UI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1084, 1335)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 1095, 1271))
        self.main_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.WindowTitle = QLabel(self.verticalLayoutWidget)
        self.WindowTitle.setObjectName(u"WindowTitle")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.WindowTitle.setFont(font)
        self.WindowTitle.setMargin(3)
        self.WindowTitle.setIndent(3)

        self.main_layout.addWidget(self.WindowTitle)

        self.gBox_IO = QGroupBox(self.verticalLayoutWidget)
        self.gBox_IO.setObjectName(u"gBox_IO")
        font1 = QFont()
        font1.setPointSize(11)
        self.gBox_IO.setFont(font1)
        self.gridLayoutWidget_3 = QWidget(self.gBox_IO)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 951, 148))
        self.gridLayout_IO = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_IO.setObjectName(u"gridLayout_IO")
        self.gridLayout_IO.setContentsMargins(25, 5, 0, 10)
        self.lbl_gnd_dir = QLabel(self.gridLayoutWidget_3)
        self.lbl_gnd_dir.setObjectName(u"lbl_gnd_dir")
        font2 = QFont()
        font2.setPointSize(9)
        self.lbl_gnd_dir.setFont(font2)

        self.gridLayout_IO.addWidget(self.lbl_gnd_dir, 1, 0, 1, 1)

        self.line_output_dir = QLineEdit(self.gridLayoutWidget_3)
        self.line_output_dir.setObjectName(u"line_output_dir")
        self.line_output_dir.setFont(font2)

        self.gridLayout_IO.addWidget(self.line_output_dir, 3, 1, 1, 1)

        self.line_config_file = QLineEdit(self.gridLayoutWidget_3)
        self.line_config_file.setObjectName(u"line_config_file")
        self.line_config_file.setFont(font2)

        self.gridLayout_IO.addWidget(self.line_config_file, 2, 1, 1, 1)

        self.lbl_isNewFolder = QLabel(self.gridLayoutWidget_3)
        self.lbl_isNewFolder.setObjectName(u"lbl_isNewFolder")
        self.lbl_isNewFolder.setFont(font2)
        self.lbl_isNewFolder.setStyleSheet(u"color:rgb(0, 0, 255)")

        self.gridLayout_IO.addWidget(self.lbl_isNewFolder, 3, 3, 1, 1)

        self.line_obj_dir = QLineEdit(self.gridLayoutWidget_3)
        self.line_obj_dir.setObjectName(u"line_obj_dir")
        self.line_obj_dir.setFont(font2)

        self.gridLayout_IO.addWidget(self.line_obj_dir, 0, 1, 1, 1)

        self.pB_search_output_dir = QPushButton(self.gridLayoutWidget_3)
        self.pB_search_output_dir.setObjectName(u"pB_search_output_dir")
        self.pB_search_output_dir.setFont(font2)

        self.gridLayout_IO.addWidget(self.pB_search_output_dir, 3, 2, 1, 1)

        self.lbl_obj_dir = QLabel(self.gridLayoutWidget_3)
        self.lbl_obj_dir.setObjectName(u"lbl_obj_dir")
        self.lbl_obj_dir.setFont(font2)

        self.gridLayout_IO.addWidget(self.lbl_obj_dir, 0, 0, 1, 1)

        self.lbl_output_dir = QLabel(self.gridLayoutWidget_3)
        self.lbl_output_dir.setObjectName(u"lbl_output_dir")
        self.lbl_output_dir.setFont(font2)

        self.gridLayout_IO.addWidget(self.lbl_output_dir, 3, 0, 1, 1)

        self.pB_search_obj_dir = QPushButton(self.gridLayoutWidget_3)
        self.pB_search_obj_dir.setObjectName(u"pB_search_obj_dir")
        self.pB_search_obj_dir.setFont(font2)

        self.gridLayout_IO.addWidget(self.pB_search_obj_dir, 0, 2, 1, 1)

        self.line_gnd_dir = QLineEdit(self.gridLayoutWidget_3)
        self.line_gnd_dir.setObjectName(u"line_gnd_dir")
        self.line_gnd_dir.setFont(font2)

        self.gridLayout_IO.addWidget(self.line_gnd_dir, 1, 1, 1, 1)

        self.lbl_config_file = QLabel(self.gridLayoutWidget_3)
        self.lbl_config_file.setObjectName(u"lbl_config_file")
        self.lbl_config_file.setFont(font2)

        self.gridLayout_IO.addWidget(self.lbl_config_file, 2, 0, 1, 1)

        self.pB_search_gnd_dir = QPushButton(self.gridLayoutWidget_3)
        self.pB_search_gnd_dir.setObjectName(u"pB_search_gnd_dir")
        self.pB_search_gnd_dir.setFont(font2)

        self.gridLayout_IO.addWidget(self.pB_search_gnd_dir, 1, 2, 1, 1)

        self.pB_search_config_file = QPushButton(self.gridLayoutWidget_3)
        self.pB_search_config_file.setObjectName(u"pB_search_config_file")
        self.pB_search_config_file.setFont(font2)

        self.gridLayout_IO.addWidget(self.pB_search_config_file, 2, 2, 1, 1)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_IO.addItem(self.horizontalSpacer_23, 2, 4, 1, 1)

        self.gridLayout_IO.setColumnStretch(1, 4)
        self.gridLayout_IO.setColumnStretch(4, 3)

        self.main_layout.addWidget(self.gBox_IO)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 5, 0, 5)
        self.lbl_Config = QLabel(self.verticalLayoutWidget)
        self.lbl_Config.setObjectName(u"lbl_Config")
        font3 = QFont()
        font3.setPointSize(11)
        font3.setUnderline(False)
        self.lbl_Config.setFont(font3)
        self.lbl_Config.setWordWrap(False)
        self.lbl_Config.setMargin(3)
        self.lbl_Config.setIndent(5)

        self.verticalLayout.addWidget(self.lbl_Config)

        self.tabWidget = QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setFont(font2)
        self.tab_Setting = QWidget()
        self.tab_Setting.setObjectName(u"tab_Setting")
        self.gridLayoutWidget = QWidget(self.tab_Setting)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 961, 701))
        self.gridLayout_Setting = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_Setting.setObjectName(u"gridLayout_Setting")
        self.gridLayout_Setting.setContentsMargins(0, 5, 0, 20)
        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(True)
        font4.setWeight(75)
        self.label_4.setFont(font4)
        self.label_4.setMargin(2)
        self.label_4.setIndent(10)

        self.gridLayout_Setting.addWidget(self.label_4, 8, 0, 1, 1)

        self.line_gravity = QLineEdit(self.gridLayoutWidget)
        self.line_gravity.setObjectName(u"line_gravity")

        self.gridLayout_Setting.addWidget(self.line_gravity, 3, 2, 1, 1)

        self.label_57 = QLabel(self.gridLayoutWidget)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setFont(font4)
        self.label_57.setMargin(2)
        self.label_57.setIndent(10)

        self.gridLayout_Setting.addWidget(self.label_57, 19, 0, 1, 1)

        self.lbl_unit = QLabel(self.gridLayoutWidget)
        self.lbl_unit.setObjectName(u"lbl_unit")

        self.gridLayout_Setting.addWidget(self.lbl_unit, 2, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_Setting.addItem(self.verticalSpacer_2, 7, 0, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_Setting.addWidget(self.label_6, 3, 1, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font4)
        self.label_5.setMargin(2)
        self.label_5.setIndent(10)

        self.gridLayout_Setting.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_29 = QLabel(self.gridLayoutWidget)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_Setting.addWidget(self.label_29, 11, 1, 1, 1)

        self.label_32 = QLabel(self.gridLayoutWidget)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_Setting.addWidget(self.label_32, 16, 1, 1, 1)

        self.line_3DviewClipEnd = QLineEdit(self.gridLayoutWidget)
        self.line_3DviewClipEnd.setObjectName(u"line_3DviewClipEnd")

        self.gridLayout_Setting.addWidget(self.line_3DviewClipEnd, 6, 2, 1, 1)

        self.sBox_noiseTreshold = QDoubleSpinBox(self.gridLayoutWidget)
        self.sBox_noiseTreshold.setObjectName(u"sBox_noiseTreshold")
        self.sBox_noiseTreshold.setMinimum(0.010000000000000)
        self.sBox_noiseTreshold.setSingleStep(0.010000000000000)

        self.gridLayout_Setting.addWidget(self.sBox_noiseTreshold, 15, 2, 1, 1)

        self.label_27 = QLabel(self.gridLayoutWidget)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_Setting.addWidget(self.label_27, 13, 1, 1, 1)

        self.line_3DviewClipStart = QLineEdit(self.gridLayoutWidget)
        self.line_3DviewClipStart.setObjectName(u"line_3DviewClipStart")

        self.gridLayout_Setting.addWidget(self.line_3DviewClipStart, 5, 2, 1, 1)

        self.comboBox_denoiser = QComboBox(self.gridLayoutWidget)
        self.comboBox_denoiser.addItem("")
        self.comboBox_denoiser.addItem("")
        self.comboBox_denoiser.addItem("")
        self.comboBox_denoiser.setObjectName(u"comboBox_denoiser")

        self.gridLayout_Setting.addWidget(self.comboBox_denoiser, 14, 2, 1, 1)

        self.label_26 = QLabel(self.gridLayoutWidget)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_Setting.addWidget(self.label_26, 6, 1, 1, 1)

        self.cBox_useOnlyCPU = QCheckBox(self.gridLayoutWidget)
        self.cBox_useOnlyCPU.setObjectName(u"cBox_useOnlyCPU")

        self.gridLayout_Setting.addWidget(self.cBox_useOnlyCPU, 16, 2, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_Setting.addItem(self.verticalSpacer_6, 22, 0, 1, 1)

        self.label_58 = QLabel(self.gridLayoutWidget)
        self.label_58.setObjectName(u"label_58")

        self.gridLayout_Setting.addWidget(self.label_58, 20, 1, 1, 1)

        self.line_engine = QLineEdit(self.gridLayoutWidget)
        self.line_engine.setObjectName(u"line_engine")

        self.gridLayout_Setting.addWidget(self.line_engine, 9, 2, 1, 1)

        self.label_31 = QLabel(self.gridLayoutWidget)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_Setting.addWidget(self.label_31, 15, 1, 1, 1)

        self.cBox_ambientOcclusion = QCheckBox(self.gridLayoutWidget)
        self.cBox_ambientOcclusion.setObjectName(u"cBox_ambientOcclusion")

        self.gridLayout_Setting.addWidget(self.cBox_ambientOcclusion, 10, 2, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_Setting.addWidget(self.label_11, 12, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_Setting.addItem(self.verticalSpacer_4, 18, 0, 1, 1)

        self.comboBox_GPUType = QComboBox(self.gridLayoutWidget)
        self.comboBox_GPUType.addItem("")
        self.comboBox_GPUType.addItem("")
        self.comboBox_GPUType.addItem("")
        self.comboBox_GPUType.setObjectName(u"comboBox_GPUType")

        self.gridLayout_Setting.addWidget(self.comboBox_GPUType, 17, 2, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_Setting.addWidget(self.label_10, 10, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_Setting.addItem(self.horizontalSpacer_2, 2, 4, 1, 1)

        self.sBox_CPUCoresNum = QSpinBox(self.gridLayoutWidget)
        self.sBox_CPUCoresNum.setObjectName(u"sBox_CPUCoresNum")
        self.sBox_CPUCoresNum.setMinimum(1)

        self.gridLayout_Setting.addWidget(self.sBox_CPUCoresNum, 12, 2, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_Setting.addWidget(self.label_8, 5, 1, 1, 1)

        self.cBox_backgroundBlack = QCheckBox(self.gridLayoutWidget)
        self.cBox_backgroundBlack.setObjectName(u"cBox_backgroundBlack")

        self.gridLayout_Setting.addWidget(self.cBox_backgroundBlack, 4, 2, 1, 1)

        self.comboBox_unit = QComboBox(self.gridLayoutWidget)
        self.comboBox_unit.addItem("")
        self.comboBox_unit.addItem("")
        self.comboBox_unit.addItem("")
        self.comboBox_unit.setObjectName(u"comboBox_unit")

        self.gridLayout_Setting.addWidget(self.comboBox_unit, 2, 2, 1, 1)

        self.label_33 = QLabel(self.gridLayoutWidget)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_Setting.addWidget(self.label_33, 17, 1, 1, 1)

        self.label_28 = QLabel(self.gridLayoutWidget)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_Setting.addWidget(self.label_28, 9, 1, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_Setting.addWidget(self.label_7, 4, 1, 1, 1)

        self.label_30 = QLabel(self.gridLayoutWidget)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_Setting.addWidget(self.label_30, 14, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(200, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Setting.addItem(self.horizontalSpacer_6, 2, 3, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Setting.addItem(self.horizontalSpacer_12, 1, 2, 1, 1)

        self.label_87 = QLabel(self.gridLayoutWidget)
        self.label_87.setObjectName(u"label_87")

        self.gridLayout_Setting.addWidget(self.label_87, 21, 1, 1, 1)

        self.cBox_saveCocoAnnotatedImage = QCheckBox(self.gridLayoutWidget)
        self.cBox_saveCocoAnnotatedImage.setObjectName(u"cBox_saveCocoAnnotatedImage")

        self.gridLayout_Setting.addWidget(self.cBox_saveCocoAnnotatedImage, 21, 2, 1, 1)

        self.sBox_imageCompression = QDoubleSpinBox(self.gridLayoutWidget)
        self.sBox_imageCompression.setObjectName(u"sBox_imageCompression")
        self.sBox_imageCompression.setDecimals(0)
        self.sBox_imageCompression.setMaximum(50.000000000000000)
        self.sBox_imageCompression.setSingleStep(1.000000000000000)

        self.gridLayout_Setting.addWidget(self.sBox_imageCompression, 11, 2, 1, 1)

        self.sBox_numOfSubdivision = QSpinBox(self.gridLayoutWidget)
        self.sBox_numOfSubdivision.setObjectName(u"sBox_numOfSubdivision")
        self.sBox_numOfSubdivision.setMinimum(3)
        self.sBox_numOfSubdivision.setMaximum(50)

        self.gridLayout_Setting.addWidget(self.sBox_numOfSubdivision, 13, 2, 1, 1)

        self.gridLayout_Setting.setRowStretch(22, 1)
        self.gridLayout_Setting.setColumnStretch(2, 1)
        self.gridLayout_Setting.setColumnStretch(3, 2)
        self.gridLayout_Setting.setColumnStretch(4, 7)
        self.tabWidget.addTab(self.tab_Setting, "")
        self.tab_Objects = QWidget()
        self.tab_Objects.setObjectName(u"tab_Objects")
        self.gridLayoutWidget_5 = QWidget(self.tab_Objects)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(0, 0, 961, 741))
        self.gridLayout_Objects = QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_Objects.setObjectName(u"gridLayout_Objects")
        self.gridLayout_Objects.setContentsMargins(0, 5, 0, 20)
        self.label_65 = QLabel(self.gridLayoutWidget_5)
        self.label_65.setObjectName(u"label_65")
        font5 = QFont()
        font5.setPointSize(9)
        font5.setUnderline(True)
        self.label_65.setFont(font5)

        self.gridLayout_Objects.addWidget(self.label_65, 1, 1, 1, 1)

        self.cBox_obj_randomColor = QCheckBox(self.gridLayoutWidget_5)
        self.cBox_obj_randomColor.setObjectName(u"cBox_obj_randomColor")

        self.gridLayout_Objects.addWidget(self.cBox_obj_randomColor, 4, 3, 1, 1)

        self.cBox_obj_keppLoadedMaterial = QCheckBox(self.gridLayoutWidget_5)
        self.cBox_obj_keppLoadedMaterial.setObjectName(u"cBox_obj_keppLoadedMaterial")

        self.gridLayout_Objects.addWidget(self.cBox_obj_keppLoadedMaterial, 6, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_Objects.addItem(self.horizontalSpacer_7, 7, 4, 1, 1)

        self.label_73 = QLabel(self.gridLayoutWidget_5)
        self.label_73.setObjectName(u"label_73")

        self.gridLayout_Objects.addWidget(self.label_73, 6, 2, 1, 1)

        self.label_74 = QLabel(self.gridLayoutWidget_5)
        self.label_74.setObjectName(u"label_74")

        self.gridLayout_Objects.addWidget(self.label_74, 8, 2, 1, 1)

        self.line_obj_friction = QLineEdit(self.gridLayoutWidget_5)
        self.line_obj_friction.setObjectName(u"line_obj_friction")

        self.gridLayout_Objects.addWidget(self.line_obj_friction, 2, 2, 1, 1)

        self.label_68 = QLabel(self.gridLayoutWidget_5)
        self.label_68.setObjectName(u"label_68")
        font6 = QFont()
        font6.setPointSize(9)
        font6.setUnderline(False)
        self.label_68.setFont(font6)

        self.gridLayout_Objects.addWidget(self.label_68, 12, 2, 1, 1)

        self.cBox_obj_sampling_adjust = QCheckBox(self.gridLayoutWidget_5)
        self.cBox_obj_sampling_adjust.setObjectName(u"cBox_obj_sampling_adjust")

        self.gridLayout_Objects.addWidget(self.cBox_obj_sampling_adjust, 14, 3, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Objects.addItem(self.horizontalSpacer_13, 0, 2, 1, 1)

        self.label_69 = QLabel(self.gridLayoutWidget_5)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setFont(font6)

        self.gridLayout_Objects.addWidget(self.label_69, 14, 2, 1, 1)

        self.line_obj_linearDamping = QLineEdit(self.gridLayoutWidget_5)
        self.line_obj_linearDamping.setObjectName(u"line_obj_linearDamping")

        self.gridLayout_Objects.addWidget(self.line_obj_linearDamping, 1, 2, 1, 1)

        self.line_obj_definedMaterial = QLineEdit(self.gridLayoutWidget_5)
        self.line_obj_definedMaterial.setObjectName(u"line_obj_definedMaterial")

        self.gridLayout_Objects.addWidget(self.line_obj_definedMaterial, 7, 3, 1, 1)

        self.label_67 = QLabel(self.gridLayoutWidget_5)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setFont(font5)

        self.gridLayout_Objects.addWidget(self.label_67, 5, 1, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Objects.addItem(self.horizontalSpacer_11, 3, 3, 1, 1)

        self.line_obj_maxHeight = QLineEdit(self.gridLayoutWidget_5)
        self.line_obj_maxHeight.setObjectName(u"line_obj_maxHeight")

        self.gridLayout_Objects.addWidget(self.line_obj_maxHeight, 13, 3, 1, 1)

        self.cBox_obj_randomMaterial = QCheckBox(self.gridLayoutWidget_5)
        self.cBox_obj_randomMaterial.setObjectName(u"cBox_obj_randomMaterial")

        self.gridLayout_Objects.addWidget(self.cBox_obj_randomMaterial, 8, 3, 1, 1)

        self.label_71 = QLabel(self.gridLayoutWidget_5)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setFont(font6)

        self.gridLayout_Objects.addWidget(self.label_71, 13, 2, 1, 1)

        self.label_66 = QLabel(self.gridLayoutWidget_5)
        self.label_66.setObjectName(u"label_66")
        self.label_66.setFont(font5)

        self.gridLayout_Objects.addWidget(self.label_66, 3, 1, 1, 1)

        self.label_76 = QLabel(self.gridLayoutWidget_5)
        self.label_76.setObjectName(u"label_76")

        self.gridLayout_Objects.addWidget(self.label_76, 4, 2, 1, 1)

        self.line_obj_minHeight = QLineEdit(self.gridLayoutWidget_5)
        self.line_obj_minHeight.setObjectName(u"line_obj_minHeight")

        self.gridLayout_Objects.addWidget(self.line_obj_minHeight, 12, 3, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_Objects.addItem(self.verticalSpacer_5, 16, 1, 1, 1)

        self.label_72 = QLabel(self.gridLayoutWidget_5)
        self.label_72.setObjectName(u"label_72")

        self.gridLayout_Objects.addWidget(self.label_72, 7, 2, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_Objects.addItem(self.verticalSpacer_9, 9, 0, 1, 1)

        self.label_63 = QLabel(self.gridLayoutWidget_5)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setFont(font4)
        self.label_63.setMargin(2)
        self.label_63.setIndent(10)

        self.gridLayout_Objects.addWidget(self.label_63, 10, 0, 1, 1)

        self.label_64 = QLabel(self.gridLayoutWidget_5)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setFont(font5)

        self.gridLayout_Objects.addWidget(self.label_64, 2, 1, 1, 1)

        self.label_62 = QLabel(self.gridLayoutWidget_5)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setFont(font4)
        self.label_62.setMargin(2)
        self.label_62.setIndent(10)

        self.gridLayout_Objects.addWidget(self.label_62, 0, 0, 1, 1)

        self.line_obj_samplingRegion = QLineEdit(self.gridLayoutWidget_5)
        self.line_obj_samplingRegion.setObjectName(u"line_obj_samplingRegion")

        self.gridLayout_Objects.addWidget(self.line_obj_samplingRegion, 15, 2, 1, 1)

        self.label_70 = QLabel(self.gridLayoutWidget_5)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setFont(font5)

        self.gridLayout_Objects.addWidget(self.label_70, 15, 1, 1, 1)

        self.label_120 = QLabel(self.gridLayoutWidget_5)
        self.label_120.setObjectName(u"label_120")
        self.label_120.setFont(font5)

        self.gridLayout_Objects.addWidget(self.label_120, 11, 1, 1, 1)

        self.gridLayout_Objects.setColumnStretch(2, 1)
        self.gridLayout_Objects.setColumnStretch(3, 1)
        self.gridLayout_Objects.setColumnStretch(4, 7)
        self.tabWidget.addTab(self.tab_Objects, "")
        self.tab_Distractor = QWidget()
        self.tab_Distractor.setObjectName(u"tab_Distractor")
        self.gridLayoutWidget_9 = QWidget(self.tab_Distractor)
        self.gridLayoutWidget_9.setObjectName(u"gridLayoutWidget_9")
        self.gridLayoutWidget_9.setGeometry(QRect(0, 0, 961, 471))
        self.gridLayout_Distractor = QGridLayout(self.gridLayoutWidget_9)
        self.gridLayout_Distractor.setObjectName(u"gridLayout_Distractor")
        self.gridLayout_Distractor.setContentsMargins(0, 5, 0, 0)
        self.label_93 = QLabel(self.gridLayoutWidget_9)
        self.label_93.setObjectName(u"label_93")
        self.label_93.setFont(font5)

        self.gridLayout_Distractor.addWidget(self.label_93, 4, 1, 1, 1)

        self.line_distractor_minHeight = QLineEdit(self.gridLayoutWidget_9)
        self.line_distractor_minHeight.setObjectName(u"line_distractor_minHeight")

        self.gridLayout_Distractor.addWidget(self.line_distractor_minHeight, 8, 3, 1, 1)

        self.line_distractor_definedSize = QLineEdit(self.gridLayoutWidget_9)
        self.line_distractor_definedSize.setObjectName(u"line_distractor_definedSize")

        self.gridLayout_Distractor.addWidget(self.line_distractor_definedSize, 3, 2, 1, 1)

        self.label_112 = QLabel(self.gridLayoutWidget_9)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setFont(font4)
        self.label_112.setMargin(2)
        self.label_112.setIndent(10)

        self.gridLayout_Distractor.addWidget(self.label_112, 6, 0, 1, 1)

        self.sBox_distractor_num = QSpinBox(self.gridLayoutWidget_9)
        self.sBox_distractor_num.setObjectName(u"sBox_distractor_num")

        self.gridLayout_Distractor.addWidget(self.sBox_distractor_num, 0, 1, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Distractor.addItem(self.horizontalSpacer_22, 10, 4, 1, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_Distractor.addItem(self.verticalSpacer_12, 1, 0, 1, 1)

        self.label_94 = QLabel(self.gridLayoutWidget_9)
        self.label_94.setObjectName(u"label_94")
        self.label_94.setFont(font5)

        self.gridLayout_Distractor.addWidget(self.label_94, 3, 1, 1, 1)

        self.line_distractor_maxHeight = QLineEdit(self.gridLayoutWidget_9)
        self.line_distractor_maxHeight.setObjectName(u"line_distractor_maxHeight")

        self.gridLayout_Distractor.addWidget(self.line_distractor_maxHeight, 9, 3, 1, 1)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_Distractor.addItem(self.verticalSpacer_16, 5, 0, 1, 1)

        self.label_108 = QLabel(self.gridLayoutWidget_9)
        self.label_108.setObjectName(u"label_108")
        self.label_108.setFont(font6)

        self.gridLayout_Distractor.addWidget(self.label_108, 8, 2, 1, 1)

        self.cBox_distractor_adjustSize = QCheckBox(self.gridLayoutWidget_9)
        self.cBox_distractor_adjustSize.setObjectName(u"cBox_distractor_adjustSize")

        self.gridLayout_Distractor.addWidget(self.cBox_distractor_adjustSize, 4, 2, 1, 1)

        self.horizontalSpacer_21 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Distractor.addItem(self.horizontalSpacer_21, 0, 2, 1, 1)

        self.label_91 = QLabel(self.gridLayoutWidget_9)
        self.label_91.setObjectName(u"label_91")
        self.label_91.setFont(font4)
        self.label_91.setMargin(2)
        self.label_91.setIndent(10)

        self.gridLayout_Distractor.addWidget(self.label_91, 2, 0, 1, 1)

        self.label_109 = QLabel(self.gridLayoutWidget_9)
        self.label_109.setObjectName(u"label_109")
        self.label_109.setFont(font4)
        self.label_109.setMargin(2)
        self.label_109.setIndent(10)

        self.gridLayout_Distractor.addWidget(self.label_109, 0, 0, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_Distractor.addItem(self.verticalSpacer_14, 11, 1, 1, 1)

        self.label_92 = QLabel(self.gridLayoutWidget_9)
        self.label_92.setObjectName(u"label_92")
        self.label_92.setFont(font5)

        self.gridLayout_Distractor.addWidget(self.label_92, 10, 1, 1, 1)

        self.line_distractor_samplingRegion = QLineEdit(self.gridLayoutWidget_9)
        self.line_distractor_samplingRegion.setObjectName(u"line_distractor_samplingRegion")

        self.gridLayout_Distractor.addWidget(self.line_distractor_samplingRegion, 10, 2, 1, 1)

        self.label_107 = QLabel(self.gridLayoutWidget_9)
        self.label_107.setObjectName(u"label_107")
        self.label_107.setFont(font6)

        self.gridLayout_Distractor.addWidget(self.label_107, 9, 2, 1, 1)

        self.label_121 = QLabel(self.gridLayoutWidget_9)
        self.label_121.setObjectName(u"label_121")
        self.label_121.setFont(font5)

        self.gridLayout_Distractor.addWidget(self.label_121, 7, 1, 1, 1)

        self.horizontalSpacer_26 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Distractor.addItem(self.horizontalSpacer_26, 0, 3, 1, 1)

        self.gridLayout_Distractor.setColumnStretch(1, 1)
        self.gridLayout_Distractor.setColumnStretch(2, 1)
        self.gridLayout_Distractor.setColumnStretch(3, 1)
        self.gridLayout_Distractor.setColumnStretch(4, 7)
        self.tabWidget.addTab(self.tab_Distractor, "")
        self.tab_Ground = QWidget()
        self.tab_Ground.setObjectName(u"tab_Ground")
        self.gridLayoutWidget_6 = QWidget(self.tab_Ground)
        self.gridLayoutWidget_6.setObjectName(u"gridLayoutWidget_6")
        self.gridLayoutWidget_6.setGeometry(QRect(0, 0, 961, 491))
        self.gridLayout_Ground = QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_Ground.setObjectName(u"gridLayout_Ground")
        self.gridLayout_Ground.setContentsMargins(10, 5, 0, 20)
        self.label_19 = QLabel(self.gridLayoutWidget_6)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font5)

        self.gridLayout_Ground.addWidget(self.label_19, 5, 0, 1, 1)

        self.label_117 = QLabel(self.gridLayoutWidget_6)
        self.label_117.setObjectName(u"label_117")

        self.gridLayout_Ground.addWidget(self.label_117, 2, 1, 1, 1)

        self.label_77 = QLabel(self.gridLayoutWidget_6)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setFont(font6)

        self.gridLayout_Ground.addWidget(self.label_77, 6, 1, 1, 1)

        self.label_79 = QLabel(self.gridLayoutWidget_6)
        self.label_79.setObjectName(u"label_79")

        self.gridLayout_Ground.addWidget(self.label_79, 12, 1, 1, 1)

        self.label_118 = QLabel(self.gridLayoutWidget_6)
        self.label_118.setObjectName(u"label_118")

        self.gridLayout_Ground.addWidget(self.label_118, 3, 1, 1, 1)

        self.label_75 = QLabel(self.gridLayoutWidget_6)
        self.label_75.setObjectName(u"label_75")
        self.label_75.setFont(font5)

        self.gridLayout_Ground.addWidget(self.label_75, 0, 0, 1, 1)

        self.label_81 = QLabel(self.gridLayoutWidget_6)
        self.label_81.setObjectName(u"label_81")

        self.gridLayout_Ground.addWidget(self.label_81, 8, 2, 1, 1)

        self.label_85 = QLabel(self.gridLayoutWidget_6)
        self.label_85.setObjectName(u"label_85")

        self.gridLayout_Ground.addWidget(self.label_85, 14, 1, 1, 1)

        self.label_83 = QLabel(self.gridLayoutWidget_6)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setFont(font5)

        self.gridLayout_Ground.addWidget(self.label_83, 9, 0, 1, 1)

        self.line_gnd_friction = QLineEdit(self.gridLayoutWidget_6)
        self.line_gnd_friction.setObjectName(u"line_gnd_friction")

        self.gridLayout_Ground.addWidget(self.line_gnd_friction, 10, 1, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_Ground.addItem(self.verticalSpacer_10, 15, 1, 1, 1)

        self.line_gnd_linearDamping = QLineEdit(self.gridLayoutWidget_6)
        self.line_gnd_linearDamping.setObjectName(u"line_gnd_linearDamping")

        self.gridLayout_Ground.addWidget(self.line_gnd_linearDamping, 9, 1, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Ground.addItem(self.horizontalSpacer_14, 0, 5, 1, 1)

        self.label_80 = QLabel(self.gridLayoutWidget_6)
        self.label_80.setObjectName(u"label_80")

        self.gridLayout_Ground.addWidget(self.label_80, 13, 1, 1, 1)

        self.cBox_gnd_randomPick = QCheckBox(self.gridLayoutWidget_6)
        self.cBox_gnd_randomPick.setObjectName(u"cBox_gnd_randomPick")

        self.gridLayout_Ground.addWidget(self.cBox_gnd_randomPick, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_Ground.addItem(self.horizontalSpacer_8, 7, 6, 1, 1)

        self.label_113 = QLabel(self.gridLayoutWidget_6)
        self.label_113.setObjectName(u"label_113")
        self.label_113.setFont(font5)

        self.gridLayout_Ground.addWidget(self.label_113, 1, 0, 1, 1)

        self.label_78 = QLabel(self.gridLayoutWidget_6)
        self.label_78.setObjectName(u"label_78")

        self.gridLayout_Ground.addWidget(self.label_78, 7, 2, 1, 1)

        self.label_82 = QLabel(self.gridLayoutWidget_6)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setFont(font5)

        self.gridLayout_Ground.addWidget(self.label_82, 10, 0, 1, 1)

        self.label_84 = QLabel(self.gridLayoutWidget_6)
        self.label_84.setObjectName(u"label_84")
        self.label_84.setFont(font5)

        self.gridLayout_Ground.addWidget(self.label_84, 11, 0, 1, 1)

        self.label_116 = QLabel(self.gridLayoutWidget_6)
        self.label_116.setObjectName(u"label_116")

        self.gridLayout_Ground.addWidget(self.label_116, 4, 1, 1, 1)

        self.line_gnd_rotX = QLineEdit(self.gridLayoutWidget_6)
        self.line_gnd_rotX.setObjectName(u"line_gnd_rotX")

        self.gridLayout_Ground.addWidget(self.line_gnd_rotX, 2, 2, 1, 1)

        self.line_gnd_rotY = QLineEdit(self.gridLayoutWidget_6)
        self.line_gnd_rotY.setObjectName(u"line_gnd_rotY")

        self.gridLayout_Ground.addWidget(self.line_gnd_rotY, 3, 2, 1, 1)

        self.line_gnd_rotZ = QLineEdit(self.gridLayoutWidget_6)
        self.line_gnd_rotZ.setObjectName(u"line_gnd_rotZ")

        self.gridLayout_Ground.addWidget(self.line_gnd_rotZ, 4, 2, 1, 1)

        self.cBox_gnd_XY_adjust = QCheckBox(self.gridLayoutWidget_6)
        self.cBox_gnd_XY_adjust.setObjectName(u"cBox_gnd_XY_adjust")

        self.gridLayout_Ground.addWidget(self.cBox_gnd_XY_adjust, 8, 5, 1, 1)

        self.horizontalSpacer_24 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Ground.addItem(self.horizontalSpacer_24, 0, 2, 1, 1)

        self.horizontalSpacer_25 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Ground.addItem(self.horizontalSpacer_25, 5, 1, 1, 1)

        self.line_gnd_definedXY = QLineEdit(self.gridLayoutWidget_6)
        self.line_gnd_definedXY.setObjectName(u"line_gnd_definedXY")

        self.gridLayout_Ground.addWidget(self.line_gnd_definedXY, 7, 5, 1, 1)

        self.cBox_gnd_keepLoadedMaterial = QCheckBox(self.gridLayoutWidget_6)
        self.cBox_gnd_keepLoadedMaterial.setObjectName(u"cBox_gnd_keepLoadedMaterial")

        self.gridLayout_Ground.addWidget(self.cBox_gnd_keepLoadedMaterial, 12, 2, 1, 1)

        self.line_gnd_definedMaterial = QLineEdit(self.gridLayoutWidget_6)
        self.line_gnd_definedMaterial.setObjectName(u"line_gnd_definedMaterial")

        self.gridLayout_Ground.addWidget(self.line_gnd_definedMaterial, 13, 2, 1, 1)

        self.cBox_gnd_randomMaterial = QCheckBox(self.gridLayoutWidget_6)
        self.cBox_gnd_randomMaterial.setObjectName(u"cBox_gnd_randomMaterial")

        self.gridLayout_Ground.addWidget(self.cBox_gnd_randomMaterial, 14, 2, 1, 1)

        self.gridLayout_Ground.setRowStretch(10, 1)
        self.gridLayout_Ground.setColumnStretch(1, 1)
        self.gridLayout_Ground.setColumnStretch(2, 1)
        self.gridLayout_Ground.setColumnStretch(5, 1)
        self.gridLayout_Ground.setColumnStretch(6, 7)
        self.tabWidget.addTab(self.tab_Ground, "")
        self.tab_Camera = QWidget()
        self.tab_Camera.setObjectName(u"tab_Camera")
        self.gridLayoutWidget_2 = QWidget(self.tab_Camera)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(0, 0, 961, 671))
        self.gridLayout_Camera = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_Camera.setObjectName(u"gridLayout_Camera")
        self.gridLayout_Camera.setContentsMargins(0, 5, 0, 20)
        self.line_cam_clipEnd = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_clipEnd.setObjectName(u"line_cam_clipEnd")

        self.gridLayout_Camera.addWidget(self.line_cam_clipEnd, 4, 2, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font5)

        self.gridLayout_Camera.addWidget(self.label_13, 1, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_Camera.addWidget(self.label_3, 12, 3, 1, 1)

        self.label_52 = QLabel(self.gridLayoutWidget_2)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font5)

        self.gridLayout_Camera.addWidget(self.label_52, 17, 1, 1, 1)

        self.label_22 = QLabel(self.gridLayoutWidget_2)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_Camera.addWidget(self.label_22, 15, 3, 1, 1)

        self.label_24 = QLabel(self.gridLayoutWidget_2)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font5)

        self.gridLayout_Camera.addWidget(self.label_24, 19, 1, 1, 1)

        self.label_16 = QLabel(self.gridLayoutWidget_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font5)

        self.gridLayout_Camera.addWidget(self.label_16, 7, 1, 1, 1)

        self.label_15 = QLabel(self.gridLayoutWidget_2)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_Camera.addWidget(self.label_15, 14, 3, 1, 1)

        self.label_86 = QLabel(self.gridLayoutWidget_2)
        self.label_86.setObjectName(u"label_86")
        self.label_86.setFont(font4)
        self.label_86.setMargin(2)
        self.label_86.setIndent(10)

        self.gridLayout_Camera.addWidget(self.label_86, 6, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.gridLayout_Camera.addWidget(self.label, 11, 3, 1, 1)

        self.label_12 = QLabel(self.gridLayoutWidget_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font5)

        self.gridLayout_Camera.addWidget(self.label_12, 2, 1, 1, 1)

        self.line_cam_imageHeight = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_imageHeight.setObjectName(u"line_cam_imageHeight")

        self.gridLayout_Camera.addWidget(self.line_cam_imageHeight, 2, 2, 1, 1)

        self.line_cam_maxRadius = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_maxRadius.setObjectName(u"line_cam_maxRadius")

        self.gridLayout_Camera.addWidget(self.line_cam_maxRadius, 12, 4, 1, 1)

        self.line_cam_minElevation = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_minElevation.setObjectName(u"line_cam_minElevation")

        self.gridLayout_Camera.addWidget(self.line_cam_minElevation, 14, 4, 1, 1)

        self.label_59 = QLabel(self.gridLayoutWidget_2)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFont(font5)

        self.gridLayout_Camera.addWidget(self.label_59, 3, 1, 1, 1)

        self.label_14 = QLabel(self.gridLayoutWidget_2)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_Camera.addWidget(self.label_14, 8, 2, 1, 1)

        self.cBox_cam_allObjectsFullyVisible = QCheckBox(self.gridLayoutWidget_2)
        self.cBox_cam_allObjectsFullyVisible.setObjectName(u"cBox_cam_allObjectsFullyVisible")

        self.gridLayout_Camera.addWidget(self.cBox_cam_allObjectsFullyVisible, 21, 3, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Camera.addItem(self.horizontalSpacer_17, 0, 2, 1, 1)

        self.cBox_cam_randomRotation = QCheckBox(self.gridLayoutWidget_2)
        self.cBox_cam_randomRotation.setObjectName(u"cBox_cam_randomRotation")

        self.gridLayout_Camera.addWidget(self.cBox_cam_randomRotation, 18, 3, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Camera.addItem(self.horizontalSpacer_15, 1, 3, 1, 1)

        self.label_61 = QLabel(self.gridLayoutWidget_2)
        self.label_61.setObjectName(u"label_61")

        self.gridLayout_Camera.addWidget(self.label_61, 18, 2, 1, 1)

        self.lbl_camera_config = QLabel(self.gridLayoutWidget_2)
        self.lbl_camera_config.setObjectName(u"lbl_camera_config")
        self.lbl_camera_config.setFont(font4)
        self.lbl_camera_config.setMargin(2)
        self.lbl_camera_config.setIndent(10)

        self.gridLayout_Camera.addWidget(self.lbl_camera_config, 0, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_Camera.addItem(self.verticalSpacer_7, 22, 1, 1, 1)

        self.line_cam_definedPos = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_definedPos.setObjectName(u"line_cam_definedPos")

        self.gridLayout_Camera.addWidget(self.line_cam_definedPos, 8, 3, 1, 1)

        self.line_cam_maxElevation = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_maxElevation.setObjectName(u"line_cam_maxElevation")

        self.gridLayout_Camera.addWidget(self.line_cam_maxElevation, 15, 4, 1, 1)

        self.label_60 = QLabel(self.gridLayoutWidget_2)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setFont(font5)

        self.gridLayout_Camera.addWidget(self.label_60, 4, 1, 1, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_Camera.addItem(self.verticalSpacer_11, 5, 0, 1, 1)

        self.label_25 = QLabel(self.gridLayoutWidget_2)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_Camera.addWidget(self.label_25, 20, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_Camera.addItem(self.horizontalSpacer_5, 3, 5, 1, 1)

        self.cBox_cam_noWorldBackground = QCheckBox(self.gridLayoutWidget_2)
        self.cBox_cam_noWorldBackground.setObjectName(u"cBox_cam_noWorldBackground")

        self.gridLayout_Camera.addWidget(self.cBox_cam_noWorldBackground, 20, 3, 1, 1)

        self.cBox_cam_randomPos = QCheckBox(self.gridLayoutWidget_2)
        self.cBox_cam_randomPos.setObjectName(u"cBox_cam_randomPos")

        self.gridLayout_Camera.addWidget(self.cBox_cam_randomPos, 9, 3, 1, 1)

        self.line_cam_center = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_center.setObjectName(u"line_cam_center")

        self.gridLayout_Camera.addWidget(self.line_cam_center, 10, 4, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Camera.addItem(self.horizontalSpacer_9, 3, 4, 1, 1)

        self.line_cam_imageWidth = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_imageWidth.setObjectName(u"line_cam_imageWidth")

        self.gridLayout_Camera.addWidget(self.line_cam_imageWidth, 1, 2, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_Camera.addWidget(self.label_9, 21, 2, 1, 1)

        self.line_cam_clipStart = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_clipStart.setObjectName(u"line_cam_clipStart")

        self.gridLayout_Camera.addWidget(self.line_cam_clipStart, 3, 2, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_Camera.addWidget(self.label_2, 10, 3, 1, 1)

        self.label_17 = QLabel(self.gridLayoutWidget_2)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_Camera.addWidget(self.label_17, 9, 2, 1, 1)

        self.line_cam_minRadius = QLineEdit(self.gridLayoutWidget_2)
        self.line_cam_minRadius.setObjectName(u"line_cam_minRadius")

        self.gridLayout_Camera.addWidget(self.line_cam_minRadius, 11, 4, 1, 1)

        self.label_114 = QLabel(self.gridLayoutWidget_2)
        self.label_114.setObjectName(u"label_114")

        self.gridLayout_Camera.addWidget(self.label_114, 13, 3, 1, 1)

        self.cBox_cam_preferSmallRadius = QCheckBox(self.gridLayoutWidget_2)
        self.cBox_cam_preferSmallRadius.setObjectName(u"cBox_cam_preferSmallRadius")

        self.gridLayout_Camera.addWidget(self.cBox_cam_preferSmallRadius, 13, 4, 1, 1)

        self.gridLayout_Camera.setColumnStretch(2, 1)
        self.gridLayout_Camera.setColumnStretch(3, 1)
        self.gridLayout_Camera.setColumnStretch(4, 1)
        self.gridLayout_Camera.setColumnStretch(5, 7)
        self.tabWidget.addTab(self.tab_Camera, "")
        self.tab_Light = QWidget()
        self.tab_Light.setObjectName(u"tab_Light")
        self.gridLayoutWidget_4 = QWidget(self.tab_Light)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(0, 0, 961, 1031))
        self.gridLayout_Light = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_Light.setObjectName(u"gridLayout_Light")
        self.gridLayout_Light.setContentsMargins(0, 5, 0, 20)
        self.label_89 = QLabel(self.gridLayoutWidget_4)
        self.label_89.setObjectName(u"label_89")

        self.gridLayout_Light.addWidget(self.label_89, 20, 2, 1, 1)

        self.label_18 = QLabel(self.gridLayoutWidget_4)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_Light.addWidget(self.label_18, 3, 2, 1, 1)

        self.label_98 = QLabel(self.gridLayoutWidget_4)
        self.label_98.setObjectName(u"label_98")
        self.label_98.setFont(font5)

        self.gridLayout_Light.addWidget(self.label_98, 17, 1, 1, 1)

        self.lbl_camera_sampler_2 = QLabel(self.gridLayoutWidget_4)
        self.lbl_camera_sampler_2.setObjectName(u"lbl_camera_sampler_2")
        self.lbl_camera_sampler_2.setFont(font4)
        self.lbl_camera_sampler_2.setMargin(2)
        self.lbl_camera_sampler_2.setIndent(10)

        self.gridLayout_Light.addWidget(self.lbl_camera_sampler_2, 16, 0, 1, 1)

        self.line_spotLight_definedWatt = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_definedWatt.setObjectName(u"line_spotLight_definedWatt")

        self.gridLayout_Light.addWidget(self.line_spotLight_definedWatt, 32, 3, 1, 1)

        self.line_spotLight_minElevation = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_minElevation.setObjectName(u"line_spotLight_minElevation")

        self.gridLayout_Light.addWidget(self.line_spotLight_minElevation, 27, 4, 1, 1)

        self.label_115 = QLabel(self.gridLayoutWidget_4)
        self.label_115.setObjectName(u"label_115")
        self.label_115.setFont(font5)

        self.gridLayout_Light.addWidget(self.label_115, 1, 1, 1, 1)

        self.cBox_spotLight_randomWatt = QCheckBox(self.gridLayoutWidget_4)
        self.cBox_spotLight_randomWatt.setObjectName(u"cBox_spotLight_randomWatt")

        self.gridLayout_Light.addWidget(self.cBox_spotLight_randomWatt, 33, 3, 1, 1)

        self.cBox_spotlight_toObjects = QCheckBox(self.gridLayoutWidget_4)
        self.cBox_spotlight_toObjects.setObjectName(u"cBox_spotlight_toObjects")

        self.gridLayout_Light.addWidget(self.cBox_spotlight_toObjects, 30, 3, 1, 1)

        self.line_ceilLight_XY = QLineEdit(self.gridLayoutWidget_4)
        self.line_ceilLight_XY.setObjectName(u"line_ceilLight_XY")

        self.gridLayout_Light.addWidget(self.line_ceilLight_XY, 13, 3, 1, 1)

        self.label_97 = QLabel(self.gridLayoutWidget_4)
        self.label_97.setObjectName(u"label_97")

        self.gridLayout_Light.addWidget(self.label_97, 30, 2, 1, 1)

        self.label_45 = QLabel(self.gridLayoutWidget_4)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_Light.addWidget(self.label_45, 26, 3, 1, 1)

        self.label_21 = QLabel(self.gridLayoutWidget_4)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_Light.addWidget(self.label_21, 27, 3, 1, 1)

        self.label_23 = QLabel(self.gridLayoutWidget_4)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font5)

        self.gridLayout_Light.addWidget(self.label_23, 31, 1, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_Light.addItem(self.verticalSpacer_8, 36, 0, 1, 1)

        self.label_40 = QLabel(self.gridLayoutWidget_4)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFont(font5)

        self.gridLayout_Light.addWidget(self.label_40, 12, 1, 1, 1)

        self.line_spotLight_spreadAngle = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_spreadAngle.setObjectName(u"line_spotLight_spreadAngle")

        self.gridLayout_Light.addWidget(self.line_spotLight_spreadAngle, 19, 3, 1, 1)

        self.line_ceilLight_minIntensity = QLineEdit(self.gridLayoutWidget_4)
        self.line_ceilLight_minIntensity.setObjectName(u"line_ceilLight_minIntensity")

        self.gridLayout_Light.addWidget(self.line_ceilLight_minIntensity, 10, 4, 1, 1)

        self.line_ceilLight_maxHeight = QLineEdit(self.gridLayoutWidget_4)
        self.line_ceilLight_maxHeight.setObjectName(u"line_ceilLight_maxHeight")

        self.gridLayout_Light.addWidget(self.line_ceilLight_maxHeight, 6, 4, 1, 1)

        self.label_47 = QLabel(self.gridLayoutWidget_4)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_Light.addWidget(self.label_47, 35, 3, 1, 1)

        self.label_50 = QLabel(self.gridLayoutWidget_4)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_Light.addWidget(self.label_50, 25, 3, 1, 1)

        self.label_88 = QLabel(self.gridLayoutWidget_4)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setFont(font5)

        self.gridLayout_Light.addWidget(self.label_88, 18, 1, 1, 1)

        self.label_55 = QLabel(self.gridLayoutWidget_4)
        self.label_55.setObjectName(u"label_55")

        self.gridLayout_Light.addWidget(self.label_55, 10, 3, 1, 1)

        self.cBox_ceilLight_fitToGround = QCheckBox(self.gridLayoutWidget_4)
        self.cBox_ceilLight_fitToGround.setObjectName(u"cBox_ceilLight_fitToGround")

        self.gridLayout_Light.addWidget(self.cBox_ceilLight_fitToGround, 14, 3, 1, 1)

        self.cBox_ceilLight_ENA = QCheckBox(self.gridLayoutWidget_4)
        self.cBox_ceilLight_ENA.setObjectName(u"cBox_ceilLight_ENA")

        self.gridLayout_Light.addWidget(self.cBox_ceilLight_ENA, 1, 2, 1, 1)

        self.line_spotLight_minWatt = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_minWatt.setObjectName(u"line_spotLight_minWatt")

        self.gridLayout_Light.addWidget(self.line_spotLight_minWatt, 34, 4, 1, 1)

        self.label_36 = QLabel(self.gridLayoutWidget_4)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_Light.addWidget(self.label_36, 9, 2, 1, 1)

        self.label_20 = QLabel(self.gridLayoutWidget_4)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font5)

        self.gridLayout_Light.addWidget(self.label_20, 2, 1, 1, 1)

        self.sBox_spotLight_num = QSpinBox(self.gridLayoutWidget_4)
        self.sBox_spotLight_num.setObjectName(u"sBox_spotLight_num")

        self.gridLayout_Light.addWidget(self.sBox_spotLight_num, 17, 2, 1, 1)

        self.line_ceilLight_maxIntensity = QLineEdit(self.gridLayoutWidget_4)
        self.line_ceilLight_maxIntensity.setObjectName(u"line_ceilLight_maxIntensity")

        self.gridLayout_Light.addWidget(self.line_ceilLight_maxIntensity, 11, 4, 1, 1)

        self.line_ceilLight_definedPos = QLineEdit(self.gridLayoutWidget_4)
        self.line_ceilLight_definedPos.setObjectName(u"line_ceilLight_definedPos")

        self.gridLayout_Light.addWidget(self.line_ceilLight_definedPos, 3, 3, 1, 1)

        self.label_95 = QLabel(self.gridLayoutWidget_4)
        self.label_95.setObjectName(u"label_95")
        self.label_95.setFont(font5)

        self.gridLayout_Light.addWidget(self.label_95, 29, 1, 1, 1)

        self.label_90 = QLabel(self.gridLayoutWidget_4)
        self.label_90.setObjectName(u"label_90")

        self.gridLayout_Light.addWidget(self.label_90, 19, 2, 1, 1)

        self.line_ceilLight_minHeight = QLineEdit(self.gridLayoutWidget_4)
        self.line_ceilLight_minHeight.setObjectName(u"line_ceilLight_minHeight")

        self.gridLayout_Light.addWidget(self.line_ceilLight_minHeight, 5, 4, 1, 1)

        self.cBox_ceilLight_randomIntensity = QCheckBox(self.gridLayoutWidget_4)
        self.cBox_ceilLight_randomIntensity.setObjectName(u"cBox_ceilLight_randomIntensity")

        self.gridLayout_Light.addWidget(self.cBox_ceilLight_randomIntensity, 9, 3, 1, 1)

        self.label_48 = QLabel(self.gridLayoutWidget_4)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font5)

        self.gridLayout_Light.addWidget(self.label_48, 21, 1, 1, 1)

        self.lbl_camera_config_2 = QLabel(self.gridLayoutWidget_4)
        self.lbl_camera_config_2.setObjectName(u"lbl_camera_config_2")
        self.lbl_camera_config_2.setFont(font4)
        self.lbl_camera_config_2.setMargin(2)
        self.lbl_camera_config_2.setIndent(10)

        self.gridLayout_Light.addWidget(self.lbl_camera_config_2, 0, 0, 1, 1)

        self.label_49 = QLabel(self.gridLayoutWidget_4)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_Light.addWidget(self.label_49, 22, 2, 1, 1)

        self.label_37 = QLabel(self.gridLayoutWidget_4)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFont(font5)

        self.gridLayout_Light.addWidget(self.label_37, 7, 1, 1, 1)

        self.line_ceilLight_definedIntensity = QLineEdit(self.gridLayoutWidget_4)
        self.line_ceilLight_definedIntensity.setObjectName(u"line_ceilLight_definedIntensity")

        self.gridLayout_Light.addWidget(self.line_ceilLight_definedIntensity, 8, 3, 1, 1)

        self.label_41 = QLabel(self.gridLayoutWidget_4)
        self.label_41.setObjectName(u"label_41")

        self.gridLayout_Light.addWidget(self.label_41, 13, 2, 1, 1)

        self.label_44 = QLabel(self.gridLayoutWidget_4)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_Light.addWidget(self.label_44, 28, 3, 1, 1)

        self.label_43 = QLabel(self.gridLayoutWidget_4)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_Light.addWidget(self.label_43, 32, 2, 1, 1)

        self.line_spotLight_blend = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_blend.setObjectName(u"line_spotLight_blend")

        self.gridLayout_Light.addWidget(self.line_spotLight_blend, 20, 3, 1, 1)

        self.label_46 = QLabel(self.gridLayoutWidget_4)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_Light.addWidget(self.label_46, 34, 3, 1, 1)

        self.label_56 = QLabel(self.gridLayoutWidget_4)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_Light.addWidget(self.label_56, 11, 3, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_Light.addItem(self.verticalSpacer_3, 15, 0, 1, 1)

        self.line_spotLight_maxElevation = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_maxElevation.setObjectName(u"line_spotLight_maxElevation")

        self.gridLayout_Light.addWidget(self.line_spotLight_maxElevation, 28, 4, 1, 1)

        self.line_spotLight_center = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_center.setObjectName(u"line_spotLight_center")

        self.gridLayout_Light.addWidget(self.line_spotLight_center, 24, 4, 1, 1)

        self.line_spotLight_minRadius = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_minRadius.setObjectName(u"line_spotLight_minRadius")

        self.gridLayout_Light.addWidget(self.line_spotLight_minRadius, 25, 4, 1, 1)

        self.label_39 = QLabel(self.gridLayoutWidget_4)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout_Light.addWidget(self.label_39, 14, 2, 1, 1)

        self.label_38 = QLabel(self.gridLayoutWidget_4)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_Light.addWidget(self.label_38, 8, 2, 1, 1)

        self.line_spotLight_maxRadius = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_maxRadius.setObjectName(u"line_spotLight_maxRadius")

        self.gridLayout_Light.addWidget(self.line_spotLight_maxRadius, 26, 4, 1, 1)

        self.label_42 = QLabel(self.gridLayoutWidget_4)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_Light.addWidget(self.label_42, 24, 3, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Light.addItem(self.horizontalSpacer_10, 4, 4, 1, 1)

        self.line_spotLight_definedPos = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_definedPos.setObjectName(u"line_spotLight_definedPos")

        self.gridLayout_Light.addWidget(self.line_spotLight_definedPos, 22, 3, 1, 1)

        self.cBox_spotLight_randomPos = QCheckBox(self.gridLayoutWidget_4)
        self.cBox_spotLight_randomPos.setObjectName(u"cBox_spotLight_randomPos")

        self.gridLayout_Light.addWidget(self.cBox_spotLight_randomPos, 23, 3, 1, 1)

        self.label_53 = QLabel(self.gridLayoutWidget_4)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_Light.addWidget(self.label_53, 5, 3, 1, 1)

        self.label_54 = QLabel(self.gridLayoutWidget_4)
        self.label_54.setObjectName(u"label_54")

        self.gridLayout_Light.addWidget(self.label_54, 33, 2, 1, 1)

        self.cBox_ceilLight_randomPos = QCheckBox(self.gridLayoutWidget_4)
        self.cBox_ceilLight_randomPos.setObjectName(u"cBox_ceilLight_randomPos")

        self.gridLayout_Light.addWidget(self.cBox_ceilLight_randomPos, 4, 3, 1, 1)

        self.label_51 = QLabel(self.gridLayoutWidget_4)
        self.label_51.setObjectName(u"label_51")

        self.gridLayout_Light.addWidget(self.label_51, 23, 2, 1, 1)

        self.label_34 = QLabel(self.gridLayoutWidget_4)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_Light.addWidget(self.label_34, 4, 2, 1, 1)

        self.label_35 = QLabel(self.gridLayoutWidget_4)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_Light.addWidget(self.label_35, 6, 3, 1, 1)

        self.line_spotLight_maxWatt = QLineEdit(self.gridLayoutWidget_4)
        self.line_spotLight_maxWatt.setObjectName(u"line_spotLight_maxWatt")

        self.gridLayout_Light.addWidget(self.line_spotLight_maxWatt, 35, 4, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Light.addItem(self.horizontalSpacer_16, 0, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_Light.addItem(self.horizontalSpacer_4, 5, 5, 1, 1)

        self.gridLayout_Light.setColumnStretch(2, 1)
        self.gridLayout_Light.setColumnStretch(3, 1)
        self.gridLayout_Light.setColumnStretch(4, 1)
        self.gridLayout_Light.setColumnStretch(5, 7)
        self.tabWidget.addTab(self.tab_Light, "")
        self.tab_Simulation = QWidget()
        self.tab_Simulation.setObjectName(u"tab_Simulation")
        self.gridLayoutWidget_8 = QWidget(self.tab_Simulation)
        self.gridLayoutWidget_8.setObjectName(u"gridLayoutWidget_8")
        self.gridLayoutWidget_8.setGeometry(QRect(0, 0, 961, 411))
        self.gridLayout_Simulation = QGridLayout(self.gridLayoutWidget_8)
        self.gridLayout_Simulation.setObjectName(u"gridLayout_Simulation")
        self.gridLayout_Simulation.setContentsMargins(10, 5, 0, 20)
        self.label_99 = QLabel(self.gridLayoutWidget_8)
        self.label_99.setObjectName(u"label_99")
        self.label_99.setFont(font5)

        self.gridLayout_Simulation.addWidget(self.label_99, 1, 0, 1, 1)

        self.label_101 = QLabel(self.gridLayoutWidget_8)
        self.label_101.setObjectName(u"label_101")
        self.label_101.setFont(font5)

        self.gridLayout_Simulation.addWidget(self.label_101, 2, 0, 1, 1)

        self.label_103 = QLabel(self.gridLayoutWidget_8)
        self.label_103.setObjectName(u"label_103")
        self.label_103.setFont(font5)

        self.gridLayout_Simulation.addWidget(self.label_103, 3, 0, 1, 1)

        self.label_100 = QLabel(self.gridLayoutWidget_8)
        self.label_100.setObjectName(u"label_100")
        self.label_100.setFont(font5)

        self.gridLayout_Simulation.addWidget(self.label_100, 0, 0, 1, 1)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_Simulation.addItem(self.horizontalSpacer_20, 4, 3, 1, 1)

        self.line_simu_checkObjectInterval = QLineEdit(self.gridLayoutWidget_8)
        self.line_simu_checkObjectInterval.setObjectName(u"line_simu_checkObjectInterval")

        self.gridLayout_Simulation.addWidget(self.line_simu_checkObjectInterval, 0, 1, 1, 1)

        self.line_simu_substepsPerFrame = QLineEdit(self.gridLayoutWidget_8)
        self.line_simu_substepsPerFrame.setObjectName(u"line_simu_substepsPerFrame")

        self.gridLayout_Simulation.addWidget(self.line_simu_substepsPerFrame, 1, 1, 1, 1)

        self.line_simu_solverIters = QLineEdit(self.gridLayoutWidget_8)
        self.line_simu_solverIters.setObjectName(u"line_simu_solverIters")

        self.gridLayout_Simulation.addWidget(self.line_simu_solverIters, 2, 1, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Simulation.addItem(self.horizontalSpacer_18, 3, 2, 1, 1)

        self.verticalSpacer_13 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_Simulation.addItem(self.verticalSpacer_13, 7, 0, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_Simulation.addItem(self.horizontalSpacer_19, 7, 1, 1, 1)

        self.label_102 = QLabel(self.gridLayoutWidget_8)
        self.label_102.setObjectName(u"label_102")

        self.gridLayout_Simulation.addWidget(self.label_102, 4, 1, 1, 1)

        self.line_simu_minTime = QLineEdit(self.gridLayoutWidget_8)
        self.line_simu_minTime.setObjectName(u"line_simu_minTime")

        self.gridLayout_Simulation.addWidget(self.line_simu_minTime, 4, 2, 1, 1)

        self.line_simu_maxTime = QLineEdit(self.gridLayoutWidget_8)
        self.line_simu_maxTime.setObjectName(u"line_simu_maxTime")

        self.gridLayout_Simulation.addWidget(self.line_simu_maxTime, 5, 2, 1, 1)

        self.label_105 = QLabel(self.gridLayoutWidget_8)
        self.label_105.setObjectName(u"label_105")

        self.gridLayout_Simulation.addWidget(self.label_105, 5, 1, 1, 1)

        self.label_104 = QLabel(self.gridLayoutWidget_8)
        self.label_104.setObjectName(u"label_104")

        self.gridLayout_Simulation.addWidget(self.label_104, 6, 1, 1, 1)

        self.cBox_simu_adjustToObjects = QCheckBox(self.gridLayoutWidget_8)
        self.cBox_simu_adjustToObjects.setObjectName(u"cBox_simu_adjustToObjects")

        self.gridLayout_Simulation.addWidget(self.cBox_simu_adjustToObjects, 6, 2, 1, 1)

        self.gridLayout_Simulation.setRowStretch(7, 1)
        self.gridLayout_Simulation.setColumnStretch(1, 1)
        self.gridLayout_Simulation.setColumnStretch(2, 1)
        self.gridLayout_Simulation.setColumnStretch(3, 7)
        self.tabWidget.addTab(self.tab_Simulation, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pB_loadConfig = QPushButton(self.verticalLayoutWidget)
        self.pB_loadConfig.setObjectName(u"pB_loadConfig")
        self.pB_loadConfig.setFont(font2)

        self.horizontalLayout_2.addWidget(self.pB_loadConfig)

        self.pB_saveConfig = QPushButton(self.verticalLayoutWidget)
        self.pB_saveConfig.setObjectName(u"pB_saveConfig")
        self.pB_saveConfig.setFont(font2)

        self.horizontalLayout_2.addWidget(self.pB_saveConfig)

        self.pB_applyConfig = QPushButton(self.verticalLayoutWidget)
        self.pB_applyConfig.setObjectName(u"pB_applyConfig")
        self.pB_applyConfig.setFont(font2)

        self.horizontalLayout_2.addWidget(self.pB_applyConfig)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.main_layout.addLayout(self.verticalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_106 = QLabel(self.verticalLayoutWidget)
        self.label_106.setObjectName(u"label_106")
        self.label_106.setFont(font2)
        self.label_106.setMargin(1)
        self.label_106.setIndent(4)

        self.gridLayout.addWidget(self.label_106, 0, 2, 1, 1)

        self.label_96 = QLabel(self.verticalLayoutWidget)
        self.label_96.setObjectName(u"label_96")
        self.label_96.setFont(font2)
        self.label_96.setMargin(1)
        self.label_96.setIndent(4)

        self.gridLayout.addWidget(self.label_96, 0, 0, 1, 1)

        self.line_numOfImages = QLineEdit(self.verticalLayoutWidget)
        self.line_numOfImages.setObjectName(u"line_numOfImages")
        self.line_numOfImages.setFont(font2)

        self.gridLayout.addWidget(self.line_numOfImages, 0, 1, 1, 1)

        self.line_minOccurences = QLineEdit(self.verticalLayoutWidget)
        self.line_minOccurences.setObjectName(u"line_minOccurences")
        self.line_minOccurences.setFont(font2)

        self.gridLayout.addWidget(self.line_minOccurences, 0, 3, 1, 1)

        self.line_maxOccurences = QLineEdit(self.verticalLayoutWidget)
        self.line_maxOccurences.setObjectName(u"line_maxOccurences")
        self.line_maxOccurences.setFont(font2)

        self.gridLayout.addWidget(self.line_maxOccurences, 2, 3, 1, 1)

        self.label_110 = QLabel(self.verticalLayoutWidget)
        self.label_110.setObjectName(u"label_110")
        self.label_110.setFont(font2)
        self.label_110.setMargin(1)
        self.label_110.setIndent(4)

        self.gridLayout.addWidget(self.label_110, 2, 2, 1, 1)

        self.line_totalOccurences = QLineEdit(self.verticalLayoutWidget)
        self.line_totalOccurences.setObjectName(u"line_totalOccurences")
        self.line_totalOccurences.setFont(font2)

        self.gridLayout.addWidget(self.line_totalOccurences, 2, 1, 1, 1)

        self.label_111 = QLabel(self.verticalLayoutWidget)
        self.label_111.setObjectName(u"label_111")
        self.label_111.setFont(font2)
        self.label_111.setMargin(1)
        self.label_111.setIndent(4)

        self.gridLayout.addWidget(self.label_111, 2, 0, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.pB_Regenerate = QPushButton(self.verticalLayoutWidget)
        self.pB_Regenerate.setObjectName(u"pB_Regenerate")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_Regenerate.sizePolicy().hasHeightForWidth())
        self.pB_Regenerate.setSizePolicy(sizePolicy)
        self.pB_Regenerate.setMinimumSize(QSize(0, 40))
        font7 = QFont()
        font7.setPointSize(10)
        font7.setBold(True)
        font7.setWeight(75)
        self.pB_Regenerate.setFont(font7)

        self.horizontalLayout.addWidget(self.pB_Regenerate)

        self.pB_generate = QPushButton(self.verticalLayoutWidget)
        self.pB_generate.setObjectName(u"pB_generate")
        sizePolicy.setHeightForWidth(self.pB_generate.sizePolicy().hasHeightForWidth())
        self.pB_generate.setSizePolicy(sizePolicy)
        self.pB_generate.setMinimumSize(QSize(0, 40))
        self.pB_generate.setFont(font7)
        self.pB_generate.setCheckable(False)

        self.horizontalLayout.addWidget(self.pB_generate)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)

        self.main_layout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_layout.addItem(self.verticalSpacer)

        self.horizontalLayout_progress = QHBoxLayout()
        self.horizontalLayout_progress.setObjectName(u"horizontalLayout_progress")
        self.lbl_progress = QLabel(self.verticalLayoutWidget)
        self.lbl_progress.setObjectName(u"lbl_progress")

        self.horizontalLayout_progress.addWidget(self.lbl_progress)

        self.progressBar = QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.horizontalLayout_progress.addWidget(self.progressBar)


        self.main_layout.addLayout(self.horizontalLayout_progress)

        self.main_layout.setStretch(1, 1)
        self.main_layout.setStretch(2, 10)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1084, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.line_obj_dir, self.pB_search_obj_dir)
        QWidget.setTabOrder(self.pB_search_obj_dir, self.line_gnd_dir)
        QWidget.setTabOrder(self.line_gnd_dir, self.pB_search_gnd_dir)
        QWidget.setTabOrder(self.pB_search_gnd_dir, self.line_config_file)
        QWidget.setTabOrder(self.line_config_file, self.pB_search_config_file)
        QWidget.setTabOrder(self.pB_search_config_file, self.line_output_dir)
        QWidget.setTabOrder(self.line_output_dir, self.pB_search_output_dir)
        QWidget.setTabOrder(self.pB_search_output_dir, self.comboBox_unit)
        QWidget.setTabOrder(self.comboBox_unit, self.line_gravity)
        QWidget.setTabOrder(self.line_gravity, self.cBox_backgroundBlack)
        QWidget.setTabOrder(self.cBox_backgroundBlack, self.line_3DviewClipStart)
        QWidget.setTabOrder(self.line_3DviewClipStart, self.line_3DviewClipEnd)
        QWidget.setTabOrder(self.line_3DviewClipEnd, self.line_engine)
        QWidget.setTabOrder(self.line_engine, self.cBox_ambientOcclusion)
        QWidget.setTabOrder(self.cBox_ambientOcclusion, self.sBox_imageCompression)
        QWidget.setTabOrder(self.sBox_imageCompression, self.sBox_CPUCoresNum)
        QWidget.setTabOrder(self.sBox_CPUCoresNum, self.sBox_numOfSubdivision)
        QWidget.setTabOrder(self.sBox_numOfSubdivision, self.comboBox_denoiser)
        QWidget.setTabOrder(self.comboBox_denoiser, self.sBox_noiseTreshold)
        QWidget.setTabOrder(self.sBox_noiseTreshold, self.cBox_useOnlyCPU)
        QWidget.setTabOrder(self.cBox_useOnlyCPU, self.comboBox_GPUType)
        QWidget.setTabOrder(self.comboBox_GPUType, self.cBox_saveCocoAnnotatedImage)
        QWidget.setTabOrder(self.cBox_saveCocoAnnotatedImage, self.line_obj_linearDamping)
        QWidget.setTabOrder(self.line_obj_linearDamping, self.line_obj_friction)
        QWidget.setTabOrder(self.line_obj_friction, self.cBox_obj_randomColor)
        QWidget.setTabOrder(self.cBox_obj_randomColor, self.cBox_obj_keppLoadedMaterial)
        QWidget.setTabOrder(self.cBox_obj_keppLoadedMaterial, self.line_obj_definedMaterial)
        QWidget.setTabOrder(self.line_obj_definedMaterial, self.cBox_obj_randomMaterial)
        QWidget.setTabOrder(self.cBox_obj_randomMaterial, self.line_obj_samplingRegion)
        QWidget.setTabOrder(self.line_obj_samplingRegion, self.sBox_distractor_num)
        QWidget.setTabOrder(self.sBox_distractor_num, self.line_distractor_definedSize)
        QWidget.setTabOrder(self.line_distractor_definedSize, self.cBox_distractor_adjustSize)
        QWidget.setTabOrder(self.cBox_distractor_adjustSize, self.line_distractor_samplingRegion)
        QWidget.setTabOrder(self.line_distractor_samplingRegion, self.cBox_gnd_randomPick)
        QWidget.setTabOrder(self.cBox_gnd_randomPick, self.line_gnd_linearDamping)
        QWidget.setTabOrder(self.line_gnd_linearDamping, self.line_gnd_friction)
        QWidget.setTabOrder(self.line_gnd_friction, self.line_cam_imageWidth)
        QWidget.setTabOrder(self.line_cam_imageWidth, self.line_cam_imageHeight)
        QWidget.setTabOrder(self.line_cam_imageHeight, self.line_cam_clipStart)
        QWidget.setTabOrder(self.line_cam_clipStart, self.line_cam_clipEnd)
        QWidget.setTabOrder(self.line_cam_clipEnd, self.line_cam_definedPos)
        QWidget.setTabOrder(self.line_cam_definedPos, self.cBox_cam_randomPos)
        QWidget.setTabOrder(self.cBox_cam_randomPos, self.line_cam_center)
        QWidget.setTabOrder(self.line_cam_center, self.line_cam_minRadius)
        QWidget.setTabOrder(self.line_cam_minRadius, self.line_cam_maxRadius)
        QWidget.setTabOrder(self.line_cam_maxRadius, self.cBox_cam_preferSmallRadius)
        QWidget.setTabOrder(self.cBox_cam_preferSmallRadius, self.line_cam_minElevation)
        QWidget.setTabOrder(self.line_cam_minElevation, self.line_cam_maxElevation)
        QWidget.setTabOrder(self.line_cam_maxElevation, self.cBox_cam_randomRotation)
        QWidget.setTabOrder(self.cBox_cam_randomRotation, self.cBox_cam_noWorldBackground)
        QWidget.setTabOrder(self.cBox_cam_noWorldBackground, self.cBox_cam_allObjectsFullyVisible)
        QWidget.setTabOrder(self.cBox_cam_allObjectsFullyVisible, self.cBox_ceilLight_ENA)
        QWidget.setTabOrder(self.cBox_ceilLight_ENA, self.line_ceilLight_definedPos)
        QWidget.setTabOrder(self.line_ceilLight_definedPos, self.cBox_ceilLight_randomPos)
        QWidget.setTabOrder(self.cBox_ceilLight_randomPos, self.line_ceilLight_minHeight)
        QWidget.setTabOrder(self.line_ceilLight_minHeight, self.line_ceilLight_maxHeight)
        QWidget.setTabOrder(self.line_ceilLight_maxHeight, self.line_ceilLight_definedIntensity)
        QWidget.setTabOrder(self.line_ceilLight_definedIntensity, self.cBox_ceilLight_randomIntensity)
        QWidget.setTabOrder(self.cBox_ceilLight_randomIntensity, self.line_ceilLight_minIntensity)
        QWidget.setTabOrder(self.line_ceilLight_minIntensity, self.line_ceilLight_maxIntensity)
        QWidget.setTabOrder(self.line_ceilLight_maxIntensity, self.line_ceilLight_XY)
        QWidget.setTabOrder(self.line_ceilLight_XY, self.cBox_ceilLight_fitToGround)
        QWidget.setTabOrder(self.cBox_ceilLight_fitToGround, self.sBox_spotLight_num)
        QWidget.setTabOrder(self.sBox_spotLight_num, self.line_spotLight_spreadAngle)
        QWidget.setTabOrder(self.line_spotLight_spreadAngle, self.line_spotLight_blend)
        QWidget.setTabOrder(self.line_spotLight_blend, self.line_spotLight_definedPos)
        QWidget.setTabOrder(self.line_spotLight_definedPos, self.cBox_spotLight_randomPos)
        QWidget.setTabOrder(self.cBox_spotLight_randomPos, self.line_spotLight_center)
        QWidget.setTabOrder(self.line_spotLight_center, self.line_spotLight_minRadius)
        QWidget.setTabOrder(self.line_spotLight_minRadius, self.line_spotLight_maxRadius)
        QWidget.setTabOrder(self.line_spotLight_maxRadius, self.line_spotLight_minElevation)
        QWidget.setTabOrder(self.line_spotLight_minElevation, self.line_spotLight_maxElevation)
        QWidget.setTabOrder(self.line_spotLight_maxElevation, self.cBox_spotlight_toObjects)
        QWidget.setTabOrder(self.cBox_spotlight_toObjects, self.line_spotLight_definedWatt)
        QWidget.setTabOrder(self.line_spotLight_definedWatt, self.cBox_spotLight_randomWatt)
        QWidget.setTabOrder(self.cBox_spotLight_randomWatt, self.line_spotLight_minWatt)
        QWidget.setTabOrder(self.line_spotLight_minWatt, self.line_spotLight_maxWatt)
        QWidget.setTabOrder(self.line_spotLight_maxWatt, self.line_simu_checkObjectInterval)
        QWidget.setTabOrder(self.line_simu_checkObjectInterval, self.line_simu_substepsPerFrame)
        QWidget.setTabOrder(self.line_simu_substepsPerFrame, self.line_simu_solverIters)
        QWidget.setTabOrder(self.line_simu_solverIters, self.line_simu_minTime)
        QWidget.setTabOrder(self.line_simu_minTime, self.line_simu_maxTime)
        QWidget.setTabOrder(self.line_simu_maxTime, self.cBox_simu_adjustToObjects)
        QWidget.setTabOrder(self.cBox_simu_adjustToObjects, self.pB_loadConfig)
        QWidget.setTabOrder(self.pB_loadConfig, self.pB_saveConfig)
        QWidget.setTabOrder(self.pB_saveConfig, self.pB_applyConfig)
        QWidget.setTabOrder(self.pB_applyConfig, self.line_numOfImages)
        QWidget.setTabOrder(self.line_numOfImages, self.line_totalOccurences)
        QWidget.setTabOrder(self.line_totalOccurences, self.line_minOccurences)
        QWidget.setTabOrder(self.line_minOccurences, self.line_maxOccurences)
        QWidget.setTabOrder(self.line_maxOccurences, self.pB_Regenerate)
        QWidget.setTabOrder(self.pB_Regenerate, self.pB_generate)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(6)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.WindowTitle.setText(QCoreApplication.translate("MainWindow", u"Data Generator", None))
        self.gBox_IO.setTitle(QCoreApplication.translate("MainWindow", u"Input/Output", None))
        self.lbl_gnd_dir.setText(QCoreApplication.translate("MainWindow", u"Ground directory", None))
        self.lbl_isNewFolder.setText(QCoreApplication.translate("MainWindow", u"Create New Folder", None))
        self.pB_search_output_dir.setText(QCoreApplication.translate("MainWindow", u"search", None))
        self.lbl_obj_dir.setText(QCoreApplication.translate("MainWindow", u"Object directory", None))
        self.lbl_output_dir.setText(QCoreApplication.translate("MainWindow", u"Output directory", None))
        self.pB_search_obj_dir.setText(QCoreApplication.translate("MainWindow", u"search", None))
        self.lbl_config_file.setText(QCoreApplication.translate("MainWindow", u"Config file", None))
        self.pB_search_gnd_dir.setText(QCoreApplication.translate("MainWindow", u"search", None))
        self.pB_search_config_file.setText(QCoreApplication.translate("MainWindow", u"search", None))
        self.lbl_Config.setText(QCoreApplication.translate("MainWindow", u"Configuration", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Renderer", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.lbl_unit.setText(QCoreApplication.translate("MainWindow", u"Unit", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Gravity (m/s2)", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"World", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Image Compression (%)", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Use Only CPU", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Number of Subdivision", None))
        self.comboBox_denoiser.setItemText(0, QCoreApplication.translate("MainWindow", u"INTEL", None))
        self.comboBox_denoiser.setItemText(1, QCoreApplication.translate("MainWindow", u"OPTIX", None))
        self.comboBox_denoiser.setItemText(2, QCoreApplication.translate("MainWindow", u"NONE", None))

        self.label_26.setText(QCoreApplication.translate("MainWindow", u"3D View Clip End", None))
        self.cBox_useOnlyCPU.setText("")
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"CC Textures Directory", None))
        self.line_engine.setText(QCoreApplication.translate("MainWindow", u"CYCLES", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Noise Treshold", None))
        self.cBox_ambientOcclusion.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"CPU Cores Count", None))
        self.comboBox_GPUType.setItemText(0, QCoreApplication.translate("MainWindow", u"CUDA", None))
        self.comboBox_GPUType.setItemText(1, QCoreApplication.translate("MainWindow", u"OPTIX", None))
        self.comboBox_GPUType.setItemText(2, QCoreApplication.translate("MainWindow", u"HIP", None))

        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Ambient Occlusion", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"3D View Clip Start", None))
        self.cBox_backgroundBlack.setText(QCoreApplication.translate("MainWindow", u"Pitch black", None))
        self.comboBox_unit.setItemText(0, QCoreApplication.translate("MainWindow", u"mm", None))
        self.comboBox_unit.setItemText(1, QCoreApplication.translate("MainWindow", u"cm", None))
        self.comboBox_unit.setItemText(2, QCoreApplication.translate("MainWindow", u"m", None))

        self.label_33.setText(QCoreApplication.translate("MainWindow", u"GPU Device Type", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Engine", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Background", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Denoiser", None))
        self.label_87.setText(QCoreApplication.translate("MainWindow", u"COCO Annotated Image", None))
        self.cBox_saveCocoAnnotatedImage.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Setting), QCoreApplication.translate("MainWindow", u"Setting", None))
        self.label_65.setText(QCoreApplication.translate("MainWindow", u"Linear Damping", None))
        self.cBox_obj_randomColor.setText("")
        self.cBox_obj_keppLoadedMaterial.setText("")
        self.label_73.setText(QCoreApplication.translate("MainWindow", u"Keep Loaded", None))
        self.label_74.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"Mininum", None))
        self.cBox_obj_sampling_adjust.setText("")
        self.label_69.setText(QCoreApplication.translate("MainWindow", u"Adjusted to Objects", None))
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"Material", None))
        self.cBox_obj_randomMaterial.setText("")
        self.label_71.setText(QCoreApplication.translate("MainWindow", u"Maximum", None))
        self.label_66.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.label_76.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_72.setText(QCoreApplication.translate("MainWindow", u"Defined", None))
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"Sampler", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u"Friction", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u"Config", None))
        self.label_70.setText(QCoreApplication.translate("MainWindow", u"Sampling Region (%)", None))
        self.label_120.setText(QCoreApplication.translate("MainWindow", u"Height", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Objects), QCoreApplication.translate("MainWindow", u"Objects", None))
        self.label_93.setText(QCoreApplication.translate("MainWindow", u"Adjust to Objects", None))
        self.label_112.setText(QCoreApplication.translate("MainWindow", u"Sampler", None))
        self.label_94.setText(QCoreApplication.translate("MainWindow", u"Defined [x,y,z]", None))
        self.label_108.setText(QCoreApplication.translate("MainWindow", u"Minimum", None))
        self.cBox_distractor_adjustSize.setText("")
        self.label_91.setText(QCoreApplication.translate("MainWindow", u"Size", None))
        self.label_109.setText(QCoreApplication.translate("MainWindow", u"Number", None))
        self.label_92.setText(QCoreApplication.translate("MainWindow", u"Sampling Region (%)", None))
        self.label_107.setText(QCoreApplication.translate("MainWindow", u"Maximum", None))
        self.label_121.setText(QCoreApplication.translate("MainWindow", u"Height", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Distractor), QCoreApplication.translate("MainWindow", u"Distractor", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"If no ground obj", None))
        self.label_117.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_77.setText(QCoreApplication.translate("MainWindow", u"Plane XY", None))
        self.label_79.setText(QCoreApplication.translate("MainWindow", u"Keep Loaded", None))
        self.label_118.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_75.setText(QCoreApplication.translate("MainWindow", u"Random Pick", None))
        self.label_81.setText(QCoreApplication.translate("MainWindow", u"Adjusted to Objects", None))
        self.label_85.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_83.setText(QCoreApplication.translate("MainWindow", u"Linear Damping", None))
        self.label_80.setText(QCoreApplication.translate("MainWindow", u"Defined", None))
        self.cBox_gnd_randomPick.setText("")
        self.label_113.setText(QCoreApplication.translate("MainWindow", u"Euler Rotation", None))
        self.label_78.setText(QCoreApplication.translate("MainWindow", u"Defined [x,y]", None))
        self.label_82.setText(QCoreApplication.translate("MainWindow", u"Friction", None))
        self.label_84.setText(QCoreApplication.translate("MainWindow", u"Material", None))
        self.label_116.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.cBox_gnd_XY_adjust.setText("")
        self.cBox_gnd_keepLoadedMaterial.setText("")
        self.cBox_gnd_randomMaterial.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Ground), QCoreApplication.translate("MainWindow", u"Ground", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Image Width", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Max. radius", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Max. Elevation", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Check", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Position", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Min. Elevation", None))
        self.label_86.setText(QCoreApplication.translate("MainWindow", u"Sampler", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Min. radius", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Image Height", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"Clip Start", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Defined [x,y,z]", None))
        self.cBox_cam_allObjectsFullyVisible.setText("")
        self.cBox_cam_randomRotation.setText("")
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.lbl_camera_config.setText(QCoreApplication.translate("MainWindow", u"Config", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"Clip End", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"No Background", None))
        self.cBox_cam_noWorldBackground.setText("")
        self.cBox_cam_randomPos.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Objects Fully Visible", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Center", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_114.setText(QCoreApplication.translate("MainWindow", u"Prefer Small Radius", None))
        self.cBox_cam_preferSmallRadius.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Camera), QCoreApplication.translate("MainWindow", u"Camera", None))
        self.label_89.setText(QCoreApplication.translate("MainWindow", u"Blend", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Defined [x,y,z]", None))
        self.label_98.setText(QCoreApplication.translate("MainWindow", u"Number", None))
        self.lbl_camera_sampler_2.setText(QCoreApplication.translate("MainWindow", u"Spot Light", None))
        self.label_115.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.cBox_spotLight_randomWatt.setText("")
        self.cBox_spotlight_toObjects.setText("")
        self.label_97.setText(QCoreApplication.translate("MainWindow", u"To Objects", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Max. Radius", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Min. Elevation", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Watt", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Plane XY", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Max. Watt", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Min. Radius", None))
        self.label_88.setText(QCoreApplication.translate("MainWindow", u"Config", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Min. Intensity", None))
        self.cBox_ceilLight_fitToGround.setText("")
        self.cBox_ceilLight_ENA.setText("")
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Position", None))
        self.label_95.setText(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_90.setText(QCoreApplication.translate("MainWindow", u"Spread Angle (\u00b0)", None))
        self.cBox_ceilLight_randomIntensity.setText("")
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Position", None))
        self.lbl_camera_config_2.setText(QCoreApplication.translate("MainWindow", u"Ceiling Light", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Defined [x,y,z]", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Intensity", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Defined [x,y]", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Max. Elevation", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Defined", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Min. Watt", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Max. Intensity", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Fit to Ground", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Defined", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Center", None))
        self.cBox_spotLight_randomPos.setText("")
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"Min. Height", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.cBox_ceilLight_randomPos.setText("")
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Max. Height", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Light), QCoreApplication.translate("MainWindow", u"Light", None))
        self.label_99.setText(QCoreApplication.translate("MainWindow", u"Substeps Per Frame", None))
        self.label_101.setText(QCoreApplication.translate("MainWindow", u"Solver Iters", None))
        self.label_103.setText(QCoreApplication.translate("MainWindow", u"Simulation Time", None))
        self.label_100.setText(QCoreApplication.translate("MainWindow", u"Check Object Interval", None))
        self.label_102.setText(QCoreApplication.translate("MainWindow", u"Mininum", None))
        self.label_105.setText(QCoreApplication.translate("MainWindow", u"Maximum", None))
        self.label_104.setText(QCoreApplication.translate("MainWindow", u"Adjust to Objects", None))
        self.cBox_simu_adjustToObjects.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Simulation), QCoreApplication.translate("MainWindow", u"Simulation", None))
        self.pB_loadConfig.setText(QCoreApplication.translate("MainWindow", u"Load Configuration", None))
        self.pB_saveConfig.setText(QCoreApplication.translate("MainWindow", u"Save Configuration", None))
        self.pB_applyConfig.setText(QCoreApplication.translate("MainWindow", u"Apply Config", None))
        self.label_106.setText(QCoreApplication.translate("MainWindow", u"Min. Occurences of a Class per Image", None))
        self.label_96.setText(QCoreApplication.translate("MainWindow", u"Number of Images", None))
        self.label_110.setText(QCoreApplication.translate("MainWindow", u"Max. Occurences of a Class per Image", None))
        self.label_111.setText(QCoreApplication.translate("MainWindow", u"Total Occurences of a Class in all Images", None))
        self.pB_Regenerate.setText(QCoreApplication.translate("MainWindow", u"Regenerate\n"
"Failed Images", None))
        self.pB_generate.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.lbl_progress.setText("")
    # retranslateUi

