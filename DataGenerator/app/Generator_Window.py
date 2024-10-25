import PySide2.QtCore as QtCore
import PySide2.QtGui as qtgui
import PySide2.QtWidgets  as qtw
import ui.Generator_Window_UI as generator_win

import traceback
import sys

from DataGenerator.renderer.loop import generate_dataset, generate_failed_imgs
from DataGenerator.utility.config import Config

class WorkerSignals(QtCore.QObject):
    """ Defines the signals available from a running worker thread """
    finished = QtCore.Signal(object)  #finished - object data returned from processing, anything
    error = QtCore.Signal(tuple)  #error - tuple (exctype, value, traceback.format_exc() )
    result = QtCore.Signal(object)  #result - object data returned from processing, anything
    no_result = QtCore.Signal(object)  #result - object data returned from processing, anything
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
        success = None
        dataset_path = None
        total_time = None
        failed_imgs = None

        try:
            returned = self.fn(*self.args, **self.kwargs)
            if returned is not None:    
                success= returned[0]
                dataset_path = returned[1]
                total_time = returned[2]
                failed_imgs = returned[3]
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]  
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if success:
                self.signals.result.emit((total_time, failed_imgs))
            elif success == False:
                self.signals.no_result.emit((total_time, failed_imgs))
        finally:
            if returned is None:
                self.signals.finished.emit(None)
            else:
                if success is None:
                    self.signals.finished.emit(None)
                elif success:
                    self.signals.finished.emit(dataset_path)  # Done
                elif success == False:
                    self.signals.finished.emit(False)

class ProgressCallback(QtCore.QObject):
    progressChanged = QtCore.Signal(object)

    def __call__(self, task, value):
        self.progressChanged.emit((task, value))

class Signals(object):
    Done_signal = QtCore.Signal(object)
    Regenerate_signal = QtCore.Signal(object)

