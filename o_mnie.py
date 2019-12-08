# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Ui_O_mnie(object):
    def setupUi(self, O_mnie):
        O_mnie.setObjectName("O_mnie")
        O_mnie.resize(527, 320)
        O_mnie.setFixedSize(527, 320)
        palette = QtGui.QPalette()

        grad = QtGui.QLinearGradient(0, 320, 527, 320)
        grad.setColorAt(0.0, QtGui.QColor(186, 171, 186))
        grad.setColorAt(1.0, QtGui.QColor(236, 233, 230))
        brush = QtGui.QBrush(grad)
        # brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

        brush = QtGui.QBrush(grad)
        # brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText,
                         brush)

        O_mnie.setPalette(palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/cow.ico"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        O_mnie.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(O_mnie)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.ikona = QtWidgets.QLabel(self.centralwidget)
        self.ikona.setEnabled(True)
        self.ikona.setSizeIncrement(QtCore.QSize(64, 0))
        self.ikona.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ikona.setPixmap(QtGui.QPixmap("icons/cow.ico"))
        self.ikona.setObjectName("ikona")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                  self.ikona)
        self.PBPZ = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.PBPZ.setFont(font)
        self.PBPZ.setObjectName("PBPZ")
        self.gridLayoutWidget = QtWidgets.QWidget(self.PBPZ)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 19, 231, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.qt_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.qt_2.setAlignment(QtCore.Qt.AlignCenter)
        self.qt_2.setObjectName("qt_2")
        self.gridLayout_3.addWidget(self.qt_2, 2, 1, 1, 1)
        self.wersja_opr_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.wersja_opr_2.setObjectName("wersja_opr_2")
        self.gridLayout_3.addWidget(self.wersja_opr_2, 1, 0, 1, 1)
        self.wersja_qt_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.wersja_qt_2.setObjectName("wersja_qt_2")
        self.gridLayout_3.addWidget(self.wersja_qt_2, 2, 0, 1, 1)
        self.wykaz_narz = QtWidgets.QLabel(self.gridLayoutWidget)
        self.wykaz_narz.setAlignment(QtCore.Qt.AlignCenter)
        self.wykaz_narz.setObjectName("wykaz_narz")
        self.gridLayout_3.addWidget(self.wykaz_narz, 0, 0, 1, 2)
        self.opr_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.opr_2.setAlignment(QtCore.Qt.AlignCenter)
        self.opr_2.setObjectName("opr_2")
        self.gridLayout_3.addWidget(self.opr_2, 1, 1, 1, 1)
        self.wersja_pyt_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.wersja_pyt_2.setObjectName("wersja_pyt_2")
        self.gridLayout_3.addWidget(self.wersja_pyt_2, 3, 0, 1, 1)
        self.pyt_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.pyt_2.setAlignment(QtCore.Qt.AlignCenter)
        self.pyt_2.setObjectName("pyt_2")
        self.gridLayout_3.addWidget(self.pyt_2, 3, 1, 1, 1)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole,
                                  self.PBPZ)
        self.stopka = QtWidgets.QLabel(self.centralwidget)
        self.stopka.setObjectName("stopka")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole,
                                  self.stopka)
        self.line = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole,
                                  self.line)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        O_mnie.setCentralWidget(self.centralwidget)

        self.retranslateUi(O_mnie)
        QtCore.QMetaObject.connectSlotsByName(O_mnie)

    def retranslateUi(self, O_mnie):
        from platform import python_version
        from PyQt5.Qt import PYQT_VERSION_STR
        try:
            from setuptools_scm import get_version
            version = get_version(root='.', relative_to=__file__)
            version = '.'.join(version.split('.')[:3])
            import os
            if os.path.exists('version'):
                os.remove('version/__init__.py')
            else:
                os.mkdir('version')
            file = open('version\__init__.py', 'w', -1, 'utf-8')
            file.write('__version__ = "{}"'.format(version))
            file.close()
            wersja = version
        except:
            print('Brak .git')
            # plus dwie linie poniżej
            import version
            wersja = version.__version__
        _translate = QtCore.QCoreApplication.translate
        O_mnie.setWindowTitle(_translate("O_mnie", "O mnie..."))
        url_link = '''<a style=" color: black;
            text-align: center;
            font-style: italic;
            text-decoration: none;
            display: inline-block;"
            href=\'https://github.com/Lioheart/Projekt_Bez_Polskich_Znakow\'>Informacje o wydaniu</a> '''
        self.stopka.setOpenExternalLinks(True)
        self.PBPZ.setTitle(_translate("O_mnie", "Program Bez Polskich Znaków".upper()))
        self.qt_2.setText(_translate("O_mnie", PYQT_VERSION_STR.upper()))
        self.wersja_opr_2.setText(
            _translate("O_mnie", "Wersja oprogramowania:"))
        self.wersja_qt_2.setText(_translate("O_mnie", "Wersja QT:"))
        self.wykaz_narz.setText(
            _translate("O_mnie", "Wykaz Narzędzi\nAutor: Jakub Hawro"))
        self.opr_2.setText(_translate("O_mnie", wersja.upper()))
        self.wersja_pyt_2.setText(_translate("O_mnie", "Wersja Python:"))
        self.pyt_2.setText(_translate("O_mnie", python_version().upper()))
        self.stopka.setText(_translate("O_mnie", url_link.upper()))

        self.wersja_qt_2.setFlat(True)
        self.wersja_qt_2.setStyleSheet("QPushButton { text-align: left; }")
        self.wersja_qt_2.clicked.connect(self.o_qt)

    def o_qt(self):
        QMessageBox.aboutQt(None)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    O_mnie = QtWidgets.QMainWindow()
    ui = Ui_O_mnie()
    ui.setupUi(O_mnie)
    O_mnie.show()
    sys.exit(app.exec_())
