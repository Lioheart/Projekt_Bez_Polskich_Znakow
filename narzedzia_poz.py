# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot, QRegExp, Qt, QSortFilterProxyModel
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, \
    QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QTableView, \
    QAbstractItemView, QInputDialog

from baza import multipolaczenie, polaczenie


class NarzPoz(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.combo_typ = QComboBox(self)
        self.lbl_typ = QLabel("Wybierz typ narzędzia")
        self.combo_poz = QComboBox(self)
        self.lbl_poz = QLabel("Wybierz pozycję:")
        self.dod_poz_btn = QPushButton("Dodaj pozycję")
        self.us_poz_btn = QPushButton("Usuń pozycję")
        self.table = QTableView(self)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('poo.db')
        if db.open():
            print('Otworzono bazę danych')
        self.model = QSqlTableModel(self, db)

        self.parent = parent
        self.formularz = QGroupBox("Przypisz narzędzia")
        self.initUI()

    def initUI(self):
        # Nagłówki kolumn
        ls_nagl = []
        for i in self.naglowki():
            ls_nagl.append(i[0])
        lista_pozycji = []
        for i in self.lista_poz():
            if "/" in i[0]:
                lista_pozycji.append(i[0])
        lista_pozycji.sort()
        if len(lista_pozycji) == 0:
            lista_pozycji.append("Brak pozycji")

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
        ok_button = QPushButton("Dodaj narzędzie do pozycji")
        cancel_button = QPushButton("Cofnij")
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        # Layouty
        layout_v = QVBoxLayout()
        l_1 = QHBoxLayout()
        l_2 = QHBoxLayout()
        l_2.addStretch(1)
        layout_h = QHBoxLayout()

        # Funkcje
        self.combo_typ.addItems(typy_narzedzi)
        self.combo_poz.addItems(lista_pozycji)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        # self.combo_poz.model().sort(0) # Sortowanie

        # Przyporzadkowanie
        l_1.addWidget(self.lbl_typ)
        l_1.addWidget(self.combo_typ)
        l_2.addWidget(self.dod_poz_btn)
        l_2.addWidget(self.us_poz_btn)
        layout_h.addWidget(self.lbl_poz)
        layout_h.addWidget(self.combo_poz)
        layout_v.addLayout(layout_h, 1)
        layout_v.addLayout(l_1)
        layout_v.addLayout(l_2)
        layout_v.addWidget(self.table)
        self.formularz.setLayout(layout_v)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formularz)
        main_layout.addLayout(hbox)
        self.setLayout(main_layout)

        # connecty
        # ok_button.clicked.connect(self.dodaj_narz)
        self.dod_poz_btn.clicked.connect(self.dodaj_poz)
        cancel_button.clicked.connect(self.anulowanie)

    def dodaj_poz(self):
        text, ok = QInputDialog.getText(self, 'Wprowadź pozycje', 'Pozycja:', text='885/630')
        if ok and text:
            query = 'CREATE TABLE IF NOT EXISTS "' + text + '" ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "id_narzedzia" ' \
                                                            'INTEGER, "id_oprawki" INTEGER);'
            print(query)
            polaczenie(query)
            self.anulowanie()
            n_p = NarzPoz(self.parent)
            self.parent.setCentralWidget(n_p)
        else:
            print("Nie wpisano pozycji")

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

    def lista_poz(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        return multipolaczenie(query)

    def naglowki(self):
        query = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        return multipolaczenie(query)

    # opcja z wyszukiwaniem
    def widok(self):

        # todo zrobić pętle zależną od ilości kolumn i nazwy kolumny, po czym podmienić nazwy

        # Ustawianie własciwości widoku
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setModel(self.model)
        # self.table.hideColumn(0)

    def anulowanie(self):
        self.parent.statusBar().clearMessage()
        from opcje_qt import Wewnatrz
        menu_gl = Wewnatrz(self.parent)
        self.parent.setCentralWidget(menu_gl)
