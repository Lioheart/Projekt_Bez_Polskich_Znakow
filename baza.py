# -*- coding: utf-8 -*-
from sqlite3 import connect


def polaczenie(query=None, tab=None):
    con = connect('poo.db')

    with con:
        cur = con.cursor()
        print("Połączono z bazą danych")

        if query and tab == None:
            cur.execute(query)
        elif query and tab:
            cur.execute(query, tab)

        data = cur.fetchone()

    con.commit()
    con.close()
    return data


def multipolaczenie(query=None, tab=None):
    con = connect('poo.db')

    with con:
        cur = con.cursor()
        print("Połączono z bazą danych")

        if query and tab == None:
            cur.execute(query)
        elif query and tab:
            cur.execute(query, tab)

        data = cur.fetchall()

    con.commit()
    con.close()
    return data


def update_bazy(query=None):
    con = connect('poo.db')

    with con:
        cur = con.cursor()
        print("Połączono z bazą danych")

        cur.execute(query)

    con.commit()
    con.close()
