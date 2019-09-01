from baza import polaczenie


def opcje_uzytkownik(haslo, id_user):
    print(id_user[0])
    query = 'UPDATE "main"."uzytkownicy" SET "haslo_uz"="' + haslo + '" WHERE' \
                                                                     ' "iduzytkownicy"=' + "'" + str(
        id_user[0]) + "'" + '; '
    polaczenie(query)


def dodaj_uzytkownik(uzytkownik):
    query = 'INSERT INTO "main"."uzytkownicy"(nazwa_uz,haslo_uz) VALUES ("' + uzytkownik + '","' + uzytkownik + '");'
    polaczenie(query)

# class Uzytkownik(QWidget):
#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.parent = parent
#         self.formularz = QGroupBox("Opcje konta")
#         self.initUI()
#
#     def initUI(self):
#         grid = QGridLayout()
#         grid.setSpacing(15)
#         grid.addWidget(self.formularz)
#         self.setLayout(grid)
