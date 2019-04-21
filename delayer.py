# -*- coding: utf-8 -*-

"""
Module implementing Formtrigger_highland.
"""
import serial
import re
import time
from PyQt5.QtCore import pyqtSlot,pyqtSignal
from serial.tools.list_ports import comports
import shelve

class delayer():
    def __init__(self):
        self.handle = None
        self.config={
            "A enable":"OFF",
            "A delay":"0.00n",
            "A width":"0.00n",
            "A polarity":"POS",
            "B enable":"OFF",
            "B delay":"0.00n",
            "B width":"0.00n",
            "B polarity":"POS",
            "C enable":"OFF",
            "C delay":"0.00n",
            "C width":"0.00n",
            "C polarity":"POS",
            "D enable":"ON",
            "D delay":"0.00n",
            "D width":"3.00n",
            "D polarity":"POS",
            "gate mode":"BUR",
            "gate level":"POS",
            # HIZ  50R
            "gate impedance":"50R",
            "burst enable":"ON",
            "burst count":1,
            "trigger mode":"SYN",
            "trigger freq":10000,
            #HIZ  50R
            "trigger impedance":"50R",
            "trigger divisor":1,
            "trigger level":2
        }
        self.connect_status=self.connect_device()
        if self.connect_status:
            self.init_device()
            self.load_status=self.load_config()
            self.gate_set(gate_mod="BUR",gate_level="POS",input_type="HIZ")
            self.channel_enable("D","OFF")
            if not self.load_status:
                self.handle.close()
                self.connect_status=False



    def load_config(self):
        channel_set=False
        gate_set=False
        count=0
        while True:
            if channel_set and gate_set:
                return True
            try:
                count+=1
                if count>10:
                    return False
                self.handle.write("ST\r".encode("ascii"))
                time.sleep(0.5)
                back = self.handle.read_all()
                result=bytes(back).decode("ascii")
                status_list=re.split("\r*\n*",result)
                for status in status_list:
                    if re.search("Ch",status):
                        channel_set=True
                        ch_status_list=re.split(" *",status)
                        channel=ch_status_list[1]
                        #ON OFF
                        self.config[channel + " enable"] = ch_status_list[3]
                        self.config[channel + " delay"]=str(float("".join(ch_status_list[5].split(",")))*10**9)+"n"
                        self.config[channel + " width"]=str(float("".join(ch_status_list[7].split(",")))*10**9)+"n"
                        #POS NEG
                        self.config[channel + " polarity"] = ch_status_list[2]
                    if re.search("Trig",status):
                        gate_set=True
                        trig_status_list=re.split(" *",status)
                        #REM SYN  INT POS NEG OFF
                        self.config["trigger mode"] = trig_status_list[1]
                        #50R HIZ
                        self.config["trigger impedance"]=trig_status_list[2]
                        self.config["trigger level"]=float(trig_status_list[4])
                        self.config["trigger divisor"]=int("".join(trig_status_list[6].split(",")))
                        self.config["trigger freq"]=float("".join(trig_status_list[8].split(",")))
                    if re.search("Gate",status):
                        #OFF INP OUT BUR REM
                        gate_status_list=re.split(" *",status)
                        self.config["gate mode"]=gate_status_list[1]
                        #POS NEG
                        self.config["gate level"]=gate_status_list[2]
                        #50R HIZ
                        self.config["gate impedance"]=gate_status_list[3]
                    if re.search("Burst",status):
                        burst_status_list=re.split(" *",status)
                        # OFF ON
                        self.config["burst enable"]=burst_status_list[1]
                        self.config["burst count"] =int("".join(burst_status_list[3].split(",")))
            except:
                pass


    def counter_reset(self):
        try:
            self.handle.write("SHots 0\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def counter_reset_mic(self):
        try:
            self.handle.write("USec 0\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def set_channel(self,channel,delay=None,width=None,polarity=None):
        "带单位"
        polarity_select={"POS":" PO","NEG":" NE"}
        txt=""
        if delay is not None:
            txt = channel + "D " + delay + ";"
        if width is not None:
            txt = txt+channel + "W " + width + ";"
        if polarity is not None:
            txt = txt+ channel+"S" + polarity_select[polarity]
        try:
            self.handle.write(txt.encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                if delay:
                    self.config[channel + " delay"]=delay
                if width:
                    self.config[channel + " width"]=width
                if polarity:
                    self.config[channel + " polarity"]=polarity
                print(self.config[channel + " width"])
                return True
            else:
                return False
        except:
            return False

    def init_device(self):
        """加载保存设置"""
        try:
            self.handle.write("RS\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def save_config(self):
        try:
            self.handle.write("SA\r".encode("ascii"))
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def load_productor_config(self):
        """加载出厂设置"""
        try:
            self.handle.write("LO DE\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def counter_query(self):
        try:
            self.handle.write("SHots\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            k="".join(str(bytes(result).decode("ascii")).split(","))
            value=int(k.strip())
            return value
        except:
            return 0


    @pyqtSlot()
    def counter_query_mic(self):
        try:
            self.handle.write("USec\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            return result
        except:
            return ""

    def channel_query(self,channel):
        try:
            txt=channel+"S"
            self.handle.write(txt.encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            return result
        except:
            return ""


    def gate_fire(self):
        try:
            self.handle.write("GA FI".encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False



    def gate_set(self,gate_mod=None,gate_level=None,input_type=None):
        # OFF INP OUT BUR REM
        gate_mode_dic={None:"","OUT":"GA OU;","INP":"GA IN;","BUR":"GA BU;","REM":"GA RE;","OFF":"GA OF;"}
        gate_level_dic={None:"","POS":"GA PO;","NEG":"GA NE;"}
        gate_type_dic={None:"","50R":"GA TE;","HIZ":"GA HI;"}
        txt = gate_mode_dic[gate_mod] + gate_level_dic[gate_level] + gate_type_dic[input_type]
        try:
            self.handle.write(txt.encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                if gate_mod:
                    self.config["gate mode"]=gate_mod
                if gate_level:
                    self.config["gate level"]=gate_level
                if input_type:
                    self.config["gate impedance"]=input_type
                return True
            else:
                return False
        except:
            return False

    def gate_query(self):
        try:
            self.handle.write("GA\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            return result
        except:
            return ""

    def channel_enable(self, channel,checked):
        channel_enable_dic={"ON":"S ON\r","OFF":"S OF\r"}
        try:
            txt = channel + channel_enable_dic[checked]
            self.handle.write(txt.encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                self.config[channel+" enable"]=checked
                return True
            else:
                return False
        except:
            return False

    def clock_unused(self):
        try:
            self.handle.write("CL HI\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def clock_save(self):
        try:
            self.handle.write("CL SA\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def clock_set(self,comboBox_clock_mode):
        if comboBox_clock_mode == 0:
            clock_mode_txt = "CL OU"
        else:
            clock_mode_txt = "CL IN"
        txt = "CT " + self.spinBox_clock_trim.text() + ";" + clock_mode_txt
        try:
            self.handle.write(txt.encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def clock_query(self):
        try:
            self.handle.write("CL\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            return result
        except:
            return ""

    def burst_turn(self, checked):
        burst_enable_dic={"OFF":"BU OF\r","ON":"BU ON\r"}
        try:
            self.handle.write(burst_enable_dic[checked].encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                self.config["burst enable"]=checked
                return True
            else:
                return False
        except:
            return False

    def burst_reseet(self):
        try:
            self.handle.write("BU RE".encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def burst_query(self):
        try:
            self.handle.write("BU".encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            return result
        except:
            return ""

    def burst_set(self,nvalue):
        "int  range 10e9"
        txt = "BN " + str(nvalue) + ";" + "BM " + str(nvalue)
        try:
            self.handle.write(txt.encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                self.config["burst count"]=nvalue
                return True
            else:
                return False
        except:
            return False

    def trigger_source(self, mode):
        # REM SYN  INT POS NEG OFF
        trigger_mode_dic={"REM":"TR RE","SYN":"TR SY","INT":"TR IN","POS":"TR PO","NEG":"TR NE","OFF":"TR OF"}
        txt = trigger_mode_dic[mode]
        try:
            self.handle.write(txt.encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                self.config["trigger mode"]=mode
                return True
            else:
                return False
        except:
            return False

    def divisor_set(self,trigger_divisor):
        "int"
        txt = "TD " + str(trigger_divisor)
        try:
            self.handle.write(txt.encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                self.config["trigger divisor"]=trigger_divisor
                return True
            else:
                return False
        except:
            return False

    def trigger_query(self):
        try:
            self.handle.write("TR".encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            return result
        except:
            return ""

    def connect_device(self):
        port_list=list(comports())
        if port_list!=[]:
            for port in port_list:
                try:
                    self.handle = serial.Serial(port[0], baudrate=38400)
                    result=self.channel_query("A")
                    if "Ch" in result:
                        return True
                    else:
                        self.handle.close()
                except:
                    pass
        return False

    def break_device(self):
        if self.handle is not None:
            if self.handle.is_open:
                self.handle.close
                return True
        return False

    def device_status(self):
        try:
            self.handle.write("ST".encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            txt=bytes(result).decode("ascii")
            return txt
        except:
            return ""

    def demo(self):
        try:
            self.handle.write("RU DE".encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                return True
            else:
                return False
        except:
            return False

    def sythesize_set(self,synthesize_freq):
        #带单位
        if synthesize_freq[-1]=="M":
            synthesize_freq=float(synthesize_freq[:-1])*10**6
        elif synthesize_freq[-1]=="K":
            synthesize_freq=float(synthesize_freq[:-1])*10**3
        else:synthesize_freq=float(synthesize_freq[:-1])

        txt = "SY %.2f"%synthesize_freq
        try:
            self.handle.write(txt.encode("ascii"))
            self.handle.write("\r".encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                self.config["trigger freq"]=synthesize_freq
                return True
            else:
                return False
        except:
            return False

    def trigger_impedance_set(self,impedance_value):
        trigger_impedance_dic={"HIZ":"TR HI\r","50R":"TR TE\r"}
        try:
            self.handle.write(trigger_impedance_dic[impedance_value].encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                self.config["trigger impedance"]=impedance_value
                return True
            else:
                return False
        except:
            return False

    def trigger_level_set(self,trigger_level):
        trigger_level_txt = "TL %.3f\r"%trigger_level
        try:
            self.handle.write(trigger_level_txt.encode("ascii"))
            time.sleep(0.1)
            result = self.handle.read_all()
            result=bytes(result).decode("ascii")
            if "OK" in result:
                self.config["trigger level"]=trigger_level
                return True
            else:
                return False
        except:
            return False

