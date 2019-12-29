# -*- coding: utf-8 -*-
# GŁÓWNE MENU
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette, QColor, QIcon, QPainter
from PyQt5.QtWidgets import QWidget, QComboBox, QGridLayout, QHBoxLayout, \
    QPushButton, QLabel, QVBoxLayout, QLineEdit, QGroupBox, QFormLayout, \
    QMessageBox, QToolButton, QSizePolicy, QStyleOptionButton, QStyle

from baza import polaczenie
from dropbox_base import backup
from narzedzia_poz import NarzPoz
from norma import Norma


class WprowadzNarzedzia(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout_h = QFormLayout()
        self.rodzaj = 'Frez palcowy'
        self.parent = parent

        # Pola do wprowadzania danych
        self.symbol_edit = QLineEdit(self)
        self.producent_edit = QLineEdit(self)
        self.srednica_edit = QLineEdit(self)
        self.dlugosc_edit = QLineEdit(self)
        self.dlugosc_rob_edit = QLineEdit(self)
        self.ilosc_pl_edit = QLineEdit(self)
        self.ilosc_kraw_edit = QLineEdit(self)
        self.symbol_pl_edit = QLineEdit(self)
        self.gwint_edit = QLineEdit(self)
        self.typ_gw_edit = QLineEdit(self)
        self.typ_opr_edit = QLineEdit(self)
        self.sr_wew_edit = QLineEdit(self)
        self.sr_zew_edit = QLineEdit(self)
        self.gr_edit = QLineEdit(self)

        self.srednica_lbl = QLabel('Średnica:', self)
        self.dlugosc_lbl = QLabel('Długość:', self)
        self.dlugosc_rob_lbl = QLabel('Długość robocza:', self)
        self.ilosc_pl_lbl = QLabel('Ilość płytek:', self)
        self.ilosc_kraw_lbl = QLabel('Ilość krawędzi na płytkę:', self)
        self.symbol_pl_lbl = QLabel('Symbol płytki:', self)
        self.gwint_lbl = QLabel('Rozmiar gwintu:', self)
        self.typ_gw_lbl = QLabel('Typ gwintownika:', self)
        self.typ_oprawki_lbl = QLabel('Typ oprawki:', self)
        self.sr_wew_lbl = QLabel('Średnica wewnętrzna:', self)
        self.sr_zew_lbl = QLabel('Średnica zewnętrzna:', self)
        self.gr_lbl = QLabel('Grubość cięcia piły:', self)

        self.formularz = QGroupBox("Dodaj narzędzie")

        self.initUI()

    def initUI(self):
        # self.setCentralWidget(self.table_widget)
        # centrowanie widżetu na pełne okno
        typy_narzedzi = [
            'Frez palcowy',
            'Frez płytkowy (głowica)',
            'Gwintownik',
            'Nóż tokarski',
            'Oprawka',
            'Piła',
            'Pozostałe',
            'Rozwiertak',
            'Wiertło',
            'Wiertło składane',
            'Wygniatak'
        ]
        # Zatwierdzenie
        ok_button = QPushButton("Dodaj")
        cancel_button = QPushButton("Cofnij")
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        # Pole wyboru
        combo = QComboBox(self)
        combo.addItems(typy_narzedzi)
        combo.activated[str].connect(self.aktywacja)

        # Etykiety
        typ_lbl = QLabel('Typ narzędzia:', self)
        symbol_lbl = QLabel('Symbol narzędzia:', self)
        producent_lbl = QLabel('Producent:', self)

        # podświetlenie
        paleta = self.palette()
        paleta.setColor(QPalette.Highlight, QColor(255, 0, 0))
        self.symbol_edit.setPalette(paleta)
        # kolor podświetlenia 189,67,243

        # Layouty
        layout_v = QVBoxLayout()

        self.layout_h.addRow(typ_lbl, combo)
        self.layout_h.addRow(symbol_lbl, self.symbol_edit)
        self.layout_h.addRow(producent_lbl, self.producent_edit)
        self.layout_h.addRow(self.srednica_lbl, self.srednica_edit)
        self.layout_h.addRow(self.dlugosc_lbl, self.dlugosc_edit)
        self.layout_h.addRow(self.dlugosc_rob_lbl, self.dlugosc_rob_edit)
        self.layout_h.addRow(self.ilosc_pl_lbl, self.ilosc_pl_edit)
        self.layout_h.addRow(self.ilosc_kraw_lbl, self.ilosc_kraw_edit)
        self.layout_h.addRow(self.symbol_pl_lbl, self.symbol_pl_edit)
        self.layout_h.addRow(self.gwint_lbl, self.gwint_edit)
        self.layout_h.addRow(self.typ_gw_lbl, self.typ_gw_edit)
        self.layout_h.addRow(self.typ_oprawki_lbl, self.typ_opr_edit)
        self.layout_h.addRow(self.sr_wew_lbl, self.sr_wew_edit)
        self.layout_h.addRow(self.sr_zew_lbl, self.sr_zew_edit)
        self.layout_h.addRow(self.gr_lbl, self.gr_edit)

        layout_v.addLayout(self.layout_h)

        self.usuwanie_layoutow()
        self.formularz.setLayout(layout_v)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formularz)
        main_layout.addLayout(hbox)
        self.setLayout(main_layout)

        # connecty
        ok_button.clicked.connect(self.dodanie)
        cancel_button.clicked.connect(self.anulowanie)

    def aktywacja(self, tekst):
        self.rodzaj = self.usuwanie_layoutow(tekst)

    def dodanie(self):
        global tab, query
        tab_select = []
        if self.rodzaj == 'Frez palcowy':
            query = "INSERT INTO frezy_palcowe(symbol_freza, producent_fr, " \
                    "srednica_fr, dl_fr, dl_rob_fr) VALUES(?,?,?,?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.srednica_edit.text().replace(',', '.'),
                self.dlugosc_edit.text().replace(',', '.'),
                self.dlugosc_rob_edit.text().replace(',', '.')
            )
            tab_select = [
                'idfrezy_palcowe',
                'frezy_palcowe',
                'symbol_freza'
            ]
        if self.rodzaj == 'Frez płytkowy (głowica)':
            query = "INSERT INTO frezy_plytkowe(symbol_freza_pl, " \
                    "producent_fp, srednica_fr_pl, ilosc_plytek, symbol_pl," \
                    "ilosc_krawedzi_pl) VALUES(?,?,?,?,?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.srednica_edit.text().replace(',', '.'),
                self.ilosc_pl_edit.text(),
                self.symbol_pl_edit.text(),
                self.ilosc_kraw_edit.text()
            )
            tab_select = [
                'idfrezy_plytkowe',
                'frezy_plytkowe',
                'symbol_frez_pl'
            ]
        if self.rodzaj == 'Gwintownik':
            query = "INSERT INTO gwintowniki(symbol_g, producent_gw, " \
                    "rozmiar_gwintu, typ_gwintownika) VALUES(?,?,?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.gwint_edit.text(),
                self.typ_gw_edit.text(),
            )
            tab_select = [
                'idgwintowniki',
                'gwintowniki',
                'symbol_g'
            ]
        if self.rodzaj == 'Nóż tokarski':
            query = "INSERT INTO noze_tokarskie(symbol_n, producent_n, " \
                    "plytki_n, ilosc_krawedzi_pl_n) VALUES(?,?,?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.symbol_pl_lbl.text(),
                self.ilosc_kraw_edit.text(),
            )
            tab_select = [
                'idnoze_tokarskie',
                'noze_tokarskie',
                'symbol_n'
            ]
        if self.rodzaj == 'Oprawka':
            query = "INSERT INTO oprawki(typ_oprawki, producent_opr, dl_opr, " \
                    "srednica_wew, srednica_zew) VALUES(?,?,?,?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.dlugosc_edit.text().replace(',', '.'),
                self.sr_wew_edit.text().replace(',', '.'),
                self.sr_zew_edit.text().replace(',', '.'),
            )
            tab_select = [
                'idoprawki',
                'oprawki',
                'typ_oprawki'
            ]
        if self.rodzaj == 'Piła':
            query = "INSERT INTO pily(symbol_p, producent_pil, srednica_p, " \
                    "grubosc_p, rodzaj_pl_p,ilosc_pl_p,ilosc_kraw_p) VALUES(" \
                    "?,?,?,?,?,?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.srednica_edit.text().replace(',', '.'),
                self.gr_edit.text(),
                self.symbol_pl_edit.text(),
                self.ilosc_pl_edit.text(),
                self.ilosc_kraw_edit.text(),
            )
            tab_select = [
                'idpily',
                'pily',
                'symbol_p'
            ]
        if self.rodzaj == 'Pozostałe':
            query = "INSERT INTO pozostale(symbol_poz, producent_poz, " \
                    "srednica_poz, ilosc_pl_poz, plytki_poz) VALUES(?,?,?,?," \
                    "?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.srednica_edit.text().replace(',', '.'),
                self.ilosc_pl_edit.text(),
                self.symbol_pl_edit.text(),
            )
            tab_select = [
                'idpozostale',
                'pozostale',
                'symbol_poz'
            ]
        if self.rodzaj == 'Rozwiertak':
            query = "INSERT INTO rozwiertaki(symbol_r, producent_roz, " \
                    "rozmiar_r) VALUES(?,?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.srednica_edit.text().replace(',', '.'),
            )
            tab_select = [
                'idrozwiertaki',
                'rozwiertaki',
                'symbol_r'
            ]
        if self.rodzaj == 'Wiertło':
            query = "INSERT INTO wiertla(symbol_w, producent_w, srednica_w, " \
                    "dlugosc_w) VALUES(?,?,?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.srednica_edit.text().replace(',', '.'),
                self.dlugosc_edit.text(),
            )
            tab_select = [
                'idwiertla',
                'wiertla',
                'symbol_w'
            ]
        if self.rodzaj == 'Wiertło składane':
            query = "INSERT INTO wiertla_skladane(symbol_w_skl, " \
                    "producent_ws, srednica_w_skl, plytki_w_skl) VALUES(?,?," \
                    "?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.srednica_edit.text().replace(',', '.'),
                self.symbol_pl_edit.text(),
            )
            tab_select = [
                'idwiertla_skladane',
                'wiertla_skladane',
                'symbol_w_skl'
            ]
        if self.rodzaj == 'Wygniatak':
            query = "INSERT INTO wygniataki(symbol_wyg, producent_wyg, " \
                    "rozmiar_gw) VALUES(?,?,?) "
            tab = (
                self.symbol_edit.text(),
                self.producent_edit.text(),
                self.gwint_edit.text(),
            )
            tab_select = [
                'idwygniataki',
                'wygniataki',
                'symbol_wyg'
            ]
        print(tab)
        q_spr = 'SELECT ' + tab_select[0] + ' FROM ' + tab_select[
            1] + ' WHERE ' + tab_select[
                    2] + '="' + self.symbol_edit.text() + '"'
        if polaczenie(q_spr) and self.symbol_edit.text() != "":
            QMessageBox.warning(self, "Duplikujące się narzędzie",
                                "Narzędzie, które dodajesz, jest już w bazie",
                                QMessageBox.Ok)
        elif self.symbol_edit.text() == "":
            QMessageBox.critical(self, "Brak symbolu narzędzia",
                                 "Nie można dodać narzędzia bez wpisania "
                                 "symbolu",
                                 QMessageBox.Ok)
        else:
            polaczenie(query, tab)
            self.parent.statusBar().showMessage("Dodano narzędzie", 10000)
            backup()

        # czyszczenie po dodaniu narzędzia
        self.symbol_edit.setText('')
        self.producent_edit.setText('')
        self.srednica_edit.setText('')
        self.dlugosc_edit.setText('')
        self.dlugosc_rob_edit.setText('')
        self.ilosc_pl_edit.setText('')
        self.ilosc_kraw_edit.setText('')
        self.symbol_pl_edit.setText('')
        self.gwint_edit.setText('')
        self.typ_gw_edit.setText('')
        self.typ_opr_edit.setText('')
        self.sr_wew_edit.setText('')
        self.sr_zew_edit.setText('')
        self.gr_edit.setText('')

    def anulowanie(self):
        self.parent.statusBar().clearMessage()
        menu_gl = Wewnatrz(self.parent)
        self.parent.setCentralWidget(menu_gl)

    def usuwanie_layoutow(self, wartosc='Frez palcowy'):
        self.srednica_lbl.hide()
        self.dlugosc_lbl.hide()
        self.dlugosc_rob_lbl.hide()
        self.ilosc_pl_lbl.hide()
        self.ilosc_kraw_lbl.hide()
        self.symbol_pl_lbl.hide()
        self.gwint_lbl.hide()
        self.typ_gw_lbl.hide()
        self.typ_oprawki_lbl.hide()
        self.sr_wew_lbl.hide()
        self.sr_zew_lbl.hide()
        self.gr_lbl.hide()

        self.srednica_edit.hide()
        self.dlugosc_edit.hide()
        self.dlugosc_rob_edit.hide()
        self.ilosc_pl_edit.hide()
        self.ilosc_kraw_edit.hide()
        self.symbol_pl_edit.hide()
        self.gwint_edit.hide()
        self.typ_gw_edit.hide()
        self.typ_opr_edit.hide()
        self.sr_wew_edit.hide()
        self.sr_zew_edit.hide()
        self.gr_edit.hide()

        if wartosc == 'Frez palcowy':
            self.srednica_lbl.show()
            self.dlugosc_lbl.show()
            self.dlugosc_rob_lbl.show()
            self.srednica_edit.show()
            self.dlugosc_edit.show()
            self.dlugosc_rob_edit.show()
        if wartosc == 'Frez płytkowy (głowica)':
            self.srednica_lbl.show()
            self.ilosc_pl_lbl.show()
            self.ilosc_kraw_lbl.show()
            self.symbol_pl_lbl.show()
            self.srednica_edit.show()
            self.ilosc_pl_edit.show()
            self.ilosc_kraw_edit.show()
            self.symbol_pl_edit.show()
        if wartosc == 'Gwintownik':
            self.gwint_lbl.show()
            self.typ_gw_lbl.show()
            self.gwint_edit.show()
            self.typ_gw_edit.show()
        if wartosc == 'Nóż tokarski':
            self.ilosc_kraw_lbl.show()
            self.symbol_pl_lbl.show()
            self.ilosc_kraw_edit.show()
            self.symbol_pl_edit.show()
        if wartosc == 'Oprawka':
            self.dlugosc_lbl.show()
            self.typ_oprawki_lbl.show()
            self.sr_wew_lbl.show()
            self.sr_zew_lbl.show()
            self.dlugosc_edit.show()
            self.typ_opr_edit.show()
            self.sr_wew_edit.show()
            self.sr_zew_edit.show()
        if wartosc == 'Piła':
            self.srednica_lbl.show()
            self.ilosc_pl_lbl.show()
            self.ilosc_kraw_lbl.show()
            self.symbol_pl_lbl.show()
            self.gr_lbl.show()
            self.srednica_edit.show()
            self.ilosc_pl_edit.show()
            self.ilosc_kraw_edit.show()
            self.symbol_pl_edit.show()
            self.gr_edit.show()
        if wartosc == 'Pozostałe':
            self.srednica_lbl.show()
            self.ilosc_pl_lbl.show()
            self.symbol_pl_lbl.show()
            self.srednica_edit.show()
            self.ilosc_pl_edit.show()
            self.symbol_pl_edit.show()
        if wartosc == 'Rozwiertak':
            self.srednica_lbl.show()
            self.srednica_edit.show()
        if wartosc == 'Wiertło':
            self.srednica_lbl.show()
            self.dlugosc_lbl.show()
            self.srednica_edit.show()
            self.dlugosc_edit.show()
        if wartosc == 'Wiertło składane':
            self.srednica_lbl.show()
            self.symbol_pl_lbl.show()
            self.srednica_edit.show()
            self.symbol_pl_edit.show()
        if wartosc == 'Wygniatak':
            self.gwint_lbl.show()
            self.gwint_edit.show()
        return wartosc

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.dodanie()