class RegeneratePopup(qtw.QWidget, Signals):
    def __init__(self):
        qtw.QWidget.__init__(self)
        self.mainLayout = qtw.QGridLayout()
        self.setLayout(self.mainLayout)
        self.instruction = qtw.QLabel()
        self.instruction.setText("Select the dataset to re-generate failed images if any.\n"+
                                 "Failed images could be a result of process cancellation or "+
                                 "wrong(very tight) configuration for scene creation and rendering.\n"+
                                 "Failed images will be re-generated according to previous object distributions.\n"+
                                 "You may alter the ground and configuration.")
        self.mainLayout.addWidget(self.instruction, 0, 0, 1, 7)
        self.setWindowTitle("Re-generate Failed Images")

        line = qtw.QFrame(self)
        line.setFrameShape(qtw.QFrame.HLine)
        line.setFrameShadow(qtw.QFrame.Sunken)
        font2 = qtgui.QFont()
        font2.setPointSize(6)
        line.setFont(font2)
        self.mainLayout.addWidget(line, 1, 0, 1, 7)

        self.lbl_dataset_dir = qtw.QLabel("Dataset directory")
        self.lbl_gnd_dir = qtw.QLabel("Ground directory")
        self.lbl_config = qtw.QLabel("Configuration")
        self.mainLayout.addWidget(self.lbl_dataset_dir, 2, 0)
        self.mainLayout.addWidget(self.lbl_gnd_dir, 3, 0)
        self.mainLayout.addWidget(self.lbl_config, 4, 0)

        self.line_dataset_dir = qtw.QLineEdit()
        self.line_gnd_dir = qtw.QLineEdit()
        self.line_config = qtw.QLineEdit()
        self.mainLayout.addWidget(self.line_dataset_dir, 2, 1, 1, 4)
        self.mainLayout.addWidget(self.line_gnd_dir, 3, 1, 1, 4)
        self.mainLayout.addWidget(self.line_config, 4, 1, 1, 4)

        self.pB_dataset_dir = qtw.QPushButton("browse")
        self.pB_gnd_dir = qtw.QPushButton("browse")
        self.pB_config = qtw.QPushButton("browse")
        self.mainLayout.addWidget(self.pB_dataset_dir, 2, 6)
        self.mainLayout.addWidget(self.pB_gnd_dir, 3, 6)
        self.mainLayout.addWidget(self.pB_config, 4, 6)

        self.V_spacer = qtw.QSpacerItem(20, 15, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        self.mainLayout.addItem(self.V_spacer, 5, 3)

        self.pB_runRegenerate = qtw.QPushButton("Re-generate")
        self.pB_runRegenerate.setFont(qtgui.QFont("MS Shell Dlg 2",10))
        self.mainLayout.addWidget(self.pB_runRegenerate, 6, 2, 1, 3)
        
        self.mainLayout.setRowStretch(0,0)
        self.mainLayout.setRowStretch(1,0)
        self.mainLayout.setRowStretch(2,0)
        self.mainLayout.setRowStretch(3,0)
        self.mainLayout.setRowStretch(4,0)
        self.mainLayout.setRowStretch(5,1)
        self.mainLayout.setRowStretch(6,0)

        # connect signals
        self.pB_dataset_dir.clicked.connect(self.openPath(self.line_dataset_dir, "Object Directory"))
        self.pB_gnd_dir.clicked.connect(self.openPath(self.line_gnd_dir, "Ground Directory"))
        self.pB_config.clicked.connect(self.searchConfig)
        self.pB_runRegenerate.clicked.connect(self.regenerateClicked)

    def openPath(self, lineEdit, name):
        def open():
            try:
                path=qtw.QFileDialog.getExistingDirectory(self, "Open "+name, "",
                                                           qtw.QFileDialog.ShowDirsOnly)
                lineEdit.setText(path)
            except Exception as e:
                self.warning("Error", str(e))
        return open

    def searchConfig(self):
        try:
            path, filter = qtw.QFileDialog.getOpenFileName(self, "Choose Configuration File", "",
                                                 "json file (*.json)")
            if path:
                self.line_config.setText(path)
        except Exception as e:
            self.warning("Error", str(e))

    def regenerateClicked(self):
        if not all([self.line_gnd_dir.text().strip(), self.line_dataset_dir.text().strip(),
                    self.line_config.text().strip()]):
            self.warning("Re-Generation Not Allowed", "All entries must be filled.")
            return

        self.Regenerate_signal.emit((self.line_dataset_dir.text(), self.line_gnd_dir.text(),
                                     self.line_config.text()))
    
    def warning(self, title:str, msg:str):
        qtw.QMessageBox.warning(self, title, msg, qtw.QMessageBox.Ok)
    
class Generator_Window(qtw.QMainWindow, generator_win.Ui_MainWindow, Signals, QtCore.QObject):
    def __init__(self, testing=False, *args, **kwargs):
        self._testing = testing
        super(Generator_Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.centralwidget = qtw.QWidget()
        self.centralwidget.setLayout(self.main_layout)
        self.setCentralWidget(self.centralwidget)
        # variables
        self.line_ccTexturesDir = qtw.QLineEdit()
        self.isNewFolder = True
        self.w = RegeneratePopup()
        
        ##threading
        self.threadpool = QtCore.QThreadPool()
        self._running = False
        self._worker = None

        self.initialize()

        # Connect slots and signals
        self.lbl_isNewFolder.mousePressEvent = self.setNewFolder
        self.pB_search_obj_dir.clicked.connect(self.openPath(self.line_obj_dir, "Object Directory"))
        self.pB_search_gnd_dir.clicked.connect(self.openPath(self.line_gnd_dir, "Ground Directory"))
        self.pB_search_output_dir.clicked.connect(self.openPath(self.line_output_dir, "Output Directory"))
        self.pB_search_config_file.clicked.connect(self.searchConfig)
        self.pB_loadConfig.clicked.connect(self.loadConfigClicked)
        self.pB_saveConfig.clicked.connect(self.saveConfigClicked)
        self.pB_applyConfig.clicked.connect(self.applyConfigClicked)
        self.pB_generate.clicked.connect(self.generateClicked)
        self.cBox_cam_allObjectsFullyVisible.stateChanged.connect(self.cBox_allObjsFullyVisibleChanged)
        self.pB_Regenerate.clicked.connect(self.regenerateClicked)
        self.w.Regenerate_signal.connect(self.runRegeneration)
        
    def initialize(self):
        # Draw general
        self.gBox_IO.setLayout(self.gridLayout_IO)
        self.statusbar.setMaximumHeight(1)
        self.lbl_progress.setFont(qtgui.QFont("MS Shell Dlg 2",8))
        self.lbl_progress.setIndent(4)
        self.progressBar.setFont(qtgui.QFont("MS Shell Dlg 2",8))
        self.progressBar.setStyleSheet("QProgressBar{"
                                       "max-height: 12px;}")
        self.hideProgress(True)
        #setting
        self.widget_setting = qtw.QWidget()
        self.widget_setting.setLayout(self.gridLayout_Setting)
        self.scroll_Setting = qtw.QScrollArea()
        self.scroll_Setting.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_Setting.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_Setting.setWidgetResizable(True)
        self.scroll_Setting.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.scroll_Setting.setWidget(self.widget_setting)
        self.gridLayout_Setting2 = qtw.QVBoxLayout()
        self.gridLayout_Setting2.addWidget(self.scroll_Setting)
        self.tab_Setting.setLayout(self.gridLayout_Setting2)
        #objects
        self.widget_objects = qtw.QWidget()
        self.widget_objects.setLayout(self.gridLayout_Objects)
        self.scroll_Objects = qtw.QScrollArea()
        self.scroll_Objects.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_Objects.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_Objects.setWidgetResizable(True)
        self.scroll_Objects.setWidget(self.widget_objects)
        self.gridLayout_Objects2 = qtw.QVBoxLayout()
        self.gridLayout_Objects2.addWidget(self.scroll_Objects)
        self.tab_Objects.setLayout(self.gridLayout_Objects2)
        #distractor
        self.widget_distractor = qtw.QWidget()
        self.widget_distractor.setLayout(self.gridLayout_Distractor)
        self.scroll_Distractor = qtw.QScrollArea()
        self.scroll_Distractor.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_Distractor.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_Distractor.setWidgetResizable(True)
        self.scroll_Distractor.setWidget(self.widget_distractor)
        self.gridLayout_Distractor2 = qtw.QVBoxLayout()
        self.gridLayout_Distractor2.addWidget(self.scroll_Distractor)
        self.tab_Distractor.setLayout(self.gridLayout_Distractor2)
        #ground
        self.widget_ground = qtw.QWidget()
        self.widget_ground.setLayout(self.gridLayout_Ground)
        self.scroll_Ground = qtw.QScrollArea()
        self.scroll_Ground.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_Ground.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_Ground.setWidgetResizable(True)
        self.scroll_Ground.setWidget(self.widget_ground)
        self.gridLayout_Ground2 = qtw.QVBoxLayout()
        self.gridLayout_Ground2.addWidget(self.scroll_Ground)
        self.tab_Ground.setLayout(self.gridLayout_Ground2)
        #camera
        self.widget_camera = qtw.QWidget()
        self.widget_camera.setLayout(self.gridLayout_Camera)
        self.scroll_Camera = qtw.QScrollArea()
        self.scroll_Camera.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_Camera.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_Camera.setWidgetResizable(True)
        self.scroll_Camera.setWidget(self.widget_camera)
        self.gridLayout_Camera2 = qtw.QVBoxLayout()
        self.gridLayout_Camera2.addWidget(self.scroll_Camera)
        self.tab_Camera.setLayout(self.gridLayout_Camera2)
        #light
        self.widget_light = qtw.QWidget()
        self.widget_light.setLayout(self.gridLayout_Light)
        self.scroll_Light = qtw.QScrollArea()
        self.scroll_Light.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_Light.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_Light.setWidgetResizable(True)
        self.scroll_Light.setWidget(self.widget_light)
        self.gridLayout_Light2 = qtw.QVBoxLayout()
        self.gridLayout_Light2.addWidget(self.scroll_Light)
        self.tab_Light.setLayout(self.gridLayout_Light2)
        #simulation
        self.widget_simulation = qtw.QWidget()
        self.widget_simulation.setLayout(self.gridLayout_Simulation)
        self.scroll_Simulation = qtw.QScrollArea()
        self.scroll_Simulation.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_Simulation.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_Simulation.setWidgetResizable(True)
        self.scroll_Simulation.setWidget(self.widget_simulation)
        self.gridLayout_Simulation2 = qtw.QVBoxLayout()
        self.gridLayout_Simulation2.addWidget(self.scroll_Simulation)
        self.tab_Simulation.setLayout(self.gridLayout_Simulation2)
        
        self.redrawUI()
        self.tabWidget.setCurrentIndex(0)

    def block(self, bool):
        self.pB_applyConfig.setDisabled(bool)

    def setNewFolder(self, event):
        if self.lbl_isNewFolder.text() == "Create New Folder":
            self.lbl_isNewFolder.setText("Append To Folder")
            self.isNewFolder = False
        else:
            self.lbl_isNewFolder.setText("Create New Folder")
            self.isNewFolder = True

    def regenerateClicked(self):
        if self.pB_generate.text() == "Cancel":
            self.warning("Re-generate Not Allowed", "Generation is running.")
            return
        
        if self.pB_Regenerate.text() == "Re-generate\nFailed Images":
            self.w.show()
        else:
            self.cancel()
            self.pB_Regenerate.setText("Re-generate\nFailed Images")
            self.pB_generate.setDisabled(True)
        
    def runRegeneration(self, x):
        self.w.hide()
        self.pB_Regenerate.setText("Cancel")
        self.pB_generate.setDisabled(True)
        try:
            # Execute
            callback = ProgressCallback()
            self._worker2 = Worker(generate_failed_imgs,
                                   dataset_dir = x[0],
                                   gnd_dir = x[1],
                                   config_file = x[2],
                                   check_CANCEL=self.get_cont,
                                   progress_callback=callback)
            self._worker2.signals.result.connect(self.progress_result)
            self._worker2.signals.no_result.connect(self.progress_no_result)
            self._worker2.signals.error.connect(self.progress_error)
            self._worker2.signals.finished.connect(self.progress_finish)
            callback.progressChanged.connect(self.progress_fn)

            self._running = True          
            self._cont = True
            self.threadpool.start(self._worker2)
            self.hideProgress(False)
            self.lbl_progress.setText("Re-Generating ...")
        except Exception as e:
            self.warning("Error", str(e))

    def generateClicked(self):
        if not all([self.line_obj_dir.text().strip(), self.line_gnd_dir.text().strip(),
                    self.line_output_dir.text().strip(), self.line_config_file.text().strip()]):
            self.warning("Generation Not Allowed", "All entries in Input/Output must be filled.")
            return
        
        if not all([self.line_numOfImages.text().strip(), self.line_minOccurences.text().strip(),
                    self.line_maxOccurences.text().strip(), self.line_totalOccurences.text().strip()]):
            self.warning("Generation Not Allowed", "All entries specifying dataset size and instance distribution must be filled.")
            return
        
        if self.pB_generate.text() == "Generate":
            self.runGeneration()
            self.pB_generate.setText("Cancel")
            self.block(True)
        else:
            self.cancel()
            self.pB_generate.setText("Generate")
            self.block(True)
        
    def runGeneration(self):
        try:
            # Execute
            callback = ProgressCallback()
            self._worker = Worker(generate_dataset,
                                  obj_dir=self.line_obj_dir.text(),
                                  gnd_dir=self.line_gnd_dir.text(),
                                  output_dir=self.line_output_dir.text(),
                                  config_file=self.line_config_file.text(),
                                  num_of_images=int(self.line_numOfImages.text()),
                                  min_occurences=int(self.line_minOccurences.text()),
                                  max_occurences=int(self.line_maxOccurences.text()),
                                  total_occurences=int(self.line_totalOccurences.text()),
                                  new_Folder=self.isNewFolder,
                                  check_CANCEL=self.get_cont,
                                  progress_callback=callback)
            self._worker.signals.result.connect(self.progress_result)
            self._worker.signals.no_result.connect(self.progress_no_result)
            self._worker.signals.error.connect(self.progress_error)
            self._worker.signals.finished.connect(self.progress_finish)
            callback.progressChanged.connect(self.progress_fn)

            self._running = True          
            self._cont = True
            self.threadpool.start(self._worker)
            self.hideProgress(False)
            self.lbl_progress.setText("Generating ...")
        except Exception as e:
            self.warning("Error", str(e))

    def cancel(self):
        self._cont = False
        self.info("Cancelling", "The program will stop after completing current task. \n"+
                  "Forcefully stopping the process may cause file corruption.")
        self.pB_generate.setDisabled(True)
        self.pB_Regenerate.setDisabled(True)

    def get_cont(self):
        return self._cont
        
    def progress_fn(self, x):  ##handes function callbacks output
       self.lbl_progress.setText(x[0])
       self.progressBar.setValue(x[1])
    
    def progress_result(self, x):
        time = x[0]
        failed_index = x[1]
        msg = "Time taken: " + str(time) + "s\n"
        if failed_index:
            msg += "In this dataset, found failed images with index: " + str(failed_index)
            msg += "\n\nYou could regenerate the failed images with different settings."
        self.info("Result", msg)
    
    def progress_no_result(self, x):
        failed_index = x[1]
        if not failed_index:
            self.info("Result", "No failed image in the dataset.")

    def progress_error(self, x):
        raise Exception("Thread error " + str(x[1])) from x[1]
    
    def progress_finish(self, x):
        if x is None:
            self.info("Cancelled Successfully", "The progress stops. You may proceed.")
        elif x == False:
            pass
        else:
            self._running = False
            self._cont = False
            self.progressBar.setValue(100)
            self.lbl_progress.setText("Done")
            self.info("Generation Complete", "Please find the dataset in \'" + x + "\'.")

        self.hideProgress(True)
        self.block(False)
        self.pB_generate.setDisabled(False)
        self.pB_Regenerate.setDisabled(False)
        self.pB_generate.setText("Generate")
        self.pB_Regenerate.setText("Re-generate\nFailed Images")
        self.Done_signal.emit(True)
    
    def hideProgress(self, hide):
        self.lbl_progress.setHidden(hide)
        self.progressBar.setHidden(hide)

    def openPath(self, lineEdit, name):
        def open():
            try:
                path=qtw.QFileDialog.getExistingDirectory(self, "Open "+name, "",
                                                           qtw.QFileDialog.ShowDirsOnly)
                lineEdit.setText(path)
            except Exception as e:
                self.warning("Error", str(e))
        return open

    def searchConfig(self):
        try:
            path, filter = qtw.QFileDialog.getOpenFileName(self, "Choose Configuration File", "",
                                                 "json file (*.json)")
            if path:
                self.line_config_file.setText(path)
                self.displayConfig()
                self.info("Configuration", "Configuration in file \'" + path + "\'loaded.")
        except Exception as e:
            self.warning("Error", str(e))
    
    def loadConfigClicked(self):
        try:
            path, filter = qtw.QFileDialog.getOpenFileName(self, "Choose Configuration File", "",
                                                 "json file (*.json)")
            if path:
                self.displayConfig(path)
                self.info("Configuration", "Configuration in file \'" + path + "\'loaded.")
                self.changeTextColor(self.pB_applyConfig, color="red")
        except Exception as e:
            self.warning("Error", str(e))

    def saveConfigClicked(self):
        try:
            fileName, filter = qtw.QFileDialog.getSaveFileName(self, "Save Config", "",
                                                       "json file (*.json);;All Files (*)")
            if fileName:
                self.saveConfig(fileName)
        except Exception as e:
            self.warning("Failed to save", str(e))

    def applyConfigClicked(self):
        if not self.line_config_file.text().strip():
            self.warning("Not Allowed", "The path to config file cannot be left empty.")
            return
        
        yes = self.question("Apply Configuration", "The config file at path: \'"
                      + self.line_config_file.text() +"\' will be overwritten."
                      + "\nAre you sure you want to continue?")
        if not yes:
            return
        self.saveConfig(self.line_config_file.text())
        self.changeTextColor(self.pB_applyConfig, color="black")

    def saveConfig(self, fileName):
        config = {"world":{}, "renderer":{}, "cc_textures_dir":str, "save_coco_annotated_image":bool,
                  "Object3D_loader":{}, "objects":{}, "flying_distractor":{}, "ground":{},
                  "camera": {}, "ceiling_light":{}, "spot_light":{}, "simulation":{}}

        #setting
        config["world"]["unit"] = self.comboBox_unit.currentText()
        config["world"]["gravitaty_ms2"] = float(self.line_gravity.text())
        config["world"]["background_black"] = bool(self.cBox_backgroundBlack.checkState())
        config["world"]["_3Dview_clip_start"] = float(self.line_3DviewClipStart.text())
        config["world"]["_3Dview_clip_end"] = float(self.line_3DviewClipEnd.text())
        config["renderer"]["ambient_occlusion"] = bool(self.cBox_ambientOcclusion.checkState())
        config["renderer"]["engine"] = self.line_engine.text()
        config["renderer"]["image_compression_perc"] = int(self.sBox_imageCompression.value())
        config["renderer"]["cpu_cores_number"] = int(self.sBox_CPUCoresNum.value())
        config["renderer"]["number_of_subdivision"] = int(self.sBox_numOfSubdivision.value())
        config["renderer"]["denoiser"] = self.comboBox_denoiser.currentText()
        config["renderer"]["noise_treshold"] = float(self.sBox_noiseTreshold.value())
        config["renderer"]["use_only_cpu"] = bool(self.cBox_useOnlyCPU.checkState())
        config["renderer"]["desired_gpu_device_type"] = self.comboBox_GPUType.currentText()
        config["cc_textures_dir"] = self.line_ccTexturesDir.text()
        config["save_coco_annotated_image"] = bool(self.cBox_saveCocoAnnotatedImage.checkState())
        config["Object3D_loader"]["file_type"] = ".obj"
        config["Object3D_loader"]["is_from_ShapeNet"] = False
        #objects
        config["objects"] = {
            "config":{
                "linear_damping": float(self.line_obj_linearDamping.text()),
                "friction": float(self.line_obj_friction.text()),
                "color":{
                    "random": bool(self.cBox_obj_randomColor.checkState())
                },
                "material":{
                    "keep_loaded": bool(self.cBox_obj_keppLoadedMaterial.checkState()),
                    "defined": self.line_obj_definedMaterial.text(),
                    "random": bool(self.cBox_obj_randomMaterial.checkState())
                } 
            },
            "sampler":{
                "min_height": float(self.line_obj_minHeight.text()),
                "max_height": float(self.line_obj_maxHeight.text()),
                "adjust_to_objects": bool(self.cBox_obj_sampling_adjust.checkState()),
                "sampling_region_percentage": float(self.line_obj_samplingRegion.text())
            }
        }
        #distractor
        config["flying_distractor"] = {
            "number": int(self.sBox_distractor_num.value()),
            "size":{
                "defined": eval(self.line_distractor_definedSize.text()),
                "adjust_to_objects": bool(self.cBox_distractor_adjustSize.checkState())
            },
            "sampler":{
                "min_height": float(self.line_distractor_minHeight.text()),
                "max_height": float(self.line_distractor_maxHeight.text()),
                "sampling_region_percentage": float(self.line_distractor_samplingRegion.text())
            }
        }
        #ground
        config["ground"] = {
            "random_pick": bool(self.cBox_gnd_randomPick.checkState()),
            "euler_rotation":{
                "X": float(self.line_gnd_rotX.text()),
                "Y": float(self.line_gnd_rotY.text()),
                "Z": float(self.line_gnd_rotZ.text())
            },
            "plane_size":{
                "defined": eval(self.line_gnd_definedXY.text()),
                "adjust_to_objects": bool(self.cBox_gnd_XY_adjust.checkState())
            },
            "linear_damping": float(self.line_gnd_linearDamping.text()),
            "friction": float(self.line_gnd_friction.text()),
            "material":{
                "keep_loaded": bool(self.cBox_gnd_keepLoadedMaterial.checkState()),
                "defined": self.line_gnd_definedMaterial.text(),
                "random": bool(self.cBox_gnd_randomMaterial.checkState())
            }
        }
        #camera
        config["camera"] = {
            "config":{
                "image_width": int(self.line_cam_imageWidth.text()), 
                "image_height": int(self.line_cam_imageHeight.text()), 
                "clip_start": float(self.line_cam_clipStart.text()), 
                "clip_end": float(self.line_cam_clipEnd.text())
            },
            "sampler":{
                "position":{
                    "defined": eval(self.line_cam_definedPos.text()),
                    "random":{
                        "enabled": bool(self.cBox_cam_randomPos.checkState()),
                        "center": eval(self.line_cam_center.text()),
                        "min_radius": float(self.line_cam_minRadius.text()),
                        "max_radius": float(self.line_cam_maxRadius.text()),
                        "prefer_small_radius": bool(self.cBox_cam_preferSmallRadius.checkState()),
                        "min_elevation": float(self.line_cam_minElevation.text()),
                        "max_elevation": float(self.line_cam_maxElevation.text()),
                    }
                },
                "rotation": {
                    "random": {
                        "enabled": bool(self.cBox_cam_randomRotation.checkState())
                    }
                },
                "check": {
                    "no_world_background": bool(self.cBox_cam_noWorldBackground.checkState()),
                    "all_objects_fully_visible": bool(self.cBox_cam_allObjectsFullyVisible.checkState())
                }
            }
        }
        #light
        config["ceiling_light"] = {
            "enabled": bool(self.cBox_ceilLight_ENA.checkState()),
            "position":{
                "defined": eval(self.line_ceilLight_definedPos.text()),
                "random": {
                    "enabled": bool(self.cBox_ceilLight_randomPos.checkState()),
                    "min_height": float(self.line_ceilLight_minHeight.text()), 
                    "max_height": float(self.line_ceilLight_maxHeight.text())
                }
            },
            "intensity":{
                "defined": float(self.line_ceilLight_definedIntensity.text()),
                "random": {
                    "enabled": bool(self.cBox_ceilLight_randomIntensity.checkState()),
                    "min": float(self.line_ceilLight_minIntensity.text()), 
                    "max": float(self.line_ceilLight_maxIntensity.text())
                }
            },
            "plane_xy":{
                "defined": eval(self.line_ceilLight_XY.text()), 
                "fit_to_ground": bool(self.cBox_ceilLight_fitToGround.checkState())
            }
        }
        config["spot_light"] = {
            "number": int(self.sBox_spotLight_num.value()),
            "config": {
                "spread_angle": float(self.line_spotLight_spreadAngle.text()),
                "blend": float(self.line_spotLight_blend.text())
            },
            "position":{
                "defined": eval(self.line_spotLight_definedPos.text()),
                "random":{
                    "enabled": bool(self.cBox_spotLight_randomPos.checkState()),
                    "center": eval(self.line_spotLight_center.text()),
                    "min_radius": float(self.line_spotLight_minRadius.text()),
                    "max_radius": float(self.line_spotLight_maxRadius.text()),
                    "min_elevation": float(self.line_spotLight_minElevation.text()),
                    "max_elevation": float(self.line_spotLight_maxElevation.text())
                }
            },
            "rotation":{
                "to_objects": bool(self.cBox_spotlight_toObjects.checkState())
            },
            "intensity_watt":{
                "defined": float(self.line_spotLight_definedWatt.text()),
                "random": {
                    "enabled": bool(self.cBox_spotLight_randomWatt.checkState()),
                    "min": float(self.line_spotLight_minWatt.text()), 
                    "max": float(self.line_spotLight_maxWatt.text())
                }
            }
        }
        #simulation
        config["simulation"] = {
            "check_object_interval": float(self.line_simu_checkObjectInterval.text()),
            "substeps_per_frame": int(self.line_simu_substepsPerFrame.text()),
            "solver_iters": int(self.line_simu_solverIters.text()),
            "time":{
                "min": float(self.line_simu_minTime.text()),
                "max": float(self.line_simu_maxTime.text()),
                "adjust_to_objects": bool(self.cBox_simu_adjustToObjects.checkState())
            }
        }
        Config.save_json(config, fileName)

    def displayConfig(self, path=None):
        if path:
            CONF = Config.load_json(path)
        else:
            CONF = Config.load_json(self.line_config_file.text())
        #setting
        self.comboBox_unit.setCurrentText(str(CONF.world.unit))
        self.line_gravity.setText(str(CONF.world.gravitaty_ms2))
        self.cBox_backgroundBlack.setChecked(bool(CONF.world.background_black))
        self.line_3DviewClipStart.setText(str(CONF.world._3Dview_clip_start))
        self.line_3DviewClipEnd.setText(str(CONF.world._3Dview_clip_end))
        self.line_engine.setText(str(CONF.renderer.engine))
        self.cBox_ambientOcclusion.setChecked(bool(CONF.renderer.ambient_occlusion))
        self.sBox_imageCompression.setValue(int(CONF.renderer.image_compression_perc))
        self.sBox_CPUCoresNum.setValue(int(CONF.renderer.cpu_cores_number))
        self.sBox_numOfSubdivision.setValue(int(CONF.renderer.number_of_subdivision))
        self.comboBox_denoiser.setCurrentText(str(CONF.renderer.denoiser))
        self.sBox_noiseTreshold.setValue(float(CONF.renderer.noise_treshold))
        self.cBox_useOnlyCPU.setChecked(bool(CONF.renderer.use_only_cpu))
        self.comboBox_GPUType.setCurrentText(str(CONF.renderer.desired_gpu_device_type))
        self.line_ccTexturesDir.setText(str(CONF.cc_textures_dir))
        self.cBox_saveCocoAnnotatedImage.setChecked(bool(CONF.save_coco_annotated_image))
        #objects
        self.line_obj_linearDamping.setText(str(CONF.objects.config.linear_damping))
        self.line_obj_friction.setText(str(CONF.objects.config.friction))
        self.cBox_obj_randomColor.setChecked(bool(CONF.objects.config.color.random))
        self.cBox_obj_keppLoadedMaterial.setChecked(bool(CONF.objects.config.material.keep_loaded))
        self.line_obj_definedMaterial.setText(str(CONF.objects.config.material.defined))
        self.cBox_obj_randomMaterial.setChecked(bool(CONF.objects.config.material.random))
        self.line_obj_minHeight.setText(str(CONF.objects.sampler.min_height))
        self.line_obj_maxHeight.setText(str(CONF.objects.sampler.max_height))
        self.line_obj_samplingRegion.setText(str(CONF.objects.sampler.sampling_region_percentage))
        self.cBox_obj_sampling_adjust.setChecked(bool(CONF.objects.sampler.adjust_to_objects))
        #distractor
        self.sBox_distractor_num.setValue(int(CONF.flying_distractor.number))
        self.line_distractor_definedSize.setText(str(CONF.flying_distractor.size.defined))
        self.cBox_distractor_adjustSize.setChecked(bool(CONF.flying_distractor.size.adjust_to_objects))
        self.line_distractor_minHeight.setText(str(CONF.flying_distractor.sampler.min_height))
        self.line_distractor_maxHeight.setText(str(CONF.flying_distractor.sampler.max_height))
        self.line_distractor_samplingRegion.setText(str(CONF.flying_distractor.sampler.sampling_region_percentage))
        #ground
        self.line_gnd_rotX.setText(str(CONF.ground.euler_rotation.X))
        self.line_gnd_rotY.setText(str(CONF.ground.euler_rotation.Y))
        self.line_gnd_rotZ.setText(str(CONF.ground.euler_rotation.Z))
        self.cBox_gnd_randomPick.setChecked(bool(CONF.ground.random_pick))
        self.line_gnd_definedXY.setText(str(CONF.ground.plane_size.defined))
        self.cBox_gnd_XY_adjust.setChecked(bool(CONF.ground.plane_size.adjust_to_objects))
        self.line_gnd_linearDamping.setText(str(CONF.ground.linear_damping))
        self.line_gnd_friction.setText(str(CONF.ground.friction))
        self.cBox_gnd_keepLoadedMaterial.setChecked(bool(CONF.ground.material.keep_loaded))
        self.line_gnd_definedMaterial.setText(str(CONF.ground.material.defined))
        self.cBox_gnd_randomMaterial.setChecked(bool(CONF.ground.material.random))
        #camera
        self.line_cam_imageWidth.setText(str(CONF.camera.config.image_width))
        self.line_cam_imageHeight.setText(str(CONF.camera.config.image_height))
        self.line_cam_clipStart.setText(str(CONF.camera.config.clip_start))
        self.line_cam_clipEnd.setText(str(CONF.camera.config.clip_end))
        self.line_cam_definedPos.setText(str(CONF.camera.sampler.position.defined))
        self.cBox_cam_randomPos.setChecked(bool(CONF.camera.sampler.position.random.enabled))
        self.line_cam_center.setText(str(CONF.camera.sampler.position.random.center))
        self.line_cam_minRadius.setText(str(CONF.camera.sampler.position.random.min_radius))
        self.line_cam_maxRadius.setText(str(CONF.camera.sampler.position.random.max_radius))
        self.cBox_cam_preferSmallRadius.setChecked(bool(CONF.camera.sampler.position.random.prefer_small_radius))
        self.line_cam_minElevation.setText(str(CONF.camera.sampler.position.random.min_elevation))
        self.line_cam_maxElevation.setText(str(CONF.camera.sampler.position.random.max_elevation))
        self.cBox_cam_randomRotation.setChecked(bool(CONF.camera.sampler.rotation.random.enabled))
        self.cBox_cam_noWorldBackground.setChecked(bool(CONF.camera.sampler.check.no_world_background))
        self.cBox_cam_allObjectsFullyVisible.setChecked(bool(CONF.camera.sampler.check.all_objects_fully_visible))
        #light
        self.cBox_ceilLight_ENA.setChecked(bool(CONF.ceiling_light.enabled))
        self.line_ceilLight_definedPos.setText(str(CONF.ceiling_light.position.defined))
        self.cBox_ceilLight_randomPos.setChecked(bool(CONF.ceiling_light.position.random.enabled))
        self.line_ceilLight_minHeight.setText(str(CONF.ceiling_light.position.random.min_height))
        self.line_ceilLight_maxHeight.setText(str(CONF.ceiling_light.position.random.max_height))
        self.line_ceilLight_definedIntensity.setText(str(CONF.ceiling_light.intensity.defined))
        self.cBox_ceilLight_randomIntensity.setChecked(bool(CONF.ceiling_light.intensity.random.enabled))
        self.line_ceilLight_minIntensity.setText(str(CONF.ceiling_light.intensity.random.min))
        self.line_ceilLight_maxIntensity.setText(str(CONF.ceiling_light.intensity.random.max))
        self.line_ceilLight_XY.setText(str(CONF.ceiling_light.plane_xy.defined))
        self.cBox_ceilLight_fitToGround.setChecked(bool(CONF.ceiling_light.plane_xy.fit_to_ground))
        self.sBox_spotLight_num.setValue(int(CONF.spot_light.number))
        self.line_spotLight_spreadAngle.setText(str(CONF.spot_light.config.spread_angle))
        self.line_spotLight_blend.setText(str(CONF.spot_light.config.blend))
        self.line_spotLight_definedPos.setText(str(CONF.spot_light.position.defined))
        self.cBox_spotLight_randomPos.setChecked(bool(CONF.spot_light.position.random.enabled))
        self.line_spotLight_center.setText(str(CONF.spot_light.position.random.center))
        self.line_spotLight_minRadius.setText(str(CONF.spot_light.position.random.min_radius))
        self.line_spotLight_maxRadius.setText(str(CONF.spot_light.position.random.max_radius))
        self.line_spotLight_minElevation.setText(str(CONF.spot_light.position.random.min_elevation))
        self.line_spotLight_maxElevation.setText(str(CONF.spot_light.position.random.max_elevation))
        self.cBox_spotlight_toObjects.setChecked(bool(CONF.spot_light.rotation.to_objects))
        self.line_spotLight_definedWatt.setText(str(CONF.spot_light.intensity_watt.defined))
        self.cBox_spotLight_randomWatt.setChecked(bool(CONF.spot_light.intensity_watt.random.enabled))
        self.line_spotLight_minWatt.setText(str(CONF.spot_light.intensity_watt.random.min))
        self.line_spotLight_maxWatt.setText(str(CONF.spot_light.intensity_watt.random.max))
        #simulation
        self.line_simu_checkObjectInterval.setText(str(CONF.simulation.check_object_interval))
        self.line_simu_substepsPerFrame.setText(str(CONF.simulation.substeps_per_frame))
        self.line_simu_solverIters.setText(str(CONF.simulation.solver_iters))
        self.cBox_simu_adjustToObjects.setChecked(bool(CONF.simulation.time.adjust_to_objects))
        self.line_simu_minTime.setText(str(CONF.simulation.time.min))
        self.line_simu_maxTime.setText(str(CONF.simulation.time.max))

    def cBox_allObjsFullyVisibleChanged(self):
        if not self.cBox_cam_allObjectsFullyVisible.checkState():
            self.info("Camera Checks Objects Fully Visible Disable",
                      "This feature is crucial for accuracy in object occlussion analysis.\n"+
                      "It is recommended to enable it although it is time costly. ")

    def redrawUI(self):
        self.pB_Regenerate.setText("Re-generate\nFailed Images")
        #setting
        self.comboBox_unit.setEditable(True)
        self.comboBox_unit.lineEdit().setAlignment(qtgui.Qt.AlignCenter)
        self.comboBox_unit.lineEdit().setReadOnly(True)
        self.line_gravity.setAlignment(qtgui.Qt.AlignCenter)
        self.line_3DviewClipStart.setAlignment(qtgui.Qt.AlignCenter)
        self.line_3DviewClipEnd.setAlignment(qtgui.Qt.AlignCenter)
        self.line_engine.setAlignment(qtgui.Qt.AlignCenter)
        self.sBox_imageCompression.setAlignment(qtgui.Qt.AlignCenter)
        self.sBox_CPUCoresNum.setAlignment(qtgui.Qt.AlignCenter)
        self.sBox_numOfSubdivision.setAlignment(qtgui.Qt.AlignCenter)
        self.comboBox_denoiser.setEditable(True)
        self.comboBox_denoiser.lineEdit().setAlignment(qtgui.Qt.AlignCenter)
        self.comboBox_denoiser.lineEdit().setReadOnly(True)
        self.sBox_noiseTreshold.setAlignment(qtgui.Qt.AlignCenter)
        self.comboBox_GPUType.setEditable(True)
        self.comboBox_GPUType.lineEdit().setAlignment(qtgui.Qt.AlignCenter)
        self.comboBox_GPUType.lineEdit().setReadOnly(True)
        self.gridLayout_Setting.addWidget(self.line_ccTexturesDir, 20, 2, 1, 2)
        self.line_ccTexturesDir.setAlignment(qtgui.Qt.AlignCenter)
        #objects
        self.line_obj_linearDamping.setAlignment(qtgui.Qt.AlignCenter)
        self.line_obj_friction.setAlignment(qtgui.Qt.AlignCenter)
        self.line_obj_definedMaterial.setAlignment(qtgui.Qt.AlignCenter)
        self.line_obj_minHeight.setAlignment(qtgui.Qt.AlignCenter)
        self.line_obj_maxHeight.setAlignment(qtgui.Qt.AlignCenter)
        self.line_obj_samplingRegion.setAlignment(qtgui.Qt.AlignCenter)
        #distractor
        self.sBox_distractor_num.setAlignment(qtgui.Qt.AlignCenter)
        self.line_distractor_definedSize.setAlignment(qtgui.Qt.AlignCenter)
        self.line_distractor_minHeight.setAlignment(qtgui.Qt.AlignCenter)
        self.line_distractor_maxHeight.setAlignment(qtgui.Qt.AlignCenter)
        self.line_distractor_samplingRegion.setAlignment(qtgui.Qt.AlignCenter)
        self.line_distractor_definedSize.setAlignment(qtgui.Qt.AlignCenter)
        #ground
        self.line_gnd_rotX.setAlignment(qtgui.Qt.AlignCenter)
        self.line_gnd_rotY.setAlignment(qtgui.Qt.AlignCenter)
        self.line_gnd_rotZ.setAlignment(qtgui.Qt.AlignCenter)
        self.line_gnd_definedXY.setAlignment(qtgui.Qt.AlignCenter)
        self.line_gnd_linearDamping.setAlignment(qtgui.Qt.AlignCenter)
        self.line_gnd_friction.setAlignment(qtgui.Qt.AlignCenter)
        self.line_gnd_definedMaterial.setAlignment(qtgui.Qt.AlignCenter)
        #camera
        self.line_cam_imageWidth.setAlignment(qtgui.Qt.AlignCenter)
        self.line_cam_imageHeight.setAlignment(qtgui.Qt.AlignCenter)
        self.line_cam_clipStart.setAlignment(qtgui.Qt.AlignCenter)
        self.line_cam_clipEnd.setAlignment(qtgui.Qt.AlignCenter)
        self.line_cam_definedPos.setAlignment(qtgui.Qt.AlignCenter)
        self.line_cam_center.setAlignment(qtgui.Qt.AlignCenter)
        self.line_cam_minRadius.setAlignment(qtgui.Qt.AlignCenter)
        self.line_cam_maxRadius.setAlignment(qtgui.Qt.AlignCenter)
        self.line_cam_minElevation.setAlignment(qtgui.Qt.AlignCenter)
        self.line_cam_maxElevation.setAlignment(qtgui.Qt.AlignCenter)
        #light
        self.line_ceilLight_definedPos.setAlignment(qtgui.Qt.AlignCenter)
        self.line_ceilLight_minHeight.setAlignment(qtgui.Qt.AlignCenter)
        self.line_ceilLight_maxHeight.setAlignment(qtgui.Qt.AlignCenter)
        self.line_ceilLight_definedIntensity.setAlignment(qtgui.Qt.AlignCenter)
        self.line_ceilLight_minIntensity.setAlignment(qtgui.Qt.AlignCenter)
        self.line_ceilLight_maxIntensity.setAlignment(qtgui.Qt.AlignCenter)
        self.line_ceilLight_XY.setAlignment(qtgui.Qt.AlignCenter)
        self.sBox_spotLight_num.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_spreadAngle.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_blend.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_definedPos.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_center.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_minRadius.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_maxRadius.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_minElevation.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_maxElevation.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_definedWatt.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_minWatt.setAlignment(qtgui.Qt.AlignCenter)
        self.line_spotLight_maxWatt.setAlignment(qtgui.Qt.AlignCenter)
        #simulation
        self.line_simu_checkObjectInterval.setAlignment(qtgui.Qt.AlignCenter)
        self.line_simu_substepsPerFrame.setAlignment(qtgui.Qt.AlignCenter)
        self.line_simu_solverIters.setAlignment(qtgui.Qt.AlignCenter)
        self.line_simu_minTime.setAlignment(qtgui.Qt.AlignCenter)
        self.line_simu_maxTime.setAlignment(qtgui.Qt.AlignCenter)
        #images
        self.line_numOfImages.setAlignment(qtgui.Qt.AlignCenter)
        self.line_minOccurences.setAlignment(qtgui.Qt.AlignCenter)
        self.line_maxOccurences.setAlignment(qtgui.Qt.AlignCenter)
        self.line_totalOccurences.setAlignment(qtgui.Qt.AlignCenter)

    def changeTextColor(self, widget, color=""):
        _color = "color: {};".format(color)
        widget.setStyleSheet(_color)

    def warning(self, title:str, msg:str):
        qtw.QMessageBox.warning(self, title, msg, qtw.QMessageBox.Ok)

    def info(self, title:str, msg:str):
        qtw.QMessageBox.information(self, title, msg, qtw.QMessageBox.Ok)

    def question(self, title:str, msg:str):
        reply = qtw.QMessageBox.question(self, title, msg, qtw.QMessageBox.Yes | qtw.QMessageBox.Cancel)
        if reply == qtw.QMessageBox.Yes:
            return True
        else:
            False

def main():
    app = qtw.QApplication()
    try:
        window = Generator_Window(testing=False)
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

