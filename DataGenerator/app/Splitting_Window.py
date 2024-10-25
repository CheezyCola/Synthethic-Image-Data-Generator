import PySide2.QtCore as QtCore
import PySide2.QtGui as qtgui
import PySide2.QtWidgets  as qtw
import ui.Dataset_Window_UI as dataset_win

import os
import sys
import traceback
from DataGenerator.splitter.splitter import train_valid_test_split

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
        dfs = None
        index_lists = None
        try:
            returned = self.fn(*self.args, **self.kwargs)
            if returned is not None:    
                done= returned[0]
                dfs = returned[1]
                index_lists = returned[2]
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]  
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if dfs:
                self.signals.result.emit((dfs, index_lists))
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

    def clear(self):
        for i in reversed(range(self.count())):
            for j in reversed(range(self.itemAt(i).count())):
                self.itemAt(i).itemAt(j).widget().setParent(None)
        for i in reversed(range(self.count())):
            self.itemAt(i).setParent(None)

class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(int(self._data.iloc[index.row(), index.column()]))
        return None

    # def headerData(self, col, orientation, role):
    #     if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
    #         return self._data.columns[col]
    #     return None
    
    def headerData(self, rowcol, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[rowcol]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self._data.index[rowcol]
        return None

class Splitting_Window(qtw.QMainWindow, dataset_win.Ui_MainWindow, Signal, QtCore.QObject):
    def __init__(self, testing=False, *args, **kwargs):
        self._testing = testing
        super(Splitting_Window, self).__init__(*args, **kwargs)
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
        self.train_path = ""
        self.validate_path = ""
        self.test_path = ""
        self.output = []
        self.train = 0.70
        self.valid = 0.15
        self.test = 0.15

        ##threading
        self.threadpool = QtCore.QThreadPool()
        self._running = False
        self._worker = None
        
        # custom widgets
        self.line_train = qtw.QLineEdit("{:.3f}".format(self.train))
        self.line_valid = qtw.QLineEdit("{:.3f}".format(self.valid))
        self.line_test = qtw.QLineEdit("{:.3f}".format(self.test))
        self.lbl_pressEnter = qtw.QLabel("Press Enter to apply")
        self.pB_split = qtw.QPushButton("Split")
        
        self.initialize()
        
        # Connect slots and signals
        self.pB_ChooseDataset.clicked.connect(self.open_path)
        self.line_train.returnPressed.connect(self.updateRatio(self.line_train, self.line_valid, self.line_test, 1))
        self.line_valid.returnPressed.connect(self.updateRatio(self.line_train, self.line_valid, self.line_test, 2))
        self.line_test.returnPressed.connect(self.updateRatio(self.line_train, self.line_valid, self.line_test, 3))
        self.line_train.textChanged.connect(self.hint)
        self.line_valid.textChanged.connect(self.hint)
        self.line_test.textChanged.connect(self.hint)
        
    def initialize(self):
        # Draw general
        self.WindowTitle.setText("Data Splitting")
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
    
    def drawTables(self, dfs, index_lists):
        for df, index in zip(dfs, index_lists):
            index = [int(x) for x in index]
            temp = df.sum()
            df.insert(loc=0, column="index", value=index)
            df.loc['Total'] = temp
        
        name = ["Training", "Validation", "Testing"]
        for i, df in enumerate(dfs):
            label = qtw.QLabel(name[i])
            table_view = qtw.QTableView()
            model = PandasModel(df)
            table_view.setModel(model)
            self.gridLayout_table.addWidget(label, i*3, 0)
            self.gridLayout_table.addWidget(table_view, (i*3)+1, 0, 1,10)
            V_spacer = qtw.QSpacerItem(5, 20, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.MinimumExpanding)
            self.gridLayout_table.addItem(V_spacer, (i*3)+2, 0, 1,10)

    def clearTables(self):
        for i in reversed(range(self.gridLayout_table.count())): 
            self.gridLayout_table.itemAt(i).widget().deleteLater()
                
    def block(self, bool):
        self.line_train.setReadOnly(bool)
        self.line_valid.setReadOnly(bool)
        self.line_test.setReadOnly(bool)
        self.pB_ChooseDataset.setDisabled(bool)
        self.line_Dataset.setReadOnly(bool)
        self.line_Output.setReadOnly(bool)
        self.line_COCO.setReadOnly(bool)
        self.line_iter.setReadOnly(bool)

    def hideProgress(self, hide):
        self.lbl_progress.setHidden(hide)
        self.progressBar.setHidden(hide)

    def changeTextColor(self, widget, color=""):
        _color = "color: {};".format(color)
        widget.setStyleSheet(_color)
   
    def open_path(self):
        try:
            self.Dataset_path = qtw.QFileDialog.getExistingDirectory(self, "Open a Dataset folder",
                                                                     self.Dataset_path,
                                                                     qtw.QFileDialog.ShowDirsOnly)
            self.line_Dataset.setText(self.Dataset_path)
            self.clearOutputs(self.outputLayout)
            self.search_COCO()
        except Exception as e:
            self.warning("Error", str(e))
    
    def search_COCO(self):
        self.COCO_path = os.path.join(os.path.join(self.Dataset_path, "coco_data"), "coco_annotations.json")
        if os.path.isfile(self.COCO_path):
            self.line_COCO.setText(self.COCO_path)
            self.changeTextColor(self.line_COCO, color="green")
            self.changeTextColor(self.line_Dataset, color="green")
            self.display_Output()
            self.widget.show()
        else:
            self.line_COCO.setText("\"coco_annotations.json\" is missing")
            self.changeTextColor(self.line_COCO, color="red")
            self.changeTextColor(self.line_Dataset, color="red")
            self.widget.hide()
            self.clearTables()
            
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

    def drawCustomUI(self):
        font = qtgui.QFont("MS Shell Dlg 2",10)
        lbl_iter = qtw.QLabel("Iteration to find best split")
        lbl_iter.setFont(font)
        lbl_iter.setAlignment(qtgui.Qt.AlignVCenter)
        
        self.line_iter = qtw.QLineEdit(str(10000))
        self.line_iter.setFont(font)
        self.line_iter.setAlignment(qtgui.Qt.AlignCenter)
        
        self.customGridLayout.addWidget(lbl_iter, 0, 0)
        self.customGridLayout.addWidget(self.line_iter, 0, 1)
        
        H_spacer02 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        H_spacer03 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        H_spacer04 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        H_spacer05 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.customGridLayout.addWidget(H_spacer02, 0, 2)
        self.customGridLayout.addWidget(H_spacer03, 0, 3)
        self.customGridLayout.addWidget(H_spacer04, 0, 4)
        self.customGridLayout.addWidget(H_spacer05, 0, 5)
        
        gridLayout = qtw.QGridLayout()
        gridLayout.setSpacing(2)
        self.customGridLayout.addWidget(gridLayout, 1, 0)
        # H_spacer11 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        # H_spacer12 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        # H_spacer13 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        # self.customGridLayout.addWidget(H_spacer11, 1, 1)
        # self.customGridLayout.addWidget(H_spacer12, 1, 2)
        # self.customGridLayout.addWidget(H_spacer13, 1, 3)
        
        ###### row 0 ######
        lbl_train = qtw.QLabel("Training")
        lbl_train.setFont(font)
        lbl_train.setAlignment(qtgui.Qt.AlignHCenter)
        
        lbl_valid = qtw.QLabel("Validation")
        lbl_valid.setFont(font)
        lbl_valid.setAlignment(qtgui.Qt.AlignHCenter)
        
        lbl_test = qtw.QLabel("Testing")
        lbl_test.setFont(font)
        lbl_test.setAlignment(qtgui.Qt.AlignHCenter)
        
        gridLayout.addWidget(lbl_train, 0, 1)
        gridLayout.addWidget(lbl_valid, 0, 2)
        gridLayout.addWidget(lbl_test, 0, 3)
        ###### row 0 ######
        
        ###### row 1 ######
        lbl_Ratio = qtw.QLabel("Unit Ratio   ")
        lbl_Ratio.setFont(font)
        lbl_Ratio.setAlignment(qtgui.Qt.AlignVCenter)
        
        self.line_train.setFont(font)
        self.line_train.setAlignment(qtgui.Qt.AlignCenter)
        
        self.line_valid.setFont(font)
        self.line_valid.setAlignment(qtgui.Qt.AlignCenter)
        
        self.line_test.setFont(font)
        self.line_test.setAlignment(qtgui.Qt.AlignCenter)
        
        self.changeTextColor(self.lbl_pressEnter, color="red")
        self.lbl_pressEnter.setHidden(True)
        gridLayout.addWidget(lbl_Ratio, 1, 0)
        gridLayout.addWidget(self.line_train, 1, 1)
        gridLayout.addWidget(self.line_valid, 1, 2)
        gridLayout.addWidget(self.line_test, 1, 3)
        gridLayout.addWidget(self.lbl_pressEnter, 1, 4)

        H_spacer15 = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        gridLayout.addItem(H_spacer15, 1, 5)

        self.pB_split.setStyleSheet("QPushButton {"
                                "font-size: 11pt;"
                                "font-weight: bold;"
                                "padding: 10px"
                                "}")
        self.pB_split.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.pB_split.clicked.connect(self.onClickedSplit)
        gridLayout.addWidget(self.pB_split, 1,6)
        ###### row 1 ######
        gridLayout.setColumnStretch(5,7)
        gridLayout.setColumnStretch(6,1)
    
        ###### row 2 ######
        # H_spacer20 = qtw.QSpacerItem(10, 10, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum)
        # gridLayout.addItem(H_spacer20, 2, 0)
        ###### row 2 ######

        ###### row 3 ######
        line = qtw.QFrame(self.verticalLayoutWidget)
        line.setFrameShape(qtw.QFrame.HLine)
        line.setFrameShadow(qtw.QFrame.Sunken)
        font2 = qtgui.QFont()
        font2.setPointSize(6)
        line.setFont(font2)
        gridLayout.addWidget(line, 3, 0, 1, 7)
        ###### row 3 ######

        self.gridLayout_table = qtw.QGridLayout()
        self.gridLayout_table.setSpacing(3)
        self.widget_V_Layout.addLayout(self.gridLayout_table)

    def onClickedSplit(self):
        if self.pB_split.text() == "Split":
            try:
                int(self.line_iter.text())
            except Exception as e:
                self.warning("Invalid iteration input", e)
                return
            self.runSplitting()
            self.pB_split.setText("Cancel")
            self.block(True)
            self.clearTables()
        else:
            self.cancel()
            self.pB_split.setText("Split")
            self.block(False)

    def runSplitting(self):
        # train_valid_test_split(self.Dataset_path, self.train, self.valid, self.test)
        try:
            # Execute
            callback = ProgressCallback()
            self._worker = Worker(train_valid_test_split,
                                  dataset_dir=self.line_Dataset.text(),
                                  train_size=self.train,
                                  valid_size=self.valid,
                                  test_size=self.test,
                                  max_iter=int(self.line_iter.text()),
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
            self.lbl_progress.setText("Splitting ...")
        except Exception as e:
            self.warning("Error", str(e))

    def cancel(self):
        self._cont = False
        self.block(False)
        self.hideProgress(True)
        self.pB_split.setText("Split")
        self.info("Splitting Cancelled", "The program will stop after completing current task.")
        
    def get_cont(self):
        return self._cont
        
    def progress_fn(self, x):  ##handes function callbacks output
       self.lbl_progress.setText(x[0])
       self.progressBar.setValue(x[1])
    
    def progress_result(self, x):
        self.drawTables(x[0], x[1])
        
    def progress_error(self, x):
        raise Exception("Thread error " + str(x[1])) from x[1]
    
    def progress_finish(self):
        self._running = False
        self._cont = False
        self.progressBar.setValue(100)
        self.lbl_progress.setText("Done")
        self.info("Splitting Complete", "Please find the datasets inside \'" + self.Dataset_path + "\'.")
        self.pB_split.setText("Split")
        self.hideProgress(True)
        self.block(False)
        self.Done_signal.emit(True)

    def hint(self):
        self.lbl_pressEnter.setHidden(False)

    def updateRatio(self, main_lineEdit, secondary_lineEdit, tertiary_lineEdit, level):
        def update():
            self.lbl_pressEnter.setHidden(True)
            main = float(main_lineEdit.text())
            
            if level == 1:
                if not 1 >= main >= 0:
                    self.warning("Invalid Input", "The sum of Unit ratio must be equal to 1. Please fix.")
                    return
                second = (1 - main)/2
                secondary_lineEdit.setText("{:.3f}".format(second))
                tertiary_lineEdit.setText("{:.3f}".format(second))
            elif level == 2:
                third = 1-main-float(secondary_lineEdit.text())
                if third < 0:
                    self.warning("Invalid Input", "The sum of Unit ratio must be equal to 1. Please fix.")
                    return
                tertiary_lineEdit.setText("{:.3f}".format(third))
            elif level == 3:
                second = 1-main-float(tertiary_lineEdit.text())
                if second < 0:
                    self.warning("Invalid Input", "The sum of Unit ratio must be equal to 1. Please fix.")
                    return
                secondary_lineEdit.setText("{:.3f}".format(second))
            
            self.train = float(self.line_train.text())
            self.valid = float(self.line_valid.text())
            self.test = float(self.line_test.text())
        return update

    def clearOutputs(self, Layout):
        children = []
        for i in range(Layout.count()):
            if i == 0:
                output = Layout.itemAt(i).widget()
                output.clear()
                continue
            child = Layout.itemAt(i).widget()
            if child:
                children.append(child)
                
        for child in children:
            child.deleteLater()

    def warning(self, title:str, msg:str):
        qtw.QMessageBox.warning(self, title, msg, qtw.QMessageBox.Ok)

    def info(self, title:str, msg:str):
        qtw.QMessageBox.information(self, title, msg, qtw.QMessageBox.Ok)

def main():
    app = qtw.QApplication()
    try:
        window = Splitting_Window(testing=False)
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
