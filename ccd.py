import clr
clr.AddReference("ICImagingControl")
from TIS.Imaging import ICImagingControl as camera
import ctypes as C
import time
import numpy as np
class ccd_174():
    """相机拥有5个缓存器，最多设置5个获取线程"""
    #MemoryCurrentGrabberColorformat内存管理图像格式
    def __init__(self):
        self.cam = camera()
        # self.extention_dll = C.CDLL("IC LabVIEW Extension 2.dll")


    def connect_device(self):
        try:
            camera_serial = self.cam.Devices[0]
            print("相机",str(camera_serial))
            running_status = self.cam.LiveVideoRunning
            if running_status:
                self.cam.LiveStop()
            else:
                pass
            self.cam.Device = str(camera_serial)
            self.cam.VideoFormat = "Y800 (1920x1200)"
            # self.cam.VideoFormat = "Y800 (1440x1080)"
            self.cam.MemoryCurrentGrabberColorformat = 5
            self.Load_Device_State()
            self.enable_strobe(True)
            self.strobe_exposure(2)
            self.cam.LiveStop()
            return True
        except:
            return False


    def start(self):
        try:
            self.cam.LiveStart()
        except:
            pass
    def stop(self):
        try:
            self.cam.LiveStop()
        except:
            pass

    def break_device(self):
        try:
            self.cam.LiveStop()
            return "camera break success"
        except:
            return "camera break error"


    def get_data(self):
        self.cam.MemorySnapImage()
        data_mem = self.cam.ImageActiveBuffer
        data_mem.Lock()
        data_pointer = int(str(data_mem.GetIntPtr()))
        if self.cam.ImageBitsPerPixel == 8:  # 根据相机位数选择读取方式
            data = (C.c_uint8 * self.cam.ImageWidth * self.cam.ImageHeight).from_address(data_pointer)
        else:
            data = (C.c_uint16 * self.cam.ImageWidth * self.cam.ImageHeight).from_address(data_pointer)
        data_mem.Unlock()
        # data=np.array(data)
        return data


    def change_format(self,format_txt):
        self.cam.LiveStop()
        format_bit_type = format_txt.split(" ")[0]
        if format_bit_type == "Y800":
                self.cam.MemoryCurrentGrabberColorformat = 5
                self.cam.VideoFormat = format_txt
        else:
            self.cam.MemoryCurrentGrabberColorformat = 5
            self.cam.VideoFormat = format_txt
            self.cam.MemoryCurrentGrabberColorformat = 11
        self.cam.LiveStart()

    def get_format(self):
        return self.cam.VideoFormat

    def enable_trigger(self,bool):
        v1 = self.cam.VCDPropertyItems
        trigger_obj = v1.get_Item(6)
        trigger = trigger_obj.get_Elements()
        trigger_mod = trigger.get_Item(0)
        trigger_mod_value = trigger_mod.get_Item(0)
        trigger_mod_value.set_Switch(bool)

    def trigger_ploarity(self,bool):
        v1 = self.cam.VCDPropertyItems
        trigger_obj = v1.get_Item(6)
        trigger = trigger_obj.get_Elements()
        trigger_ploarity = trigger.get_Item(2)
        trigger_ploarity_value = trigger_ploarity.get_Item(0)
        trigger_ploarity_value.set_Switch(bool)

    def trigger_exposure_mode(self,value):
        v1 = self.cam.VCDPropertyItems
        trigger_obj = v1.get_Item(6)
        trigger = trigger_obj.get_Elements()
        trigger_ploarity = trigger.get_Item(3)
        trigger_ploarity_value = trigger_ploarity.get_Item(0)
        trigger_ploarity_value.set_Value(value)

    def enable_strobe(self,bool):
        v1 = self.cam.VCDPropertyItems
        strobe_obj = v1.get_Item(15)
        strobe = strobe_obj.get_Elements()
        strobe_mod = strobe.get_Item(0)
        strobe_mod_value = strobe_mod.get_Item(0)
        strobe_mod_value.set_Switch(bool)

    def strobe_ploarity(self,bool):
        v1 = self.cam.VCDPropertyItems
        v2 = v1.get_Item(15)
        strobe = v2.get_Elements()
        strobe_polarity = strobe.get_Item(2)
        strobe_polarity_value = strobe_polarity.get_Item(0)
        strobe_polarity_value.set_Switch(bool)

    def strobe_exposure(self,value):
        v1 = self.cam.VCDPropertyItems
        v2 = v1.get_Item(15)
        strobe = v2.get_Elements()
        strobe_mod = strobe.get_Item(1)
        strobe_mod_value = strobe_mod.get_Item(0)
        strobe_mod_value.set_Value(value)

    def exposure(self,value):
        """曝光时间，分数形式"""
        v1 = self.cam.VCDPropertyItems
        v2 = v1.get_Item(5)
        exp = v2.get_Elements()
        exposure_value_element = exp.get_Item(0)
        exposure_value = exposure_value_element.get_Item(0)
        exposure_value.set_Value(value)

    def set_integration_time(self,value):
        v1 = self.cam.VCDPropertyItems
        v2 = v1.get_Item(5)
        exp = v2.get_Elements()
        exposure_value_element = exp.get_Item(0)
        exposure_value = exposure_value_element.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E08")
        exposure_value.set_Value(value)

    def get_formats(self):
        formats_list = self.cam.VideoFormats
        formats = []
        for i in formats_list:
            formats.append(i.Name)
        return formats

    def set_flip_horizontal(self,value):
        self.cam.LiveStop()
        self.cam.set_DeviceFlipHorizontal(value)
        self.cam.LiveStart()

    def set_flip_vertical(self,value):
        self.cam.LiveStop()
        self.cam.set_DeviceFlipVertical(value)
        self.cam.LiveStart()

    def get_frames(self):
        frame_list = self.cam.DeviceFrameRates
        frames = []
        for i in frame_list:
            frames.append(i)
        return frames


    def get_integration_time(self):
        v1 = self.cam.VCDPropertyItems
        # for i in range(16):
        #     print(i,v1.get_Item(i).Name)
        v2 = v1.get_Item(5)
        exp = v2.get_Elements()
        exposure_value_element = exp.get_Item(0)
        exposure_value = exposure_value_element.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E08")
        exposure_time=exposure_value.get_Value()
        return exposure_time


    def exposure_max_auto(self,bool):
        v1 = self.cam.VCDPropertyItems
        v2 = v1.get_Item(5)
        exp = v2.get_Elements()
        exposure_max_auto_element= exp.get_Item(4)
        exposure_max_auto_value = exposure_max_auto_element.get_Item(0)
        exposure_max_auto_value.set_Switch(bool)

    def get_exposure_max_auto(self):
        v1 = self.cam.VCDPropertyItems
        v2 = v1.get_Item(5)
        exp = v2.get_Elements()
        exposure_max_auto_element = exp.get_Item(4)
        exposure_max_auto_value = exposure_max_auto_element.get_Item(0)
        value=exposure_max_auto_value.get_Switch()
        return value


    def exposure_value_auto(self, bool):
        v1 = self.cam.VCDPropertyItems
        v2 = v1.get_Item(5)
        exp = v2.get_Elements()
        exposure_auto = exp.get_Item(1)
        exposure_auto_value = exposure_auto.get_Item(0)
        exposure_auto_value.set_Switch(bool)


    def set_bright(self,value):
        v1 = self.cam.VCDPropertyItems
        brightness_mod=v1.get_Item(0)
        bright_elements = brightness_mod.get_Elements()
        bright_element = bright_elements.get_Item(0)
        bright_value = bright_element.get_Item(0)
        bright_value.set_Value(value)

    def set_gain(self,value):
        v1 = self.cam.VCDPropertyItems
        gain_mod = v1.get_Item(3)
        print(gain_mod.Name,"set_gain")
        gain_elements = gain_mod.get_Elements()
        gain_element = gain_elements.get_Item(0)
        gain_value = gain_element.get_Item(0)
        print(gain_value.get_Value())
        gain_value.set_Value(value*10)


    def get_gain(self):
        v1 = self.cam.VCDPropertyItems
        gain_mod = v1.get_Item(3)
        print(gain_mod.Name,"get_gain")
        gain_elements = gain_mod.get_Elements()
        gain_element = gain_elements.get_Item(0)
        gain_value = gain_element.get_Item(0)
        gain_value=gain_value.get_Value()
        return gain_value


    def gain_auto(self,bool):
        v1 = self.cam.VCDPropertyItems
        gain_mod = v1.get_Item(3)
        gain_elements = gain_mod.get_Elements()
        gain_auto_element = gain_elements.get_Item(1)
        gain_auto_value = gain_auto_element.get_Item(0)
        gain_auto_value.set_Switch(bool)

    def get_gain_auto(self):
        v1 = self.cam.VCDPropertyItems
        gain_mod = v1.get_Item(3)
        gain_elements = gain_mod.get_Elements()
        gain_auto_element = gain_elements.get_Item(1)
        gain_auto_value = gain_auto_element.get_Item(0)
        value=gain_auto_value.get_Switch()
        return value




    def set_frame_rate(self,rate):
        try:
            self.cam.LiveStop()
            self.cam.set_DeviceFrameRate(rate)
            self.cam.LiveStart()
            return "set frame success"
        except:
            return "set frame error"

    def get_frame_rate(self):
        """DeviceFrameRate,相机帧速名称"""
        frame_rate=self.cam.get_DeviceFrameRate()
        return frame_rate


    def get_image_bit(self):
        return self.cam.ImageBitsPerPixel

    def get_image_height(self):
        return self.cam.ImageHeight

    def get_image_width(self):
        return self.cam.ImageWidth

    def set_Memory_Pixel_Format(self):
        self.cam.LiveStop()
        self.cam.set_MemoryPixelFormat()
        self.cam.LiveStart()

    def set_Memory_Current_Grabber_Colorformat(self):
        self.cam.LiveStop()
        self.cam.set_MemoryCurrentGrabberColorformat()
        self.cam.LiveStart()

    def set_Video_Format(self,image_format):
        self.cam.LiveStop()
        time.sleep(0.1)
        self.cam.set_VideoFormat(image_format)
        self.cam.LiveStart()

    def Load_Device_State(self):
        self.cam.LiveStop()
        self.cam.LoadDeviceState
        self.cam.LiveStart()


    def Save_Device_State(self):
        self.cam.LiveStop()
        self.cam.SaveDeviceState
        self.cam.LiveStart()




