# -*- coding: utf-8 -*-
# SPIS POMOCY - przypisz narzędzia do pozycji
from PyQt5.QtCore import pyqtSlot, QRegExp, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, \
    QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QTableView, \
    QAbstractItemView, QInputDialog, QMenu, QAction, QMessageBox

from baza import multipolaczenie, polaczenie


class NarzPoz(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy_poz = QSortFilterProxyModel(self)
        self.edit_wysz = QLineEdit(self)
        self.combo_typ = QComboBox(self)
        self.lbl_wysz = QLabel("Wyszukaj")
        self.lbl_typ = QLabel("Wybierz typ narzędzia")
        self.combo_poz = QComboBox(self)
        self.lbl_poz = QLabel("Wybierz pozycję:")
        self.listaPozycji = []
        self.table = QTableView(self)
        self.table_narz = QTableView(self)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('poo.db')
        if db.open():
            print('Otworzono bazę danych')
        self.model = QSqlTableModel(self, db)
        self.model_poz = QSqlTableModel(self, db)

        self.parent = parent
        self.formularz = QGroupBox("Przypisz narzędzia")
        self.initUI()

    def initUI(self):
        self.naglowki_kolumn()

        # todo dodać okno z wyborem oprawki po wyborze narzędzia
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
        # Zatwierdzenie
        ok_button = QPushButton("Dodaj do pozycji")
        cancel_button = QPushButton("Cofnij")
        wydrukuj_btn = QPushButton("Wydrukuj")
        usun_btn = QPushButton("Usuń pozycję")
        dodaj_btn = QPushButton("Dodaj pozycję")
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        # Layouty
        layout_v = QVBoxLayout()
        l_1 = QHBoxLayout()
        l_2 = QHBoxLayout()
        l_3 = QHBoxLayout()
        layout_h = QHBoxLayout()

        # Funkcje
        self.combo_typ.addItems(typy_narzedzi)
        self.combo_poz.addItems(self.listaPozycji)
        self.proxy_poz.setSourceModel(self.model_poz)
        self.table.setModel(self.proxy_poz)
        self.proxy.setSourceModel(self.model)
        self.table_narz.setModel(self.proxy)

        # Przyporzadkowanie
        l_1.addWidget(self.lbl_typ)
        l_1.addWidget(self.combo_typ)
        l_2.addWidget(self.lbl_wysz)
        l_2.addWidget(self.edit_wysz)
        l_3.addWidget(wydrukuj_btn)
        l_3.addWidget(usun_btn)
        l_3.addWidget(dodaj_btn)
        layout_h.addWidget(self.lbl_poz)
        layout_h.addWidget(self.combo_poz)
        layout_v.addLayout(layout_h, 1)
        layout_v.addLayout(l_1)
        layout_v.addLayout(l_2)
        layout_v.addLayout(l_3)
        layout_v.addWidget(self.table)
        layout_v.addWidget(self.table_narz)
        self.formularz.setLayout(layout_v)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formularz)
        main_layout.addLayout(hbox)
        self.setLayout(main_layout)

        # connecty
        # ok_button.clicked.connect(self.dodaj)
        cancel_button.clicked.connect(self.anulowanie)
        dodaj_btn.clicked.connect(self.dodaj_poz)
        ok_button.clicked.connect(self.klikniecie)
        usun_btn.clicked.connect(self.usun_pozycje)
        self.edit_wysz.textChanged.connect(self.wyszukiwanie)
        self.combo_typ.activated[str].connect(self.onActiveNarz)
        self.combo_poz.activated[str].connect(self.onActivePoz)
        # Menu kontekstowe własne
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.prawoklik)

    def naglowki_kolumn(self):
        # Nagłówki kolumn
        self.listaPozycji.append('Brak')
        for i in self.naglowki():
            if "/" in i[0]:
                self.listaPozycji.append(i[0])

    def usun_pozycje(self):

        text, ok = QInputDialog.getItem(self, 'Usuń pozycje',
                                        'Wybierz pozycję do usunięcia',
                                        self.listaPozycji[1:])
        if ok:
            if text != 'Brak':
                print(text)
                query = 'DROP TABLE "main"."' + text + '";'
                polaczenie(query)
                self.listaPozycji.clear()
                self.naglowki_kolumn()
                indeks = self.combo_poz.findText(text)
                self.combo_poz.removeItem(indeks)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowIcon(QIcon('icons/cow.png'))
                msg.setText("Wybierz poprawną pozycję")
                msg.setWindowTitle("Niewłaściwa pozycja")
                msg.exec_()
                self.usun_pozycje()

    def prawoklik(self):
        menu = QMenu(self)
        akcja = QAction('Usuń narzędzie', self)
        akcja.triggered.connect(self.usun_wiersz)
        menu.addAction(akcja)
        menu.exec_(QCursor.pos())

    def usun_wiersz(self):
        selected = self.table.currentIndex()
        self.model_poz.removeRow(selected.row())
        self.model_poz.submitAll()
        self.model_poz.select()

    def dodaj_poz(self):
        text, ok = QInputDialog.getText(self, 'Wprowadź pozycje', 'Pozycja:')
        if ok and text:
            query = 'CREATE TABLE "' + text + '" ("id_poz" INTEGER PRIMARY ' \
                                              'KEY AUTOINCREMENT, ' \
                                              '"symbol_narz"	TEXT, ' \
                                              '"vc" INTEGER,	"obroty" ' \
                                              'INTEGER, "fz" REAL, "posuw" ' \
                                              'INTEGER); '
            print(query)
            polaczenie(query)
            self.listaPozycji.clear()
            self.combo_poz.addItem(text)
            self.naglowki_kolumn()
        else:
            print("Nie wpisano pozycji")

    def onActivePoz(self, tekst):
        naglowki = {
            'id_poz': 'ID',
            'symbol_narz': 'Symbol narzędzia',
            'vc': 'Prędkość skrawania Vc [m/min]',
            'obroty': 'Obroty [obr/min]',
            'fz': 'Posuw na ząb [mm/ostrze]',
            'posuw': 'Posuw liniowy [mm/min]'
        }
        self.model_poz.setTable(tekst)
        self.model_poz.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_poz.select()

        # Ustawianie nagłówków
        ilosc_kolumn = self.model_poz.columnCount()
        for i in range(ilosc_kolumn):
            nazwa_kolumn = self.model_poz.headerData(i, Qt.Horizontal)
            self.model_poz.setHeaderData(i, Qt.Horizontal,
                                         naglowki[nazwa_kolumn])

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

    def naglowki(self):
        query = "SELECT name FROM sqlite_master WHERE type ='table' AND name " \
                "NOT LIKE 'sqlite_%'; "
        return multipolaczenie(query)

    @pyqtSlot(str)
    def wyszukiwanie(self, text):
        search = QRegExp(text,
                         Qt.CaseInsensitive,
                         QRegExp.RegExp
                         )
        self.proxy.setFilterRegExp(search)
        # Odpowiedzialne za kolumnę, po której filtruje
        self.proxy.setFilterKeyColumn(-1)

    # opcja z wyszukiwaniem
    def widok(self):
        # Ustawianie własciwości widoku
        self.table_narz.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_narz.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_narz.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_narz.verticalHeader().setVisible(False)
        self.table_narz.setSortingEnabled(True)
        self.table_narz.setModel(self.model)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setModel(self.model_poz)
        # self.table.hideColumn(0)
        self.table_narz.doubleClicked.connect(self.klikniecie)

    @pyqtSlot()
    def klikniecie(self):
        x = self.table_narz.currentIndex().row()
        y = self.table_narz.currentIndex().column()
        nazwa = self.table_narz.currentIndex().sibling(x, 1).data()
        print(nazwa)

        # Dodanie narzędzia do pozycji
        if nazwa:
            print(nazwa)
            query = "INSERT INTO '" + self.model_poz.tableName() + "'(symbol_narz) VALUES ('" + nazwa + "') "
            polaczenie(query)
            # Odświeża tabelę
            self.model_poz.select()
        else:
            print(self.model_poz.tableName())
            print("Brak wybranego narzędzia")

    def anulowanie(self):
        self.parent.statusBar().clearMessage()
        from opcje_qt import Wewnatrz
        menu_gl = Wewnatrz(self.parent)
        self.parent.setCentralWidget(menu_gl)
