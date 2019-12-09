# -*- coding: utf-8 -*-
# NORMY - stoper
import json

from PyQt5.QtCore import QSortFilterProxyModel, pyqtSlot, QRegExp, Qt
from PyQt5.QtGui import QKeySequence, QCursor, QPalette, QColor
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel, \
    QSqlRelation
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QTableView, QGroupBox, QLabel, QLineEdit, \
    QShortcut, QComboBox, QItemDelegate, QAbstractItemView, \
    QMenu, QAction, QMessageBox, QDialog, QGridLayout, QTabWidget

from baza import multipolaczenie, update_bazy, polaczenie, sciezka


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


class MultiDialog(QDialog):

    def __init__(self, parent=None):
        super(MultiDialog, self).__init__(parent)

        # lista wybieralna
        with open('./resources/Maszyny i operacje.json', 'r',
                  encoding='utf-8') as file:
            plik_json = json.load(file)
        maszyny = plik_json['Maszyny']
        operacje = plik_json['Operacje']

        paleta = self.palette()
        paleta.setColor(QPalette.Highlight, QColor(255, 0, 0))

        poz_lbl = QLabel('Pozycja')
        masz_lbl = QLabel('Maszyna')
        op_lbl = QLabel('Operacja')
        tm_lbl = QLabel('Czas Tm')
        tp_lbl = QLabel('Czas Tp')
        self.poz = QLineEdit()
        self.masz = QComboBox()
        self.op = QComboBox()
        self.tm = QLineEdit()
        self.tp = QLineEdit()
        self.resize(300, 150)
        self.setWhatsThis('Pole wymagane - Pozycja')
        self.poz.setPalette(paleta)
        self.masz.addItems(maszyny)
        self.masz.InsertPolicy(QComboBox.NoInsert)
        self.op.addItems(operacje)

        # Box odpowiedzialny za OK i Anuluj
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Anuluj")
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        # Układ główny
        uklad = QGridLayout(self)
        uklad.addWidget(poz_lbl, 0, 0)
        uklad.addWidget(self.poz, 0, 1)
        uklad.addWidget(masz_lbl, 1, 0)
        uklad.addWidget(self.masz, 1, 1)
        uklad.addWidget(op_lbl, 2, 0)
        uklad.addWidget(self.op, 2, 1)
        uklad.addWidget(tm_lbl, 3, 0)
        uklad.addWidget(self.tm, 3, 1)
        uklad.addWidget(tp_lbl, 4, 0)
        uklad.addWidget(self.tp, 4, 1)
        uklad.addLayout(hbox, 5, 0, 2, 0)

        # Sygnały
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        self.setModal(True)
        self.setWindowTitle('Wprowadź pozycje')
        self.setLayout(uklad)

    def pola_wpr(self):
        return (
            self.poz.text().strip(),
            self.masz.currentText().strip(),
            self.op.currentText().strip(),
            self.tm.text().strip(),
            self.tp.text().strip()
        )

    @staticmethod
    def getMultidialog(parent=None):
        multidialog = MultiDialog(parent)
        multidialog.poz.setFocus()
        multidialog.show()
        ok = multidialog.exec_()
        poz, masz, op, tm, tp = multidialog.pola_wpr()
        return poz, masz, op, tm, tp, ok == QDialog.Accepted


