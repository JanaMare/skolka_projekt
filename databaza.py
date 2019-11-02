#importuju knihovnu pro práci s PostgreSQL
import psycopg2
import psycopg2.extras
#knihovna na interakci s operačním systémem
import os
from flask import g,flash, request
import datetime
from functools import lru_cache

#funkce pro spojení s databází

def get_db():
    """ Connection with database. """

    if not hasattr(g, 'db') or g.db.closed == 1:
    # https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
        database_url = os.environ["DATABASE_URL"]
        con = psycopg2.connect(database_url, sslmode='require', cursor_factory=psycopg2.extras.NamedTupleCursor)
        g.db = con
    return g.db

def get_activities():
    #spojení s databází, linka mezi flaskem a mým počítačem
    db = get_db()
    #cursor = spouští sql dotazy, cursor() je součástí knihovny psychopg2, cursor mají všechny py knihovny s různými
    #databázemi PostgreSQL není databáze ale db ms = database management system
    cur = db.cursor()
    cur.execute('SELECT * FROM public.skolky limit 10;')
    #cursor vrátí všechny záznamy dle sql dotazu a mám je u sebe a je třeba si o ně říci
    #fetchall() vrátí seznam všech řádků, fetchone() vrátí jeden řádek výsledků
    activities = cur.fetchall()
    #už po tobě nebudu chtít nic s tímto dotazem a s těmito výsledky
    cur.close()
    return activities

def tabulka_skolky():

    sql = """SELECT * 
                    FROM public.skolky """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    family_table = cur.fetchall()
    return family_table


