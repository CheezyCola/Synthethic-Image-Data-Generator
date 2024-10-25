import PySide2.QtCore as QtCore
import PySide2.QtGui as qtgui
import PySide2.QtWidgets  as qtw
import ui.Main_Window_UI as main_win
import Generator_Window as GW
import Splitting_Window as SW
import Augmentation_Window as AW
import Evaluation_Window as EW

# class Signals(object):
#     Done_signal = QtCore.Signal(object)

class Main_Window(qtw.QMainWindow, main_win.Ui_MainWindow):
    def __init__(self, testing=False, *args, **kwargs):
        self._testing = testing
        super(Main_Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Synthetic Data Generator")
        self.centralwidget = qtw.QWidget()
        self.centralwidget.setLayout(self.main_layout)
        self.setCentralWidget(self.centralwidget)

        self.initialize()
        
    def initialize(self):
        # Draw general
        Gen_Win = GW.Generator_Window()
        self.tabWidget.addTab(Gen_Win, "Generator")
        Split_Win = SW.Splitting_Window()
        self.tabWidget.addTab(Split_Win, "Splitting")
        Aug_Win = AW.Augmentation_Window()
        self.tabWidget.addTab(Aug_Win, "Augmentation")
        Eva_Win = EW.Evaluation_Window()
        self.tabWidget.addTab(Eva_Win, "Evaluation")
        # Connect slots and signals
        
        # Draw Custom UI
        self.drawCustomUI()
   
    def changeTextColor(self, widget, color=""):
        _color = "color: {};".format(color)
        widget.setStyleSheet(_color)

            
    def drawCustomUI(self):
        pass
        
        
def main():
    app = qtw.QApplication()
    try:
        window = Main_Window(testing=False)
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


