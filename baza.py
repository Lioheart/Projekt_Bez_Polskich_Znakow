# -*- coding: utf-8 -*-
# POŁĄCZENIE Z BAZĄ
import os
import sys
from sqlite3 import connect

from dropbox_base import download, backup

if os.path.exists('./poo.db'):
    sciezka = './poo.db'
else:
    print('Nie znaleziono bazy')
    sys.exit()


def polaczenie(query=None, tab=None):
    con = connect(sciezka)

    with con:
        cur = con.cursor()
        print("Połączono z bazą danych")

        if query and tab is None:
            cur.execute(query)
        elif query and tab:
            cur.execute(query, tab)

        data = cur.fetchone()

    con.commit()
    con.close()
    return data


def multipolaczenie(query=None, tab=None):
    con = connect(sciezka)

    with con:
        cur = con.cursor()
        print("Połączono z bazą danych (multi)")

        if query and tab is None:
            cur.execute(query)
        elif query and tab:
            cur.execute(query, tab)

        data = cur.fetchall()

    con.commit()
    con.close()
    return data


def update_bazy(query=None):
    con = connect(sciezka)

    with con:
        cur = con.cursor()
        # print("Połączono z bazą danych")
        print('Update bazy')

        cur.execute(query)

    con.commit()
    con.close()