# Klasa odpowiedzialna za resize ikon
class myPushButton(QPushButton):
    def __init__(self, label=None, parent=None):
        super(myPushButton, self).__init__(label, parent)

        self.pad = 4  # padding between the icon and the button frame
        self.minSize = 8  # minimum size of the icon

        sizePolicy = QSizePolicy(QSizePolicy.Expanding,
                                 QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        # ---- get default style ----
        opt = QStyleOptionButton()
        self.initStyleOption(opt)

        # ---- scale icon to button size ----
        Rect = opt.rect
        h = Rect.height()
        w = Rect.width()
        iconSize = max(min(h, w) - 2 * self.pad, self.minSize)
        opt.iconSize = QSize(iconSize, iconSize)

        # ---- draw button ----
        self.style().drawControl(QStyle.CE_PushButton, opt, qp, self)
        qp.end()


class Wewnatrz(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        btn_wpr_n = QToolButton()
        btn_wpr_norm = QToolButton()
        btn_przyp = QToolButton()

        btn_wpr_n.setIcon(QIcon('icons\\narzedzia.png'))
        btn_wpr_n.setIconSize(QSize(128, 128))
        btn_wpr_n.setToolTip('Wprowadź narzędzia')
        btn_wpr_n.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn_wpr_n.setText("Wprowadź narzędzia")
        btn_wpr_n.setToolTipDuration(0.5)
        # btn_wpr_n.setFlat(True)
        btn_wpr_norm.setIcon(QIcon('icons\\stoper.png'))
        btn_wpr_norm.setIconSize(QSize(128, 128))
        btn_wpr_norm.setText('Wprowadź normy')
        btn_wpr_norm.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn_wpr_norm.setToolTip('Wprowadź normy')
        btn_wpr_norm.setToolTipDuration(0.5)
        # btn_wpr_norm.setFlat(True)
        btn_przyp.setIcon(QIcon('icons\\poz_narz.png'))
        btn_przyp.setIconSize(QSize(128, 128))
        btn_przyp.setText('Przypisz narzędzia do pozycji')
        btn_przyp.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn_przyp.setToolTip('Przypisz narzędzia do pozycji')
        btn_przyp.setToolTipDuration(0.5)
        # btn_przyp.setFlat(True)

        grid.addWidget(btn_wpr_n, 0, 0)
        grid.addWidget(btn_wpr_norm, 0, 1)
        grid.addWidget(btn_przyp, 0, 2)

        btn_wpr_n.clicked.connect(self.narzedzia)
        btn_przyp.clicked.connect(self.narz_poz)
        btn_wpr_norm.clicked.connect(self.norma)

    def narzedzia(self):
        narz = WprowadzNarzedzia(self.parent)
        self.parent.setCentralWidget(narz)

    def norma(self):
        nor = Norma(self.parent)
        self.parent.setCentralWidget(nor)

    def narz_poz(self):
        n_p = NarzPoz(self.parent)
        self.parent.setCentralWidget(n_p)


def wysylanie(text=None, nazwa=0):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import time

    now = time.strftime("%c")
    query = 'SELECT "nazwa_uz" FROM "uzytkownicy" WHERE iduzytkownicy IS ' + str(
        nazwa)
    nazwa = polaczenie(query)

    sender_email = "thm@kuznia.com.pl"
    receiver_email = "jakubhawro@kuznia.com.pl"
    password = 't#567#hm'

    message = MIMEMultipart("alternative")
    message["Date"] = now
    message["Subject"] = "Zgłoś problem PBPZ - ID: " + str(nazwa[0])
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("poczta.hb.pl", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    print('Wysłano')
