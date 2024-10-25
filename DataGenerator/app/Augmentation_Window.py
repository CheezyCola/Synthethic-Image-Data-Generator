import PySide2.QtCore as QtCore
import PySide2.QtGui as qtgui
import PySide2.QtWidgets  as qtw
import ui.Dataset_Window_UI as dataset_win

import os
import sys
import traceback
from DataGenerator.augmentator.augmentator import Augmentator
from DataGenerator.augmentator.ui_function_mapping import *

class WorkerSignals(QtCore.QObject):
    """ Defines the signals available from a running worker thread """
    finished = QtCore.Signal(object)  #finished - object data returned from processing, anything
    error = QtCore.Signal(tuple)  #error - tuple (exctype, value, traceback.format_exc() )
    result = QtCore.Signal(object)  #result - object data returned from processing, anything
    progress = QtCore.Signal(object)  #progress - tuple(int, str) int indicating % progress, str indicating step

class Worker(QtCore.QRunnable):  ##with no progress signal
    def __init__(self, callback, *args, **kwargs):
        '''
        Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
        :param callback: The function callback to run on this worker thread. Supplied args and
                    kwargs will be passed through to the runner.
        :type callback: function
        :param args: Arguments to pass to the callback function
        :param kwargs: Keywords to pass to the callback function
        '''
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = callback
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        
        # if 'progress_callback' in self.kwargs.keys():
        #     self.kwargs['progress_callback'] = self.signals.progress

    @QtCore.Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        done = None
        try:
            returned = self.fn(*self.args, **self.kwargs)
            if returned is not None:    
                done=returned

        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]  
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if done:
                self.signals.result.emit(None)
        finally:
            if done:
                self.signals.finished.emit(None)  # Done

class ProgressCallback(QtCore.QObject):
    progressChanged = QtCore.Signal(object)

    def __call__(self, task, value):
        self.progressChanged.emit((task, value))

class Signal(object):
    Done_signal = QtCore.Signal(object)
    
class CustomGridLayout(qtw.QVBoxLayout):
    def __init__(self):
        super(CustomGridLayout, self).__init__()
        self.setAlignment(QtCore.Qt.AlignTop)  # !!!
        self.setSpacing(10)

    def addWidget(self, widget, row, col):
        # 1. How many horizontal layouts (rows) are present?
        horLaysNr = self.count()

        # 2. Add rows if necessary
        if row < horLaysNr:
            pass
        else:
            while row >= horLaysNr:
                lyt = qtw.QHBoxLayout()
                lyt.setAlignment(QtCore.Qt.AlignLeft)
                self.addLayout(lyt)
                horLaysNr = self.count()

        # 3. Insert the widget at specified column
        if isinstance(widget, qtw.QWidget):
            self.itemAt(row).insertWidget(col, widget)
        elif isinstance(widget, qtw.QLayout):
            self.itemAt(row).addLayout(widget)
        else:
            self.itemAt(row).addItem(widget)

    def insertRow(self, row):
        lyt = qtw.QHBoxLayout()
        lyt.setAlignment(QtCore.Qt.AlignLeft)
        self.insertLayout(row, lyt)

    def deleteRow(self, row):
        for j in reversed(range(self.itemAt(row).count())):
            self.itemAt(row).itemAt(j).widget().setParent(None)
        self.itemAt(row).setParent(None)
    
    def clearLayout(self, Layout):
        children = []
        for i in reversed(range(Layout.count())):
            layout = Layout.itemAt(i)
            if layout: 
                child = layout.widget()
            else:
                layout = Layout
            if child:
                children.append(child)
            elif layout.spacerItem():
                Layout.removeItem(layout)

        for child in children:
            child.deleteLater()
            child.setParent(None)
            
    def deleteLayout(self, row, col):
        if self.itemAt(row).itemAt(col):
            # for x in reversed(range(self.itemAt(row).itemAt(col).layout().count())):
            #     print(type(self.itemAt(row).itemAt(col).itemAt(x)))
            self.clearLayout(self.itemAt(row).itemAt(col).layout())
            self.itemAt(row).itemAt(col).layout().deleteLater()
            self.itemAt(row).itemAt(col).layout().setParent(None)
                
    def clear(self):
        for i in reversed(range(self.count())):
            for j in reversed(range(self.itemAt(i).count())):
                self.itemAt(i).itemAt(j).widget().setParent(None)

        for i in reversed(range(self.count())):
            self.itemAt(i).setParent(None)


