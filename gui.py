# -*- coding: utf-8 -*-
# LOGOWANIE
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QPushButton, \
    QHBoxLayout, QVBoxLayout, QLineEdit, QGroupBox, QDialog, QFormLayout, \
    QLabel, QMainWindow, QAction, QInputDialog, QMessageBox, QFileDialog

from baza import polaczenie
from opcje_qt import Wewnatrz
from uzytkownicy import opcje_uzytkownik, dodaj_uzytkownik

id_user = 0


# centrowanie
def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())


class Logowanie(QDialog):

    def __init__(self):
        super().__init__()

        # Edycja podwietlenia
        paleta = self.palette()
        paleta.setColor(QPalette.Highlight, QColor(189, 67, 243))
        self.setPalette(paleta)

        # Dane okna formularza
        self.haslo = QLineEdit()
        self.haslo.setEchoMode(QLineEdit.Password)
        self.login = QLineEdit()
        self.formularz = QGroupBox("Logowanie")
        self.title = 'Logowanie'
        self.setWhatsThis('Pole logowania')
        self.width = 300
        self.height = 150

        self.init_ui()

    def init_ui(self):
        self.width = 300
        self.height = 150
        self.setWindowTitle('Logowanie do wykazu narzędzi')
        self.setWindowIcon(QIcon('icons/cow.png'))
        self.resize(self.width, self.height)

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Anuluj")
        # Box odpowiedzialny za OK i Anuluj
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        # layout logowania
        layout = QFormLayout()
        layout.addRow(QLabel("Login:"), self.login)
        layout.addRow(QLabel("Hasło:"), self.haslo)
        self.formularz.setLayout(layout)

        # Do USUNIECIA
        # self.login.setText('admin')
        # self.haslo.setText('admin')

        center(self)

        # connecty
        ok_button.clicked.connect(self.logowanie)
        cancel_button.clicked.connect(self.reject)

        main_layout = QVBoxLayout()
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
            QMessageBox.information(self, 'Błąd logowania', "Niepoprawne "
                                                            "hasło lub login"
                                                            " \nSpróbuj "
                                                            "ponownie",
                                    QMessageBox.Ok, QMessageBox.Ok)


class Window(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.id_user = user
        self.widget = Wewnatrz(self)
        self.title = 'Wykaz narzędzi'
        self.width = 1440
        self.height = 900

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
        self.setCentralWidget(self.widget)  # centrowanie widżetu na pełneokno

        # Wyswietlanie
        # todo zaproponowanie skrótów
        wysw_act1 = QAction('Wyświetl normy pozycji', self)
        # wysw_act1.setShortcut('Ctrl+Q')
        # wysw_act1.triggered.connect(self.close)
        wysw_act2 = QAction('Wyświetl narzędzia pozycji', self)
        # wysw_act2.setShortcut('Ctrl+Q')
        # wysw_act2.triggered.connect(self.close)

        # Wydruk
        wydr_act1 = QAction('Wydrukuj normy do pliku', self)
        # wydr_act1.setShortcut('Ctrl+Q')
        wydr_act1.triggered.connect(self.export_norma)
        wydr_act2 = QAction('Wydrukuj wykaz narzędzi do pliku', self)
        # wydr_act2.setShortcut('Ctrl+Q')
        # wydr_act2.triggered.connect(self.close)

        # Opcje
        opcje_act1 = QAction('Zmiana hasła', self)
        # wydr_act1.setShortcut('Ctrl+Q')
        opcje_act1.triggered.connect(self.uzytkownik)
        opcje_act2 = QAction('Dodaj użytkownika', self)
        opcje_act2.triggered.connect(self.nowy_uzytkownik)
        opcje_act3 = QAction('Informacje o autorze', self)
        # opcje_act2.setShortcut('Ctrl+Q')
        # opcje_act2.triggered.connect(self.close)

        menubar = self.menuBar()
        wyswietlanie = menubar.addMenu('Wyświetl')
        wydrukowanie = menubar.addMenu('Wydrukuj')
        opcje = menubar.addMenu('Opcje')
        wyswietlanie.addAction(wysw_act1)
        wyswietlanie.addAction(wysw_act2)
        wydrukowanie.addAction(wydr_act1)
        wydrukowanie.addAction(wydr_act2)
        opcje.addAction(opcje_act1)
        if id_user[0] == 1:
            opcje.addAction(opcje_act2)
        opcje.addAction(opcje_act3)

        self.show()

    def nowy_uzytkownik(self):
        text, ok = QInputDialog.getText(self, 'Dodaj użytkownika',
                                        'Wprowadź nowego użytkownika:')
        if ok and text:
            dodaj_uzytkownik(text)

    def uzytkownik(self):
        text, ok = QInputDialog.getText(self, 'Zmiana hasła',
                                        'Wprowadź nowe hasło:',
                                        QLineEdit.Password)
        if ok and text:
            opcje_uzytkownik(text, id_user)

    # uzytk = Uzytkownik(self)
    # self.setCentralWidget(uzytk)

    def export_norma(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisywanie jako",
            "",
            "Skoroszyt programu Excel (*.xlsx);",
            options=options
        )
        if fileName:
            print(fileName)

        from xlsxwriter import Workbook
        workbook = Workbook(fileName)
        worksheet = workbook.add_worksheet()

        import sqlite3
        conn = sqlite3.connect('poo.db')
        cursor = conn.cursor()
        mysel = cursor.execute('SELECT * FROM detale')
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        workbook.close()

        stylizacja(fileName)


def stylizacja(plik):
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.table import Table, TableStyleInfo

    lista = [
        'Detal',
        'Maszyna',
        'Ilość maszyn',
        'Ilość raportowanych sztuk',
        'Numer operacji',
        'Norma',
        'Uwagi'
    ]

    szer = 0.71
    szer_lista = [
        7.14,
        11.86,
        11.29,
        23.43,
        14.14,
        6.29,
        20
    ]
    work = load_workbook(plik)
    worksheet = work[work.sheetnames[0]]
    worksheet.insert_rows(0)
    worksheet.delete_cols(12)
    worksheet.delete_cols(7, 3)
    worksheet.delete_cols(1)

    for h in range(7):
        worksheet.column_dimensions[get_column_letter(h + 1)].width = \
            szer_lista[h] + szer

    for i, col in enumerate(lista):
        worksheet.cell(row=1, column=i + 1).value = col

    # tabela
    rozmiar = 'A1:G' + str(len(worksheet['A']))
    tab = Table(displayName='Table1', ref=rozmiar)
    style = TableStyleInfo(
        name='TableStyleMedium1',
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )
    tab.tableStyleInfo = style
    worksheet.add_table(tab)

    work.save(plik)
    work.close()
    print('Udane')


def aplikacja():
    app = QApplication(sys.argv)
    from PyQt5.QtWidgets import QStyleFactory
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = Logowanie()

    if ex.exec_() == QtWidgets.QDialog.Accepted:
        main_window = Window(id_user)
        # main_window.showMaximized()  # maksymalizuje
        main_window.show()
        sys.exit(app.exec_())
