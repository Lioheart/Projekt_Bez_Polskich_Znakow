# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uzytkownik.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.resize(450, 580)
        Form.setMaximumWidth(500)
        Form.setMinimumWidth(400)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 330, 280))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidget)

        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.verticalLayout.addWidget(self.scrollArea)

        QtCore.QMetaObject.connectSlotsByName(Form)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