class Norma(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tab1 = NormaOdk(parent)
        self.tab2 = NormaKol(parent)

        self.tabs.addTab(self.tab1, "Odkuwki")
        self.tabs.addTab(self.tab2, "Kołnierze")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class NormaOdk(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.skrot = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.naglowki = {
            'iddetale': 'ID',
            'nr_detalu': 'Detal',
            'maszyna': 'Maszyna',
            "ilosc_m": 'Ilość maszyn',
            'ilosc_szt': 'Ilość sztuk na operację',
            'nazwa_op': 'Nazwa operacji',
            'nr_op': 'Nr operacji',
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
        self.db.setDatabaseName(sciezka)
        if self.db.open():
            print('Otworzono bazę danych')
        self.model = QSqlRelationalTableModel(self, self.db)
        self.initUI()

    def initUI(self):
        # Zainicjowanie tabeli zawsze przed wszystkim
        self.tabela()

        # lista wybieralna
        with open('./resources/Maszyny i operacje.json', 'r',
                  encoding='utf-8') as file:
            plik_json = json.load(file)
        masz = plik_json['Maszyny']
        operacje = plik_json['Operacje']
        self.table.setItemDelegateForColumn(2, ComboDelegate(self, masz))
        self.table.setItemDelegateForColumn(6, ComboDelegate(self, operacje))
        for row in range(0, self.model.rowCount()):
            self.table.openPersistentEditor(self.model.index(row, 2))
            self.table.openPersistentEditor(self.model.index(row, 6))

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
        # Menu kontekstowe własne
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.prawoklik)

    def prawoklik(self):
        menu = QMenu(self)
        if self.model.rowCount():
            akcja = QAction('Usuń wiersz', self)
            akcja.triggered.connect(self.usun_wiersz)
            menu.addAction(akcja)
            menu.exec_(QCursor.pos())

    def usun_wiersz(self):
        ok = QMessageBox.question(self, 'Potwierdzenie',
                                  'Czy na pewno chcesz usunąć pozycję?',
                                  QMessageBox.Ok, QMessageBox.Cancel)
        if ok == QMessageBox.Ok:
            selected = self.table.currentIndex()
            self.model.removeRow(selected.row())
            self.model.submitAll()
            self.model.select()

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
        self.model.setRelation(12, QSqlRelation('uzytkownicy', 'iduzytkownicy',
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

        # Odpowiada za edycję pojednynczym kliknieciem
        '''
        Constant    Value   Description
        QAbstractItemView::NoEditTriggers   0   No editing possible.
        QAbstractItemView::CurrentChanged   1   Editing start whenever current item changes.
        QAbstractItemView::DoubleClicked    2   Editing starts when an item is double clicked.
        QAbstractItemView::SelectedClicked  4   Editing starts when clicking on an already selected item.
        QAbstractItemView::EditKeyPressed   8   Editing starts when the platform edit key has been pressed over an item.
        QAbstractItemView::AnyKeyPressed    16  Editing starts when any key is pressed over an item.
        QAbstractItemView::AllEditTriggers  31  Editing starts for all above actions.
        '''
        if self.odczyt():
            self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        else:
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
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

    def odczyt(self):
        id = str(self.parent.id_user[0])
        query = 'SELECT odczyt FROM uzytkownicy WHERE iduzytkownicy=' + id
        return polaczenie(query)[0]

    def dodaj(self):
        poz, masz, op, tm, tp, ok = MultiDialog().getMultidialog(self)
        print(poz, masz, op, tm, tp, ok)
        id = self.parent.id_user[0]
        if ok and poz:
            query = "INSERT INTO detale(nr_detalu,maszyna,nazwa_op,tm,tp," \
                    "id_uzytkownika) VALUES ('" + poz + "','" + masz + "','" + op + "','" + tm + "','" + tp + "','" + str(
                id) + "');"
            print(query)
            polaczenie(query)
            if tm and tp:
                try:
                    self.uzupelniene()
                except:
                    pass
            self.model.select()
            self.parent.statusBar().showMessage("Dodano nową pozycję", 10000)
        else:
            print("Nie wpisano pozycji")


class NormaKol(NormaOdk):
    @pyqtSlot()
    def uzupelniene(self):
        # Pobranie tp, tm z bazy
        query = 'SELECT iddetale, tm, tp, ilosc_m, ilosc_szt FROM kolnierze'
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
            query = 'UPDATE "kolnierze" SET "tj" = ' + str(
                round(tjh, 5)) + ', "norma" = ' + str(round(
                norma)) + ' WHERE "iddetale" = ' + str(dane_db[i][0])
            update_bazy(query)
            # query = 'UPDATE "detale" SET "norma" = ' + str(round(norma)) +
            # ' WHERE "iddetale" = ' + str(dane_db[i][0]) update_bazy(query)

    def tabela(self):
        self.model.setTable('kolnierze')
        self.model.setRelation(12, QSqlRelation('uzytkownicy', 'iduzytkownicy',
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

        # Odpowiada za edycję pojednynczym kliknieciem
        if self.odczyt():
            self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        else:
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.resizeColumnsToContents()

        # self.table.doubleClicked.connect(self.klikniecie)

    def dodaj(self):
        poz, masz, op, tm, tp, ok = MultiDialog().getMultidialog(self)
        print(poz, masz, op, tm, tp, ok)
        id = self.parent.id_user[0]
        if ok and poz:
            query = "INSERT INTO kolnierze(nr_detalu,maszyna,nazwa_op,tm,tp," \
                    "id_uzytkownika) VALUES ('" + poz + "','" + masz + "','" + op + "','" + tm + "','" + tp + "','" + str(
                id) + "');"
            print(query)
            polaczenie(query)
            if tm and tp:
                try:
                    self.uzupelniene()
                except:
                    pass
            self.model.select()
            self.parent.statusBar().showMessage("Dodano nową pozycję", 10000)
        else:
            print("Nie wpisano pozycji")
