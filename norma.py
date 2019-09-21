# -*- coding: utf-8 -*-
# NORMY - stoper
from PyQt5.QtCore import QSortFilterProxyModel, pyqtSlot, QRegExp, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel, \
    QSqlRelation
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QTableView, QGroupBox, QLabel, QLineEdit, \
    QInputDialog, QShortcut, QComboBox, QItemDelegate, QAbstractItemView

from baza import multipolaczenie, polaczenie, update_bazy


def lista_norm():
    query = "SELECT nr_detalu FROM detale"
    return multipolaczenie(query)


class ComboDelegate(QItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied

    source: https://gist.github.com/Riateche/5984815
    """

    def __init__(self, parent, items):
        self.items = items
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        li = []
        for item in self.items:
            li.append(item)
        combo.addItems(li)
        combo.currentIndexChanged.connect(self.currentIndexChanged)
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        text = index.model().data(index, Qt.DisplayRole)
        try:
            i = self.items.index(text)
        except ValueError:
            i = 0
        editor.setCurrentIndex(i)
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())



class Norma(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.skrot = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.naglowki = {
            'iddetale': 'ID',
            'nr_detalu': 'Detal',
            'maszyna': 'Maszyna',
            "ilosc_m": 'Ilość maszyn',
            'ilosc_szt': 'Ilość raportowanych sztuk',
            'nr_operacji': 'Nr operacji',
            'tm': 'Czas Tm [s]',
            'tp': 'Czas Tp [s]',
            'tj': 'Czas Tj [h]',
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

        # lista wybieralna
        masz = ['Frezarka AXA',
                'Frezarka Hi-V410D',
                'Frezarka manualna FWA41M',
                'Frezarka MAZAK HCN-5000-III',
                'Frezarka MAZAK VTC-200B-II',
                'Frezarka pozioma manulana',
                'Frezarka TBI',
                'Gwinciarka HCP',
                'Malowanie',
                'Tokarka CTX',
                'Tokarka Multiplex',
                'Tokarka SKT',
                'Tokarka TZC',
                'Wiertarka wieloosiowa'
                ]
        operacje = ['Fazowanie',
                    'I i II operacja',
                    'I operacja',
                    'II operacja',
                    'III operacja',
                    'Konserwacja',
                    'Na gotowo',
                    'Szyjka',
                    'Toczenie',
                    'Wiercenie'
                    ]
        self.table.setItemDelegateForColumn(2, ComboDelegate(self, masz))
        self.table.setItemDelegateForColumn(5, ComboDelegate(self, operacje))
        for row in range(0, self.model.rowCount()):
            self.table.openPersistentEditor(self.model.index(row, 2))
            self.table.openPersistentEditor(self.model.index(row, 5))

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

        # export
        # self.export()
        # Funkcje
        cancel_button.clicked.connect(self.anulowanie)
        ok_button.clicked.connect(self.dodaj)
        self.edit_w.textChanged.connect(self.wyszukiwanie)
        self.btn_odswiez.clicked.connect(self.refresh_db)
        self.skrot.activated.connect(self.refresh_db)

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
        query = 'SELECT iddetale, tm, tp, ilosc_m, ilosc_szt FROM detale'
        dane_db = multipolaczenie(query)
        for i in range(len(dane_db)):
            # if dane_db[i][1] and dane_db[i][2]:
            tm = dane_db[i][1]
            tp1 = dane_db[i][2]
            ilosc_m = dane_db[i][3]
            ilosc_szt = dane_db[i][4]
            if not ilosc_m:
                ilosc_m = 1
                zm = 1
            else:
                zm = 0.95
            if not ilosc_szt:
                ilosc_szt = 1
            if isinstance(tm, int) and isinstance(tp1, int):
                tw = tm + tp1
            else:
                tw = 0
            tp2 = tw * 0.05
            tj = (tw + tp2) * 1.1
            tjh = tj / 3600

            if tj != 0:
                norma = 8 / tj * 3600 * ilosc_m * zm * ilosc_szt
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
        self.model.setRelation(11, QSqlRelation('uzytkownicy', 'iduzytkownicy',
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

        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.resizeColumnsToContents()

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
