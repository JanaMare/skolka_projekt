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
    skolky.nazev,
    adresa_skolky.ulice as ulice,
    adresa_skolky.mesto as mesto,
    skolky.id_skolky,
    skolky.lat,
    skolky.lng,
    skolky.mail,
    skolky.web,
    skolky.kontakt,
    skolky_postizeni.id_typ as postizeni,
    druhy.id,
    druhy.typ
    from public.skolky_postizeni
    left join public.skolky on skolky_postizeni.id_skolky= skolky.id_skolky
    left join public.adresa_skolky on skolky_postizeni.id_skolky=adresa_skolky.id_skolky
    left join public.druhy on skolky_postizeni.id_typ = druhy.id
    where adresa_skolky.mesto in %s and skolky_postizeni.id_typ IN (SELECT druhy.id FROM public.druhy WHERE typ in %s)
    """
    #params=[tuple(mesto),tuple(postizeni)]

    #if mesto: 
    #sql = sql + "adresa_skolky.mesto = %s"
    #params.append(mesto) 

    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, (mesto, postizeni))
        expectation_table = cur.fetchall()
        print(expectation_table)
        return expectation_table
    finally:
        if conn is not None:
            conn.close()

def skolky_mesto():
    sql = """
    SELECT 
    adresa_skolky.mesto
    
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


