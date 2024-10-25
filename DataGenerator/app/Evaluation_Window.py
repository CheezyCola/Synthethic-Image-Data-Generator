import PySide2.QtCore as QtCore
import PySide2.QtGui as qtgui
import PySide2.QtWidgets  as qtw
import ui.Dataset_Window_UI as dataset_win

from pycocotools.coco import COCO
import os
import traceback
import sys
import pandas as pd

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
matplotlib.use('Qt5Agg')

from DataGenerator.evaluator.analyzer import visualize_class_occlusion

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
        df = None
        try:
            returned = self.fn(*self.args, **self.kwargs)
            if returned is not None:    
                done= returned[0]
                df = returned[1]

        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]  
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if done:
                self.signals.result.emit(df)
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
        if self.itemAt(row):
            for j in reversed(range(self.itemAt(row).count())):
                if isinstance (self.itemAt(row).itemAt(j), qtw.QLayout):
                    self.clearLayout(self.itemAt(row).itemAt(j))
            self.clearLayout(self.itemAt(row))
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
            if self.itemAt(row).itemAt(col).layout():
                for x in reversed(range(self.itemAt(row).itemAt(col).layout().count())):
                    print(type(self.itemAt(row).itemAt(col).itemAt(x)))
                    
                self.clearLayout(self.itemAt(row).itemAt(col).layout())
                self.itemAt(row).itemAt(col).layout().deleteLater()
                self.itemAt(row).itemAt(col).layout().setParent(None)
                
    def clear(self):
        for i in reversed(range(self.count())):
            for j in reversed(range(self.itemAt(i).count())):
                self.itemAt(i).itemAt(j).widget().setParent(None)
        for i in reversed(range(self.count())):
            self.itemAt(i).setParent(None)

