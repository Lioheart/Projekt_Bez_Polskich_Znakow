# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFormLayout, \
    QGroupBox, QVBoxLayout, QLabel, QLineEdit, QMessageBox

from baza import polaczenie


class Pozycja(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.pozycja_edit = QLineEdit()
        self.pozycja_lbl = QLabel("Dodaj pozycję:")
        self.layout = QFormLayout()
        self.formularz = QGroupBox("Dodaj nową pozycję")
        self.initUI()

    def initUI(self):
        # Zatwierdzenie
        ok_button = QPushButton("Dodaj")
        cancel_button = QPushButton("Cofnij")
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        layout_h = QHBoxLayout()
        layout_h.addWidget(self.pozycja_lbl)
        layout_h.addWidget(self.pozycja_edit)

        self.formularz.setLayout(layout_h)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formularz)
        main_layout.addLayout(hbox)
        self.setLayout(main_layout)

        # connecty
        ok_button.clicked.connect(self.dodaj)
        cancel_button.clicked.connect(self.anulowanie)

    def anulowanie(self):
        self.parent.statusBar().clearMessage()
        from opcje_qt import Wewnatrz
        menu_gl = Wewnatrz(self.parent, id_user)
        self.parent.setCentralWidget(menu_gl)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.dodaj()

    def dodaj(self):
        query = 'INSERT INTO detale(nr_detalu) VALUES("' + self.pozycja_edit.text() + '")'
        q_spr = 'SELECT iddetale FROM detale WHERE nr_detalu="' + self.pozycja_edit.text() + '"'
        if polaczenie(q_spr) and self.pozycja_edit.text() != "":
            QMessageBox.warning(self, "Dana pozycja znajduje się bazie",
                                "Pozycja, którą chcesz dodać, znajduje się już w bazie",
                                QMessageBox.Ok)
        elif self.pozycja_edit.text() == "":
            QMessageBox.critical(self, "Brak detalu",
                                 "Nie można dodać pustego detalu",
                                 QMessageBox.Ok)
        else:
            polaczenie(query)
            self.pozycja_edit.clear()
            self.parent.statusBar().showMessage("Dodano pozycję", 10000)
