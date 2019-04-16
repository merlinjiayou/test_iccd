from PyQt5 import QtWidgets
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import ctypes
pg.setConfigOption('background', [150,150,150])
pg.setConfigOption('foreground', [250,250,250])
class graph_widget(QtGui.QWidget):
    def __init__(self,):
        QtGui.QWidget.__init__(self)
        self.main_layout=QtGui.QGridLayout()
        self.setLayout(self.main_layout)
        self.tool_layout=QtGui.QGridLayout()
        self.main_layout.addLayout(self.tool_layout,0,0)
        self.roi_button=QtGui.QPushButton('ROI_RECT')
        self.roi_button.setCheckable(True)
        self.tool_layout.addWidget(self.roi_button)
        self.roi_button.toggled.connect(self.new_roi)

        self.line_button = QtGui.QPushButton('ROI_LINE')
        self.line_button.setCheckable(True)
        self.tool_layout.addWidget(self.line_button,0,1)
        self.line_button.toggled.connect(self.new_line)

        self.binning_button = QtGui.QPushButton('binning')
        self.binning_button.setCheckable(True)
        self.tool_layout.addWidget(self.binning_button, 0, 2)
        self.binning_button.toggled.connect(self.binning_show)

        self.message_button = QtGui.QPushButton('数据信息')
        self. message_button.setCheckable(True)
        self.tool_layout.addWidget(self.message_button, 0, 3)
        self.message_button.toggled.connect(self.display_message)

        # self.table_button = QtGui.QPushButton('表格显示')
        # self. table_button.setCheckable(True)
        # self.tool_layout.addWidget(self.table_button, 0, 4)
        # self.table_button.toggled.connect(self.display_table)

        self.FVB_button = QtGui.QPushButton('纵向合并')
        self.FVB_button.setCheckable(True)
        self.tool_layout.addWidget(self.FVB_button, 0, 4)
        self.FVB_button.toggled.connect(self.FVB_enable)


        self.FHB_button = QtGui.QPushButton('横向合并')
        self.FHB_button.setCheckable(True)
        self.tool_layout.addWidget(self.FHB_button, 0, 5)
        self.FHB_button.toggled.connect(self.FHB_enable)


        # self.multi_button = QtGui.QPushButton('X10')
        # self.multi_button.setCheckable(True)
        # self.tool_layout.addWidget(self.multi_button, 0, 3)
        # self.multi_button.toggled.connect(self.multi_show)





        self.layout = QtGui.QGridLayout()
        self.main_layout.addLayout(self.layout,1,0)
        self.graphicslw=pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.graphicslw)
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.dll_lib = ctypes.WinDLL("C_find_peaks.dll")
        self.setWindowTitle('实时窗口')

        self.layout2=self.graphicslw.addLayout(colspan=1)
        self.label = pg.LabelItem(justify='right')
        self.layout2.addItem(self.label,row=0, col=2,colspan=3)
        self.p1 = self.layout2.addPlot(row=1, col=1)
        self.img = pg.ImageItem()
        self.p1.addItem(self.img)



        self.vb = self.p1.vb
        self.vb.setAspectLocked(True)
        self.proxy = pg.SignalProxy(self.p1.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img)
        self.layout2.addItem(self.hist, row=1, col=2,rowspan=1)
        self.hist.vb.setMouseEnabled(y=True,x=True) # makes user interaction a little easier
        self.graphicslw.nextRow()
        self.p2 = self.layout2.addPlot(row=2, col=1,colspan=1)
        self.p2.setMaximumHeight(100)
        self.p2_vLine = pg.InfiniteLine(angle=90, movable=False)
        self.p2_hLine = pg.InfiniteLine(angle=0, movable=False)
        self.p2.addItem(self.p2_vLine, ignoreBounds=True)
        self.p2.addItem(self.p2_hLine, ignoreBounds=True)

        self.p2_vb = self.p2.vb



        self.p2_proxy = pg.SignalProxy(self.p2.scene().sigMouseMoved, rateLimit=60, slot=self.p2_mouseMoved)


        # self.data = np.random.normal(size=(1080, 1440))
        self.data=np.zeros([1080,1440])
        self.img.setImage(self.data)

        self.p3=self.layout2.addPlot(row=1,col=0,cospan=0)
        self.p3.setMaximumWidth(100)
        self.p2.hide()
        self.p3.hide()


        self.updatePlot()
        self.p2.setXLink(self.p1)
        self.p3.setYLink(self.p1)
        self.plot_spectral()

    def FVB_enable(self):
        if self.FVB_button.isChecked():
            self.p2.show()
        else:self.p2.hide()


    def FHB_enable(self):
        if self.FHB_button.isChecked():
            self.p3.show()
        else:self.p3.hide()

    def p2_mouseMoved(self,evt):
        try:
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if self.p2.sceneBoundingRect().contains(pos):
                mousePoint = self.p2_vb.mapSceneToView(pos)
                index = int(mousePoint.x())
                if index > 0 and index < len(self.p2_data):
                    self.label.setText(
                        "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (
                            mousePoint.x(), self.p2_data[index], self.p2_data[index]))
                self.p2_vLine.setPos(mousePoint.x())
                self.p2_hLine.setPos(mousePoint.y())
        except:
            pass

    def new_roi(self):
        if self.roi_button.isChecked():
            self.roi = pg.ROI([round(self.data.shape[0]/2), round(self.data.shape[1]/2)], [ round(self.data.shape[1]/10),round(self.data.shape[0]/10)])
            self.roi.addScaleHandle([1, 0], [0.5, 0.5])
            self.p1.addItem(self.roi)
            self.roi.setZValue(10)  # make sure ROI is drawn above image
            self.roi.sigRegionChanged.connect(self.updatePlot)
        else:
            self.p1.removeItem(self.roi)
            self.plot_spectral()

    def new_line(self):
        if self.line_button.isChecked():
            self.roi_line = pg.LineSegmentROI([[0, 0], [500, 0]], pen='g')
            self.p1.addItem(self.roi_line)
            self.roi_line.sigRegionChanged.connect(self.update_time)
        else:
            self.p1.removeItem(self.roi_line)
            self.plot_spectral()


    def display_message(self):
        if self.message_button.isChecked():
            my_sum=0
            self.table = pg.TableWidget()
            self.main_layout.addWidget(self.table,1,1)
            self.max=np.max(self.data)
            self.min=np.min(self.data)
            for i in self.data:
                for j in i:
                    my_sum=my_sum+j
            # self.total=np.sum(self.data)
            print(my_sum)
            self.total=np.float(my_sum)
            self.mean=np.average(self.data)
            # print(self.mean)
            # print(np.average([1,2,3,4,5,6]))
            # print(np.sum([1,2,3,4,5,6]))
            data = np.array([
                ('max',self.max),
                ('min',self.min),
                ('total',self.total),
                ('mean',self.mean),
            ], dtype=[('Column 1', object), ('Column 2', float)])
            self.table.setData(data)
            self.table.show()
        else:
            self.table.hide()

    def display_table(self):
        if self.table_button.isChecked():
            data={"data":self.data}
            self.table_view = pg.DataTreeWidget(data=data)
            self.main_layout.addWidget(self.table_view,1,2)
            self.table_view.show()
        else:
            self.table_view.hide()



    def multi_show(self):
        if self.multi_button.isChecked():
            self.data=self.data*10
            self.plot(self.data)
        else:
            self.data = self.data/10
            self.plot(self.data)

    def binning_show(self):
        x_num,y_num=self.data.shape
        x_num=int(x_num/2)
        y_num=int(y_num/2)
        self.binnin_data=np.zeros([x_num,y_num])
        for i in range(x_num-1):
            for j in range(y_num-1):
                self.binnin_data[i,j]=self.data[2*i,2*j]+self.data[2*i+1,2*j]+self.data[2*i,2*j+1]+self.data[2*i+1,2*j+1]
        if self.binning_button.isChecked():
            self.oringe_data=self.data
            self.plot(self.binnin_data)
        else:
            self.plot(self.oringe_data)

    def plot_spectral(self):
        spectral_x=np.sum(self.data,axis=0)
        spectral_y=np.sum(self.data,axis=1)
        self.p2_data=spectral_x
        self.p3_data=spectral_y
        self.p2.plot(spectral_x, clear=True)
        self.p3.plot(spectral_y,np.arange(0,spectral_y.shape[0],1), clear=True)


    def update_time(self):
        try:
            d3 = np.round(self.roi_line.getArrayRegion(self.data.transpose(), self.img,order=0))
            self.p2_data=d3
            self.p2.plot(d3,clear=True)
        except:
            pass

    def plot(self,data=None):
        if data is not None:
            if "ushort" in str(type(data)):
                self.data=np.array(data,dtype=np.uint16)
            elif 'numpy' in str(type(data)):
                self.data=data
            else:
                self.data = np.array(data, dtype=np.uint8)
            self.img.setImage(self.data)
            self.plot_spectral()



    def build_isocurves(self):
        # build isocurves from smoothed data
        self.iso.setData(pg.gaussianFilter(self.data, (2, 2)))

    def updateIsocurve(self):
        # global isoLine, iso
        self.iso.setLevel(self.isoLine.value())

    def updatePlot(self):
        # global img, roi, data, p2
        try:
            selected = self.roi.getArrayRegion(self.data, self.img)
            point=self.roi.pos()
            rct=self.roi.size()
            self.p2_data=selected.sum(axis=0)
            self.p3_data=selected.sum(axis=1)
            self.p2.plot(np.arange(point[0],point[0]+rct[0],1),self.p2_data, clear=True)
            self.p3.plot(selected.sum(axis=1),np.arange(point[1],point[1]+rct[1],1) ,clear=True)
            # self.p2.plot(selected.mean(axis=0), clear=True)
        except:
            pass



    def mouseMoved(self,evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.p1.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index_x = int(mousePoint.x())
            index_y = int(mousePoint.y())
            if index_x > 0 and index_x < self.data.shape[1] and index_y>0 and index_y<self.data.shape[0]:
                self.label.setText("<span style='font-size: 12pt'>X,Y=%d,%d</span>, <span style='font-size: 12pt'>Value=%d</span>" % (index_x, index_y, self.data[index_y,index_x]))



