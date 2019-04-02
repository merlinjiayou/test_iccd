# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\ProgramProjects\ICCD1.0\shutter_control.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_shutter_control(object):
    def setupUi(self, shutter_control):
        shutter_control.setObjectName("shutter_control")
        shutter_control.resize(274, 134)
        shutter_control.setMinimumSize(QtCore.QSize(274, 134))
        shutter_control.setMaximumSize(QtCore.QSize(5000, 5000))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/ico_file/1078438.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        shutter_control.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(shutter_control)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(shutter_control)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_auto = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_auto.setChecked(True)
        self.radioButton_auto.setObjectName("radioButton_auto")
        self.verticalLayout.addWidget(self.radioButton_auto)
        self.radioButton_permanently_open = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_permanently_open.setObjectName("radioButton_permanently_open")
        self.verticalLayout.addWidget(self.radioButton_permanently_open)
        self.radioButton_permanently_close = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_permanently_close.setObjectName("radioButton_permanently_close")
        self.verticalLayout.addWidget(self.radioButton_permanently_close)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(shutter_control)
        QtCore.QMetaObject.connectSlotsByName(shutter_control)

    def retranslateUi(self, shutter_control):
        _translate = QtCore.QCoreApplication.translate
        shutter_control.setWindowTitle(_translate("shutter_control", "快门控制"))
        self.groupBox.setTitle(_translate("shutter_control", "内部快门"))
        self.radioButton_auto.setText(_translate("shutter_control", "全自动"))
        self.radioButton_permanently_open.setText(_translate("shutter_control", "完全打开"))
        self.radioButton_permanently_close.setText(_translate("shutter_control", "完全关闭"))

import source_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    shutter_control = QtWidgets.QWidget()
    ui = Ui_shutter_control()
    ui.setupUi(shutter_control)
    shutter_control.show()
    sys.exit(app.exec_())

