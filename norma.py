# -*- coding: utf-8 -*-
# NORMY - stoper
from PyQt5.QtCore import QSortFilterProxyModel, pyqtSlot, QRegExp, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel, \
    QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QTableView, QGroupBox, QLabel, QLineEdit, \
    QInputDialog

from baza import multipolaczenie, polaczenie, update_bazy


def lista_norm():
    query = "SELECT nr_detalu FROM detale"
    return multipolaczenie(query)


class Norma(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.naglowki = {
            'iddetale': 'ID',
            'nr_detalu': 'Detal',
            'maszyna': 'Maszyna',
            'nr_operacji': 'Nr operacji',
            'tm': 'Czas Tm [s]',
            'tp': 'Czas Tp [s]',
            'tj': 'Czas Tj [s]',
            'norma': 'Norma [szt.]',
            'uwagi': 'Uwagi',
            'id_uzytkownika': 'Użytkownik'
        }
        self.proxy = QSortFilterProxyModel(self)
        self.parent = parent
        self.formularz = QGroupBox("Normy")
        self.lbl_w = QLabel("Wyszukaj")
        self.edit_w = QLineEdit(self)
        self.table = QTableView(self)
        self.btn_odswiez = QPushButton("Odśwież bazę")
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('poo.db')
        if self.db.open():
            print('Otworzono bazę danych')
        self.model = QSqlRelationalTableModel(self, self.db)
        self.initUI()

    def initUI(self):
        # Zainicjowanie tabeli zawsze przed wszystkim
        self.tabela()


        # Zatwierdzenie
        ok_button = QPushButton("Dodaj")
        cancel_button = QPushButton("Cofnij")
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btn_odswiez)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        # Layouty
        layout_v = QVBoxLayout()
        layout_h = QHBoxLayout()

        # Tabela
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)

        # przyporządkowanie
        layout_h.addWidget(self.lbl_w)
        layout_h.addWidget(self.edit_w)
        layout_v.addLayout(layout_h)
        layout_v.addWidget(self.table)
        self.formularz.setLayout(layout_v)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formularz)
        main_layout.addLayout(hbox)
        self.setLayout(main_layout)

        # Funkcje
        cancel_button.clicked.connect(self.anulowanie)
        ok_button.clicked.connect(self.dodaj)
        self.edit_w.textChanged.connect(self.wyszukiwanie)
        self.btn_odswiez.clicked.connect(self.refresh_db)

    @pyqtSlot(str)
    def wyszukiwanie(self, text):
        search = QRegExp(text,
                         Qt.CaseInsensitive,
                         QRegExp.RegExp
                         )
        self.proxy.setFilterRegExp(search)
        # Odpowiedzialne za kolumnę, po której filtruje
        self.proxy.setFilterKeyColumn(-1)

    @pyqtSlot()
    def uzupelniene(self):
        # y = self.table.currentIndex().column()
        #
        # # Odwrócony słownik nagłówków
        # temp_nagl = {}
        # test = self.model.headerData(y, Qt.Horizontal)
        # for key, value in self.naglowki.items():
        #     temp_nagl.update({value: key})
        # Wyświetlanie aktualnego nagłówka (może okazać się zbędne)
        # print(temp_nagl[test])

        # Pobranie tp, tm z bazy
        query = 'SELECT iddetale, tm, tp FROM detale'
        dane_db = multipolaczenie(query)
        for i in range(len(dane_db)):
            # if dane_db[i][1] and dane_db[i][2]:
            tm = dane_db[i][1]
            tp1 = dane_db[i][2]
            if isinstance(tm, int) and isinstance(tp1, int):
                tw = tm + tp1
            else:
                tw = 0
            tp2 = tw * 0.05
            tj = (tw + tp2) * 1.1
            tjh = tj / 3600

            if tj != 0:
                norma = 8 / tj * 3600
            else:
                norma = 0
            print(round(norma))
            # update bazy
            query = 'UPDATE "detale" SET "tj" = ' + str(
                round(tjh, 5)) + ', "norma" = ' + str(round(
                norma)) + ' WHERE "iddetale" = ' + str(dane_db[i][0])
            update_bazy(query)
            # query = 'UPDATE "detale" SET "norma" = ' + str(round(norma)) +
            # ' WHERE "iddetale" = ' + str(dane_db[i][0]) update_bazy(query)

    @pyqtSlot()
    def refresh_db(self):
        try:
            self.uzupelniene()
        except:
            pass
        # Odświeżenie tabeli
        self.model.select()

    def tabela(self):
        self.model.setTable('detale')
        self.model.setRelation(9, QSqlRelation('uzytkownicy', 'iduzytkownicy',
                                               'nazwa_uz'))
        # Za zmianę w bazie odpowiada OnFieldChange
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)

        # Ustawianie nagłówków
        ilosc_kolumn = self.model.columnCount()
        for i in range(ilosc_kolumn):
            nazwa_kolumn = self.model.headerData(i, Qt.Horizontal)
            self.model.setHeaderData(i, Qt.Horizontal,
                                     self.naglowki[nazwa_kolumn])
        self.model.select()

        # self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()
        self.table.setModel(self.model)

        # self.table.doubleClicked.connect(self.klikniecie)

    def anulowanie(self):
        self.parent.statusBar().clearMessage()
        from opcje_qt import Wewnatrz
        menu_gl = Wewnatrz(self.parent)
        self.parent.setCentralWidget(menu_gl)

    def dodaj(self):
        text, ok = QInputDialog.getText(self, 'Wprowadź pozycje', 'Pozycja:')
        id = self.parent.id_user[0]
        if ok and text:
            query = "INSERT INTO detale(nr_detalu,id_uzytkownika) VALUES ('" + text + "','" + str(
                id) + "');"
            print(query)
            polaczenie(query)
            self.model.select()
        else:
            print("Nie wpisano pozycji")
