# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tresc.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon

from baza import polaczenie
from dropbox_base import backup


class Ui_H_Form(object):
    def setupUi(self, H_Form):
        self.horizontalLayout = QtWidgets.QHBoxLayout(H_Form)
        self.label = QtWidgets.QLabel(H_Form)
        self.horizontalLayout.addWidget(self.label)
        self.haslo = QtWidgets.QPushButton(H_Form)
        self.horizontalLayout.addWidget(self.haslo)
        self.login = QtWidgets.QPushButton(H_Form)
        self.horizontalLayout.addWidget(self.login)
        self.usun = QtWidgets.QPushButton(H_Form)
        self.horizontalLayout.addWidget(self.usun)

        self.retranslateUi(H_Form)
        QtCore.QMetaObject.connectSlotsByName(H_Form)

        self.usun.clicked.connect(self.usun_konto)
        self.login.clicked.connect(self.zmien_login)
        self.haslo.clicked.connect(self.zmien_haslo)

    def id_uz(self):
        # ID użytkownika
        query = 'SELECT iduzytkownicy FROM uzytkownicy WHERE nazwa_uz IS ("' + str(
            self.label.text()) + '");'
        return polaczenie(query)[0]

    def retranslateUi(self, H_Form):
        _translate = QtCore.QCoreApplication.translate
        self.haslo.setText(_translate("H_Form", "Zmień hasło"))
        self.login.setText(_translate("H_Form", "Zmień login"))
        self.usun.setText(_translate("H_Form", "Usuń użytkownika"))

    def zmien_login(self):
        from PyQt5.QtWidgets import QInputDialog
        self.input_msg = QInputDialog()
        self.input_msg.setWindowIcon(QIcon('icons/cow.png'))
        self.input_msg.setWindowTitle('Zmiana loginu')
        self.input_msg.setLabelText('Wpisz nowy login:')
        self.input_msg.setCancelButtonText('Anuluj')
        id = str(self.id_uz())
        if self.input_msg.exec_():
            login = str(self.input_msg.textValue())
            query = 'UPDATE uzytkownicy SET nazwa_uz = "' + login + '" WHERE iduzytkownicy = ' + id + ';'
            polaczenie(query)
            backup()

    def zmien_haslo(self):
        from PyQt5.QtWidgets import QInputDialog
        from PyQt5.QtWidgets import QLineEdit
        self.input_msgh = QInputDialog()
        self.input_msgh.setWindowIcon(QIcon('icons/cow.png'))
        self.input_msgh.setWindowTitle('Zmiana hasła')
        self.input_msgh.setLabelText('Wpisz nowe hasło:')
        self.input_msgh.setCancelButtonText('Anuluj')
        self.input_msgh.setTextEchoMode(QLineEdit.Password)
        id = str(self.id_uz())
        if self.input_msgh.exec_():
            haslo = str(self.input_msgh.textValue())
            query = 'UPDATE uzytkownicy SET haslo_uz = "' + haslo + '" WHERE iduzytkownicy = ' + id + ';'
            polaczenie(query)
            backup()

    def usun_konto(self):
        from PyQt5.QtWidgets import QMessageBox
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setWindowIcon(QIcon('icons/cow.png'))
        self.msg.setText('Czy na pewno chcesz usunąć konto?')
        self.msg.setWindowTitle('Usuwanie konta')
        self.msg.addButton('Tak', QMessageBox.YesRole)
        self.msg.addButton('Nie', QMessageBox.NoRole)
        msg = self.msg.exec_()
        id = self.id_uz()

        if not msg:
            query = 'DELETE FROM "uzytkownicy" WHERE "iduzytkownicy" IS ("' + str(
                id) + '");'
            polaczenie(query)
            self.horizontalLayout.removeWidget(self.label)
            self.label.hide()
            self.horizontalLayout.removeWidget(self.haslo)
            self.haslo.hide()
            self.horizontalLayout.removeWidget(self.login)
            self.login.hide()
            self.horizontalLayout.removeWidget(self.usun)
            self.usun.hide()
            backup()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    H_Form = QtWidgets.QWidget()
    ui = Ui_H_Form()
    ui.setupUi(H_Form)
    H_Form.show()
    sys.exit(app.exec_())
