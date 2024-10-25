# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Dataset_Window_UI.ui'
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
        MainWindow.resize(907, 717)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 901, 661))
        self.main_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(10, 0, 10, 5)
        self.WindowTitle = QLabel(self.verticalLayoutWidget)
        self.WindowTitle.setObjectName(u"WindowTitle")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.WindowTitle.setFont(font)
        self.WindowTitle.setMargin(3)
        self.WindowTitle.setIndent(4)

        self.main_layout.addWidget(self.WindowTitle)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(5, -1, 5, 15)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, -1, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(10)
        self.label_2.setFont(font1)
        self.label_2.setMargin(1)
        self.label_2.setIndent(3)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(15, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 2, 1, 1)

        self.line_Dataset = QLineEdit(self.verticalLayoutWidget)
        self.line_Dataset.setObjectName(u"line_Dataset")
        self.line_Dataset.setFont(font1)
        self.line_Dataset.setReadOnly(True)

        self.gridLayout.addWidget(self.line_Dataset, 0, 1, 1, 1)

        self.line_COCO = QLineEdit(self.verticalLayoutWidget)
        self.line_COCO.setObjectName(u"line_COCO")
        self.line_COCO.setFont(font1)
        self.line_COCO.setReadOnly(True)

        self.gridLayout.addWidget(self.line_COCO, 1, 1, 1, 1)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)
        self.label.setMargin(1)
        self.label.setIndent(3)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.outputLayout = QVBoxLayout()
        self.outputLayout.setSpacing(0)
        self.outputLayout.setObjectName(u"outputLayout")
        self.line_Output = QLineEdit(self.verticalLayoutWidget)
        self.line_Output.setObjectName(u"line_Output")
        self.line_Output.setFont(font1)
        self.line_Output.setReadOnly(True)

        self.outputLayout.addWidget(self.line_Output)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.outputLayout.addItem(self.verticalSpacer_2)

        self.outputLayout.setStretch(1, 1)

        self.gridLayout.addLayout(self.outputLayout, 2, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setMargin(1)
        self.label_3.setIndent(3)

        self.verticalLayout_2.addWidget(self.label_3)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)


        self.gridLayout.addLayout(self.verticalLayout_2, 2, 0, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.pB_ChooseDataset = QPushButton(self.verticalLayoutWidget)
        self.pB_ChooseDataset.setObjectName(u"pB_ChooseDataset")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_ChooseDataset.sizePolicy().hasHeightForWidth())
        self.pB_ChooseDataset.setSizePolicy(sizePolicy)
        self.pB_ChooseDataset.setFont(font1)

        self.gridLayout_2.addWidget(self.pB_ChooseDataset, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 5)
        self.gridLayout_2.setColumnStretch(2, 3)

        self.main_layout.addLayout(self.gridLayout_2)

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName(u"line")
        font2 = QFont()
        font2.setPointSize(8)
        self.line.setFont(font2)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setFrameShape(QFrame.HLine)

        self.main_layout.addWidget(self.line)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.verticalLayoutWidget)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)


        self.main_layout.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_layout.addItem(self.verticalSpacer)

        self.horizontalLayout_progress = QHBoxLayout()
        self.horizontalLayout_progress.setObjectName(u"horizontalLayout_progress")
        self.lbl_progress = QLabel(self.verticalLayoutWidget)
        self.lbl_progress.setObjectName(u"lbl_progress")

        self.horizontalLayout_progress.addWidget(self.lbl_progress)

        self.progressBar = QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setFont(font2)
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QProgressBar.TopToBottom)

        self.horizontalLayout_progress.addWidget(self.progressBar)


        self.main_layout.addLayout(self.horizontalLayout_progress)

        self.main_layout.setStretch(3, 20)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 907, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.WindowTitle.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"COCO annotations", None))
        self.line_Dataset.setPlaceholderText(QCoreApplication.translate("MainWindow", u"choose a Dataset directory", None))
        self.line_COCO.setPlaceholderText(QCoreApplication.translate("MainWindow", u"auto-search in Dataset directory", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Dataset", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Output", None))
        self.pB_ChooseDataset.setText(QCoreApplication.translate("MainWindow", u"Choose\n"
"Dataset", None))
        self.lbl_progress.setText("")
    # retranslateUi

