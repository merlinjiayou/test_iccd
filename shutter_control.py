# -*- coding: utf-8 -*-

"""
Module implementing shutter_control.
"""

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget
from Ui_shutter_control import Ui_shutter_control


class shutter_control(QWidget, Ui_shutter_control):
    update_message_signal=pyqtSignal(str)

    def __init__(self, parent=None,delayer=None,ccd=None):
        super(shutter_control, self).__init__(parent)
        self.setupUi(self)
        self.delayer=delayer
        self.ccd=ccd
        self.init_ui()

    def init_ui(self):
        try:
            self.setEnabled(self.delayer.connect_status)
            if self.delayer.config["gate mode"]=="  BUR" and self.delayer.config["burst enable"]=="ON" and self.ccd.get_strobe_enable():
                self.radioButton_auto.setChecked(True)
            elif self.delayer.config["gate mode"]=="OFF" and self.delayer.config["burst enable"]=="OFF" and self.ccd.get_strobe_enable():
                self.radioButton_permanently_open.setChecked(True)
            elif self.delayer.config["d enable"]=="OFF" and self.delayer.config["d polarity"]=="POS":
                self.radioButton_permanently_close.setChecked(True)
        except:
            self.update_message_signal.emit("初始化失败")

    
    @pyqtSlot(bool)
    def on_radioButton_auto_clicked(self, checked):
        if checked:
            self.delayer.channel_enable("D","ON")
            self.delayer.set_channel("D",polarity="POS")
    
    @pyqtSlot(bool)
    def on_radioButton_permanently_open_clicked(self, checked):
        if checked:
            self.delayer.channel_enable("D","OFF")
            self.delayer.set_channel("D",polarity="NEG")

    
    @pyqtSlot(bool)
    def on_radioButton_permanently_close_clicked(self, checked):
        if checked:
            self.delayer.channel_enable("D","OFF")
            self.delayer.set_channel("D",polarity="POS")
