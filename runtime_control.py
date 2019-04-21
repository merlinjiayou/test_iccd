# -*- coding: utf-8 -*-

"""
Module implementing runtime_control.
"""

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from Ui_runtime_control import Ui_runtime_control



class runtime_control(QWidget, Ui_runtime_control):
    update_message_signal=pyqtSignal(str)

    def __init__(self, parent=None,delayer=None,gain_controler=None,ccd=None):
        super(runtime_control, self).__init__(parent)
        self.setupUi(self)
        self.delayer=delayer
        self.gain_controler=gain_controler
        self.ccd=ccd
        self.init_ui()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def closeEvent(self, QCloseEvent):
        self.hide()


    def init_ui(self):
        if self.gain_controler.connect_status and self.delayer.connect_status and self.gain_controler.connect_status:
            self.setEnabled(True)
        else:
            self.setDisabled(True)
        try:
            self.doubleSpinBox_delay_d.setValue(float(self.delayer.config["D delay"][0:-1]))
            self.comboBox_delay_d.setCurrentText(self.delayer.config["D delay"][-1]+"s")
            self.doubleSpinBox_width_d.setValue(float(self.delayer.config["D width"][0:-1]))
            self.comboBox_width_d.setCurrentText(self.delayer.config["D width"][-1]+"s")

            enable_dic={"ON":True,"OFF":False}
            self.checkBox_channel_enable_a.setChecked(enable_dic[self.delayer.config["A enable"]])
            self.doubleSpinBox_delay_a.setValue(float(self.delayer.config["A delay"][0:-1]))
            self.comboBox_delay_a.setCurrentText(self.delayer.config["A delay"][-1] + "s")
            self.doubleSpinBox_width_a.setValue(float(self.delayer.config["A width"][0:-1]))
            self.comboBox_width_a.setCurrentText(self.delayer.config["A width"][-1] + "s")

            self.checkBox_channel_enable_b.setChecked(enable_dic[self.delayer.config["B enable"]])
            self.doubleSpinBox_delay_b.setValue(float(self.delayer.config["B delay"][0:-1]))
            self.comboBox_delay_b.setCurrentText(self.delayer.config["B delay"][-1] + "s")
            self.doubleSpinBox_width_b.setValue(float(self.delayer.config["B width"][0:-1]))
            self.comboBox_width_b.setCurrentText(self.delayer.config["B width"][-1] + "s")

            self.checkBox_channel_enable_c.setChecked(enable_dic[self.delayer.config["C enable"]])
            self.doubleSpinBox_delay_c.setValue(float(self.delayer.config["C delay"][0:-1]))
            self.comboBox_delay_c.setCurrentText(self.delayer.config["C delay"][-1] + "s")
            self.doubleSpinBox_width_c.setValue(float(self.delayer.config["C width"][0:-1]))
            self.comboBox_width_c.setCurrentText(self.delayer.config["C width"][-1] + "s")

            self.doubleSpinBox_exposure.setValue(self.ccd.get_integration_time())

            self.spinBox_mcp_gain.setValue(self.gain_controler.gain_value)
        except:
            pass
            # self.update_message_signal.emit("初始化错误")


    @pyqtSlot(bool)
    def on_checkBox_channel_enable_c_clicked(self, checked):
            enable_dic={True:"ON",False:"OFF"}
            self.delayer.channel_enable("C",enable_dic[checked])

    
    @pyqtSlot()
    def on_doubleSpinBox_delay_c_editingFinished(self):
        self.delayer.set_channel("C",delay=self.doubleSpinBox_delay_c.text()+self.comboBox_delay_c.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_width_c_editingFinished(self):
        self.delayer.set_channel("C",width=self.doubleSpinBox_width_c.text()+self.comboBox_width_c.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_delay_c_activated(self, p0):
        self.delayer.set_channel("C",delay=self.doubleSpinBox_delay_c.text()+self.comboBox_delay_c.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_width_c_activated(self, p0):
        self.delayer.set_channel("C",width=self.doubleSpinBox_width_c.text()+self.comboBox_width_c.currentText()[0])
    
    @pyqtSlot(bool)
    def on_checkBox_channel_enable_b_clicked(self, checked):
        enable_dic = {True: "ON", False: "OFF"}
        self.delayer.channel_enable("B",enable_dic[checked])
    
    @pyqtSlot()
    def on_doubleSpinBox_delay_b_editingFinished(self):
        self.delayer.set_channel("B",delay=self.doubleSpinBox_delay_b.text()+self.comboBox_delay_b.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_width_b_editingFinished(self):
        self.delayer.set_channel("B",width=self.doubleSpinBox_width_b.text()+self.comboBox_width_b.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_delay_b_activated(self, p0):
        self.delayer.set_channel("B",delay=self.doubleSpinBox_delay_b.text()+self.comboBox_delay_b.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_width_b_activated(self, p0):
        self.delayer.set_channel("B",width=self.doubleSpinBox_width_b.text()+self.comboBox_width_b.currentText()[0])
    
    @pyqtSlot(bool)
    def on_checkBox_channel_enable_a_clicked(self, checked):
        enable_dic = {True: "ON", False: "OFF"}
        self.delayer.channel_enable("A",enable_dic[checked])
    
    @pyqtSlot()
    def on_doubleSpinBox_delay_a_editingFinished(self):
        self.delayer.set_channel("A",delay=self.doubleSpinBox_delay_a.text()+self.comboBox_delay_a.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_width_a_editingFinished(self):
        self.delayer.set_channel("A",width=self.doubleSpinBox_width_a.text()+self.comboBox_width_a.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_delay_a_activated(self, p0):
        self.delayer.set_channel("A", delay=self.doubleSpinBox_delay_a.text()+self.comboBox_delay_a.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_width_a_activated(self, p0):
        self.delayer.set_channel("A",width=self.doubleSpinBox_width_a.text()+self.comboBox_width_a.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_delay_d_activated(self, p0):
        self.delayer.set_channel("D",delay=self.doubleSpinBox_delay_d.text()+self.comboBox_delay_d.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_delay_d_editingFinished(self):
        self.delayer.set_channel("D", delay=self.doubleSpinBox_delay_d.text()+self.comboBox_delay_d.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_width_d_editingFinished(self):
        self.delayer.set_channel("D",width=self.doubleSpinBox_width_d.text()+self.comboBox_width_d.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_width_d_activated(self, p0):
        self.delayer.set_channel("D",width=self.doubleSpinBox_width_d.text()+self.comboBox_width_d.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_exposure_editingFinished(self):
        self.ccd.set_integration_time(self.doubleSpinBox_exposure.value())

    @pyqtSlot()
    def on_spinBox_mcp_gain_editingFinished(self):
        self.gain_controler.set_current_vot(self.spinBox_mcp_gain.value()/1000)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = runtime_control()
    ui.show()
    sys.exit(app.exec_())