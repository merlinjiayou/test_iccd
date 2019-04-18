# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QMainWindow
from Ui_MainWindow import Ui_MainWindow
from delayer import delayer
from gain_controler import gain_controler
from ccd import ccd_em16
import threading
from runtime_control import runtime_control
from aquisition_setup import aquisition_setup
from graph_widget import graph_widget
import ctypes
import time
import numpy as np
import cv2
import os

class mdisubwindow(QtWidgets.QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.graph_widget=graph_widget()
        self.setWidget(self.graph_widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/ico_file/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

    def closeEvent(self, QCloseEvent):
        self.deleteLater()

class realtime_subwindow(QtWidgets.QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.graph_widget=graph_widget()
        self.setWidget(self.graph_widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/ico_file/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

    def closeEvent(self, QCloseEvent):
        self.hide()


class MainWindow(QMainWindow, Ui_MainWindow):
    update_progressbar_signal=pyqtSignal(int)
    plot_active_subwindow_signal=pyqtSignal()
    update_buttom_signal=pyqtSignal()
    add_subwindow_signal=pyqtSignal()
    show_message_box_signal=pyqtSignal(str)
    update_realtime_subwindow_signal=pyqtSignal()
    update_connect_status_signal=pyqtSignal()
    add_sequence_data_signal=pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.find_peaks_dll = ctypes.WinDLL("C_find_peaks.dll")
        self.update_progressbar_signal.connect(self.update_progressbar)
        self.plot_active_subwindow_signal.connect(self.update_active_subwindow)
        self.update_buttom_signal.connect(self.update_buttom)
        self.add_subwindow_signal.connect(self.add_subwindow)
        self.show_message_box_signal.connect(self.show_message_box)
        self.update_realtime_subwindow_signal.connect(self.update_realtime_subwindow)
        self.update_connect_status_signal.connect(self.init_ui)
        self.add_sequence_data_signal.connect(self.add_sequence_data)

        self.lock=threading.Lock()
        self.war_times = 0
        self.data_list=[]
        self.count_list=[]
        self.file_path={"save":"C:\\","open":"C:\\"}
        self.delayer=delayer()
        self.gain_controler=gain_controler()
        self.ccd=ccd_em16()

        self.synch_widget=None
        self.aquisition_widget=None

        self.aquisition_widget = aquisition_setup(delayer=self.delayer, gain_controler=self.gain_controler,
                                                  ccd=self.ccd)
        self.synch_widget = runtime_control(delayer=self.delayer, gain_controler=self.gain_controler, ccd=self.ccd)

        self.realtime_subwindow = realtime_subwindow()
        self.mdiArea.addSubWindow(self.realtime_subwindow)

        self.init_ui()
        check_connect_status_worker=threading.Thread(target=self.check_connect_status)
        check_connect_status_worker.setDaemon(True)
        check_connect_status_worker.start()
        self.connect_widget_status()




    def check_connect_status(self):
        while True:
            if self.ccd.cam.DeviceValid:
                time.sleep(3)
                self.update_connect_status_signal.emit()
            else:
                self.ccd.connect_status=False
                self.update_connect_status_signal.emit()
                break

    def update_message_status(self,text):
        self.statusBar.showMessage(text)

    def auto_save_function(self):
        if self.aquisition_widget.config["auto_save"]:
            file_dirpath=self.aquisition_widget.config["file_path"]
            file_name=self.aquisition_widget.config["file_name"]
            if self.aquisition_widget.config["operator_enable"]:
                operator=self.aquisition_widget.config["operator_name"]
            else:operator=""
            if self.aquisition_widget.config["date_enable"]:
                date=time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
            else:date=""
            auto_save_format=self.aquisition_widget.config["file_format"]
            file_number = 0
            while True:
                if file_number==0:
                    file_path = file_name + operator + date + auto_save_format
                else:
                    file_path=file_name+operator+date+"_"+str(file_number)+auto_save_format
                save_path=os.path.join(file_dirpath,file_path)
                if os.path.exists(save_path):
                    file_number+=1
                else:break
            if save_path:
                try:
                    if ".csv" in save_path:
                        np.savetxt(save_path, self.image, fmt="%f", delimiter=",")
                    else:
                        self.image=np.array(self.image,np.int32)
                        # io.imsave(save_path,self.active_image)
                        cv2.imwrite(save_path,self.image)
                except:
                    pass


    def connect_widget_status(self):
        self.aquisition_widget.doubleSpinBox_delay_d.valueChanged["double"].connect(self.synch_widget.doubleSpinBox_delay_d.setValue)
        self.aquisition_widget.doubleSpinBox_delay_a.valueChanged["double"].connect(self.synch_widget.doubleSpinBox_delay_a.setValue)
        self.aquisition_widget.doubleSpinBox_delay_b.valueChanged["double"].connect(self.synch_widget.doubleSpinBox_delay_b.setValue)
        self.aquisition_widget.doubleSpinBox_delay_c.valueChanged["double"].connect(self.synch_widget.doubleSpinBox_delay_c.setValue)

        self.aquisition_widget.doubleSpinBox_width_a.valueChanged["double"].connect(self.synch_widget.doubleSpinBox_width_a.setValue)
        self.aquisition_widget.doubleSpinBox_width_b.valueChanged["double"].connect(self.synch_widget.doubleSpinBox_width_b.setValue)
        self.aquisition_widget.doubleSpinBox_width_c.valueChanged["double"].connect(self.synch_widget.doubleSpinBox_width_c.setValue)
        self.aquisition_widget.doubleSpinBox_width_d.valueChanged["double"].connect(self.synch_widget.doubleSpinBox_width_d.setValue)

        self.aquisition_widget.comboBox_delay_d.activated["int"].connect(self.synch_widget.comboBox_delay_d.setCurrentIndex)
        self.aquisition_widget.comboBox_delay_a.activated["int"].connect(self.synch_widget.comboBox_delay_a.setCurrentIndex)
        self.aquisition_widget.comboBox_delay_b.activated["int"].connect(self.synch_widget.comboBox_delay_b.setCurrentIndex)
        self.aquisition_widget.comboBox_delay_c.activated["int"].connect(self.synch_widget.comboBox_delay_c.setCurrentIndex)

        self.aquisition_widget.comboBox_width_a.activated["int"].connect(self.synch_widget.comboBox_width_a.setCurrentIndex)
        self.aquisition_widget.comboBox_width_b.activated["int"].connect(self.synch_widget.comboBox_width_b.setCurrentIndex)
        self.aquisition_widget.comboBox_width_c.activated["int"].connect(self.synch_widget.comboBox_width_c.setCurrentIndex)
        self.aquisition_widget.comboBox_width_d.activated["int"].connect(self.synch_widget.comboBox_width_d.setCurrentIndex)

        self.aquisition_widget.checkBox_channel_enable_a.clicked["bool"].connect(self.synch_widget.checkBox_channel_enable_a.setChecked)
        self.aquisition_widget.checkBox_channel_enable_b.clicked["bool"].connect(self.synch_widget.checkBox_channel_enable_b.setChecked)
        self.aquisition_widget.checkBox_channel_enable_c.clicked["bool"].connect(self.synch_widget.checkBox_channel_enable_c.setChecked)

        self.aquisition_widget.doubleSpinBox_exposure_time.valueChanged["double"].connect(self.synch_widget.doubleSpinBox_exposure.setValue)
        self.aquisition_widget.spinBox_mcp_gain.valueChanged["int"].connect(self.synch_widget.spinBox_mcp_gain.setValue)

        ###########################################################
        self.synch_widget.doubleSpinBox_delay_d.valueChanged["double"].connect(self.aquisition_widget.doubleSpinBox_delay_d.setValue)
        self.synch_widget.doubleSpinBox_delay_a.valueChanged["double"].connect(self.aquisition_widget.doubleSpinBox_delay_a.setValue)
        self.synch_widget.doubleSpinBox_delay_b.valueChanged["double"].connect(self.aquisition_widget.doubleSpinBox_delay_b.setValue)
        self.synch_widget.doubleSpinBox_delay_c.valueChanged["double"].connect(self.aquisition_widget.doubleSpinBox_delay_c.setValue)

        self.synch_widget.doubleSpinBox_width_a.valueChanged["double"].connect(self.aquisition_widget.doubleSpinBox_width_a.setValue)
        self.synch_widget.doubleSpinBox_width_b.valueChanged["double"].connect(self.aquisition_widget.doubleSpinBox_width_b.setValue)
        self.synch_widget.doubleSpinBox_width_c.valueChanged["double"].connect(self.aquisition_widget.doubleSpinBox_width_c.setValue)
        self.synch_widget.doubleSpinBox_width_d.valueChanged["double"].connect(self.aquisition_widget.doubleSpinBox_width_d.setValue)

        self.synch_widget.comboBox_delay_d.activated["int"].connect(self.aquisition_widget.comboBox_delay_d.setCurrentIndex)
        self.synch_widget.comboBox_delay_a.activated["int"].connect(self.aquisition_widget.comboBox_delay_a.setCurrentIndex)
        self.synch_widget.comboBox_delay_b.activated["int"].connect(self.aquisition_widget.comboBox_delay_b.setCurrentIndex)
        self.synch_widget.comboBox_delay_c.activated["int"].connect(self.aquisition_widget.comboBox_delay_c.setCurrentIndex)

        self.synch_widget.comboBox_width_a.activated["int"].connect(self.aquisition_widget.comboBox_width_a.setCurrentIndex)
        self.synch_widget.comboBox_width_b.activated["int"].connect(self.aquisition_widget.comboBox_width_b.setCurrentIndex)
        self.synch_widget.comboBox_width_c.activated["int"].connect(self.aquisition_widget.comboBox_width_c.setCurrentIndex)
        self.synch_widget.comboBox_width_d.activated["int"].connect(self.aquisition_widget.comboBox_width_d.setCurrentIndex)

        self.synch_widget.checkBox_channel_enable_a.clicked["bool"].connect(self.aquisition_widget.checkBox_channel_enable_a.setChecked)
        self.synch_widget.checkBox_channel_enable_b.clicked["bool"].connect(self.aquisition_widget.checkBox_channel_enable_b.setChecked)
        self.synch_widget.checkBox_channel_enable_c.clicked["bool"].connect(self.aquisition_widget.checkBox_channel_enable_c.setChecked)

        self.synch_widget.doubleSpinBox_exposure.valueChanged["double"].connect(self.aquisition_widget.doubleSpinBox_exposure_time.setValue)
        self.synch_widget.spinBox_mcp_gain.valueChanged["int"].connect(self.aquisition_widget.spinBox_mcp_gain.setValue)




    def init_ui(self):
        self.aquisition_widget.tabWidget.setWindowTitle("config")
        print(self.delayer.connect_status,self.gain_controler.connect_status,self.ccd.connect_status)
        if self.delayer.connect_status and self.gain_controler.connect_status and self.ccd.connect_status:
            self.label_resolution_value.setText(str(self.ccd.get_format()))
            self.doubleSpinBox_frame_value.setValue(self.ccd.get_frame_rate())
            self.label_connect_value.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            self.toolButton_realtime.setDisabled(True)
            self.toolButton_take_signal.setDisabled(True)
            self.toolButton_stop.setDisabled(True)
            self.action_aquisition_setup.setDisabled(True)
            self.action_synch.setDisabled(True)
            self.aquisition_widget.setDisabled(True)
            self.synch_widget.setDisabled(True)
            self.label_connect_value.setStyleSheet("background-color: rgb(255, 0, 0);")
            if self.war_times==0:
                self.war_times+=1
                QtWidgets.QMessageBox.warning(self, "提示", "相机未连接", QtWidgets.QMessageBox.Ok)



    def single_measure(self):
        self.lock.acquire()
        self.delayer.channel_enable("D","ON")
        time.sleep(0.1)
        if self.ccd.cam.LiveVideoRunning:
            worker=threading.Thread(target=self.single_measure_worker)
            worker.setDaemon(True)
            worker.start()
            worker.join()
        self.delayer.channel_enable("D", "OFF")
        time.sleep(0.1)
        self.auto_save_function()
        self.lock.release()

    def single_measure_worker(self):
        self.image=np.array(self.ccd.get_data())
        self.plot_active_subwindow_signal.emit()
        self.update_buttom_signal.emit()


    def accumulation(self):
        self.lock.acquire()
        self.delayer.channel_enable("D", "ON")
        time.sleep(0.1)
        if self.ccd.cam.LiveVideoRunning:
            worker_list = []
            self.count_list.clear()
            self.data_list.clear()

            display_worker = threading.Thread(target=self.display_data)
            display_worker.setDaemon(True)
            display_worker.start()

            total_count=self.aquisition_widget.spinBox_frame_count.value()
            for i in range(5):
                count=total_count//(5-i)
                total_count=total_count-count
                self.count_list.append(0)
                self.data_list.append((ctypes.c_uint32 * self.ccd.cam.ImageWidth * self.ccd.cam.ImageHeight)())
                worker=threading.Thread(target=self.accumulation_worker,args=(i,count))
                worker.setDaemon(True)
                worker_list.append(worker)
                worker.start()
            for worker in worker_list:
                worker.join()
        self.delayer.channel_enable("D", "OFF")
        time.sleep(0.1)
        self.auto_save_function()
        self.lock.release()


    def accumulation_worker(self,num,count):
        height = ctypes.c_int(self.ccd.cam.ImageHeight)
        width = ctypes.c_int(self.ccd.cam.ImageWidth)
        while self.toolButton_take_signal.isChecked():
            if self.count_list[num] >= count:
                break
            if self.ccd.cam.LiveVideoRunning:
                try:
                    data = self.ccd.get_data()
                    if self.ccd.get_image_bit() == 8:
                        # data_ptr = ctypes.cast(data.ctypes.data, ctypes.POINTER(ctypes.c_uint8))
                        self.find_peaks_dll.add_arry_8(ctypes.byref(data), ctypes.byref(self.data_list[num]), height, width)
                        self.count_list[num] += 1
                    else:
                        # data_ptr = ctypes.cast(data.ctypes.data, ctypes.POINTER(ctypes.c_uint16))
                        self.find_peaks_dll.add_arry_16(ctypes.byref(data), ctypes.byref(self.data_list[num]), height, width)
                        self.count_list[num] += 1
                except:
                    pass
            else:
                time.sleep(0.01)



    def spc(self):
        self.lock.acquire()
        self.delayer.channel_enable("D", "ON")
        time.sleep(0.1)
        if self.ccd.cam.LiveVideoRunning:
            worker_list = []
            self.count_list.clear()
            self.data_list.clear()

            display_worker = threading.Thread(target=self.display_data)
            display_worker.setDaemon(True)
            display_worker.start()

            total_count = self.aquisition_widget.spinBox_frame_count.value()
            for i in range(5):
                count = total_count // (5 - i)
                total_count = total_count - count
                self.count_list.append(0)
                self.data_list.append((ctypes.c_uint16 * self.ccd.cam.ImageWidth * self.ccd.cam.ImageHeight)())
                worker = threading.Thread(target=self.spc_worker,args=(i,count))
                worker.setDaemon(True)
                worker_list.append(worker)
                worker.start()
            for worker in worker_list:
                worker.join()
        self.delayer.channel_enable("D", "OFF")
        time.sleep(0.1)
        self.auto_save_function()
        self.lock.release()


    def spc_worker(self,num,count):
        height = ctypes.c_int(self.ccd.cam.ImageHeight)
        width = ctypes.c_int(self.ccd.cam.ImageWidth)
        min_value = ctypes.c_int(int(self.ccd.get_bright() * 30 / 500 + 3))
        while self.toolButton_take_signal.isChecked():
            if self.count_list[num] >= count:
                break
            if self.ccd.cam.LiveVideoRunning:
                try:
                    data = self.ccd.get_data()
                    if self.ccd.get_image_bit() == 8:
                        self.find_peaks_dll.find_peak_8(ctypes.byref(data), ctypes.byref(self.data_list[num]), height, width,min_value,ctypes.c_int(self.aquisition_widget.spinBox_threshold.value()))
                        self.count_list[num] += 1
                    else:
                        self.find_peaks_dll.find_peak_16(ctypes.byref(data), ctypes.byref(self.data_list[num]), height, width,min_value,ctypes.c_int(self.aquisition_widget.spinBox_threshold.value()))
                        self.count_list[num] += 1
                except:
                    pass
            else:
                time.sleep(0.01)

    def sequence(self):
        self.lock.acquire()
        self.delayer.channel_enable("D", "ON")
        for i in range(self.aquisition_widget.spinBox_measure_count.value()):
            if self.toolButton_stop.isChecked():
                break
            self.set_sequence_parameter()
            self.get_sequence_data()
            self.add_sequence_data_signal.emit()
        self.aquisition_widget.recovery_parameter()
        self.delayer.channel_enable("D", "OFF")
        self.lock.release()


    def get_sequence_data(self):
        if self.aquisition_widget.comboBox_measure_mode.currentText()=="单次":
            if self.ccd.cam.LiveVideoRunning:
                self.image = np.array(self.ccd.get_data())
                self.plot_active_subwindow_signal.emit()
        elif self.aquisition_widget.comboBox_measure_mode.currentText()=="累加":
            if self.ccd.cam.LiveVideoRunning:
                worker_list = []
                self.count_list.clear()
                self.data_list.clear()

                display_worker = threading.Thread(target=self.display_data)
                display_worker.setDaemon(True)
                display_worker.start()

                total_count = self.aquisition_widget.spinBox_frame_count.value()
                for i in range(5):
                    count = total_count // (5 - i)
                    total_count = total_count - count
                    self.count_list.append(0)
                    self.data_list.append((ctypes.c_uint32 * self.ccd.cam.ImageWidth * self.ccd.cam.ImageHeight)())
                    worker = threading.Thread(target=self.accumulation_worker, args=(i, count))
                    worker.setDaemon(True)
                    worker_list.append(worker)
                    worker.start()
                for worker in worker_list:
                    worker.join()
        elif self.aquisition_widget.comboBox_measure_mode.currentText()=="光子计数":
            if self.ccd.cam.LiveVideoRunning:
                worker_list = []
                self.count_list.clear()
                self.data_list.clear()

                display_worker = threading.Thread(target=self.display_data)
                display_worker.setDaemon(True)
                display_worker.start()

                total_count = self.aquisition_widget.spinBox_frame_count.value()
                for i in range(5):
                    count = total_count // (5 - i)
                    total_count = total_count - count
                    self.count_list.append(0)
                    self.data_list.append((ctypes.c_uint16 * self.ccd.cam.ImageWidth * self.ccd.cam.ImageHeight)())
                    worker = threading.Thread(target=self.spc_worker, args=(i, count))
                    worker.setDaemon(True)
                    worker_list.append(worker)
                    worker.start()
                for worker in worker_list:
                    worker.join()
        return self.image


    def add_sequence_data(self):
        self.active_subwindow.graph_widget.add_image_3D(self.image)



    def display_data(self):
        while self.toolButton_take_signal.isChecked():
            total_count = 0
            if self.count_list!=[]:
                for count in self.count_list:
                    total_count+=count
                value=round(total_count / self.aquisition_widget.config["frame_count"]*100)
                self.update_progressbar_signal.emit(value)
            if total_count>=self.aquisition_widget.config["frame_count"] or (not self.toolButton_take_signal.isChecked()):
                print("总计",total_count)
                self.update_buttom_signal.emit()
            if self.data_list!=[]:
                for num ,data in enumerate(self.data_list):
                    data=np.array(data)
                    if num==0:
                        self.image=data
                    else:
                        self.image=np.add(self.image,data)
                self.plot_active_subwindow_signal.emit()
            time.sleep(0.03)


    def show_message_box(self,text):
        QtWidgets.QMessageBox.warning(self, "提示", text, QtWidgets.QMessageBox.Ok)


    def update_active_subwindow(self):
        self.active_subwindow.graph_widget.plot_image(self.image)

    def update_realtime_subwindow(self):
        self.realtime_subwindow.graph_widget.plot(self.realtime_image)



    def update_progressbar(self,value):
        self.progressBar.setValue(value)

    def update_buttom(self):
        self.toolButton_stop.setChecked(True)


    def add_subwindow(self):
        if len(self.mdiArea.subWindowList())>40:
            QtWidgets.QMessageBox.warning(self,"警告！","打开窗口过多，请关闭一部分",QtWidgets.QMessageBox.Ok)
        else:
            self.active_subwindow = mdisubwindow()
            self.active_subwindow.setWindowTitle("图像" + str(len(self.mdiArea.subWindowList())))
            self.mdiArea.addSubWindow(self.active_subwindow)
            self.active_subwindow.resize(800, 500)
            self.active_subwindow.show()
            self.mdiArea.setActiveSubWindow(self.active_subwindow)


    
    @pyqtSlot(bool)
    def on_toolButton_realtime_toggled(self, checked):
        if checked:
            self.realtime_subwindow.show()
            self.mdiArea.setActiveSubWindow(self.realtime_subwindow)
            worker=threading.Thread(target=self.realtime_worker)
            worker.setDaemon(True)
            worker.start()



    def realtime_worker(self):
        self.lock.acquire()
        self.delayer.channel_enable("D", "ON")
        time.sleep(0.1)
        while self.toolButton_realtime.isChecked():
            if self.ccd.cam.LiveVideoRunning:
                self.realtime_image=self.ccd.get_data()
                self.update_realtime_subwindow_signal.emit()
            time.sleep(0.03)
        self.delayer.channel_enable("D", "OFF")
        time.sleep(0.1)
        self.lock.release()


    
    @pyqtSlot(bool)
    def on_toolButton_take_signal_toggled(self, checked):
        if checked:
            self.add_subwindow_signal.emit()
            mode_dic={"单次":self.single_measure,"累加":self.accumulation,"运动":None,"光子计数":self.spc}
            worker=threading.Thread(target=mode_dic[self.aquisition_widget.config["mode"]])
            worker.setDaemon(True)
            worker.start()

    
    @pyqtSlot(bool)
    def on_toolButton_stop_toggled(self, checked):
        pass
    
    @pyqtSlot()
    def on_action_aquisition_setup_triggered(self):
        self.aquisition_widget.resize(self.aquisition_widget.minimumSizeHint())
        self.aquisition_widget.show()


    
    @pyqtSlot()
    def on_action_save_triggered(self):
        self.worker=threading.Thread(target=self.save_worker)
        self.worker.start()

    def save_worker(self):
        filepath,_=QtWidgets.QFileDialog.getSaveFileName(caption="保存文件",directory=self.file_path["save"],filter="file type(*.tiff);;file type(*.png);;file type(*.jpg);;file type(*.csv)")
        if filepath:
            self.file_path["save"] = os.path.split(filepath)[0]
            active_subwindow = self.mdiArea.activeSubWindow()
            if "图像" in active_subwindow.windowTitle():
                data = active_subwindow.graph_widget.image_data
                data = np.array(data, np.int32)
                if ".csv" in filepath:
                    np.savetxt(filepath, data, fmt="%f", delimiter=",")
                else:
                    cv2.imwrite(filepath, data)
            else:
                self.show_message_box_signal.emit("请选择图像")


    
    @pyqtSlot()
    def on_action_open_triggered(self):
        worker=threading.Thread(target=self.open_file_worker)
        worker.start()

    def open_file_worker(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(caption="打开文件", directory=self.file_path["open"],
                                                            filter="file type(*.tiff);;file type(*.png);;file type(*.jpg);;file type(*.csv)")
        if filepath:
            self.file_path["open"] = os.path.split(filepath)[0]
            file_name = os.path.split(filepath)[1]
            try:
                if ".csv" in file_name:
                    self.image = np.loadtxt(filepath, delimiter=",")
                else:
                    self.image = cv2.imread(filepath, 0)
                self.image=self.image[::-1]
                self.add_subwindow_signal.emit()
                self.plot_active_subwindow_signal.emit()
            except:
                self.show_message_box_signal.emit("文件格式错误")

    @pyqtSlot()
    def on_action_open_sequence_file_triggered(self):
        worker=threading.Thread(target=self.open_sequence_file_worker)
        worker.setDaemon(True)
        worker.start()

    def open_sequence_file_worker(self):
        file_path_list,_=QtWidgets.QFileDialog.getOpenFileNames(self,"打开序列文件",self.file_path["open"],"file type(*.tiff);;file type(*.png);;file type(*.jpg);;file type(*.csv)")
        if file_path_list:
            file_path_list=[]
            file_path_list.sort()
            self.add_subwindow_signal.emit()
            for file_path in file_path_list:
                try:
                    self.file_path["open"] = os.path.split(file_path)[0]
                    if ".csv" in file_path:
                        self.image = np.loadtxt(file_path, delimiter=",")
                    else:
                        self.image = cv2.imread(file_path, 0)
                    self.image = self.image[::-1]
                    self.add_sequence_data_signal.emit()
                except:
                    self.show_message_box_signal.emit("文件格式错误")



    @pyqtSlot()
    def on_action_save_sequence_file_triggered(self):
        worker=threading.Thread(target=self.save_sequence_file_worker)
        worker.setDaemon(True)
        worker.start()

    def save_sequence_file_worker(self):
        file_path,_=QtWidgets.QFileDialog.getSaveFileName(self,"保存序列文件",self.file_path["save"],"file type(*.tiff);;file type(*.png);;file type(*.jpg);;file type(*.csv)")
        if file_path:
            self.file_path["save"] = os.path.split(file_path)[0]
            file_name_full=os.path.split(file_path)[0]
            file_name=os.path.splitext(file_name_full)[0]
            file_exp=os.path.splitext(file_name_full)[1]
            active_subwindow = self.mdiArea.activeSubWindow()
            if "图像" in active_subwindow.windowTitle():
                for num,data in enumerate(active_subwindow.graph_widget.image_list):
                    try:
                        save_file_path=os.path.join(self.file_path["save"],file_name+"_%d"%num+file_exp)
                        data = np.array(data, np.int32)
                        if ".csv" in save_file_path:
                            np.savetxt(save_file_path, data, fmt="%f", delimiter=",")
                        else:
                            cv2.imwrite(save_file_path, data)
                    except:
                        self.show_message_box_signal.emit("数据错误")

    @pyqtSlot()
    def on_action_save_config_triggered(self):
        worker=threading.Thread(target=self.save_config_worker)
        worker.setDaemon(True)
        worker.start()

    def save_config_worker(self):
        file_path,_=QtWidgets.QFileDialog.getSaveFileName(self,"保存配置",self.file_path["save"],"file type(*.ini)")
        if file_path:
            self.aquisition_widget.save_config(file_path)


    @pyqtSlot()
    def on_action_open_config_triggered(self):
        worker=threading.Thread(target=self.open_config_worker)
        worker.setDaemon(True)
        worker.start()

    def open_config_worker(self):
        file_path,_=QtWidgets.QFileDialog.getOpenFileName(self,"加载配置",self.file_path["open"],"file type(*.ini)")
        if file_path:
            self.aquisition_widget.load_config(file_path)

    
    @pyqtSlot()
    def on_action_exit_triggered(self):
        sys.exit()

    @pyqtSlot()
    def on_action_synch_triggered(self):
        self.synch_widget.show()


    def closeEvent(self, *args, **kwargs):
        sys.exit()

    @pyqtSlot()
    def on_action_tiling_triggered(self):
        self.mdiArea.tileSubWindows()
        self.ccd.Save_Device_State()

    @pyqtSlot()
    def on_action_cascade_triggered(self):
        self.mdiArea.cascadeSubWindows()

    @pyqtSlot()
    def on_action_clear_triggered(self):
        self.mdiArea.closeAllSubWindows()

    @pyqtSlot(bool)
    def on_action_subwindow_toggled(self, p0):
        if p0:
            self.mdiArea.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        else:
            self.mdiArea.setViewMode(QtWidgets.QMdiArea.TabbedView)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("Logo.png"))
    splash.showMessage("您好，相机正在初始化中，请稍等...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.show()  # 显示启动界面
    QtWidgets.qApp.processEvents()
    MainWindow = MainWindow()
    MainWindow.show()
    splash.finish(MainWindow)
    sys.exit(app.exec_())
    

