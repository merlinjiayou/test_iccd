# -*- coding: utf-8 -*-

"""
Module implementing graph_widget.
"""
import pyqtgraph as pg
from pyqtgraph import Qt
import pyqtgraph.opengl as gl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from Ui_graph_widget import Ui_MainWindow
import numpy as np

pg.setConfigOption('background', [115,115,115])
pg.setConfigOption('foreground', [250,250,250])
class graph_widget(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        super(graph_widget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("实时显示")
        self.centralWidget.hide()
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.image_list=[]
        self.abridge_list=[]
        self.imgitem = pg.ImageItem()
        self.last_imageitem=None
        self.vertical_data=np.zeros(100)
        self.horizontal_data = np.zeros(100)
        self.roiline_data=np.zeros(100)
        #添加3D窗口
        self.window_3D = gl.GLViewWidget()
        self.window_3D.setMinimumHeight(100)
        self.window_3D.setBackgroundColor([110,110,110])
        self.verticalLayout_3D.addWidget(self.window_3D)

        #添加图像窗口
        self.image_widget = pg.GraphicsLayoutWidget()
        self.verticalLayout_image.addWidget(self.image_widget)
        self.image_layout = self.image_widget.addLayout(colspan=1)
        self.image_plot = self.image_layout.addPlot(row=1, col=1)
        self.image_plot.addItem(self.imgitem)
        self.image_vb = self.image_plot.vb
        self.image_vb.setAspectLocked(True)
        self.image_mouse_event = pg.SignalProxy(self.image_plot.scene().sigMouseMoved, rateLimit=60, slot=self.view_pixel_value)

        #添加纵向合并
        self.vertical_binning_widget = pg.GraphicsLayoutWidget()
        self.verticalLayout_binning_vertical.addWidget(self.vertical_binning_widget)
        self.layout_vertical_binning = self.vertical_binning_widget.addLayout(colspan=1)
        self.vertical_plot = self.layout_vertical_binning.addPlot(row=2, col=1, colspan=1)
        self.vertical_item=self.vertical_plot.plot()
        self.vertical_vLine = pg.InfiniteLine(angle=90, movable=False)
        self.vertical_hLine = pg.InfiniteLine(angle=0, movable=False)
        self.vertical_plot.addItem(self.vertical_vLine, ignoreBounds=True)
        self.vertical_plot.addItem(self.vertical_hLine, ignoreBounds=True)
        self.vertical_vb=self.vertical_plot.vb
        self.vertical_mouse_move_signal=pg.SignalProxy(self.vertical_plot.scene().sigMouseMoved, rateLimit=60, slot=self.vertical_mouseMoved)

        #添加横向合并
        self.horizontal_binning_widget = pg.GraphicsLayoutWidget()
        self.verticalLayout_binning_horizontal.addWidget(self.horizontal_binning_widget)
        self.layout_horizontal_binning = self.horizontal_binning_widget.addLayout(colspan=1)
        self.horizontal_plot = self.layout_horizontal_binning.addPlot(row=2, col=1, colspan=1)
        self.horizontal_item=self.horizontal_plot.plot()
        self.horizontal_vLine = pg.InfiniteLine(angle=90, movable=False)
        self.horizontal_hLine = pg.InfiniteLine(angle=0, movable=False)
        self.horizontal_plot.addItem(self.horizontal_vLine, ignoreBounds=True)
        self.horizontal_plot.addItem(self.horizontal_hLine, ignoreBounds=True)
        self.horizontal_vb = self.horizontal_plot.vb
        self.horizontal_mouse_move_signal = pg.SignalProxy(self.horizontal_plot.scene().sigMouseMoved, rateLimit=60, slot=self.horizontal_mouseMoved)

        #添加局部线
        self.roiline_widget = pg.GraphicsLayoutWidget()
        self.verticalLayout_roi_line.addWidget(self.roiline_widget)
        self.layout_roiline = self.roiline_widget.addLayout(colspan=1)
        self.roiline_plot = self.layout_roiline.addPlot(row=2, col=1, colspan=1)
        self.roiline_item=self.roiline_plot.plot()
        self.roiline_vLine = pg.InfiniteLine(angle=90, movable=False)
        self.roiline_hLine = pg.InfiniteLine(angle=0, movable=False)
        self.roiline_plot.addItem(self.roiline_vLine, ignoreBounds=True)
        self.roiline_plot.addItem(self.roiline_hLine, ignoreBounds=True)
        self.roiline_vb = self.roiline_plot.vb
        self.roiline_mouse_move_signal = pg.SignalProxy(self.roiline_plot.scene().sigMouseMoved, rateLimit=60, slot=self.roiline_mouseMoved)


        #添加柱状图
        self.hist_widget = pg.GraphicsLayoutWidget()
        self.verticalLayout_hist.addWidget(self.hist_widget)
        self.layout_hist= self.hist_widget.addLayout(colspan=1)
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.imgitem)
        self.hist.vb.setMouseEnabled(y=True, x=True)  # makes user interaction a little easier
        self.layout_hist.addItem(self.hist)


        #添加信息列表
        self.table = pg.TableWidget()
        self.verticalLayout_hist.addWidget(self.table)


        #初始化界面
        self.dockWidget_roi_line.hide()
        self.dockWidget_binning_horizontal.hide()
        self.dockWidget_binning_vertical.hide()
        self.dockWidget_3D.hide()
        self.dockWidget_message.hide()
        self.window_3D.reset_window()
        self.init_ui()

        # 连接坐标轴
        self.vertical_plot.setXLink(self.image_plot)
        self.horizontal_plot.setYLink(self.image_plot)
        # 设置示例
        # self.add_3d_example()


    def init_ui(self):
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,self.dockWidget_3D)
        self.splitDockWidget(self.dockWidget_3D,self.dockWidget_binning_horizontal,QtCore.Qt.Vertical)
        self.splitDockWidget(self.dockWidget_binning_horizontal, self.dockWidget_image, QtCore.Qt.Horizontal)
        self.splitDockWidget(self.dockWidget_image, self.dockWidget_message, QtCore.Qt.Horizontal)
        self.splitDockWidget(self.dockWidget_image, self.dockWidget_binning_vertical, QtCore.Qt.Vertical)
        self.splitDockWidget(self.dockWidget_binning_vertical, self.dockWidget_roi_line, QtCore.Qt.Vertical)


    def vertical_mouseMoved(self,evt):
        """纵向合并控件中，鼠标移动事件"""
        try:
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if self.vertical_plot.sceneBoundingRect().contains(pos):
                mousePoint = self.vertical_vb.mapSceneToView(pos)
                index = int(mousePoint.x())
                if self.vertical_x_arr[0]<index < self.vertical_x_arr[-1]:
                    position=np.where(self.vertical_x_arr>=index)[0][0]
                    self.label_vertical.setText( "X=%.2f,Y=%.2f"% (index, self.vertical_data[position]))
                self.vertical_vLine.setPos(mousePoint.x())
                self.vertical_hLine.setPos(mousePoint.y())
        except:
            pass

    def horizontal_mouseMoved(self,evt):
        """横向合并中鼠标移动时间"""
        try:
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if self.horizontal_plot.sceneBoundingRect().contains(pos):
                mousePoint = self.horizontal_vb.mapSceneToView(pos)
                index = int(mousePoint.y())
                if self.horizontal_x_arr[0]<index < self.horizontal_x_arr[-1]:
                    position=np.where(self.horizontal_x_arr>=index)[0][0]
                    self.label_horizontal.setText( "X=%.2f,Y=%.2f"% (index, self.horizontal_data[position]))
                self.horizontal_vLine.setPos(mousePoint.x())
                self.horizontal_hLine.setPos(mousePoint.y())
        except:
            pass


    def roiline_mouseMoved(self,evt):
        """局部线控件鼠标移动事件"""
        try:
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if self.roiline_plot.sceneBoundingRect().contains(pos):
                mousePoint = self.roiline_vb.mapSceneToView(pos)
                index = int(mousePoint.x())
                if self.roiline_x_arr[0]<=index < self.roiline_x_arr[-1]:
                    position=np.where(self.roiline_x_arr>=index)[0][0]
                    self.label_roiline.setText( "X=%.2f,Y=%.2f"% (index, self.roiline_data[position]))
                self.roiline_vLine.setPos(mousePoint.x())
                self.roiline_hLine.setPos(mousePoint.y())
        except:
            pass

    def add_3d_example(self):
        shape = (100, 100, 70)
        data = pg.gaussianFilter(np.random.normal(size=shape), (4, 4, 4))
        data += pg.gaussianFilter(np.random.normal(size=shape), (15, 15, 15)) * 15
        data = data[:, 50]
        self.add_image_3D(data)
        self.add_image_3D(data*2)
        self.add_image_3D(data*3)
        self.add_image_3D(data*4)



    def add_image_3D(self,data):
        """向3D控件中添加图像"""
        if "ushort" in str(type(data)):
            data = np.array(data, dtype=np.uint16)
        elif 'numpy' in str(type(data)):
            data = data
        elif "long" in str(type(data)):
            data=np.array(data,dtype=np.int32)
        else:
            data = np.array(data, dtype=np.uint8)
        data_3d=data[::4,::4]+data[1:,1:][::4,::4]+data[2:,2:][::4,::4]+data[3:,3:][::4,::4]
        # self.abridge_list.append(data_3d)
        self.image_list.append(data)
        image_count=len(self.window_3D.items)

        levels = (0, 1)
        tex1 = pg.makeRGBA(data_3d, levels=levels)[0]  # yz plane
        ## Create three image items from textures, add to view
        v1 = gl.GLImageItem(tex1)
        v1.translate(0, 0,-image_count*data.shape[0])
        v1.rotate(90, 10, 0, 0)



        self.window_3D.addItem(v1)
        self.set_camera_position(image_count,data.shape[0])
        self.plot_image(data)
        max_position=len(self.window_3D.items)-1
        self.horizontalSlider_3d.setMaximum(max_position)
        self.horizontalSlider_3d.setValue(max_position)
        self.label_3D.setText("图像：%d" % max_position)


    def set_camera_position(self,index,value):
        """更新相机目标位置"""
        self.window_3D.setCameraPosition(pos=(0,index*value,0), distance=value*20)

    def clear_image_3D(self):
        """清除3D控件的图像"""
        for item in self.window_3D.items:
            self.window_3D.removeItem(item)

    def plot_image(self,data):
        """图形控件中更新绘图数据"""
        if data is not None:
            if "ushort" in str(type(data)):
                self.image_data=np.array(data,dtype=np.uint16)
            elif 'numpy' in str(type(data)):
                self.image_data=data
            else:
                self.image_data = np.array(data, dtype=np.uint8)
            self.imgitem.setImage(self.image_data)
        self.on_action_display_message_triggered(self.action_display_message.isChecked())
        if self.action_roi_line.isChecked():
            self.update_roi_line_plot()
        if self.action_roi_rectangle.isChecked():
            self.update_roi_rectangle_plot()
        elif self.action_vertical_binning.isChecked() or self.action_horizontal_binning.isChecked():
            self.plot_spectral()

    def view_pixel_value(self,evt):
        try:
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if self.image_plot.sceneBoundingRect().contains(pos):
                mousePoint = self.image_vb.mapSceneToView(pos)
                index_x = int(mousePoint.x())
                index_y = int(mousePoint.y())
                if index_x > 0 and index_x < self.image_data.shape[1] and index_y > 0 and index_y < self.image_data.shape[0]:
                    self.label_image.setText("X,Y=%.2f,%.2f  Value=%.2f" % (index_x, index_y, self.image_data[index_y, index_x]))
        except:
            pass

    @pyqtSlot(bool)
    def on_action_vertical_binning_triggered(self, checked):
        if checked:
            if self.action_roi_rectangle.isChecked():
                self.update_roi_rectangle_plot()
            else:
                self.plot_spectral()

    @pyqtSlot(bool)
    def on_action_horizontal_binning_triggered(self, checked):
        if checked:
            if self.action_roi_rectangle.isChecked():
                self.update_roi_rectangle_plot()
            else:
                self.plot_spectral()

    @pyqtSlot(bool)
    def on_action_roi_rectangle_triggered(self, checked):
        """新建/删除局部矩形选区"""
        if checked:
            self.dockWidget_binning_vertical.show()
            self.dockWidget_binning_horizontal.show()
            self.roi_rectangle = pg.ROI([round(self.image_data.shape[0]/2), round(self.image_data.shape[1]/2)], [ round(self.image_data.shape[1]/10),round(self.image_data.shape[0]/10)])
            self.roi_rectangle.addScaleHandle([1, 0], [0.5, 0.5])
            self.image_plot.addItem(self.roi_rectangle)
            self.roi_rectangle.setZValue(10)  # make sure ROI is drawn above image
            self.roi_rectangle.sigRegionChanged.connect(self.update_roi_rectangle_plot)
            self.update_roi_rectangle_plot()
        else:
            self.dockWidget_binning_vertical.hide()
            self.dockWidget_binning_horizontal.hide()
            self.image_plot.removeItem(self.roi_rectangle)
            self.plot_spectral()

    def update_roi_rectangle_plot(self):
        """局部矩形纵向横向合并描绘光谱图"""
        try:
            selected = self.roi_rectangle.getArrayRegion(self.image_data, self.imgitem)
            point=self.roi_rectangle.pos()
            rct=self.roi_rectangle.size()
            self.vertical_data=selected.sum(axis=0)
            self.horizontal_data=selected.sum(axis=1)
            self.vertical_x_arr=np.arange(point[0],point[0]+rct[0],1)
            self.horizontal_x_arr=np.arange(point[1],point[1]+rct[1])
            self.vertical_item.setData(self.vertical_x_arr,self.vertical_data)
            self.horizontal_item.setData(self.horizontal_data,self.horizontal_x_arr)
        except:
            pass

    def plot_spectral(self):
        """描绘纵向及横向合并的光谱曲线"""
        self.vertical_data = np.sum(self.image_data, axis=0)
        self.horizontal_data = np.sum(self.image_data, axis=1)
        self.vertical_x_arr=np.arange(self.vertical_data.shape[0])
        self.horizontal_x_arr=np.arange(self.horizontal_data.shape[0])
        self.vertical_item.setData(self.vertical_data)
        self.horizontal_item.setData(self.horizontal_data, np.arange(0, self.horizontal_data.shape[0], 1))



    @pyqtSlot(bool)
    def on_action_roi_line_triggered(self, checked):
        """新建/删除局部线"""
        if checked:
            self.roi_line = pg.LineSegmentROI([[0, 0], [500, 0]], pen='g')
            self.image_plot.addItem(self.roi_line)
            self.roi_line.sigRegionChanged.connect(self.update_roi_line_plot)
            self.update_roi_line_plot()
        else:
            self.image_plot.removeItem(self.roi_line)

    def update_roi_line_plot(self):
        """描绘线区域光谱曲线"""
        try:
            self.roiline_data = self.roi_line.getArrayRegion(self.image_data.transpose(), self.imgitem,order=0)
            self.roiline_x_arr=np.arange(self.roiline_data.shape[0])
            self.roiline_item.setData(self.roiline_data)
        except:
            pass


    @pyqtSlot()
    def on_toolButton_advance_clicked(self):
        current_position=self.horizontalSlider_3d.value()
        if current_position-1 >=self.horizontalSlider_3d.minimum():
            self.horizontalSlider_3d.setValue(current_position-1)
            self.on_horizontalSlider_3d_sliderMoved(current_position-1)

    @pyqtSlot()
    def on_toolButton_next_clicked(self):
        current_position = self.horizontalSlider_3d.value()
        if current_position+1<=self.horizontalSlider_3d.maximum():
            self.horizontalSlider_3d.setValue(current_position + 1)
            self.on_horizontalSlider_3d_sliderMoved(current_position + 1)
    
    @pyqtSlot(int)
    def on_horizontalSlider_3d_sliderMoved(self, position):
        """滑条滑动在3d控件中选择图像"""
        self.label_3D.setText("图像：%d"%position)
        if self.last_imageitem is not None:
            self.last_imageitem.scale(0.5,0.5,1)
        data=self.image_list[position]
        self.plot_image(data)
        self.last_imageitem=self.window_3D.items[position]
        self.last_imageitem.scale(2,2,1)
        self.set_camera_position(position,data.shape[0])


    @pyqtSlot(bool)
    def on_action_display_message_triggered(self, checked):
        """显示图像统计信息"""
        if checked:
            self.max=np.max(self.image_data)
            self.min=np.min(self.image_data)
            self.total=np.sum(self.image_data)
            self.mean=np.average(self.image_data)
            data = np.array([
                ('max',self.max),
                ('min',self.min),
                ('total',self.total),
                ('mean',self.mean),
            ], dtype=[('Column 1', object), ('Column 2', float)])
            self.table.setData(data)

    @pyqtSlot(bool)
    def on_action_binning2x2_triggered(self, checked):
        """转换像素合并模式"""
        if checked:
            x_num, y_num = self.image_data.shape
            x_num = int(x_num / 2)
            y_num = int(y_num / 2)
            self.binnin_data = np.zeros([x_num, y_num])
            for i in range(x_num):
                for j in range(y_num):
                    self.binnin_data[i, j] = self.image_data[2 * i, 2 * j] + self.image_data[2 * i + 1, 2 * j] + self.image_data[2 * i, 2 * j + 1] + self.image_data[2 * i + 1, 2 * j + 1]
            self.oringe_data = self.image_data
            self.plot_image(self.binnin_data)
        else:
            self.plot_image(self.oringe_data)



# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = graph_widget()
#     MainWindow.show()
#     sys.exit(app.exec_())
    

    

    

    



    

