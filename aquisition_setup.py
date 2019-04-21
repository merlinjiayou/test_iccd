# -*- coding: utf-8 -*-

"""
Module implementing aquisition_setup.
"""

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from Ui_aquisition_setup import Ui_aquisition_setup
# from delayer import delayer
# from gain_controler import gain_controler
# from ccd import ccd_em16
import threading
import math
# import time
from PyQt5.QtCore import Qt
import configparser


class aquisition_setup(QWidget, Ui_aquisition_setup):
    update_init_signal=pyqtSignal()
    update_message_signal=pyqtSignal(str)
    update_frame_rates_signal=pyqtSignal()
    update_current_autoparameter=pyqtSignal(float,float)

    def __init__(self, parent=None,delayer=None,gain_controler=None,ccd=None):

        super(aquisition_setup, self).__init__(parent)
        self.setupUi(self)
        self.update_init_signal.connect(self.init_ui)
        self.update_frame_rates_signal.connect(self.update_frame_rates)
        self.update_current_autoparameter.connect(self.display_current_autoparameter)
        self.delayer=delayer
        self.gain_controler=gain_controler
        self.ccd=ccd
        if self.ccd.connect_status:
            if self.ccd.cam.Devices[0].Name == "DMK 33UX174":
                self.roi_list=[(0,0,1920,1200,"")]
            else:
                self.roi_list = [(0, 0, 1440, 1080, "")]
        self.config={"mode":"单次",
                     "frame_count":1,
                     "read_mode":"图像",
                    "auto_save":False,
                     "file_format":".tiff",
                     "file_name":"Image",
                     "file_path":"C:\\",
                     "date_enable":False,
                     "operator_enable":False,
                     "operator_name":"admin"
                     }
        self.init_ui()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def closeEvent(self, QCloseEvent):
        self.hide()

    def update_frame_rates(self):
        frame_list = self.ccd.get_frames()
        self.comboBox_frame_rate.clear()
        for num, framerate in enumerate(frame_list):
            self.comboBox_frame_rate.addItem("")
            self.comboBox_frame_rate.setItemText(num, str(framerate))
        frame_rate=self.ccd.get_frame_rate()
        if frame_rate in frame_list:
            self.comboBox_frame_rate.setCurrentText(str(frame_rate))
        else:
            self.comboBox_frame_rate.addItem("")
            self.comboBox_frame_rate.setItemText(num, str(frame_rate))
            self.comboBox_frame_rate.setCurrentText(str(frame_rate))



    def init_ui(self):
        # try:
            self.spinBox_mcp_gain.setValue(self.gain_controler.gain_value)
            self.doubleSpinBox_exposure_time.setValue(self.ccd.get_integration_time())
            self.doubleSpinBox_pre_gain.setValue(self.ccd.get_gain())
            self.spinBox_roi_left.setValue(0)
            self.spinBox_roi_bottom.setValue(0)
            self.spinBox_roi_right.setValue(self.ccd.get_image_width())
            self.spinBox_roi_top.setValue(self.ccd.get_image_height())
            self.spinBox_roi_height.setValue(self.ccd.get_image_height())
            self.spinBox_roi_width.setValue(self.ccd.get_image_width())
            if self.ccd.connect_status:
                if self.ccd.cam.Devices[0].Name=="DMK 33UX174":
                    self.groupBox_5.setDisabled(True)
            else:
                binning_value=self.ccd.get_binning()
                if binning_value==1:
                    self.radioButton_binning1.setChecked(True)
                elif binning_value==5:
                    self.radioButton_binning2.setChecked(True)
                elif binning_value==6:
                    self.radioButton_binning3.setChecked(True)
                elif binning_value==7:
                    self.radioButton_binning4.setChecked(True)
            frame_list=self.ccd.get_frames()
            self.comboBox_frame_rate.clear()
            for num,framerate in enumerate(frame_list):
                self.comboBox_frame_rate.addItem("")
                self.comboBox_frame_rate.setItemText(num,str(framerate))
            self.comboBox_frame_rate.setCurrentText(str(self.ccd.get_frame_rate()))

            trigger_mode_dic={"SYN":"内触发","POS":"外触发","NEG":"外触发","YN":"内触发"}
            self.comboBox_trigger_mode.setCurrentText(trigger_mode_dic[self.delayer.config["trigger mode"]])
            self.doubleSpinBox_internal_trigger_rate.setValue(self.delayer.config["trigger freq"])
            if self.delayer.config["trigger mode"]=="NEG":
                self.comboBox_trigger_edge.setCurrentText("下降沿")
            else:self.comboBox_trigger_edge.setCurrentText("上升沿")
            trigger_impedance_dic={"HIZ":"HIZ","50R":"50Ω","50":"50Ω"}
            self.doubleSpinBox_divisor.setValue(self.delayer.config["trigger divisor"])
            self.comboBox_trigger_impedance.setCurrentText(trigger_impedance_dic[self.delayer.config["trigger impedance"]])
            self.doubleSpinBox_trigger_level.setValue(self.delayer.config["trigger level"])

            polarity_dic={"POS":"正","NEG":"负","OS":"正"}
            self.doubleSpinBox_delay_d.setValue(float(self.delayer.config["D delay"][0:-1]))
            self.comboBox_delay_d.setCurrentText(self.delayer.config["D delay"][-1] + "s")
            self.doubleSpinBox_width_d.setValue(float(self.delayer.config["D width"][0:-1]))
            self.comboBox_width_d.setCurrentText(self.delayer.config["D width"][-1] + "s")



            enable_dic = {"ON": True, "OFF": False}
            self.checkBox_channel_enable_a.setChecked(enable_dic[self.delayer.config["A enable"]])
            self.doubleSpinBox_delay_a.setValue(float(self.delayer.config["A delay"][0:-1]))
            self.comboBox_delay_a.setCurrentText(self.delayer.config["A delay"][-1] + "s")
            self.doubleSpinBox_width_a.setValue(float(self.delayer.config["A width"][0:-1]))
            self.comboBox_width_a.setCurrentText(self.delayer.config["A width"][-1] + "s")
            self.comboBox_polarity_a.setCurrentText(polarity_dic[self.delayer.config["A polarity"]])

            self.checkBox_channel_enable_b.setChecked(enable_dic[self.delayer.config["B enable"]])
            self.doubleSpinBox_delay_b.setValue(float(self.delayer.config["B delay"][0:-1]))
            self.comboBox_delay_b.setCurrentText(self.delayer.config["B delay"][-1] + "s")
            self.doubleSpinBox_width_b.setValue(float(self.delayer.config["B width"][0:-1]))
            self.comboBox_width_b.setCurrentText(self.delayer.config["B width"][-1] + "s")
            self.comboBox_polarity_b.setCurrentText(polarity_dic[self.delayer.config["B polarity"]])

            self.checkBox_channel_enable_c.setChecked(enable_dic[self.delayer.config["C enable"]])
            self.doubleSpinBox_delay_c.setValue(float(self.delayer.config["C delay"][0:-1]))
            self.comboBox_delay_c.setCurrentText(self.delayer.config["C delay"][-1] + "s")
            self.doubleSpinBox_width_c.setValue(float(self.delayer.config["C width"][0:-1]))
            self.comboBox_width_c.setCurrentText(self.delayer.config["C width"][-1] + "s")
            print(self.delayer.config)
            self.comboBox_polarity_c.setCurrentText(polarity_dic[self.delayer.config["C polarity"]])

            self.spinBox_burst_count.setValue(self.delayer.config["burst count"])
            if self.delayer.config["gate mode"]=="OFF" and self.delayer.config["burst enable"]=="OFF":
                self.checkBox_enable_ioc.setChecked(True)
                self.radioButton_fit_ccd.setChecked(True)
            elif self.delayer.config["gate mode"]=="BUR" and self.delayer.config["burst enable"]=="ON":
                self.radioButton_burst.setChecked(True)
                if self.delayer.config["burst count"]==1:
                    self.checkBox_enable_ioc.setChecked(False)
                else:
                    self.checkBox_enable_ioc.setChecked(True)
        # except:
        #     pass
        #     self.update_message_signal.emit("初始化失败")


    

    
    @pyqtSlot()
    def on_spinBox_roi_left_editingFinished(self):
        width=((self.spinBox_roi_right.value()-self.spinBox_roi_left.value())//16)*16
        self.spinBox_roi_width.setValue(width)
    
    @pyqtSlot()
    def on_spinBox_roi_bottom_editingFinished(self):
        height=((self.spinBox_roi_top.value()-self.spinBox_roi_bottom.value())//4)*4
        self.spinBox_roi_height.setValue(height)
    
    @pyqtSlot()
    def on_spinBox_roi_right_editingFinished(self):
        width = ((self.spinBox_roi_right.value() - self.spinBox_roi_left.value()) // 16) * 16
        self.spinBox_roi_width.setValue(width)


    @pyqtSlot()
    def on_spinBox_roi_top_editingFinished(self):
        height = ((self.spinBox_roi_top.value() - self.spinBox_roi_bottom.value()) // 4) * 4
        self.spinBox_roi_height.setValue(height)

    @pyqtSlot()
    def on_pushButton_roi_sure_clicked(self):
        "Y800 (300x288)"
        # status=self.delayer.device_status()
        # print(status)
        binning_mode=self.ccd.get_binning()
        roi_dic={1:"",5:"[Skipping 2x]",6:"[Skipping 2x vertical]",7:"[Skipping 2x horizontal]"}
        width=self.spinBox_roi_width.value()
        height=self.spinBox_roi_height.value()
        if height<4 or width<256:
            if height<4:
                QtWidgets.QMessageBox.warning(self,"错误！","高度值过小")
            else:
                QtWidgets.QMessageBox.warning(self, "错误！", "宽度值过小")
        else:
            print(self.ccd.get_image_bit())
            position_x = self.ccd.get_x_offset() + self.spinBox_roi_left.value()
            position_y = self.ccd.get_y_offset() + (self.ccd.get_image_height() - self.spinBox_roi_top.value())
            if self.ccd.get_image_bit()==8:
                self.ccd.set_Video_Format("Y800 (%dx%d) %s"%(width,height,roi_dic[binning_mode]))
            else:
                print(self.ccd.get_format())
                self.ccd.set_Video_Format("Y16 (%dx%d) %s" % (width, height,roi_dic[binning_mode]))
            self.ccd.set_x_offset(position_x)
            self.ccd.set_y_offset(position_y)
            self.roi_list.append((position_x,position_y,width,height,roi_dic[binning_mode]))
            self.spinBox_roi_left.setValue(0)
            self.spinBox_roi_bottom.setValue(0)
            self.spinBox_roi_right.setValue(width)
            self.spinBox_roi_top.setValue(height)
            self.update_frame_rates_signal.emit()

    @pyqtSlot()
    def on_pushButton_roi_resume_clicked(self):
        width = self.roi_list[0][2]
        height = self.roi_list[0][3]
        position_x = self.roi_list[0][0]
        position_y = self.roi_list[0][1]

        if self.ccd.get_image_bit() == 8:
            print(width,height)
            self.ccd.set_Video_Format("Y800 (%dx%d)" % (width, height))
        else:
            self.ccd.set_Video_Format("Y16 (%dx%d)" % (width, height))

        self.ccd.set_x_offset(position_x)
        self.ccd.set_y_offset(position_y)

        self.update_init_signal.emit()

        # self.spinBox_roi_left.setValue(0)
        # self.spinBox_roi_bottom.setValue(0)
        # self.spinBox_roi_right.setValue(width)
        # self.spinBox_roi_top.setValue(height)





    @pyqtSlot()
    def on_pushButton_revoke_clicked(self):
        if len(self.roi_list)>1:
            self.roi_list.pop()
            width = self.roi_list[-1][2]
            height = self.roi_list[-1][3]
            position_x = self.roi_list[-1][0]
            position_y = self.roi_list[-1][1]
            binning=self.roi_list[-1][4]

            if self.ccd.get_image_bit() == 8:
                self.ccd.set_Video_Format("Y800 (%dx%d) %s" % (width, height,binning))
            else:
                self.ccd.set_Video_Format("Y16 (%dx%d) %s" % (width, height,binning))

            self.ccd.set_x_offset(position_x)
            self.ccd.set_y_offset(position_y)

            self.update_init_signal.emit()

            # self.spinBox_roi_left.setValue(0)
            # self.spinBox_roi_bottom.setValue(0)
            # self.spinBox_roi_right.setValue(width)
            # self.spinBox_roi_top.setValue(height)
    
    @pyqtSlot(bool)
    def on_radioButton_binning1_clicked(self, checked):
        if checked:
            self.ccd.set_binning(1)
            self.update_init_signal.emit()
    
    @pyqtSlot(bool)
    def on_radioButton_binning2_clicked(self, checked):
        print(checked)
        if checked:
            self.ccd.set_binning(5)
            self.update_init_signal.emit()


    @pyqtSlot(bool)
    def on_radioButton_binning3_clicked(self, checked):
        if checked:
            self.ccd.set_binning(6)
            self.update_init_signal.emit()

    @pyqtSlot(bool)
    def on_radioButton_binning4_clicked(self, checked):
        if checked:
            self.ccd.set_binning(7)
            self.update_init_signal.emit()
    
    @pyqtSlot()
    def on_spinBox_mcp_gain_editingFinished(self):
        self.gain_controler.set_current_vot(self.spinBox_mcp_gain.value()/1000)
    
    @pyqtSlot(bool)
    def on_checkBox_channel_enable_c_clicked(self, checked):
        enable_dic={True:"ON",False:"OFF"}
        self.delayer.channel_enable("C",enable_dic[checked])
    
    @pyqtSlot()
    def on_doubleSpinBox_width_c_editingFinished(self):
        self.delayer.set_channel("C",width=self.doubleSpinBox_width_c.text()+self.comboBox_width_c.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_delay_c_activated(self, p0):
        self.delayer.set_channel("C",delay=self.doubleSpinBox_delay_c.text()+self.comboBox_delay_c.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_width_c_activated(self, p0):
        self.delayer.set_channel("C",width=self.doubleSpinBox_width_c.text()+self.comboBox_width_c.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_delay_c_editingFinished(self):
        self.delayer.set_channel("C",delay=self.doubleSpinBox_delay_c.text()+self.comboBox_delay_c.currentText()[0])
    
    @pyqtSlot(int)
    def on_comboBox_polarity_c_activated(self, p0):
        polarit_dic={0:"POS",1:"NEG"}
        self.delayer.set_channel("C",polarity=polarit_dic[p0])
    
    @pyqtSlot(bool)
    def on_checkBox_same_to_gate_c_clicked(self, checked):
        if checked:
            self.delayer.set_channel("C",delay=self.doubleSpinBox_delay_d.text()+self.comboBox_delay_d.currentText()[0],width=self.doubleSpinBox_width_d.text()+self.comboBox_width_d.currentText()[0])
        else:
            self.delayer.set_channel("C",delay=self.doubleSpinBox_delay_c.text()+self.comboBox_delay_c.currentText()[0],width=self.doubleSpinBox_width_c.text()+self.comboBox_width_c.currentText()[0])
    
    @pyqtSlot(bool)
    def on_checkBox_channel_enable_b_clicked(self, checked):
        enable_dic = {True: "ON", False: "OFF"}
        self.delayer.channel_enable("B", enable_dic[checked])

    
    @pyqtSlot()
    def on_doubleSpinBox_width_b_editingFinished(self):
        self.delayer.set_channel("B",width=self.doubleSpinBox_width_b.text()+self.comboBox_width_b.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_delay_b_activated(self, p0):
        self.delayer.set_channel("B",delay=self.doubleSpinBox_delay_b.text()+self.comboBox_delay_b.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_width_b_activated(self, p0):
        self.delayer.set_channel("B",width=self.doubleSpinBox_width_b.text()+self.comboBox_width_b.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_delay_b_editingFinished(self):
        self.delayer.set_channel("B",delay=self.doubleSpinBox_delay_b.text()+self.comboBox_delay_b.currentText()[0])
    
    @pyqtSlot(int)
    def on_comboBox_polarity_b_activated(self, p0):
        polarit_dic={0:"POS",1:"NEG"}
        self.delayer.set_channel("B",polarity=polarit_dic[p0])
    
    @pyqtSlot(bool)
    def on_checkBox_same_to_gate_b_clicked(self, checked):
        if checked:
            self.delayer.set_channel("B",delay=self.doubleSpinBox_delay_d.text()+self.comboBox_delay_d.currentText()[0],width=self.doubleSpinBox_width_d.text()+self.comboBox_width_d.currentText()[0])
        else:
            self.delayer.set_channel("B",delay=self.doubleSpinBox_delay_b.text()+self.comboBox_delay_b.currentText()[0],width=self.doubleSpinBox_width_b.text()+self.comboBox_width_b.currentText()[0])
    
    @pyqtSlot(bool)
    def on_checkBox_channel_enable_a_clicked(self, checked):
        enable_dic = {True: "ON", False: "OFF"}
        self.delayer.channel_enable("A", enable_dic[checked])
    
    @pyqtSlot()
    def on_doubleSpinBox_width_a_editingFinished(self):
        self.delayer.set_channel("A",width=self.doubleSpinBox_width_a.text()+self.comboBox_width_a.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_delay_a_activated(self, p0):
        self.delayer.set_channel("A",delay=self.doubleSpinBox_delay_a.text()+self.comboBox_delay_a.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_width_a_activated(self, p0):
        self.delayer.set_channel("A",width=self.doubleSpinBox_width_a.text()+self.comboBox_width_a.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_delay_a_editingFinished(self):
        self.delayer.set_channel("A",delay=self.doubleSpinBox_delay_a.text()+self.comboBox_delay_a.currentText()[0])
    
    @pyqtSlot(int)
    def on_comboBox_polarity_a_activated(self, p0):
        polarit_dic={0:"POS",1:"NEG"}
        self.delayer.set_channel("A",polarity=polarit_dic[p0])
    
    @pyqtSlot(bool)
    def on_checkBox_same_to_gate_a_clicked(self, checked):
        if checked:
            self.delayer.set_channel("A",delay=self.doubleSpinBox_delay_d.text()+self.comboBox_delay_d.currentText()[0],width=self.doubleSpinBox_width_d.text()+self.comboBox_width_d.currentText()[0])
        else:
            self.delayer.set_channel("A",delay=self.doubleSpinBox_delay_a.text()+self.comboBox_delay_a.currentText()[0],width=self.doubleSpinBox_width_a.text()+self.comboBox_width_a.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_width_d_editingFinished(self):
        self.delayer.set_channel("D",width=self.doubleSpinBox_width_d.text()+self.comboBox_width_d.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_delay_d_activated(self, p0):
        self.delayer.set_channel("D",delay=self.doubleSpinBox_delay_d.text()+self.comboBox_delay_d.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_width_d_activated(self, p0):
        self.delayer.set_channel("D",width=self.doubleSpinBox_width_d.text()+self.comboBox_width_d.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_delay_d_editingFinished(self):
        self.delayer.set_channel("D",delay=self.doubleSpinBox_delay_d.text()+self.comboBox_delay_d.currentText()[0])
    
    @pyqtSlot(bool)
    def on_checkBox_enable_ioc_clicked(self, checked):
        if checked:
            if self.radioButton_fit_ccd.isChecked():
                self.on_radioButton_fit_ccd_clicked(True)
            else:self.on_radioButton_burst_clicked(True)
        else:
            self.delayer.gate_set(gate_mod="BUR")
            self.delayer.burst_turn("ON")
            self.delayer.burst_set(1)
    
    @pyqtSlot(bool)
    def on_radioButton_fit_ccd_clicked(self, checked):
        if checked:
            self.delayer.gate_set(gate_mod="OFF")
            self.delayer.burst_turn("OFF")
    
    @pyqtSlot(bool)
    def on_radioButton_burst_clicked(self, checked):
        if checked:
            self.delayer.gate_set(gate_mod="BUR")
            self.delayer.burst_turn("ON")
            self.delayer.burst_set(self.spinBox_burst_count.value())
    
    @pyqtSlot()
    def on_spinBox_burst_count_editingFinished(self):
        self.delayer.burst_set(self.spinBox_burst_count.value())
    
    @pyqtSlot(str)
    def on_comboBox_measure_mode_activated(self, p0):
        self.config["mode"]=p0
        if p0=="单次":
            self.widget_total_frame_count.hide()
        else:
            self.widget_total_frame_count.show()
        if p0=="光子计数":
            self.widget_2.show()
        else:
            self.widget_2.hide()
    
    @pyqtSlot(str)
    def on_comboBox_trigger_mode_activated(self, p0):
        if p0=="内触发":
            self.delayer.trigger_source("SYN")
        else:
            trigger_edge={"上升沿":"POS","下降沿":"NEG"}
            self.delayer.trigger_source(trigger_edge[self.comboBox_trigger_edge.currentText()])

    @pyqtSlot(str)
    def on_comboBox_trigger_impedance_activated(self, p0):
        trigger_impedance_dic={"50Ω":"50R","HIZ":"HIZ"}
        self.delayer.trigger_impedance_set(trigger_impedance_dic[p0])

    @pyqtSlot(str)
    def on_comboBox_trigger_edge_activated(self, p0):
        trigger_edge_dic={"上升沿":"POS","下降沿":"NEG"}
        self.delayer.trigger_source(trigger_edge_dic[p0])

    @pyqtSlot()
    def on_doubleSpinBox_trigger_level_editingFinished(self):
        self.delayer.trigger_level_set(self.doubleSpinBox_trigger_level.value())


    @pyqtSlot(str)
    def on_comboBox_readout_mode_activated(self, p0):
        self.config["read_mode"]=p0
    
    @pyqtSlot()
    def on_doubleSpinBox_exposure_time_editingFinished(self):
        self.ccd.set_integration_time(self.doubleSpinBox_exposure_time.value())
    
    @pyqtSlot()
    def on_spinBox_frame_count_editingFinished(self):
        self.config["frame_count"]=self.spinBox_frame_count.value()
    
    @pyqtSlot(str)
    def on_comboBox_frame_rate_activated(self, p0):
        self.ccd.set_frame_rate(float(p0))
    
    @pyqtSlot()
    def on_doubleSpinBox_pre_gain_editingFinished(self):
        self.ccd.set_gain(self.doubleSpinBox_pre_gain.value())
    
    @pyqtSlot()
    def on_lineEdit_file_name_editingFinished(self):
        self.config["file_name"]=self.lineEdit_file_name.text()
    
    @pyqtSlot()
    def on_lineEdit_operator_editingFinished(self):
        self.config["operator_name"]=self.lineEdit_operator.text()
    
    @pyqtSlot(str)
    def on_lineEdit_file_path_textChanged(self, p0):
        self.config["file_path"]=p0


    @pyqtSlot(bool)
    def on_checkBox_enable_autosave_clicked(self, checked):
        self.config["auto_save"] = checked


    @pyqtSlot(bool)
    def on_checkBox_date_clicked(self, checked):
        self.config["date_enable"] = checked


    @pyqtSlot()
    def on_pushButton_choose_filepath_clicked(self):

        worker=threading.Thread(target=self.choose_file_path_worker)
        worker.start()

    def choose_file_path_worker(self):
        file_path=QtWidgets.QFileDialog.getExistingDirectory(caption="选择文件夹",directory=self.config["file_path"])
        if file_path:
            self.lineEdit_file_path.setText(file_path)



    @pyqtSlot(str)
    def on_comboBox_file_format_activated(self, p0):
        self.config["file_format"] = p0


    @pyqtSlot(bool)
    def on_checkBox_operator_clicked(self, checked):
        self.config["operator_enable"] = checked
    
    
    @pyqtSlot(str)
    def on_comboBox_internal_trigger_rate_unit_activated(self, p0):
        self.delayer.sythesize_set(self.doubleSpinBox_internal_trigger_rate.text()+self.comboBox_internal_trigger_rate_unit.currentText()[0])
    
    @pyqtSlot()
    def on_doubleSpinBox_internal_trigger_rate_editingFinished(self):
        self.delayer.sythesize_set(self.doubleSpinBox_internal_trigger_rate.text()+self.comboBox_internal_trigger_rate_unit.currentText()[0])
    
    @pyqtSlot(str)
    def on_comboBox_trigger_mode_currentIndexChanged(self, p0):
        if p0=="内触发":
            self.widget_internal_trigger.show()
            self.widget_external_trigger.hide()
        else:
            self.widget_internal_trigger.hide()
            self.widget_external_trigger.show()
    
    @pyqtSlot()
    def on_doubleSpinBox_divisor_editingFinished(self):
        self.delayer.divisor_set(self.doubleSpinBox_divisor.value())

    def set_sequence_parameter(self,value):
        if self.radioButton_autodelay_enable_linear.isChecked():
            delay_value=self.doubleSpinBox_autodelay_linear_s.value()+self.doubleSpinBox_autodelay_linear_k.value()*(value+self.doubleSpinBox_autodelay_linear_b.value())
        elif self.radioButton_autodelay_enable_index.isChecked():
            delay_value=self.doubleSpinBox_autodelay_index_s.value()+self.doubleSpinBox_autodelay_index_a.value()**(self.doubleSpinBox_autodelay_index_k.value()*(value+self.doubleSpinBox_autodelay_index_b.value() ))
        elif self.radioButton_autodelay_enable_logarithm.isChecked():
            delay_value=self.doubleSpinBox_autodelay_log_s.value()+math.log(self.doubleSpinBox_autodelay_log_k.value()*(value+self.doubleSpinBox_autodelay_log_b.value()),self.doubleSpinBox_autodelay_log_a.value())

        if self.radioButton_autowidth_enable_linear.isChecked():
            width=self.doubleSpinBox_autowidth_linear_s.value()+self.doubleSpinBox_autowidth_linear_k.value()*(value+self.doubleSpinBox_autowidth_linear_b.value())
        elif self.radioButton_autowidth_enable_index.isChecked():
            width=self.doubleSpinBox_autowidth_index_s.value()+self.doubleSpinBox_autowidth_index_a.value()**(self.doubleSpinBox_autowidth_index_k.value()*(self.doubleSpinBox_autowidth_index_b.value()+value))
        elif self.radioButton_autowidth_enable_logarithm.isChecked():

            width=self.doubleSpinBox_autowidth_log_s.value()+math.log(self.doubleSpinBox_autowidth_log_k.value()*(value+self.doubleSpinBox_autowidth_log_b.value()),self.doubleSpinBox_autowidth_log_a.value())

        if self.checkBox_autodelay_enable_gate.isChecked():
            self.delayer.set_channel(channel="D",delay="%.2fn"%delay_value)
        if self.checkBox_autodelay_enable_a.isChecked():
            self.delayer.set_channel(channel="A", delay="%.2fn" % delay_value)
        if self.checkBox_autodelay_enable_b.isChecked():
            self.delayer.set_channel(channel="B", delay="%.2fn" % delay_value)
        if self.checkBox_autodelay_enable_c.isChecked():
            self.delayer.set_channel(channel="C", delay="%.2fn" % delay_value)

        if self.checkBox_autowidth_enable_gate.isChecked():
            self.delayer.set_channel("D",width="%.2fn"%width)
        if self.checkBox_autowidth_enable_a.isChecked():
            self.delayer.set_channel("A", width="%.2fn" % width)
        if self.checkBox_autowidth_enable_b.isChecked():
            self.delayer.set_channel("B", width="%.2fn" % width)
        if self.checkBox_autowidth_enable_c.isChecked():
            self.delayer.set_channel("C", width="%.2fn" % width)
        self.update_current_autoparameter.emit(delay_value,width)


    def display_current_autoparameter(self,delay=0,width=0):
        """更新界面自动延时及脉宽参数值"""
        if self.checkBox_autodelay_enable_gate.isChecked() or self.checkBox_autodelay_enable_a.isChecked() or self.checkBox_autodelay_enable_b.isChecked() or self.checkBox_autodelay_enable_c.isChecked():
            if self.radioButton_autodelay_enable_linear.isChecked():
                self.doubleSpinBox_autodelay_linear_y.setValue(delay)
            if self.radioButton_autodelay_enable_index.isChecked():
                self.doubleSpinBox_autodelay_index_y.setValue(delay)
            if self.radioButton_autodelay_enable_logarithm.isChecked():
                self.doubleSpinBox_autodelay_log_y.setValue(delay)
        if self.checkBox_autowidth_enable_gate.isChecked() or self.checkBox_autowidth_enable_a.isChecked() or self.checkBox_autowidth_enable_b.isChecked() or self.checkBox_autowidth_enable_c.isChecked():
            if self.radioButton_autowidth_enable_linear.isChecked():
                self.doubleSpinBox_autowidth_linear_y.setValue(width)
            if self.radioButton_autowidth_enable_index.isChecked():
                self.doubleSpinBox_autowidth_index_y.setValue(width)
            if self.radioButton_autowidth_enable_logarithm.isChecked():
                self.doubleSpinBox_autowidth_log_y.setValue(width)

    def recovery_parameter(self):
        """恢复界面延时及脉宽参数值"""
        self.delayer.set_channel(channel="A",delay=self.doubleSpinBox_delay_a.text()+self.comboBox_delay_a.currentText()[0],width=self.doubleSpinBox_width_a.text()+self.comboBox_width_a.currentText()[0])
        self.delayer.set_channel(channel="B",delay=self.doubleSpinBox_delay_b.text()+self.comboBox_delay_b.currentText()[0],width=self.doubleSpinBox_width_b.text()+self.comboBox_width_b.currentText()[0])
        self.delayer.set_channel(channel="C",delay=self.doubleSpinBox_delay_c.text()+self.comboBox_delay_c.currentText()[0],width=self.doubleSpinBox_width_c.text()+self.comboBox_width_c.currentText()[0])
        self.delayer.set_channel(channel="D",delay=self.doubleSpinBox_delay_d.text()+self.comboBox_delay_d.currentText()[0],width=self.doubleSpinBox_width_d.text()+self.comboBox_width_d.currentText()[0])


    def save_config(self,file_path):
        config = configparser.ConfigParser()
        # 添加域
        config.add_section("camera_setup")
        config.add_section("gate_setup")
        config.add_section("sequence")
        config.add_section("binning/roi_setup")
        config.add_section("autosave")

        config.set("camera_setup", "measure_mode", self.comboBox_measure_mode.currentText())
        config.set("camera_setup","readout_mode",self.comboBox_readout_mode.currentText())
        config.set("camera_setup","trigger_mode",self.comboBox_trigger_mode.currentText())
        config.set("camera_setup","exposuretime",self.doubleSpinBox_exposure_time.text())
        config.set("camera_setup","sql_threshold",str(self.spinBox_threshold.value()))
        config.set("camera_setup","frame_count",self.spinBox_frame_count.text())
        config.set("camera_setup","readoutspeed",self.comboBox_frame_rate.currentText())
        config.set("camera_setup","ccd_gain",self.doubleSpinBox_pre_gain.text())
        config.set("camera_setup","trigger_freq_value",self.doubleSpinBox_internal_trigger_rate.text())
        config.set("camera_setup","trigger_freq_unit",self.comboBox_internal_trigger_rate_unit.currentText())
        config.set("camera_setup","divisor",self.doubleSpinBox_divisor.text())
        config.set("camera_setup","rise_edge",self.comboBox_trigger_edge.currentText())
        config.set("camera_setup","impedance",self.comboBox_trigger_impedance.currentText())
        config.set("camera_setup","trigger_threshold",self.doubleSpinBox_trigger_level.text())

        config.set("gate_setup","mcp_gain",str(self.spinBox_mcp_gain.value()))
        config.set("gate_setup","ioc_enable",str(self.checkBox_enable_ioc.isChecked()))
        config.set("gate_setup","fit_ccd",str(self.radioButton_fit_ccd.isChecked()))
        config.set("gate_setup","burst",str(self.radioButton_burst.isChecked()))
        config.set("gate_setup","burst_count",self.spinBox_burst_count.text())
        config.set("gate_setup","delay_value_d",self.doubleSpinBox_delay_d.text())
        config.set("gate_setup","delay_unit_d",self.comboBox_delay_d.currentText())
        config.set("gate_setup","width_value_d",self.doubleSpinBox_width_d.text())
        config.set("gate_setup","width_unit_d",self.comboBox_width_d.currentText())

        config.set("gate_setup","channel_enable_a",str(self.checkBox_channel_enable_a.isChecked()))
        config.set("gate_setup","delay_value_a",self.doubleSpinBox_delay_a.text())
        config.set("gate_setup","delay_unit_a",self.comboBox_delay_a.currentText())
        config.set("gate_setup","width_value_a",self.doubleSpinBox_width_a.text())
        config.set("gate_setup","width_unit_a",self.comboBox_width_a.currentText())
        config.set("gate_setup","polarity_a",str(self.comboBox_polarity_a.currentIndex()))
        config.set("gate_setup","same_to_gate_a",str(self.checkBox_same_to_gate_a.isChecked()))

        config.set("gate_setup", "channel_enable_b", str(self.checkBox_channel_enable_b.isChecked()))
        config.set("gate_setup", "delay_value_b", self.doubleSpinBox_delay_b.text())
        config.set("gate_setup", "delay_unit_b", self.comboBox_delay_b.currentText())
        config.set("gate_setup", "width_value_b", self.doubleSpinBox_width_b.text())
        config.set("gate_setup", "width_unit_b", self.comboBox_width_b.currentText())
        config.set("gate_setup", "polarity_b", str(self.comboBox_polarity_b.currentIndex()))
        config.set("gate_setup", "same_to_gate_b", str(self.checkBox_same_to_gate_b.isChecked()))

        config.set("gate_setup", "channel_enable_c", str(self.checkBox_channel_enable_c.isChecked()))
        config.set("gate_setup", "delay_value_c", self.doubleSpinBox_delay_c.text())
        config.set("gate_setup", "delay_unit_c", self.comboBox_delay_c.currentText())
        config.set("gate_setup", "width_value_c", self.doubleSpinBox_width_c.text())
        config.set("gate_setup", "width_unit_c", self.comboBox_width_c.currentText())
        config.set("gate_setup", "polarity_c", str(self.comboBox_polarity_c.currentIndex()))
        config.set("gate_setup", "same_to_gate_c", str(self.checkBox_same_to_gate_c.isChecked()))

        config.set("sequence","sequence_enable",str(self.checkBox_enable_sequence.isChecked()))
        config.set("sequence","sequence_measure_count",self.spinBox_measure_count.text())
        config.set("sequence","autodelay_enable_d",str(self.checkBox_autodelay_enable_gate.isChecked()))
        config.set("sequence","autodelay_enable_a",str(self.checkBox_autodelay_enable_a.isChecked()))
        config.set("sequence","autodelay_enable_b",str(self.checkBox_autodelay_enable_b.isChecked()))
        config.set("sequence","autodelay_enable_c",str(self.checkBox_autodelay_enable_c.isChecked()))
        config.set("sequence","autodelay_enable_linear",str(self.radioButton_autodelay_enable_linear.isChecked()))
        config.set("sequence","autodelay_enable_index",str(self.radioButton_autodelay_enable_index.isChecked()))
        config.set("sequence","autodelay_enable_log",str(self.radioButton_autodelay_enable_logarithm.isChecked()))

        config.set("sequence","autodelay_linear_start",str(self.doubleSpinBox_autodelay_linear_s.value()))
        config.set("sequence","autodelay_linear_k",str(self.doubleSpinBox_autodelay_linear_k.value()))
        config.set("sequence","autodealy_linear_b",str(self.doubleSpinBox_autodelay_linear_b.value()))
        config.set("sequence","autodelay_index_start",str(self.doubleSpinBox_autodelay_index_s.value()))
        config.set("sequence","autodelay_index_a",str(self.doubleSpinBox_autodelay_index_a.value()))
        config.set("sequence","autodelay_index_k",str(self.doubleSpinBox_autodelay_index_k.value()))
        config.set("sequence","autodelay_index_b",str(self.doubleSpinBox_autodelay_index_b.value()))
        config.set("sequence","autodelay_log_start",str(self.doubleSpinBox_autodelay_log_s.value()))
        config.set("sequence","autodelay_log_a",str(self.doubleSpinBox_autodelay_log_a.value()))
        config.set("sequence","autodelay_log_k",str(self.doubleSpinBox_autodelay_log_k.value()))
        config.set("sequence","autodelay_log_b",str(self.doubleSpinBox_autodelay_log_b.value()))

        config.set("sequence","autowidth_enable_d",str(self.checkBox_autowidth_enable_gate.isChecked()))
        config.set("sequence","autowidth_enable_a",str(self.checkBox_autowidth_enable_a.isChecked()))
        config.set("sequence","autowidth_enable_b",str(self.checkBox_autowidth_enable_b.isChecked()))
        config.set("sequence","autowidth_enable_c",str(self.checkBox_autowidth_enable_c.isChecked()))
        config.set("sequence","autowidth_enable_linear",str(self.radioButton_autowidth_enable_linear.isChecked()))
        config.set("sequence","autowidth_enable_index",str(self.radioButton_autowidth_enable_index.isChecked()))
        config.set("sequence","autowidth_enable_log",str(self.radioButton_autowidth_enable_logarithm.isChecked()))

        config.set("sequence","autowidth_linear_start",str(self.doubleSpinBox_autowidth_linear_s.value()))
        config.set("sequence","autowidth_linear_k",str(self.doubleSpinBox_autowidth_linear_k.value()))
        config.set("sequence","autowidth_linear_b",str(self.doubleSpinBox_autowidth_linear_b.value()))
        config.set("sequence","autowidth_index_start",str(self.doubleSpinBox_autowidth_index_s.value()))
        config.set("sequence","autowidth_index_a",str(self.doubleSpinBox_autowidth_index_a.value()))
        config.set("sequence","autowidth_index_k",str(self.doubleSpinBox_autowidth_index_k.value()))
        config.set("sequence","autowidth_index_b",str(self.doubleSpinBox_autowidth_index_b.value()))
        config.set("sequence","autowidth_log_start",str(self.doubleSpinBox_autowidth_log_s.value()))
        config.set("sequence","autowidth_log_a",str(self.doubleSpinBox_autowidth_log_a.value()))
        config.set("sequence","autowidth_log_k",str(self.doubleSpinBox_autowidth_log_k.value()))
        config.set("sequence","autowidth_log_b",str(self.doubleSpinBox_autowidth_log_b.value()))

        config.set("binning/roi_setup","roi_left",self.spinBox_roi_left.text())
        config.set("binning/roi_setup","roi_right",self.spinBox_roi_right.text())
        config.set("binning/roi_setup","roi_bottom",self.spinBox_roi_bottom.text())
        config.set("binning/roi_setup","roi_top",self.spinBox_roi_top.text())
        config.set("binning/roi_setup","binning_disable",str(self.radioButton_binning1.isChecked()))
        config.set("binning/roi_setup","binning_2x2",str(self.radioButton_binning2.isChecked()))
        config.set("binning/roi_setup","binning_1x2",str(self.radioButton_binning3.isChecked()))
        config.set("binning/roi_setup","bining_2x1",str(self.radioButton_binning4.isChecked()))

        config.set("autosave","file_type",self.comboBox_file_format.currentText())
        config.set("autosave","file_name",self.lineEdit_file_name.text())
        config.set("autosave","file_dir",self.lineEdit_file_path.text())
        config.set("autosave","file_date_enable",str(self.checkBox_date.isChecked()))
        config.set("autosave","operator_enable",str(self.checkBox_operator.isChecked()))
        config.set("autosave","operator_name",self.lineEdit_operator.text())

        config.write(open(file_path,"w+"))

    def load_config(self,file_path):
        config=configparser.ConfigParser()
        config.read(file_path)
        camera_setup=dict(config.items("camera_setup"))
        gate_setup=dict(config.items("gate_setup"))
        sequence=dict(config.items("sequence"))
        binning_roi_setup=dict(config.items("binning/roi_setup"))
        autosave=dict(config.items("autosave"))

        self.comboBox_measure_mode.setCurrentText(camera_setup["measure_mode"])
        self.on_comboBox_measure_mode_activated(camera_setup["measure_mode"])
        self.doubleSpinBox_exposure_time.setValue(float(camera_setup["exposuretime"]))
        self.on_doubleSpinBox_exposure_time_editingFinished()
        self.spinBox_threshold.setValue(int(camera_setup["sql_threshold"]))
        self.spinBox_frame_count.setValue(int(camera_setup["frame_count"]))
        self.on_spinBox_frame_count_editingFinished()
        self.doubleSpinBox_pre_gain.setValue(float(camera_setup["ccd_gain"]))
        self.on_doubleSpinBox_pre_gain_editingFinished()
        self.doubleSpinBox_internal_trigger_rate.setValue(float(camera_setup["trigger_freq_value"]))
        self.comboBox_internal_trigger_rate_unit.setCurrentText(camera_setup["trigger_freq_unit"])
        self.on_comboBox_internal_trigger_rate_unit_activated(camera_setup["trigger_freq_unit"])
        self.doubleSpinBox_divisor.setValue(float(camera_setup["divisor"]))
        self.on_doubleSpinBox_divisor_editingFinished()
        self.comboBox_trigger_edge.setCurrentText(camera_setup["rise_edge"])
        self.on_comboBox_trigger_edge_activated(camera_setup["rise_edge"])
        self.comboBox_trigger_impedance.setCurrentText(camera_setup["impedance"])
        self.on_comboBox_trigger_impedance_activated(camera_setup["impedance"])
        self.doubleSpinBox_trigger_level.setValue(float(camera_setup["trigger_threshold"]))
        self.on_doubleSpinBox_trigger_level_editingFinished()
        self.comboBox_trigger_mode.setCurrentText(camera_setup["trigger_mode"])
        self.on_comboBox_trigger_mode_activated(camera_setup["trigger_mode"])

        self.spinBox_mcp_gain.setValue(int(gate_setup["mcp_gain"]))
        self.gain_controler.gain_value=int(gate_setup["mcp_gain"])
        # print(int(gate_setup["mcp_gain"]),"*********************************")
        self.on_spinBox_mcp_gain_editingFinished()
        self.radioButton_fit_ccd.setChecked(bool(gate_setup["fit_ccd"]=="True"))
        self.on_radioButton_fit_ccd_clicked(bool(gate_setup["fit_ccd"]=="True"))
        self.spinBox_burst_count.setValue(int(gate_setup["burst_count"]))
        self.on_spinBox_burst_count_editingFinished()
        self.radioButton_burst.setChecked(bool(gate_setup["burst"]=="True"))
        self.on_radioButton_burst_clicked(bool(gate_setup["burst"]=="True"))
        self.checkBox_enable_ioc.setChecked(bool(gate_setup["ioc_enable"]=="True"))
        self.on_checkBox_enable_ioc_clicked(bool(gate_setup["ioc_enable"]=="True"))

        self.doubleSpinBox_delay_d.setValue(float(gate_setup["delay_value_d"]))
        self.comboBox_delay_d.setCurrentText(gate_setup["delay_unit_d"])
        self.on_comboBox_delay_d_activated(gate_setup["delay_unit_d"])
        self.doubleSpinBox_width_d.setValue(float(gate_setup["width_value_d"]))
        self.comboBox_width_d.setCurrentText(gate_setup["width_unit_d"])
        self.on_comboBox_width_d_activated(gate_setup["width_unit_d"])

        self.doubleSpinBox_delay_a.setValue(float(gate_setup["delay_value_a"]))
        self.comboBox_delay_a.setCurrentText(gate_setup["delay_unit_a"])
        self.on_comboBox_delay_a_activated(gate_setup["delay_unit_a"])
        self.doubleSpinBox_width_a.setValue(float(gate_setup["width_value_a"]))
        self.comboBox_width_a.setCurrentText(gate_setup["width_unit_a"])
        self.on_comboBox_width_a_activated(gate_setup["width_unit_a"])
        self.comboBox_polarity_a.setCurrentIndex(int(gate_setup["polarity_a"]))
        self.on_comboBox_polarity_a_activated(int(gate_setup["polarity_a"]))
        self.checkBox_same_to_gate_a.setChecked(bool(gate_setup["same_to_gate_a"]=="True"))
        self.on_checkBox_same_to_gate_a_clicked(bool(gate_setup["same_to_gate_a"]=="True"))
        self.checkBox_channel_enable_a.setChecked(bool(gate_setup["channel_enable_a"]=="True"))
        self.on_checkBox_channel_enable_a_clicked(bool(gate_setup["channel_enable_a"]=="True"))

        self.doubleSpinBox_delay_b.setValue(float(gate_setup["delay_value_b"]))
        self.comboBox_delay_b.setCurrentText(gate_setup["delay_unit_b"])
        self.on_comboBox_delay_b_activated(gate_setup["delay_unit_b"])
        self.doubleSpinBox_width_b.setValue(float(gate_setup["width_value_b"]))
        self.comboBox_width_b.setCurrentText(gate_setup["width_unit_b"])
        self.on_comboBox_width_b_activated(gate_setup["width_unit_b"])
        self.comboBox_polarity_b.setCurrentIndex(int(gate_setup["polarity_b"]))
        self.on_comboBox_polarity_b_activated(int(gate_setup["polarity_b"]))
        self.checkBox_same_to_gate_b.setChecked(bool(gate_setup["same_to_gate_b"]=="True"))
        self.on_checkBox_same_to_gate_b_clicked(bool(gate_setup["same_to_gate_b"]=="True"))
        self.checkBox_channel_enable_b.setChecked(bool(gate_setup["channel_enable_b"]=="True"))
        self.on_checkBox_channel_enable_b_clicked(bool(gate_setup["channel_enable_b"]=="True"))

        self.doubleSpinBox_delay_c.setValue(float(gate_setup["delay_value_c"]))
        self.comboBox_delay_c.setCurrentText(gate_setup["delay_unit_c"])
        self.on_comboBox_delay_c_activated(gate_setup["delay_unit_c"])
        self.doubleSpinBox_width_c.setValue(float(gate_setup["width_value_c"]))
        self.comboBox_width_c.setCurrentText(gate_setup["width_unit_c"])
        self.on_comboBox_width_c_activated(gate_setup["width_unit_c"])
        self.comboBox_polarity_c.setCurrentIndex(int(gate_setup["polarity_c"]))
        self.on_comboBox_polarity_c_activated(int(gate_setup["polarity_c"]))
        self.checkBox_same_to_gate_c.setChecked(bool(gate_setup["same_to_gate_c"]=="True"))
        self.on_checkBox_same_to_gate_c_clicked(bool(gate_setup["same_to_gate_c"]=="True"))
        self.checkBox_channel_enable_c.setChecked(bool(gate_setup["channel_enable_c"]=="True"))
        self.on_checkBox_channel_enable_c_clicked(bool(gate_setup["channel_enable_c"]=="True"))

        self.checkBox_enable_sequence.setChecked(bool(sequence["sequence_enable"]=="True"))
        self.spinBox_measure_count.setValue(int(sequence["sequence_measure_count"]))
        self.checkBox_autodelay_enable_gate.setChecked(bool(sequence["autodelay_enable_d"]=="True"))
        self.checkBox_autodelay_enable_a.setChecked(bool(sequence["autodelay_enable_a"]=="True"))
        self.checkBox_autodelay_enable_b.setChecked(bool(sequence["autodelay_enable_b"]=="True"))
        self.checkBox_autodelay_enable_c.setChecked(bool(sequence["autodelay_enable_c"]=="True"))
        self.radioButton_autodelay_enable_linear.setChecked(bool(sequence["autodelay_enable_linear"]=="True"))
        self.radioButton_autodelay_enable_index.setChecked(bool(sequence["autodelay_enable_index"]=="True"))
        self.radioButton_autodelay_enable_logarithm.setChecked(bool(sequence["autodelay_enable_log"]=="True"))
        self.doubleSpinBox_autodelay_linear_s.setValue(float(sequence["autodelay_linear_start"]))
        self.doubleSpinBox_autodelay_linear_k.setValue(float(sequence["autodelay_linear_k"]))
        self.doubleSpinBox_autodelay_linear_b.setValue(float(sequence["autodealy_linear_b"]))
        self.doubleSpinBox_autodelay_index_s.setValue(float(sequence["autodelay_index_start"]))
        self.doubleSpinBox_autodelay_index_a.setValue(float(sequence["autodelay_index_a"]))
        self.doubleSpinBox_autodelay_index_k.setValue(float(sequence["autodelay_index_k"]))
        self.doubleSpinBox_autodelay_index_b.setValue(float(sequence["autodelay_index_b"]))
        self.doubleSpinBox_autodelay_log_s.setValue(float(sequence["autodelay_log_start"]))
        self.doubleSpinBox_autodelay_log_a.setValue(float(sequence["autodelay_log_a"]))
        self.doubleSpinBox_autodelay_log_k.setValue(float(sequence["autodelay_log_k"]))
        self.doubleSpinBox_autodelay_log_b.setValue(float(sequence["autodelay_log_b"]))

        self.checkBox_autowidth_enable_gate.setChecked(bool(sequence["autowidth_enable_d"]=="True"))
        self.checkBox_autowidth_enable_a.setChecked(bool(sequence["autowidth_enable_a"]=="True"))
        self.checkBox_autowidth_enable_b.setChecked(bool(sequence["autowidth_enable_b"]=="True"))
        self.checkBox_autowidth_enable_c.setChecked(bool(sequence["autowidth_enable_c"]=="True"))
        self.radioButton_autowidth_enable_linear.setChecked(bool(sequence["autowidth_enable_linear"]=="True"))
        self.radioButton_autowidth_enable_index.setChecked(bool(sequence["autowidth_enable_index"]=="True"))
        self.radioButton_autowidth_enable_logarithm.setChecked(bool(sequence["autowidth_enable_log"]=="True"))
        self.doubleSpinBox_autowidth_linear_s.setValue(float(sequence["autowidth_linear_start"]))
        self.doubleSpinBox_autowidth_linear_k.setValue(float(sequence["autowidth_linear_k"]))
        self.doubleSpinBox_autowidth_linear_b.setValue(float(sequence["autodealy_linear_b"]))
        self.doubleSpinBox_autowidth_index_s.setValue(float(sequence["autowidth_index_start"]))
        self.doubleSpinBox_autowidth_index_a.setValue(float(sequence["autowidth_index_a"]))
        self.doubleSpinBox_autowidth_index_k.setValue(float(sequence["autowidth_index_k"]))
        self.doubleSpinBox_autowidth_index_b.setValue(float(sequence["autowidth_index_b"]))
        self.doubleSpinBox_autowidth_log_s.setValue(float(sequence["autowidth_log_start"]))
        self.doubleSpinBox_autowidth_log_a.setValue(float(sequence["autowidth_log_a"]))
        self.doubleSpinBox_autowidth_log_k.setValue(float(sequence["autowidth_log_k"]))
        self.doubleSpinBox_autowidth_log_b.setValue(float(sequence["autowidth_log_b"]))


        self.spinBox_roi_left.setValue(int(binning_roi_setup["roi_left"]))
        self.spinBox_roi_right.setValue(int(binning_roi_setup["roi_right"]))
        self.spinBox_roi_bottom.setValue(int(binning_roi_setup["roi_bottom"]))
        self.spinBox_roi_top.setValue(int(binning_roi_setup["roi_top"]))
        self.on_pushButton_roi_sure_clicked()
        if self.ccd.cam.Devices[0].Name != "DMK 33UX174":
            self.radioButton_binning1.setChecked(bool(binning_roi_setup["binning_disable"]=="True"))
            self.on_radioButton_binning1_clicked(bool(binning_roi_setup["binning_disable"]=="True"))
            self.radioButton_binning2.setChecked(bool(binning_roi_setup["binning_2x2"]=="True"))
            self.on_radioButton_binning2_clicked(bool(binning_roi_setup["binning_2x2"]=="True"))
            self.radioButton_binning3.setChecked(bool(binning_roi_setup["binning_1x2"]=="True"))
            self.on_radioButton_binning3_clicked(bool(binning_roi_setup["binning_1x2"]=="True"))
            self.radioButton_binning4.setChecked(bool(binning_roi_setup["bining_2x1"]=="True"))
            self.on_radioButton_binning4_clicked(bool(binning_roi_setup["bining_2x1"]=="True"))


        self.comboBox_file_format.setCurrentText(autosave["file_type"])
        self.lineEdit_file_name.setText(autosave["file_name"])
        self.lineEdit_file_path.setText(autosave["file_dir"])
        self.checkBox_date.setChecked(bool(autosave["file_date_enable"]=="True"))
        self.checkBox_operator.setChecked(bool(autosave["operator_enable"]=="True"))
        self.lineEdit_operator.setText(autosave["operator_name"])

        self.comboBox_frame_rate.setCurrentText(camera_setup["readoutspeed"])
        self.on_comboBox_frame_rate_activated(camera_setup["readoutspeed"])




















































































