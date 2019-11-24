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


#vyhladavanie v skolkach
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
    left join public.adresa_skolky on skolky_postizeni.id_skolky = adresa_skolky.id_skolky
    where skolky_postizeni.id_typ IN (SELECT druhy.id FROM public.druhy WHERE typ IN %s)
    
    """
    params= [tuple(postizeni)]

    if mesto:
      sql = sql + """ and adresa_skolky.mesto = %s"""
      params.append(mesto)


    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, tuple(params))
        expectation_table = cur.fetchall()
        #print(expectation_table)
        return expectation_table
    except Exception as err:
        print(err)
        print("Something is wrong in skolky_vyhladavanie")
    finally:
        if conn is not None:
            conn.close()

#vrati zoznam miest, kde sa nachadzaju specialne skolky
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
        mesto_table = cur.fetchall()
        #print(expectation_table)
        return mesto_table
    except Exception as err:
        print(err)
        print("Something is wrong in skolky_mesto")
    finally:
        if conn is not None:
            conn.close()

#vráti tabulku školky detail 
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
        #print(skolky_detail)
        return skolky_detail
    except Exception as err:
        print(err)
        print("Something is wrong in tabulka_skolky_detail")
    finally:
        if conn is not None:
            conn.close()

#tabulka ranna peceg
def tab_ranna_pece():
    sql = """
    SELECT
    * 
    from public.rannak;
    """

    conn = get_db()

    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        ranna_pece = cur.fetchall()
        return ranna_pece
    except Exception as err:
        print(err)
        print("Something is wrong in tab_ranna_pece")
    finally:
        if conn is not None:
            conn.close()

#vypis ranna pece detail
def tab_ranna_detial(id):
    sql = """
    SELECT
    rannak.id as id,
    rannak.nazev_zarizeni_poskytovatele as nazev,
    rannak.ico,
    rannak.vedouci_zarizeni,
    rannak.adresa_zarizeni_poskytovatele as adresa,
    rannak.vekova_kategorie as vek,
    rannak.pocet_luzek,
    rannak.provozni_doba,
    rannak.kontakt
    from public.rannak
    where id= %s;

    """
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, (id,))
        ranna_detail = cur.fetchone()
        return ranna_detail
    except Exception as err:
        print(err)
        print("Something is wrong in tab_ranna_detail")
    finally:
        if conn is not None:
            conn.close()

#vypis odlehcovaci pece detail
def tab_odlehcovaci_detail(id):
    sql = """
    SELECT
    odlehcovacipece1.id,
    odlehcovacipece1.nazev,
    odlehcovacipece1.ulice,
    odlehcovacipece1.mesto,
    odlehcovacipece1.psc,
    odlehcovacipece1.vedouci_zarizeni,
    odlehcovacipece1.forma,
    odlehcovacipece1.pocetluzek,
    odlehcovacipece1.provoznidoma,
    odlehcovacipece1.telefon,
    odlehcovacipece1.mail,
    odlehcovacipece1.web
    from public.odlehcovacipece1
    where id= %s;
    """
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, (id,))
        odlehcovaci_detail = cur.fetchone()
        return odlehcovaci_detail
    except Exception as err:
        print(err)
        print("Something is wrong in tab_odlehcovaci_detail")
    finally:
        if conn is not None:
            conn.close()

#tabulka odlehcovaci pece
def tab_odlehcovaci():
    sql = """
    SELECT
    * 
    from public.odlehcovacipece1;
    """

    conn = get_db()

    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        odlehcovaci = cur.fetchall()
        return odlehcovaci
    except Exception as err:
        print(err)
        print("Something is wrong in tab_odlehcovaci")
    finally:
        if conn is not None:
            conn.close()