class Augmentation_Window(qtw.QMainWindow, dataset_win.Ui_MainWindow, Signal, QtCore.QObject):
    def __init__(self, testing=False, *args, **kwargs):
        self._testing = testing
        super(Augmentation_Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.centralwidget = qtw.QWidget()
        self.centralwidget.setLayout(self.main_layout)
        self.setCentralWidget(self.centralwidget)
        self.widget_V_Layout = qtw.QVBoxLayout()
        self.customGridLayout = CustomGridLayout()
        self.widget_V_Layout.addLayout(self.customGridLayout)
        self.widget.setLayout(self.widget_V_Layout)
        # variables
        self.Dataset_path = ""
        self.COCO_path = ""
        self.Output = []
        self.Images_path = ""
        
        # custom variables
        self.Transforms = {
            "Pixel-level": [
                "Gaussian Noise",
                "Gaussian Blur",
                "Random Brightness Contrast",
                "Hue Saturation Value",
                "Random Gamma",
                "Motion Blur",
                "CLAHE"
            ],
            "Spatial-level": [
                "Vertical Flip",
                "Horizontal Flip",
                "Rotate"
            ],
            "Cropping": [
                "Random Crop Near Bounding Box (+Resize)",
                "Random Sized Bounding Box Safe Crop (+Resize)"
            ]
        }
        
        self.tree = qtw.QTreeWidget()
        self.gridLayout = qtw.QGridLayout()
        self.checked_parent = []
        self.checked_pixel = []
        self.checked_spatial = []
        self.checked_cropping = []
        self.line_img_num = qtw.QLineEdit()
        self.line_out_img_num = qtw.QLineEdit()
        self.cBox_save_annotated_img = qtw.QCheckBox()
        self.line_output2 = qtw.QLineEdit()
        self.line_output2.setFont(qtgui.QFont("MS Shell Dlg 2",10))
        self.pB_augmentate = qtw.QPushButton("Augmentate")
        
        ##threading
        self.threadpool = QtCore.QThreadPool()
        self._running = False
        self._worker = None

        self.initialize()

        # Connect slots and signals
        self.pB_ChooseDataset.clicked.connect(self.open_path)
        self.cBox_save_annotated_img.stateChanged.connect(self.updateOutput)
        self.pB_augmentate.clicked.connect(self.onClickedAugmentate)
        
    def initialize(self):
        # Draw general
        self.WindowTitle.setText("Data Augmentation")
        self.statusbar.setMaximumHeight(1)
        widget_retain = self.widget.sizePolicy()
        widget_retain.setRetainSizeWhenHidden(True)
        self.widget.setSizePolicy(widget_retain)
        self.widget.hide()
        self.line_Dataset.clear()
        self.line_COCO.clear()
        self.line_Output.clear()
        self.changeTextColor(self.line_Dataset, color="black")
        self.changeTextColor(self.line_COCO, color="black")
        self.lbl_progress.setFont(qtgui.QFont("MS Shell Dlg 2",8))
        self.lbl_progress.setIndent(4)
        self.progressBar.setFont(qtgui.QFont("MS Shell Dlg 2",8))
        self.progressBar.setStyleSheet("QProgressBar{"
                                       "max-height: 12px;}")
        self.hideProgress(True)
        
        # Draw Custom UI
        self.drawCustomUI()

    def hideProgress(self, hide):
        self.lbl_progress.setHidden(hide)
        self.progressBar.setHidden(hide)

    def updateOutput(self, state):
        if self.cBox_save_annotated_img.checkState():
            self.outputLayout.insertWidget(1, self.line_output2)
        else:
            self.outputLayout.removeWidget(self.line_output2)
            self.line_output2.setParent(None)

    def changeTextColor(self, widget, color=""):
        _color = "color: {};".format(color)
        widget.setStyleSheet(_color)
   
    def open_path(self):
        try:
            _path = qtw.QFileDialog.getExistingDirectory(self, "Open a Dataset folder",
                                                                     "",
                                                                     qtw.QFileDialog.ShowDirsOnly)
            if _path:
                self.Dataset_path = _path
                self.line_Dataset.setText(self.Dataset_path)
                self.search_COCO()
        except Exception as e:
            self.warning("Error", str(e))
    
    def search_COCO(self):
        self.COCO_path = os.path.join(os.path.join(self.Dataset_path, "coco_data"), "coco_annotations.json")
        if os.path.isfile(self.COCO_path):
            self.line_COCO.setText(self.COCO_path)
            self.changeTextColor(self.line_COCO, color="green")
            self.changeTextColor(self.line_Dataset, color="green")
            self.Images_path = os.path.join(os.path.join(self.Dataset_path, "coco_data"), "images")
            self.COCO_Images_path = os.path.join(os.path.join(self.Dataset_path, "coco_data"), "annotated_images")
            self.line_Output.setText(self.Images_path)
            self.line_output2.setText(self.COCO_Images_path)
            img_num = len([name for name in os.listdir(self.Images_path) if
                            os.path.isfile(os.path.join(self.Images_path, name)) and ".jpg" in name])
            self.line_img_num.setText(str(img_num))
            self.line_out_img_num.setText(str(img_num))
            self.widget.show()
        else:
            self.line_COCO.setText("\"coco_annotations.json\" is missing")
            self.changeTextColor(self.line_COCO, color="red")
            self.changeTextColor(self.line_Dataset, color="red")
            self.line_Output.clear()
            self.line_output2.clear()
            self.widget.hide()
    
    def drawCustomUI(self):
        ############################################ Tree ############################################
        header_font = qtgui.QFont()
        header_font.setPixelSize(20)
        self.tree.headerItem().setText(0, "  Transfrom")
        self.tree.headerItem().setFont(0, header_font)

        font = qtgui.QFont()
        font.setPixelSize(18)
        child_font = qtgui.QFont()
        child_font.setPixelSize(16)
        for i, (k,v) in enumerate(self.Transforms.items()):
            parent = qtw.QTreeWidgetItem(self.tree)
            parent.setText(0, "{}".format(k))
            parent.setFont(0, font)
            parent.setFlags(parent.flags() | QtCore.Qt.ItemFlag.ItemIsAutoTristate | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
            for x in v:
                child = qtw.QTreeWidgetItem(parent)
                child.setFlags(child.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                child.setText(0, "{}".format(x))
                child.setFont(0, child_font)
                child.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
        
        self.tree.itemChanged[qtw.QTreeWidgetItem, int].connect(self.get_item)
        
        self.tree.setStyleSheet("QTreeView::item {"
                                "padding: 5px;"
                                "color: blue;"
                                "}")
        self.tree.show() 
        self.customGridLayout.addWidget(self.tree, 0, 0)
        ############################################ Tree ############################################
        
        self.show_process() # in customGridLayout position (0,1) 
        
        V_spacer10 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Fixed)
        self.customGridLayout.addWidget(V_spacer10, 1, 0)

        ############################################ img num ############################################
        gridLayout2 = qtw.QGridLayout()
        gridLayout2.setSpacing(3)
        self.widget_V_Layout.addLayout(gridLayout2)

        font = qtgui.QFont("MS Shell Dlg 2",11)

        lbl_img_num = qtw.QLabel("Number of Input Image")
        lbl_img_num.setFont(font)
        lbl_img_num.setAlignment(qtgui.Qt.AlignVCenter)
        lbl_img_num.setIndent(5)
        lbl_out_img_num = qtw.QLabel("Number of Output Image")
        lbl_out_img_num.setFont(font)
        lbl_out_img_num.setAlignment(qtgui.Qt.AlignVCenter)
        lbl_out_img_num.setIndent(5)
        
        self.line_img_num.setFont(font)
        self.line_img_num.setReadOnly(True)
        self.line_img_num.setAlignment(qtgui.Qt.AlignCenter)
        self.line_out_img_num.setFont(font)
        self.line_out_img_num.setReadOnly(True)
        self.line_out_img_num.setAlignment(qtgui.Qt.AlignCenter)
        
        gridLayout2.addWidget(lbl_img_num, 0, 0)
        gridLayout2.addWidget(self.line_img_num, 0, 2)
        gridLayout2.addWidget(lbl_out_img_num, 1, 0)
        gridLayout2.addWidget(self.line_out_img_num, 1, 2)
        H_spacer01 = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        H_spacer03 = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        gridLayout2.addItem(H_spacer01, 0, 1)
        gridLayout2.addItem(H_spacer03, 0, 3)
        ############################################ img num ############################################

        ############################################ save COCO ############################################
        # HLayout = qtw.QHBoxLayout()
        lbl_save_annotated_img = qtw.QLabel("COCO annotated image")
        lbl_save_annotated_img.setAlignment(qtgui.Qt.AlignCenter)
        lbl_save_annotated_img.setFont(font)
        lbl_save_annotated_img.setIndent(5)
        lbl_save_annotated_img.setAlignment(qtgui.Qt.AlignCenter)
        self.cBox_save_annotated_img.setText("Save")
        self.cBox_save_annotated_img.setFont(font)
        gridLayout2.addWidget(lbl_save_annotated_img, 2, 0)
        gridLayout2.addWidget(self.cBox_save_annotated_img, 2, 2)
        ############################################ save COCO ############################################

        ############################################ augmentate ############################################
        self.pB_augmentate.setStyleSheet("QPushButton {"
                                    "font-size: 11pt;"
                                    "font-weight: bold;"
                                    "padding: 10px"
                                    "}")
        self.pB_augmentate.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        gridLayout2.addWidget(self.pB_augmentate, 0, 4, 3, 1)
        gridLayout2.setColumnStretch(0,1)
        gridLayout2.setColumnStretch(1,0)
        gridLayout2.setColumnStretch(2,1)
        gridLayout2.setColumnStretch(3,7)
        gridLayout2.setColumnStretch(4,1)
        ############################################ augmentate ############################################
    
        self.customGridLayout.setStretch(0,6)
        self.customGridLayout.setStretch(1,0)
        self.customGridLayout.setStretch(2,1)
    
    def onClickedAugmentate(self):
        if not any([self.checked_pixel, self.checked_spatial, self.checked_cropping]):
            self.warning("Augmentation Refused", "No input for augmentations transforms is selected.")
            return
        
        self.runAugmentation()

    def runAugmentation(self):
        Aug =  Augmentator(self.Dataset_path, self.cBox_save_annotated_img.checkState())
        if self.checked_pixel:
            transforms = [ui_function_mapping[x] for x in self.checked_pixel]
            Aug.pixel_transforms = transforms
        else:
            Aug.pixel_transforms = []
        if self.checked_spatial:
            transforms = [ui_function_mapping[x] for x in self.checked_spatial]
            Aug.spatial_transforms = transforms
        else:
            Aug.spatial_transforms = []
        if self.checked_cropping:
            transforms = [ui_function_mapping[x] for x in self.checked_cropping]
            Aug.cropping_transforms = transforms
        else:
            Aug.cropping_transforms = []

        try:
            # Execute
            callback = ProgressCallback()
            self._worker = Worker(Aug.augmentate,
                                  check_CANCEL=self.get_cont,
                                  progress_callback=callback)
            self._worker.signals.result.connect(self.progress_result)
            self._worker.signals.error.connect(self.progress_error)
            self._worker.signals.finished.connect(self.progress_finish)
            callback.progressChanged.connect(self.progress_fn)

            self._running = True          
            self._cont = True
            self.threadpool.start(self._worker)
            self.hideProgress(False)
            self.lbl_progress.setText("Augmentating ...")
        except Exception as e:
            self.warning("Error", str(e))

    def block(self, bool):
        self.pB_ChooseDataset.setDisabled(bool)
        self.line_Dataset.setReadOnly(bool)
        self.line_Output.setReadOnly(bool)
        self.line_COCO.setReadOnly(bool)
        self.tree.setDisabled(bool)

    def cancel(self):
        self._cont = False
        self.block(False)
        self.hideProgress(True)
        self.pB_augmentate.setText("Augmentate")
        self.info("Augmentation Cancelled", "The program will stop after completing current task.")
        
    def get_cont(self):
        return self._cont
        
    def progress_fn(self, x):  ##handes function callbacks output
       self.lbl_progress.setText(x[0])
       self.progressBar.setValue(x[1])
    
    def progress_result(self, x):
        pass
        
    def progress_error(self, x):
        raise Exception("Thread error " + str(x[1])) from x[1]
    
    def progress_finish(self):
        self._running = False
        self._cont = False
        self.progressBar.setValue(100)
        self.lbl_progress.setText("Done")
        self.info("Augmentation Complete", "Please find the augmentated images inside \'" + self.line_Output.text() + "\'.")
        self.pB_augmentate.setText("Augmentation")
        self.hideProgress(True)
        self.block(False)
        self.Done_signal.emit(True)

    def get_item(self, item, column):
        w_name = item.text(column)
        if item.checkState(column) == QtCore.Qt.Checked or item.checkState(column) == QtCore.Qt.PartiallyChecked:
            # Checked or partially checked
            if not item.parent(): # parent
                if not w_name in self.checked_parent:
                    self.checked_parent.append(w_name)
                if "Cropping" in self.checked_parent:
                    temp = [x for x in self.checked_parent if x != "Cropping"]
                    self.checked_parent = temp
                    self.checked_parent.append("Cropping")
                self.customGridLayout.deleteLayout(0,1)
                self.show_process()
            else: # child
                # print(f'{item.text(column)} was checked')
                if item.parent().text(column) == "Pixel-level":
                    self.checked_pixel.append(w_name)
                elif item.parent().text(column) == "Spatial-level":
                    print("haah")
                    self.checked_spatial.append(w_name)
                elif item.parent().text(column) == "Cropping":
                    self.checked_cropping.append(w_name)                       
        else:
            # Not checked
            if not item.parent(): # parent
                if w_name in self.checked_parent:
                    self.checked_parent.remove(w_name)
                self.customGridLayout.deleteLayout(0,1)
                self.show_process()
            else: # child
                # print(f'{item.text(column)} was unchecked')
                if item.parent().text(column) == "Pixel-level":
                    self.checked_pixel.remove(w_name)
                elif item.parent().text(column) == "Spatial-level":
                    self.checked_spatial.remove(w_name)
                elif item.parent().text(column) == "Cropping":
                    self.checked_cropping.remove(w_name)
    
    def update_process(self):
        def Box(text: str, color=None):
            if text == "Input Images":
                pass
            elif text != "Cropping":
                text = "Input Images -> " + text
            else:
                temp = ["Input Images"]+[x for x in self.checked_parent if x != "Cropping"]
                text = "(" + " + ".join(temp) + ") -> " + text
            box = qtw.QLabel(text)
            box.setMargin(5)
            box.setFont(qtgui.QFont("MS Shell Dlg 2",11))
            box.setAlignment(qtgui.Qt.AlignCenter)
            if color:
                color = "background-color : {}".format(color)
                box.setStyleSheet(color)
            return box
        
        row = self.gridLayout.rowCount()
        if row == 1:
            self.gridLayout.addWidget(Box("Input Images", "grey"), row, 1, rowSpan = 1, colSpan = 2, alignment = QtCore.Qt.Alignment())
        
        row = self.gridLayout.rowCount()
        ori_num = None
        if self.line_img_num.text() != "":
            ori_num = int(self.line_img_num.text())
        out_num = ori_num
        
        for aug in self.checked_parent:
            plus = qtw.QLabel("+")
            plus.setFont(qtgui.QFont("MS Shell Dlg 2",11))
            plus.setAlignment(qtgui.Qt.AlignCenter)
            self.gridLayout.addWidget(plus, row, 1, rowSpan = 1, colSpan = 2, alignment = QtCore.Qt.Alignment())
            self.gridLayout.addWidget(Box(aug, "grey"), row+1, 1, rowSpan = 1, colSpan = 2, alignment = QtCore.Qt.Alignment())
            row += 2
            
            if ori_num:
                if aug != "Cropping":
                    out_num += ori_num
                else:
                    out_num += out_num
                
                self.line_out_img_num.setText(str(out_num))
        
        if not self.checked_parent:
            self.line_out_img_num.setText(str(ori_num))
                         
    def show_process(self):
        ############################################ Process ############################################
        def Box(text: str, color=None):
            box = qtw.QLabel(text)
            box.setMargin(5)
            box.setFont(qtgui.QFont("MS Shell Dlg 2",11))
            box.setAlignment(qtgui.Qt.AlignCenter)
            if color:
                color = "background-color : {}".format(color)
                box.setStyleSheet(color)
            return box
        
        self.gridLayout = qtw.QGridLayout()
        self.gridLayout.setSpacing(4)
        self.customGridLayout.addWidget(self.gridLayout, 0, 1)
        
        H_spacer00 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        H_spacer02 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        
        self.gridLayout.addItem(H_spacer00, 0, 0)
        self.gridLayout.addWidget(Box("Output are:", "cyan"), 0, 1, rowSpan = 1, colSpan = 2, alignment = QtCore.Qt.Alignment())
        self.gridLayout.addItem(H_spacer02, 0, 2)
        self.gridLayout.setColumnStretch(0,1)
        self.gridLayout.setColumnStretch(1,3)
        self.gridLayout.setColumnStretch(2,1)

        self.update_process()
        ############################################ Process ############################################

    def warning(self, title:str, msg:str):
        qtw.QMessageBox.warning(self, title, msg, qtw.QMessageBox.Ok)

    def info(self, title:str, msg:str):
        qtw.QMessageBox.information(self, title, msg, qtw.QMessageBox.Ok)

def main():
    app = qtw.QApplication()
    try:
        window = Augmentation_Window(testing=False)
        window.setWindowFlags(window.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        window.setWindowFlags(window.windowFlags() & QtCore.Qt.CustomizeWindowHint)
#        window.setWindowFlags(window.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        window.show()
    except Exception as e:
        print("Error:", e)
    else:
        app.exec_()
    finally:
        app.quit()
    
if __name__ == '__main__':
    main()