class Evaluation_Window(qtw.QMainWindow, dataset_win.Ui_MainWindow, Signal, QtCore.QObject):
    def __init__(self, testing=False, *args, **kwargs):
        self._testing = testing
        super(Evaluation_Window, self).__init__(*args, **kwargs)
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
        
        ##threading
        self.threadpool = QtCore.QThreadPool()
        self._running = False
        self._worker = None

        # custom widgets
        self.line_num_img = qtw.QLineEdit()
        self.line_occlusion_thres = qtw.QLineEdit("20.00")
        self.pB_evaluate = qtw.QPushButton("Evaluate")
        # a figure instance to plot on
        self.figure = plt.figure(tight_layout=True)
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.initialize()

         # Connect slots and signals
        self.pB_ChooseDataset.clicked.connect(self.open_path)
        
    def initialize(self):
        # Draw general
        self.WindowTitle.setText("Data Evaluation")
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

    def drawFigure(self, df):
        # get the total for each row
        total = df['Total']

        class_ids = df.index.to_list()
        class_names = df['Name'].to_list()
        class_labels = ["{} - {} ".format(x[0], x[1]) for x in zip(class_ids, class_names)]

        if "Total" in df.columns:
            df = df.drop('Total', axis=1)
        if "Name" in df.columns:
            df = df.drop('Name', axis=1)

        # instead of ax.hold(False)
        self.figure.clear()
        # create an axis
        _ax = self.figure.add_subplot(1,1,1)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        # _ax.plot(ax=ax)        

        # calculate the percent for each row
        per = df.div(total, axis=0).mul(100).round(2)

        # plot the pivoted dataframe
        __ax = df.plot(use_index=True, kind='bar', stacked=True, rot=0,
                       title="Number of Instances by Class and Occlusion Difficulty with Threshold {}%".format(
                           self.line_occlusion_thres.text()), ax = _ax)

        # set the colors for each Class
        segment_colors = {'Easy': 'black', 'Difficult': 'red'}

        # iterate through the containers
        for c in __ax.containers:
            # get the current segment label (a string); corresponds to column / legend
            label = c.get_label()

            # create custom labels with the bar height and the percent from the per column
            # the column labels in per and dfp are int, so convert label to int
            labels = [f'{int(v.get_height())}\n({row}%)' if v.get_height() > 0 else '' for v, row in zip(c, per[label])]

            # add the annotation
            __ax.bar_label(c, labels=labels, label_type='center', color=segment_colors[label])

        mean = total.sum()/len(total)
        __ax.axhline(mean, color='darkgreen', ls='--')
        __ax.text(1, mean, f'mean: {mean:.3f}\n',ha='right',
                va='center', color='darkgreen', transform=__ax.get_yaxis_transform())

        # move the legend
        class_handles = [Line2D([0], [0], c='k', marker='o', linestyle='') for x in class_labels]
        handles, labels = __ax.get_legend_handles_labels()
        _ = __ax.legend(handles=handles+class_handles, labels=labels+class_labels,
                        bbox_to_anchor=(1, 1.01), loc='upper left')
        
        # refresh canvas
        self.canvas.draw()

    def hideProgress(self, hide):
        self.lbl_progress.setHidden(hide)
        self.progressBar.setHidden(hide)

    def display_Output(self):
        self.train_path = os.path.join(self.Dataset_path, "train")
        self.validate_path = os.path.join(self.Dataset_path, "validate")
        self.test_path = os.path.join(self.Dataset_path, "test")

        self.outputs = [self.train_path, self.validate_path, self.test_path]

        for i, x in enumerate(self.outputs):
            if i < 1:
                self.line_Output.setText(x)
            else:
                line_output = qtw.QLineEdit(x)
                line_output.setReadOnly(True)
                line_output.setFont(qtgui.QFont("MS Shell Dlg 2",10))
                self.outputLayout.addWidget(line_output)
   
    def changeTextColor(self, widget, color=""):
        _color = "color: {};".format(color)
        widget.setStyleSheet(_color)
   
    def open_path(self):
        try:
            self.Dataset_path = qtw.QFileDialog.getExistingDirectory(self, "Open a Dataset folder",
                                                                     "",
                                                                     qtw.QFileDialog.ShowDirsOnly)
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
            img_num = len([name for name in os.listdir(self.Images_path) if
                            os.path.isfile(os.path.join(self.Images_path, name)) and ".jpg" in name])
            self.line_num_img.setText(str(img_num))
            self.show_class_id_name()
            self.widget.show()
            self.pB_evaluate.show()
        else:
            self.line_COCO.setText("\"coco_annotations.json\" is missing")
            self.changeTextColor(self.line_COCO, color="red")
            self.changeTextColor(self.line_Dataset, color="red")
            self.widget.hide()
            self.pB_evaluate.hide()
            self.figure.clear()
            
    def drawCustomUI(self):
        #########################################################################################
        lbl_num_img = qtw.QLabel("Number of Images found")
        lbl_num_img.setFont(qtgui.QFont("MS Shell Dlg 2",10))
        lbl_num_img.setAlignment(qtgui.Qt.AlignCenter)
        
        self.line_num_img.setReadOnly(True)
        self.line_num_img.setFont(qtgui.QFont("MS Shell Dlg 2",10))
        self.line_num_img.setAlignment(qtgui.Qt.AlignCenter)
        
        self.customGridLayout.addWidget(lbl_num_img, 0, 0)
        self.customGridLayout.addWidget(self.line_num_img, 0, 1)
        H_spacer02 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        H_spacer03 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.customGridLayout.addWidget(H_spacer02, 0, 2)
        self.customGridLayout.addWidget(H_spacer03, 0, 3)
        
        lbl_occlusion_thres = qtw.QLabel("Occlussion Difficulty Threshold (%)")
        lbl_occlusion_thres.setFont(qtgui.QFont("MS Shell Dlg 2",10))
        lbl_occlusion_thres.setAlignment(qtgui.Qt.AlignCenter)
        
        self.line_occlusion_thres.setFont(qtgui.QFont("MS Shell Dlg 2",10))
        self.line_occlusion_thres.setAlignment(qtgui.Qt.AlignCenter)
        
        self.customGridLayout.addWidget(lbl_occlusion_thres, 0, 4)
        self.customGridLayout.addWidget(self.line_occlusion_thres, 0, 5)
        H_spacer06 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        H_spacer07 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.customGridLayout.addWidget(H_spacer06, 0, 6)
        self.customGridLayout.addWidget(H_spacer07, 0, 7)
        ########################################################################################


        self.pB_evaluate.setStyleSheet("QPushButton {"
                                "font-size: 11pt;"
                                "font-weight: bold;"
                                "padding: 10px"
                                "}")
        self.pB_evaluate.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.pB_evaluate.clicked.connect(self.onClickedEvaluate)
        self.gridLayout_2.addWidget(self.pB_evaluate, 0, 3, 1, 1)
        #########################################################################################

        self.widget_V_Layout.addWidget(self.toolbar)
        self.widget_V_Layout.addWidget(self.canvas)
        self.widget_V_Layout.setStretch(0,0)
        self.widget_V_Layout.setStretch(1,0)
        self.widget_V_Layout.setStretch(2,10)

    def block(self, bool):
        self.pB_ChooseDataset.setDisabled(bool)
        self.line_Dataset.setReadOnly(bool)
        self.line_Output.setReadOnly(bool)
        self.line_COCO.setReadOnly(bool)
        self.line_occlusion_thres.setReadOnly(bool)

    def cancel(self):
        self._cont = False
        self.block(False)
        self.hideProgress(True)
        self.pB_evaluate.setText("Split")
        self.info("Splitting Cancelled", "The program will stop after completing current task.")

    def onClickedEvaluate(self):
        if not all([self.line_Dataset.text().strip(), self.line_COCO.text().strip()]):
            self.warning("Evaluation Not Allowed", "Missing entries in Input/Output.")
            return

        if self.pB_evaluate.text() == "Evaluate":
            try:
                float(self.line_occlusion_thres.text())
            except Exception as e:
                self.warning("Invalid Occlusion Threshold Input", e)
                return
            self.runEvaluation()
            self.pB_evaluate.setText("Cancel")
            self.block(True)
        else:
            self.cancel()
            self.pB_evaluate.setText("Evaluate")
            self.block(False)

    def runEvaluation(self):
        # visualize_class_occlusion(dataset_dir=self.Dataset_path, difficult_threshold=float(self.line_occlusion_thres.text()))
        try:
            # Execute
            callback = ProgressCallback()
            self._worker = Worker(visualize_class_occlusion,
                                  dataset_dir=self.line_Dataset.text(),
                                  difficult_threshold=float(self.line_occlusion_thres.text()),
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
            self.lbl_progress.setText("Evaluating ...")
        except Exception as e:
            self.warning("Error", str(e))

    def get_cont(self):
        return self._cont
        
    def progress_fn(self, x):  ##handes function callbacks output
       self.lbl_progress.setText(x[0])
       self.progressBar.setValue(x[1])
    
    def progress_result(self, x):
        df = x
        self.drawFigure(df)
        
    def progress_error(self, x):
        raise Exception("Thread error " + str(x[1])) from x[1]
    
    def progress_finish(self):
        self._running = False
        self._cont = False
        self.progressBar.setValue(100)
        self.lbl_progress.setText("Done")
        self.info("Splitting Complete", "Process Completed.")
        self.pB_evaluate.setText("Evaluate")
        self.hideProgress(True)
        self.block(False)
        self.Done_signal.emit(True)

    def show_class_id_name(self):
        coco = COCO(self.COCO_path)
        cat = coco.dataset["categories"]
        self.customGridLayout.deleteRow(1)
        
        lbl_classes = qtw.QLabel("Classes")
        lbl_classes.setFont(qtgui.QFont("MS Shell Dlg 2",10))
        lbl_classes.setAlignment(qtgui.Qt.AlignTop)
        self.customGridLayout.addWidget(lbl_classes, 1, 0)
        
        def divide_chunks(l, n): 
            # looping till length l 
            for i in range(0, len(l), n):  
                yield l[i:i + n]
        
        x = divide_chunks(cat, 12)
        
        gridLayout = qtw.QGridLayout()
        gridLayout.setSpacing(4)
        self.customGridLayout.addWidget(gridLayout, 1, 1)
        H_spacer12 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.customGridLayout.addWidget(H_spacer12, 1, 2)
        
        for row, _x in enumerate(x):
            lbl_id = qtw.QLabel("id")
            lbl_id.setFont(qtgui.QFont("MS Shell Dlg 2",9))
            lbl_id.setAlignment(qtgui.Qt.AlignTop)
            gridLayout.addWidget(lbl_id, row*4, 0)
            
            font_line = qtgui.QFont()
            font_line.setPointSize(5)
            
            HLine = qtw.QFrame()
            HLine.setFont(font_line)
            HLine.setFrameShadow(qtw.QFrame.Sunken)
            HLine.setFrameShape(qtw.QFrame.HLine)
            gridLayout.addWidget(HLine, row*4+1, 0)
            
            lbl_name = qtw.QLabel("name")
            lbl_name.setFont(qtgui.QFont("MS Shell Dlg 2",9))
            lbl_name.setAlignment(qtgui.Qt.AlignTop)
            gridLayout.addWidget(lbl_name, row*4+2, 0)
            
            VLine = qtw.QFrame()
            VLine.setFont(font_line)
            VLine.setFrameShadow(qtw.QFrame.Sunken)
            VLine.setFrameShape(qtw.QFrame.VLine)
            gridLayout.addWidget(VLine, row*4, 1)
            
            VLine2 = qtw.QFrame()
            VLine2.setFont(font_line)
            VLine2.setFrameShadow(qtw.QFrame.Sunken)
            VLine2.setFrameShape(qtw.QFrame.VLine)
            gridLayout.addWidget(VLine2, row*4+2, 1)
            
            i = 2
            for x in _x:
                _lbl_id = qtw.QLabel("{}".format(x["id"]))
                _lbl_id.setFont(qtgui.QFont("MS Shell Dlg 2",9))
                _lbl_id.setAlignment(qtgui.Qt.AlignCenter)
                gridLayout.addWidget(_lbl_id, row*4, i)
                _HLine = qtw.QFrame()
                _HLine.setFont(font_line)
                _HLine.setFrameShadow(qtw.QFrame.Sunken)
                _HLine.setFrameShape(qtw.QFrame.HLine)
                gridLayout.addWidget(_HLine, row*4+1, i)
                _line_name = qtw.QLineEdit("{}".format(x["name"]))
                _line_name.setReadOnly(True)
                _line_name.setFont(qtgui.QFont("MS Shell Dlg 2",9))
                _line_name.setAlignment(qtgui.Qt.AlignCenter)
                gridLayout.addWidget(_line_name, row*4+2, i)
                
                i += 1
                _VLine = qtw.QFrame()
                _VLine.setFont(font_line)
                _VLine.setFrameShadow(qtw.QFrame.Sunken)
                _VLine.setFrameShape(qtw.QFrame.VLine)
                gridLayout.addWidget(_VLine, row*4, i)
                
                _VLine2 = qtw.QFrame()
                _VLine2.setFont(font_line)
                _VLine2.setFrameShadow(qtw.QFrame.Sunken)
                _VLine2.setFrameShape(qtw.QFrame.VLine)
                gridLayout.addWidget(_VLine2, row*4+2, i)
                
                i += 1
            
            V_spacer = qtw.QSpacerItem(20, 3, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
            gridLayout.addItem(V_spacer, row*4+3, 0)
        #########################################################################################
        
    def warning(self, title:str, msg:str):
        qtw.QMessageBox.warning(self, title, msg, qtw.QMessageBox.Ok)

    def info(self, title:str, msg:str):
        qtw.QMessageBox.information(self, title, msg, qtw.QMessageBox.Ok)

def main():
    app = qtw.QApplication()
    try:
        window = Evaluation_Window(testing=False)
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

