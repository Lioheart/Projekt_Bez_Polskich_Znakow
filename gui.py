# -*- coding: utf-8 -*-
# LOGOWANIE
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, pyqtSlot, QRegExp
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QPushButton, \
    QHBoxLayout, QVBoxLayout, QLineEdit, QGroupBox, QDialog, QFormLayout, \
    QLabel, QMainWindow, QAction, QInputDialog, QMessageBox, QFileDialog, \
    QWidget, QComboBox, QTableView, QAbstractItemView

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


class Wyswietl(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.proxy = QSortFilterProxyModel(self)
        self.edit_wysz = QLineEdit(self)
        self.combo_typ = QComboBox(self)
        self.lbl_wysz = QLabel("Wyszukaj")
        self.lbl_typ = QLabel("Wybierz typ narzędzia:")
        self.table = QTableView(self)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('poo.db')
        if db.open():
            print('Otworzono bazę danych')
        self.model = QSqlTableModel(self, db)

        self.formularz = QGroupBox("Wyświetl narzędzia")
        self.initUI()

    def initUI(self):
        typy_narzedzi = [
            'Brak',
            'Frez palcowy',
            'Frez płytkowy (głowica)',
            'Gwintownik',
            'Nóż tokarski',
            # 'Oprawka',
            'Piła',
            'Pozostałe',
            'Rozwiertak',
            'Wiertło',
            'Wiertło składane',
            'Wygniatak'
        ]
        self.widok()
        self.combo_typ.addItems(typy_narzedzi)

        cancel_button = QPushButton("Cofnij")
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(cancel_button)

        l_h = QHBoxLayout()
        l_h.addWidget(self.lbl_typ)
        l_h.addWidget(self.combo_typ)

        l_h2 = QHBoxLayout()
        l_h2.addWidget(self.lbl_wysz)
        l_h2.addWidget(self.edit_wysz)

        layout_v = QVBoxLayout()
        layout_v.addLayout(l_h)
        layout_v.addLayout(l_h2)
        layout_v.addWidget(self.table)

        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)

        main_layout = QVBoxLayout()
        self.formularz.setLayout(layout_v)
        main_layout.addWidget(self.formularz)
        main_layout.addLayout(hbox)
        self.setLayout(main_layout)

        cancel_button.clicked.connect(self.anulowanie)
        self.edit_wysz.textChanged.connect(self.wyszukiwanie)
        self.combo_typ.activated[str].connect(self.onActiveNarz)

    def onActiveNarz(self, tekst):
        slownik = {
            'Frez palcowy': 'frezy_palcowe',
            'Frez płytkowy (głowica)': 'frezy_plytkowe',
            'Gwintownik': 'gwintowniki',
            'Nóż tokarski': 'noze_tokarskie',
            'Oprawka': 'oprawki',
            'Piła': 'pily',
            'Pozostałe': 'pozostale',
            'Rozwiertak': 'rozwiertaki',
            'Wiertło': 'wiertla',
            'Wiertło składane': 'wiertla_skladane',
            'Wygniatak': 'wygniataki',
            'Brak': ''
        }
        naglowki = {
            'idfrezy_palcowe': 'ID',
            'symbol_freza': 'Symbol',
            'producent_fr': 'Producent',
            'srednica_fr': 'Średnica',
            'dl_fr': 'Długość całkowita',
            'dl_rob_fr': 'Długość robocza',
            'idfrezy_plytkowe': 'ID',
            'symbol_frez_pl': 'Symbol',
            'producent_fp': 'Producent',
            'srednica_fr_pl': 'Średnica',
            'ilosc_plytek': 'Ilość płytek',
            'symbol_pl': 'Symbol płytek',
            'ilosc_krawedzi_pl': 'Ilość krawędzi płytki',
            'idgwintowniki': 'ID',
            'symbol_g': 'Symbol',
            'producent_gw': 'Producent',
            'rozmiar_gwintu': 'Rozmiar gwintu i skok',
            'typ_gwintownika': 'Typ gwintownika',
            'idnoze_tokarskie': 'ID',
            'symbol_n': 'Symbol',
            'producent_n': 'Producent',
            'plytki_n': 'Symbol płytek',
            'ilosc_krawedzi_pl_n': 'Ilość krawędzi',
            'idpily': 'ID',
            'symbol_p': 'Symbol',
            'producent_pil': 'Producent',
            'srednica_p': 'Średnica',
            'grubosc_p': 'Grubość',
            'rodzaj_pl_p': 'Symbol płytek',
            'ilosc_pl_p': 'Ilość płytek',
            'ilosc_kraw_p': 'Ilość krawędzi płytki',
            'idpozostale': 'ID',
            'symbol_poz': 'Symbol',
            'producent_poz': 'Producent',
            'srednica_poz': 'Średnica',
            'ilosc_pl_poz': 'Ilość płytek',
            'plytki_poz': 'Symbol płytek',
            'idrozwiertaki': 'ID',
            'symbol_r': 'Symbol',
            'producent_roz': 'Producent',
            'rozmiar_r': 'Rozmiar',
            'idwiertla': 'ID',
            'symbol_w': 'Symbol',
            'producent_w': 'Producent',
            'srednica_w': 'Średnica',
            'dlugosc_w': 'Długość [mm]',
            'idwiertla_skladane': 'ID',
            'symbol_w_skl': 'Symbol',
            'producent_ws': 'Producent',
            'srednica_w_skl': 'Średnica',
            'plytki_w_skl': 'Symbol płytek',
            'idwygniataki': 'ID',
            'symbol_wyg': 'Symbol',
            'producent_wyg': 'Producent',
            'rozmiar_gw': 'Rozmiar gwintu'
        }
        self.model.setTable(slownik[tekst])
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()

        # Ustawianie nagłówków
        ilosc_kolumn = self.model.columnCount()
        for i in range(ilosc_kolumn):
            nazwa_kolumn = self.model.headerData(i, Qt.Horizontal)
            self.model.setHeaderData(i, Qt.Horizontal, naglowki[nazwa_kolumn])

    @pyqtSlot(str)
    def wyszukiwanie(self, text):
        search = QRegExp(text,
                         Qt.CaseInsensitive,
                         QRegExp.RegExp
                         )
        self.proxy.setFilterRegExp(search)
        # Odpowiedzialne za kolumnę, po której filtruje
        self.proxy.setFilterKeyColumn(-1)

    def widok(self):
        # Ustawianie własciwości widoku
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setModel(self.model)

    def anulowanie(self):
        self.parent.statusBar().clearMessage()
        from opcje_qt import Wewnatrz
        menu_gl = Wewnatrz(self.parent)
        self.parent.setCentralWidget(menu_gl)


class About(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('O mnie...')


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
        wysw_act1.triggered.connect(self.widget.norma)
        wysw_act2 = QAction('Wyświetl narzędzia pozycji', self)
        # wysw_act2.setShortcut('Ctrl+Q')
        wysw_act2.triggered.connect(self.wyswietl)

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
        opcje_act3.triggered.connect(self.about)

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

    def wyswietl(self):
        wysw = Wyswietl(self)
        self.setCentralWidget(wysw)

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

    def about(self):
        o_mnie = About()
        o_mnie.show()

    # uzytk = Uzytkownik(self)
    # self.setCentralWidget(uzytk)

    def export_norma(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisywanie jako",
            "Normy",
            "Skoroszyt programu Excel (*.xlsx)",
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
            # todo Jeśli rowcont jest -1, wtedy przerwać zapisywanie i
            #  ostrzeżenie
            print(mysel.rowcount)
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
