# -*- coding: utf-8 -*-
# POŁĄCZENIE Z BAZĄ
import os
from sqlite3 import connect

if os.path.exists(r'\\raspberrypi\PBPZ\poo.db'):
    sciezka = r'\\raspberrypi\PBPZ\poo.db'
else:
    sciezka = 'poo.db'


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
        print("Połączono z bazą danych")

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
        print("Połączono z bazą danych")

        cur.execute(query)

    con.commit()
    con.close()
