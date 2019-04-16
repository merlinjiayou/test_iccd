# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
import serial
import time
import shelve
from serial.tools.list_ports import comports

class gain_controler():
    def __init__(self):
        self.power_handle = None
        self.gain_value=0
        self.connect_status=self.connect_device()
        # if self.connect_status:
        #     self.set_current_vot(0)


    def connect_device(self):
        port_list=list(comports())
        if port_list!=[]:
            for i in range(4):
                for port in port_list:
                    try:
                        self.power_handle = serial.Serial(port[0], baudrate=115200)
                        result=self.query()
                        print(port[0])
                        if result:
                            if "2POWER" in result:
                                return True
                        self.power_handle.close()
                    except:
                        pass
        return False

    def break_device(self):
        if self.power_handle is not None:
            if self.power_handle.is_open:
                self.power_handle.close()
                return True
        return False


    def set_current_vot(self,current_value):
        try:
            vot_txt = list("%.2f"%current_value)
            print(vot_txt)
            my_array = [170, 85, 15, 3, 2, int(vot_txt[0]), int(vot_txt[2]), int(vot_txt[3]), 0, 170]
            check_sum = self.uchar_checksum(my_array)
            my_array.append(check_sum)
            self.power_handle.write(bytearray(my_array))
            time.sleep(0.1)
            result = self.power_handle.read_all()
            if result==b'\xaaUO\x03\xaa\x05':
                self.gain_value=current_value*4095/5
                return 1
            elif result == b'\xaaU\x00\x04\xaaS':
                return 0
            else:
                return -1
        except:
            return 0

    def query(self):
        try:
            my_array = [170, 85, 15, 1, 1, 1, 2, 3, 0, 170]
            check_sum = self.uchar_checksum(my_array)
            my_array.append(check_sum)
            self.power_handle.write(bytearray(my_array))
            time.sleep(0.2)
            result = self.power_handle.read_all()
            print(result)
            return bytes(result).decode("ascii")
        except:
            return False

    def set_init_vot(self,init_value):
        try:
            vot_txt = list(str(init_value))
            my_array = [170, 85, 15, 6, 2, int(vot_txt[0]), int(vot_txt[2]), int(vot_txt[3]), 0, 170]
            check_sum = self.uchar_checksum(my_array)
            my_array.append(check_sum)
            self.power_handle.write(bytearray(my_array))
            time.sleep(0.1)
            result = self.power_handle.read_all()
            if result==b'\xaaUO\x04\xaa\x04':
                return 1
            elif result==b'\xaaU\x00\x04\xaaS':
                return 0
            else:
                return -1
        except:
            return 0

    def set_range_vot(self,range_value):
        try:
            vot_txt = list(str(range_value))
            my_array = [170, 85, 15, 5, 2, int(vot_txt[0]), int(vot_txt[2]), int(vot_txt[3]), 0, 170]
            check_sum = self.uchar_checksum(my_array)
            my_array.append(check_sum)
            self.power_handle.write(bytearray(my_array))
            time.sleep(0.1)
            result = self.power_handle.read_all()
            if result == b'\xaaUO\x04\xaa\x04':
                return 1
            elif result == b'\xaaU\x00\x04\xaaS':
                return 0
            else:
                return -1
        except:
            return 0

    def uchar_checksum(self, data):
        length = len(data)
        checksum = 0
        for i in range(0, length):
            checksum += data[i]
            checksum &= 0xFF  # 强制截断
        checksum = 256 - checksum
        return checksum