class ccd_em16():
    """相机拥有5个缓存器，最多设置5个获取线程"""
    #MemoryCurrentGrabberColorformat内存管理图像格式
    def __init__(self):
        self.cam = camera()
        self.connect_status=self.connect_device()
        if self.connect_status:
            self.init_device()
            if self.cam.Devices[0].Name=="DMK 33UX174":
                self.cam.VideoFormat = "Y800 (1920x1200)"
            else:
                self.cam.VideoFormat = "Y800 (1440x1080)"
            self.cam.MemoryCurrentGrabberColorformat = 5
            self.set_auto_center(False)
            self.cam.LiveStart()


    def init_device(self):
        self.Load_Device_State()
        self.set_bright(0)
        self.set_exposure_value_auto(False)
        self.set_exposure_max_auto(False)
        self.set_gain_auto(False)
        self.enable_strobe(True)
        self.set_strobe_mode(2)
        self.strobe_ploarity(True)


    def connect_device(self):
        if self.cam.Devices.Length>0:
            self.cam.LiveStop()
            self.cam.Device = self.cam.Devices[0].Name
            return True
        else:
            return False


    def start(self):
        try:
            self.cam.LiveStart()
            return True
        except:
            return False

    def stop(self):
        try:
            self.cam.LiveStop()
            return True
        except:
            return False

    def break_device(self):
        try:
            self.cam.LiveStop()
            return True
        except:
            return False


    def get_data(self):
        self.cam.MemorySnapImage()
        data_mem = self.cam.ImageActiveBuffer
        data_mem.Lock()
        data_pointer = int(str(data_mem.GetIntPtr()))
        if self.get_image_bit() == 8:  # 根据相机位数选择读取方式
            data = (C.c_uint8 * self.cam.ImageWidth * self.cam.ImageHeight).from_address(data_pointer)
        else:
            data = (C.c_uint16 * self.cam.ImageWidth * self.cam.ImageHeight).from_address(data_pointer)
        data_mem.Unlock()
        return data



    def get_format(self):
        return self.cam.VideoFormat

    def enable_trigger(self,bool):
        trigger_obj = self.cam.VCDPropertyItems.FindItem("90D57031-E43B-4366-AAEB-7A7A10B448B4")
        trigger = trigger_obj.get_Elements()
        trigger_mod = trigger.get_Item(0)
        trigger_mod_value = trigger_mod.get_Item(0)
        trigger_mod_value.set_Switch(bool)

    def trigger_ploarity(self,bool):
        trigger_obj = self.cam.VCDPropertyItems.FindItem("90D57031-E43B-4366-AAEB-7A7A10B448B4")
        trigger = trigger_obj.get_Elements()
        trigger_ploarity = trigger.get_Item(2)
        trigger_ploarity_value = trigger_ploarity.get_Item(0)
        trigger_ploarity_value.set_Switch(bool)

    def trigger_exposure_mode(self,value):
        trigger_obj = self.cam.VCDPropertyItems.FindItem("90D57031-E43B-4366-AAEB-7A7A10B448B4")
        trigger = trigger_obj.get_Elements()
        trigger_ploarity = trigger.get_Item(3)
        trigger_ploarity_value = trigger_ploarity.get_Item(0)
        trigger_ploarity_value.set_Value(value)

    def enable_strobe(self,bool):
        strobe_obj = self.cam.VCDPropertyItems.FindItem("DC320EDE-DF2E-4A90-B926-71417C71C57C")
        strobe = strobe_obj.get_Elements()
        strobe_mod = strobe.get_Item(0)
        strobe_mod_value = strobe_mod.get_Item(0)
        strobe_mod_value.set_Switch(bool)

    def get_strobe_enable(self):
        strobe_obj = self.cam.VCDPropertyItems.FindItem("DC320EDE-DF2E-4A90-B926-71417C71C57C")
        strobe = strobe_obj.get_Elements()
        strobe_mod = strobe.get_Item(0)
        strobe_mod_value = strobe_mod.get_Item(0)
        value=strobe_mod_value.get_Switch()
        return value


    def strobe_ploarity(self,bool):
        v2 = self.cam.VCDPropertyItems.FindItem("DC320EDE-DF2E-4A90-B926-71417C71C57C")
        strobe = v2.get_Elements()
        strobe_polarity = strobe.get_Item(2)
        strobe_polarity_value = strobe_polarity.get_Item(0)
        strobe_polarity_value.set_Switch(bool)

    def set_strobe_mode(self,value):
        v2 = self.cam.VCDPropertyItems.FindItem("DC320EDE-DF2E-4A90-B926-71417C71C57C")
        strobe = v2.get_Elements()
        strobe_mod = strobe.get_Item(1)
        strobe_mod_value = strobe_mod.get_Item(0)
        strobe_mod_value.set_Value(value)


    def show_base_settingdialog(self):
        if self.cam.DeviceValid:
            if self.cam.LiveVideoRunning:
                self.cam.LiveStop()
                self.cam.ShowDeviceSettingsDialog()
                self.cam.LiveStart()
            else:
                self.cam.ShowDeviceSettingsDialog()
        else:
            pass



    def show_advance_settingdialog(self):
        if self.cam.DeviceValid:
            if self.cam.LiveVideoRunning:
                self.cam.LiveStop()
                self.cam.ShowPropertyDialog()
                self.cam.LiveStart()
            else:
                self.cam.ShowPropertyDialog()

    def set_integration_time(self,value):
        exoposure = self.cam.VCDPropertyItems.FindItem("90D5702E-E43B-4366-AAEB-7A7A10B448B4")
        exoposure_value = exoposure.FindElement("B57D3000-0AC6-4819-A609-272A33140ACA")
        value_item = exoposure_value.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E08")
        value_item.set_Value(value)


    def set_binning(self,value):
        "1disable  5  2x2 6 vertical  7 horizontal"
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            formate_dic={"1":"Y800 (1440x1080) ","5":"Y800 (720x540)  [Skipping 2x]","6":"Y800 (1440x540) [Skipping 2x vertical]","7":"Y800 (720x1080) [Skipping 2x horizontal]"}
            self.set_Video_Format(formate_dic[str(value)])
            binning = self.cam.VCDPropertyItems.FindItem("4F95A06D-9C15-407B-96AB-CF3FED047BA4")
            binning_mode = binning.FindElement("B57D3000-0AC6-4819-A609-272A33140ACA")
            value_item = binning_mode.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E06")
            value_item.set_Value(value)
            print(self.get_binning())
            print(self.get_formats())
            self.cam.LiveStart()
        else:
            binning = self.cam.VCDPropertyItems.FindItem("4F95A06D-9C15-407B-96AB-CF3FED047BA4")
            binning_mode = binning.FindElement("B57D3000-0AC6-4819-A609-272A33140ACA")
            value_item = binning_mode.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E06")
            value_item.set_Value(value)


    def get_binning(self):
        binning = self.cam.VCDPropertyItems.FindItem("4F95A06D-9C15-407B-96AB-CF3FED047BA4")
        binning_mode = binning.FindElement("B57D3000-0AC6-4819-A609-272A33140ACA")
        value_item = binning_mode.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E06")
        value=value_item.get_Value()
        return value


    def get_formats(self):
        formats_list = self.cam.VideoFormats
        formats = []
        for i in formats_list:
            formats.append(i.Name)
        return formats

    def set_flip_horizontal(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            self.cam.set_DeviceFlipHorizontal(value)
            self.cam.LiveStart()
        else:
            self.cam.set_DeviceFlipHorizontal(value)

    def set_flip_vertical(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            self.cam.set_DeviceFlipVertical(value)
            self.cam.LiveStart()
        else:
            self.cam.set_DeviceFlipVertical(value)

    def get_frames(self):
        frame_list = self.cam.DeviceFrameRates
        frames = []
        for i in frame_list:
            frames.append(i)
        return frames


    def get_integration_time(self):
        exoposure = self.cam.VCDPropertyItems.FindItem("90D5702E-E43B-4366-AAEB-7A7A10B448B4")
        exoposure_value = exoposure.FindElement("B57D3000-0AC6-4819-A609-272A33140ACA")
        value_item = exoposure_value.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E08")
        value=value_item.get_Value()
        return value



    def set_exposure_max_auto(self,bool):
        exoposure = self.cam.VCDPropertyItems.FindItem("90D5702E-E43B-4366-AAEB-7A7A10B448B4")
        exoposure_auto_max = exoposure.FindElement("65190390-1AD8-4E91-9021-66D64090CC85")
        value_item = exoposure_auto_max.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E04")
        value_item.set_Switch(bool)

    def get_exposure_max_auto(self):
        exoposure = self.cam.VCDPropertyItems.FindItem("90D5702E-E43B-4366-AAEB-7A7A10B448B4")
        exoposure_value = exoposure.FindElement("65190390-1AD8-4E91-9021-66D64090CC85")
        value_item = exoposure_value.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E04")
        value =value_item.get_Switch()
        return value


    def set_exposure_value_auto(self, value):
        exoposure = self.cam.VCDPropertyItems.FindItem("90D5702E-E43B-4366-AAEB-7A7A10B448B4")
        exoposure_auto = exoposure.FindElement("B57D3001-0AC6-4819-A609-272A33140ACA")
        value_item = exoposure_auto.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E04")
        value_item.set_Switch(value)



    def set_bright(self,value):
        bright = self.cam.VCDPropertyItems.FindItem("284C0E06-010B-45BF-8291-09D90A459B28")
        bright_value = bright.FindElement("B57D3000-0AC6-4819-A609-272A33140ACA")
        value_item = bright_value.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E03")
        value_item.set_Value(value)



    def get_bright(self):
        bright = self.cam.VCDPropertyItems.FindItem("284C0E06-010B-45BF-8291-09D90A459B28")
        bright_value = bright.FindElement("B57D3000-0AC6-4819-A609-272A33140ACA")
        value_item = bright_value.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E03")
        light_value=value_item.get_Value()
        return light_value

    def set_gain(self,value):
        gain = self.cam.VCDPropertyItems.FindItem("284C0E0F-010B-45BF-8291-09D90A459B28")
        gain_value = gain.FindElement("B57D3000-0AC6-4819-A609-272A33140ACA")
        value_item = gain_value.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E08")
        value_item.set_Value(value)



    def get_gain(self):
        gain = self.cam.VCDPropertyItems.FindItem("284C0E0F-010B-45BF-8291-09D90A459B28")
        gain_value = gain.FindElement("B57D3000-0AC6-4819-A609-272A33140ACA")
        value_item = gain_value.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E08")
        gain_value=value_item.get_Value()
        return gain_value


    def set_gain_auto(self,value):
        gain = self.cam.VCDPropertyItems.FindItem("284C0E0F-010B-45BF-8291-09D90A459B28")
        gain_auto = gain.FindElement("B57D3001-0AC6-4819-A609-272A33140ACA")
        value_item = gain_auto.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E04")
        value_item.set_Switch(value)

    def get_gain_auto(self):
        gain = self.cam.VCDPropertyItems.FindItem("284C0E0F-010B-45BF-8291-09D90A459B28")
        gain_auto = gain.FindElement("B57D3001-0AC6-4819-A609-272A33140ACA")
        value_item = gain_auto.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E04")
        value=value_item.get_Switch()
        return value




    def set_frame_rate(self,rate):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            self.cam.set_DeviceFrameRate(rate)
            self.cam.LiveStart()
        else:
            self.cam.set_DeviceFrameRate(rate)



    def get_frame_rate(self):
        """DeviceFrameRate,相机帧速名称"""
        frame_rate=self.cam.get_DeviceFrameRate()
        return frame_rate


    def get_image_bit(self):
        if "Y800" in self.cam.VideoFormat:
            return 8
        elif "Y16" in self.cam.VideoFormat:
            return 16


    def get_image_height(self):
        return self.cam.ImageHeight

    def get_image_width(self):
        return self.cam.ImageWidth

    def set_Memory_Pixel_Format(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            self.cam.set_MemoryPixelFormat(value)
            self.cam.LiveStart()
        else:
            self.cam.set_MemoryPixelFormat(value)

    def set_Memory_Current_Grabber_Colorformat(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            self.cam.set_MemoryCurrentGrabberColorformat(value)
            self.cam.LiveStart()
        else:
            self.cam.set_MemoryCurrentGrabberColorformat(value)


    def set_Video_Format(self,image_format):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            self.cam.set_VideoFormat(image_format)
            self.cam.LiveStart()
        else:
            self.cam.set_VideoFormat(image_format)

    def Load_Device_State(self):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            self.cam.LoadDeviceState
            self.cam.LiveStart()
        else:
            self.cam.LoadDeviceState


    def Save_Device_State(self):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            self.cam.SaveDeviceState()
            self.cam.LiveStart()
        else:
            self.cam.SaveDeviceState()

    def set_y_offset(self, value):
        # max1076  min 0
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            Partial_scan = self.cam.VCDPropertyItems.FindItem("2CED6FD6-AB4D-4C74-904C-D682E53B9CC5")
            y_offset = Partial_scan.FindElement("87FB6C02-98A8-46B0-B18D-6442D9775CD3")
            value_item = y_offset.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E03")
            value_item.set_Value(value)
            self.cam.LiveStart()
        else:
            Partial_scan = self.cam.VCDPropertyItems.FindItem("2CED6FD6-AB4D-4C74-904C-D682E53B9CC5")
            y_offset = Partial_scan.FindElement("87FB6C02-98A8-46B0-B18D-6442D9775CD3")
            value_item = y_offset.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E03")
            value_item.set_Value(value)

        # VCDPropertyItems.Find  FindElement FindInterface   FindItem  get_Item

    def set_x_offset(self, value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            Partial_scan = self.cam.VCDPropertyItems.FindItem("2CED6FD6-AB4D-4C74-904C-D682E53B9CC5")
            x_offset = Partial_scan.FindElement("5E59F654-7B47-4458-B4C6-5D4F0D175FC1")
            value_item = x_offset.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E03")
            value_item.set_Value(value)
            self.cam.LiveStart()
        else:
            Partial_scan = self.cam.VCDPropertyItems.FindItem("2CED6FD6-AB4D-4C74-904C-D682E53B9CC5")
            x_offset = Partial_scan.FindElement("5E59F654-7B47-4458-B4C6-5D4F0D175FC1")
            value_item = x_offset.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E03")
            value_item.set_Value(value)


    def get_y_offset(self):
        # max1076  min 0
        Partial_scan = self.cam.VCDPropertyItems.FindItem("2CED6FD6-AB4D-4C74-904C-D682E53B9CC5")
        y_offset = Partial_scan.FindElement("87FB6C02-98A8-46B0-B18D-6442D9775CD3")
        value_item = y_offset.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E03")
        value=value_item.get_Value()
        return value
        # VCDPropertyItems.Find  FindElement FindInterface   FindItem  get_Item

    def get_x_offset(self):
        Partial_scan = self.cam.VCDPropertyItems.FindItem("2CED6FD6-AB4D-4C74-904C-D682E53B9CC5")
        x_offset = Partial_scan.FindElement("5E59F654-7B47-4458-B4C6-5D4F0D175FC1")
        value_item = x_offset.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E03")
        value=value_item.get_Value()
        return value

    def set_auto_center(self, value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
            Partial_scan = self.cam.VCDPropertyItems.FindItem("2CED6FD6-AB4D-4C74-904C-D682E53B9CC5")
            auto_center = Partial_scan.FindElement("36EAA683-3321-44BE-9D73-E1FD4C3FDB87")
            value_item = auto_center.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E04")
            value_item.set_Switch(value)
            self.cam.LiveStart()
        else:
            Partial_scan = self.cam.VCDPropertyItems.FindItem("2CED6FD6-AB4D-4C74-904C-D682E53B9CC5")
            auto_center = Partial_scan.FindElement("36EAA683-3321-44BE-9D73-E1FD4C3FDB87")
            value_item = auto_center.FindInterface("99B44940-BFE1-4083-ADA1-BE703F4B8E04")
            value_item.set_Switch(value)

    def set_display_height(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
        self.cam.set_LiveDisplayHeight(value)

    def set_display_left(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
        self.cam.set_LiveDisplayLeft(value)

    def set_display_position(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
        self.cam.set_LiveDisplayPosition(value)

    def set_display_size(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
        self.cam.set_LiveDisplaySize(value)

    def set_display_top(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
        self.cam.set_LiveDisplayTop(value)

    def set_display_width(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
        self.cam.set_LiveDisplayWidth(value)

    def set_display_zoom(self,value):
        if self.cam.LiveVideoRunning:
            self.cam.LiveStop()
        self.cam.set_LiveDisplayZoomFactor(value)

    def set_display_default_enable(self,value):
        self.cam.set_LiveDisplayDefault(value)

    def set_trigger(self,value):
        self.cam.set_DeviceTrigger(value)

    def set_videonorm_enable(self,value):
        self.cam.set_VideoNorm(value)



#添加功能项
    def set_height(self,int_height):
        self.cam.ImageSize.set_Height(int_height)

    def set_width(self,int_width):
        self.cam.ImageSize.set_Width(int_width)


    def set_location_x(self,int_x):
        self.cam.Location.set_X(int_x)

    def set_location_y(self,int_y):
        self.cam.Location.set_Y(int_y)

    def get_width(self):
        width=self.cam.get_Width()
        return width

    def get_videoformats(self):
        formats=self.cam.get_VideoFormats()
        return formats

    def get_format(self):
        video_format=self.cam.get_VideoFormat()
        return video_format


    def get_videonorms(self):
        video_norms=self.cam.get_VideoNorms()
        return video_norms

    def get_v_scroll(self):
        v_scroll=self.cam.get_VerticalScroll()
        return v_scroll

    def get_vscroll(self):
        vscroll=self.cam.get_VScroll()
        return vscroll

    def get_top(self):
        top=self.cam.get_Top()
        return top

    def get_right(self):
        right=self.cam.get_Right()
        return right

    def get_left(self):
        left=self.cam.get_Left()
        return left

    def get_height(self):
        height=self.cam.get_Height()
        return height

    def get_bottom(self):
        bottom=self.cam.get_Bottom()
        return bottom

    def get_region(self):
        region=self.cam.get_Region()
        return region

    def get_size(self):
        size=self.cam.get_Size()
        return size

    def get_site(self):
        site=self.cam.get_Site()
        return site

    def get_scaechildren(self):
        scale_children=self.cam.get_ScaleChildren()
        return scale_children

    def get_right_to_left(self):
        right_to_left=self.cam.get_RightToLeft()
        return right_to_left


    def get_over_bitmap_position(self):
        over_bitmap_position=self.cam.get_OverlayBitmapPosition()
        return over_bitmap_position

    def get_overlay_bitmap(self):
        overlay_bitmap=self.cam.get_OverlayBitmap()
        return overlay_bitmap

    def get_min_size(self):
        min_size=self.cam.get_MinimumSize()
        return min_size

    def get_pix_format(self):
        pix_format=self.cam.get_MemoryPixelFormat()
        return pix_format

    def get_memory_grab_colorformat(self):
        colorformat=self.cam.get_MemoryCurrentGrabberColorformat()
        return colorformat

    def get_max_size(self):
        max_size=self.cam.get_MaximumSize()
        return max_size

    def get_location(self):
        location=self.cam.get_Location()
        return location

    def get_live_width(self):
        width=self.cam.get_LiveDisplayWidth()
        return width
    def get_live_top(self):
        top=self.cam.get_LiveDisplayTop()
        return top

    def get_live_size(self):
        size=self.cam.get_LiveDisplaySize()
        return size

    def get_live_position(self):
        position=self.cam.get_LiveDisplayPosition()
        return position

    def get_live_width(self):
        width=self.cam.get_LiveDisplayOutputWidth()
        return width

    def get_live_out_size(self):
        size=self.cam.get_LiveDisplayOutputSize()
        return size

    def get_live_out_height(self):
        height=self.cam.get_LiveDisplayOutputHeight()
        return height

    def get_live_left(self):
        left=self.cam.get_LiveDisplayLeft()
        return left

    def get_live_height(self):
        height=self.cam.get_LiveDisplayHeight()
        return height

    def get_live_default(self):
        default=self.cam.get_LiveDisplayDefault()
        return default


    def get_imagewidth(self):
        width=self.cam.get_ImageWidth()
        return width

    def get_image_size(self):
        size=self.cam.get_ImageSize()
        return size

    def get_image_buffer_size(self):
        size=self.cam.get_ImageRingBufferSize()
        return size

    def get_image_height(self):
        height=self.cam.get_ImageHeight()
        return height

    def get_imagebuffers(self):
        buffers=self.cam.get_ImageBuffers()
        return buffers

    def get_h_scroll(self):
        h_scroll=self.cam.get_HorizontalScroll()
        return h_scroll

    def get_hscroll(self):
        hscroll=self.cam.get_HScroll()
        return hscroll

    def get_display_rectangle(self):
        rectangle=self.cam.get_DisplayRectangle()
        return rectangle

    def get_divices(self):
        devices=self.cam.get_Devices()
        return devices

    def get_trigger_enable(self):
        enable=self.cam.get_DeviceTriggerAvailable()
        return enable

    def get_trigger(self):
        trigger=self.cam.get_DeviceTrigger()
        return trigger

    def get_devices_state(self):
        state=self.cam.get_DeviceState()
        return state


    def get_frame_filter(self):
        frame_filter=self.cam.get_DeviceFrameFilters()
        return frame_filter

    def get_flit_v_enbale(self):
        enable=self.cam.get_DeviceFlipVerticalAvailable()
        return enable
    def get_flipvertical(self):
        flip=self.cam.get_DeviceFlipVertical()
        return flip

    def get_flip_h_enable(self):
        enable=self.cam.get_DeviceFlipHorizontalAvailable()
        return enable

    def get_fliphorizontal(self):
        flip=self.cam.get_DeviceFlipHorizontal()
        return flip

    def get_device(self):
        device=self.cam.get_Device()
        return device

    def get_defaultsize(self):
        size=self.cam.get_DefaultSize()
        return size

    def get_default_min_size(self):
        size=self.cam.get_DefaultMinimumSize()
        return size

    def get_default_max_size(self):
        size=self.cam.get_DefaultMaximumSize()
        return size

    def get_auto_sizemode(self):
        mode=self.cam.get_AutoSizeMode()
        return mode

    def get_autosize(self):
        size=self.cam.get_AutoSize()
        return size

    def get_auto_scroll_position(self):
        position=self.cam.get_AutoScrollPosition()
        return position

    def get_auto_scroll_offset(self):
        offset=self.cam.get_AutoScrollOffset()
        return offset

    def get_auto_scroll_minsize(self):
        size=self.cam.get_AutoScrollMinSize()
        return size

    def get_auto_scroll_margin(self):
        margin=self.cam.get_AutoScrollMargin()
        return margin

    def get_auto_scroll(self):
        auto_scroll=self.cam.get_AutoScroll()
        return auto_scroll

    def get_auto_scale_mode(self):
        mode=self.cam.get_AutoScaleMode()
        return mode

    def get_auto_scal_factor(self):
        factor=self.cam.get_AutoScaleFactor()
        return factor








# set_AutoScaleMode
# set_AutoScroll
# set_AutoScrollOffset
# set_AutoScrollPosition
# set_AutoSize
# set_AutoSizeMode
# set_LiveDisplayDefault
# set_LiveDisplayHeight
# set_LiveDisplayLeft
# set_LiveDisplayPosition
# set_LiveDisplaySize
# set_LiveDisplayTop
# set_LiveDisplayWidth
# set_LiveDisplayZoomFactor
# set_Location
# set_MinimumSize
# set_MaximumSize
# set_MemoryCurrentGrabberColorformat
# set_MemoryPixelFormat
# set_MinimumSize
# set_Region
# set_RightToLeft
# set_Site
# set_Size
# set_Top
# set_Width
# set_Height
# set_Left
# set_VScroll
# set_HScroll
# set_DeviceFlipHorizontal
# set_DeviceFlipVertical
# set_VideoFormat
# set_DeviceFrameRate
# set_DeviceTrigger


# get_VCDPropertyItems


# kkk=ccd_em16()
#
# kkk.cam
# kkk.enable_strobe(True)
# kkk.set_strobe_mode(2)
# kkk.strobe_ploarity(True)
# sss=kkk.get_devices_state()
# print("%.2f"%0)
# kkk.stop()

# kkk.set_Video_Format("Y16 (576x408)")
# print(kkk.get_image_bit())
# kkk.cam.set_VideoFormat("Y16 (576x408)")
# kkk.start()
# sss=kkk.get_imagebits()
# print(sss)
# while True:
#     sss=kkk.get_data()
#     print(sss)
#     time.sleep(0.01)
# from PyQt5 import QtWidgets
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = ccd_em16()
#     while True:
#         sss = MainWindow.get_data()
#         print(sss)
#         time.sleep(0.01)
#     sys.exit(app.exec_())


# kkk.set_display_default_enable(False)
# sss=kkk.get_imagebits()
# print(sss)
# kkk.set_display_default_enable(True)

# kkk.set_videonorm_enable("Y800 (300x288)")
# kkk.set_display_size([1440,1080])
# kkk.show_base_settingdialog()
# SSS=kkk.cam
# kkk.cam.set_Width(500)

# kkk.cam.set_Size()
# kkk.cam.set_Left(200)
# kkk.cam.set_Height(600)
# kkk.set_width(500)
# kkk.set_x_offset(500)
# kkk.set_Video_Format("Y800 (300x288)")
# kkk.set_display_width(400)
# kkk.set_display_zoom()
# print(kkk.get_live_size())
# print(kkk.get_image_width())
# print(kkk.get_width())
# print(kkk.get_frame_rate())
# print(kkk.get_frames())
# print(kkk.get_format())
# print(kkk.get_formats())
# print(kkk.get_live_height())
# print(kkk.get_live_width())
# sss=kkk.get_frame_rate()
# print(1)
# print(kkk.get_live_position())
# print(kkk.get_trigger())
# print(kkk.get_trigger_enable())


# ImageBitsPerPixel