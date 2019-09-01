# -*- coding: utf-8 -*-
import sys

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QPushButton, \
    QHBoxLayout, QVBoxLayout, QLineEdit, QGroupBox, QDialog, QFormLayout, \
    QLabel, QMainWindow, QAction

from baza import polaczenie
from opcje_qt import Wewnatrz
id_user = 0


# centrowanie
def center(self):
    qr = self.frameGeometry()
    cp = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())


class Logowanie(PyQt5.QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        # Edycja podwietlenia
        paleta = self.palette()
        paleta.setColor(QPalette.Highlight, QColor(189, 67, 243))
        self.setPalette(paleta)

        # Dane okna formularza
        self.haslo = PyQt5.QtWidgets.QLineEdit()
        self.haslo.setEchoMode(PyQt5.QtWidgets.QLineEdit.Password)
        self.login = PyQt5.QtWidgets.QLineEdit()
        self.formularz = PyQt5.QtWidgets.QGroupBox("Logowanie")
        self.title = 'Logowanie'
        self.setWhatsThis('Pole logowania')
        self.width = 300
        self.height = 150

        self.initUI()

    def initUI(self):
        self.width = 300
        self.height = 150
        self.setWindowTitle('Logowanie do wykazu narzędzi')
        self.setWindowIcon(QIcon('icons/cow.png'))
        self.resize(self.width, self.height)

        ok_button = PyQt5.QtWidgets.QPushButton("OK")
        cancel_button = PyQt5.QtWidgets.QPushButton("Anuluj")
        # Box odpowiedzialny za OK i Anuluj
        hbox = PyQt5.QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        # layout logowania
        layout = PyQt5.QtWidgets.QFormLayout()
        layout.addRow(PyQt5.QtWidgets.QLabel("Login:"), self.login)
        layout.addRow(PyQt5.QtWidgets.QLabel("Hasło:"), self.haslo)
        self.formularz.setLayout(layout)

        # Do USUNIECIA
        self.login.setText('admin')
        self.haslo.setText('admin')

        center(self)

        # connecty
        ok_button.clicked.connect(self.logowanie)
        cancel_button.clicked.connect(self.reject)

        main_layout = PyQt5.QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.formularz)
        main_layout.addLayout(hbox)
        self.setLayout(main_layout)

        self.show()

    def logowanie(self):
        query = "SELECT iduzytkownicy FROM uzytkownicy WHERE nazwa_uz = '" + str(
            self.login.text()) + "' AND haslo_uz = '" + str(
            self.haslo.text()) + "';"
        global id_user
        id_user = polaczenie(query)
        if id_user:
            print("Logowanie udane")
            self.accept()
        else:
            print("Coś jest nie tak...")


class Window(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.id_user = user
        self.widget = Wewnatrz(self)
        self.title = 'Wykaz narzędzi'
        self.width = 854
        self.height = 480

        # Edycja podwietlenia głównego okna
        paleta = self.palette()
        paleta.setColor(QPalette.Highlight, QColor(189, 67, 243))
        self.setPalette(paleta)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icons/cow.png'))
        self.resize(self.width, self.height)
        center(self)
        self.setCentralWidget(self.widget)  # centrowanie widżetu na pełne okno

        # Wyswietlanie
        # todo zaproponowanie skrótów
        wyswAct1 = PyQt5.QtWidgets.QAction('Wyświetl normy pozycji', self)
        # wyswAct1.setShortcut('Ctrl+Q')
        wyswAct1.triggered.connect(self.close)
        wyswAct2 = PyQt5.QtWidgets.QAction('Wyświetl narzędzia pozycji', self)
        # wyswAct2.setShortcut('Ctrl+Q')
        wyswAct2.triggered.connect(self.close)

        # Wydruk
        wydrAct1 = PyQt5.QtWidgets.QAction('Wydrukuj do pliku', self)
        # wydrAct1.setShortcut('Ctrl+Q')
        wydrAct1.triggered.connect(self.close)
        wydrAct2 = PyQt5.QtWidgets.QAction('Wydrukuj na drukarkę', self)
        # wydrAct2.setShortcut('Ctrl+Q')
        wydrAct2.triggered.connect(self.close)

        # Opcje
        opcjeAct1 = PyQt5.QtWidgets.QAction('Zmiana hasła', self)
        # wydrAct1.setShortcut('Ctrl+Q')
        opcjeAct1.triggered.connect(self.close)
        opcjeAct2 = PyQt5.QtWidgets.QAction('Informacje o autorze', self)
        # opcjeAct2.setShortcut('Ctrl+Q')
        opcjeAct2.triggered.connect(self.close)

        menubar = self.menuBar()
        wyswietlanie = menubar.addMenu('Wyświetl')
        wydrukowanie = menubar.addMenu('Wydrukuj')
        opcje = menubar.addMenu('Opcje')
        wyswietlanie.addAction(wyswAct1)
        wyswietlanie.addAction(wyswAct2)
        wydrukowanie.addAction(wydrAct1)
        wydrukowanie.addAction(wydrAct2)
        opcje.addAction(opcjeAct1)
        opcje.addAction(opcjeAct2)

        self.show()


def aplikacja():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    from PyQt5.QtWidgets import QStyleFactory
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = Logowanie()

    if ex.exec_() == QtWidgets.QDialog.Accepted:
        main_window = Window(id_user)
        # main_window.showMaximized()  # maksymalizuje
        main_window.show()
        sys.exit(app.exec_())
