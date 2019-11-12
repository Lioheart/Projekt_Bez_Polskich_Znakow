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


def zmiana_uzytkownik(uzytkownik, id_user):
    query = 'UPDATE uzytkownicy SET nazwa_uz = "' + uzytkownik + '" WHERE iduzytkownicy = ' + \
            id_user[0] + ';'
    polaczenie(query)
