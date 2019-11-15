#importuju knihovnu pro práci s PostgreSQL
import psycopg2
import psycopg2.extras

import os
from flask import g,flash, request
import datetime
from functools import lru_cache

#funkce pro spojení s databází
#export DATABASE_URL=postgres://dbhxhmtwzzbvaj:3380a42d9f11c4ee1378d5816f30b9e3b103958212a1c968d6c2fcc97274f79f@ec2-54-246-92-116.eu-west-1.compute.amazonaws.com:5432/d18snuuetbnac7

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

def skolky_vyhladavanie(nazev, postizeni, mesto, ulice):
    sql = """
    SELECT
    skolky.nazev AS nazev,
    skolky_postizeni.id_typ AS postizeni,
    skolky.id_skolky AS id_skolky,
    skolky.typ_postizeni AS typ_postizeni,
    skolky.mesto, 
    skolky.ulice,
    skolky.web,
    skolky.mail,
    skolky.kontakt,
    skolky.lng,
    skolky.lat
    from public.skolky_postizeni
    left join public.skolky on skolky_postizeni.id_skolky = skolky.id_skolky
    where skolky_postizeni.id_typ IN (SELECT druhy.id FROM public.druhy WHERE typ IN %s)
    order by skolky.mesto asc
    """
    params= [tuple(postizeni)]

    if mesto: 
      sql = sql + " and skolky.mesto = %s"
      params.append(mesto)


    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, tuple(params))
        expectation_table = cur.fetchall()
        #print(expectation_table)
        return expectation_table
    finally:
        if conn is not None:
            conn.close()

def skolky_mesto():
    sql = """
    SELECT 
    mesto
    
    from public.adresa_skolky
    GROUP BY mesto
    ORDER BY mesto ASC
  
    """
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        expectation_table = cur.fetchall()
        #print(expectation_table)
        return expectation_table
    finally:
        if conn is not None:
            conn.close()

def tabulka_skolky_detail(id_skolky):
    sql = """
    SELECT skolky.nazev,
    skolky.id_skolky,
    skolky.ulice,
    skolky.mesto,
    skolky.psc,
    skolky.typ,
    skolky.mail,
    skolky.kontakt,
    skolky.web,
    skolky.typ_postizeni
    from public.skolky
    where id_skolky= %s

    """
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, (id_skolky,))
        skolky_detail = cur.fetchone()
        print(skolky_detail)
        return skolky_detail
    finally:
        if conn is not None:
            conn.close()


