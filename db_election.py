# ============================================
# File 2 of 4 : db_election.py
# Dinhi ra ang tanang SQL. Wala niy menu.
# ============================================

import mysql.connector

# DB: settings sa koneksyon (host, user, password, database).
DB = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "retchie",
}

# connect(): mohimo og bag-ong koneksyon sa MySQL.
def connect():
    return mysql.connector.connect(**DB)

# add_candidate(): CREATE - mopasulod og bag-ong record.
def add_candidate(name, position):
    conn = connect()
    cur = conn.cursor()
    try:
        # %s = parameterized query (dili ma-SQL injection)
        cur.execute(
            "INSERT INTO candidates (name, position_name) VALUES (%s, %s)",
            (name, position),
        )
        conn.commit()  # i-save gyud sa database
        return cur.lastrowid
    except mysql.connector.Error:
        conn.rollback()  # kung naay error, i-cancel
        raise
    finally:
        cur.close()  # sigurohon nga ma-close
        conn.close()

# get_candidates(): READ - mokuha sa tanang record.
def get_candidates():
    conn = connect()
    cur = conn.cursor(dictionary=True)  # dictionary -> row['name']
    try:
        cur.execute("SELECT * FROM candidates ORDER BY id")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

# update_candidate(): UPDATE - usbon ang record pinaagi sa ID.
def update_candidate(cid, name, position):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE candidates SET name = %s, position_name = %s WHERE id = %s",
            (name, position, cid),
        )
        conn.commit()
        return cur.rowcount  # 1 = na-usab, 0 = wala makit-i
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

# delete_candidate(): DELETE - papason ang record pinaagi sa ID.
def delete_candidate(cid):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM candidates WHERE id = %s", (cid,))
        conn.commit()
        return cur.rowcount  # 1 = na-delete, 0 = wala makit-i
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

# ============================================
# SUMMARY: DATABASE side; dinhi ra ang tanang SQL.
# SYNTAX: def=function | return=value | %s=parameter
#         try/except=dakpon error | finally=close
#         commit=save | rollback=cancel | cursor=mo-run sa SQL
# ============================================
