# ===== PROBLEMA =====
# Manwal ang botohan sa Student Election. Madaling madoble ang boto, hindi
# malinaw ang tally, at matagal bago malaman kung sino ang panalo. May duda
# rin kung tunay na isang boto lang ang bawat estudyante sa bawat posisyon.
#
# ===== SOLUSYON =====
# Ang UNIQUE (election_id, voter_id, position_id) sa votes table ang pumipigil
# sa doble at maramihang boto. Ang tally ay COUNT() per candidate at GROUP BY
# position, may percentage, winner detection, at turnout per grade level.

import os

import mysql.connector
from mysql.connector import Error


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "school_election_db")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
    )


def test_connection():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM elections LIMIT 1")
            cursor.fetchone()
            return True, "Koneksyon sa Student Election database ay OK na."
        return False, "Hindi makakonekta sa database."
    except Error as error:
        return False, str(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ELECTIONS
def add_election(title, school_year):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO elections (title, school_year) VALUES (%s,%s)",
            (title, school_year),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_active_election():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM elections
            WHERE status = 'OPEN'
            ORDER BY election_id DESC
            LIMIT 1
            """
        )
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_election(election_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM elections WHERE election_id = %s", (election_id,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_elections():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM elections ORDER BY election_id DESC")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def close_election(election_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE elections SET status = 'CLOSED' WHERE election_id = %s AND status = 'OPEN'",
            (election_id,),
        )
        connection.commit()
        return cursor.rowcount
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# POSITIONS
def add_position(election_id, position_name, max_winners, display_order):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO positions (election_id, position_name, max_winners, display_order)
            VALUES (%s,%s,%s,%s)
            """,
            (election_id, position_name, max_winners, display_order),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_positions(election_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM positions
            WHERE election_id = %s
            ORDER BY display_order, position_name
            """,
            (election_id,),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_position(position_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM positions WHERE position_id = %s", (position_id,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# CANDIDATES
def add_candidate(position_id, full_name, grade_level, section, party):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO candidates (position_id, full_name, grade_level, section, party)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (position_id, full_name, grade_level, section, party),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_candidates(position_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM candidates
            WHERE position_id = %s
            ORDER BY full_name
            """,
            (position_id,),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_candidate(candidate_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.*, p.position_name, p.election_id, e.title, e.status AS election_status
            FROM candidates c
            JOIN positions p ON p.position_id = c.position_id
            JOIN elections e ON e.election_id = p.election_id
            WHERE c.candidate_id = %s
            """,
            (candidate_id,),
        )
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# VOTERS
def add_voter(voter_id, full_name, grade_level, section):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO voters (voter_id, full_name, grade_level, section)
            VALUES (%s,%s,%s,%s)
            """,
            (voter_id, full_name, grade_level, section),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_voter(voter_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM voters WHERE voter_id = %s", (voter_id,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_voters():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM voters ORDER BY grade_level, section, full_name")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def has_voted(election_id, voter_id, position_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM votes
            WHERE election_id = %s AND voter_id = %s AND position_id = %s
            """,
            (election_id, voter_id, position_id),
        )
        row = cursor.fetchone()
        return (row["total"] if row else 0) > 0
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# VOTING
def cast_vote(election_id, position_id, candidate_id, voter_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.candidate_id, c.position_id, p.election_id, e.status
            FROM candidates c
            JOIN positions p ON p.position_id = c.position_id
            JOIN elections e ON e.election_id = p.election_id
            WHERE c.candidate_id = %s
            """,
            (candidate_id,),
        )
        cand = cursor.fetchone()
        if not cand:
            raise ValueError("Wala ang kandidato sa database.")
        if cand["election_id"] != election_id:
            raise ValueError("Hindi kabilang sa aktibong election ang kandidato.")
        if cand["position_id"] != position_id:
            raise ValueError("Hindi tugma ang kandidato sa napiling posisyon.")
        if cand["status"] != "OPEN":
            raise ValueError("Sarado na ang election na ito. Hindi na tumatanggap ng boto.")
        cursor.execute(
            """
            INSERT INTO votes (election_id, position_id, candidate_id, voter_id)
            VALUES (%s,%s,%s,%s)
            """,
            (election_id, position_id, candidate_id, voter_id),
        )
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.IntegrityError as error:
        if connection is not None:
            connection.rollback()
        if "Duplicate entry" in str(error):
            raise ValueError("Nakaboto na ang estudyanteng ito sa posisyong ito.")
        raise
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# REPORTS
def voter_status(election_id, voter_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT p.position_id, p.position_name, p.display_order,
                   CASE WHEN v.vote_id IS NULL THEN 0 ELSE 1 END AS voted,
                   c.full_name AS voted_for
            FROM positions p
            LEFT JOIN votes v
                   ON v.position_id = p.position_id
                  AND v.voter_id = %s
                  AND v.election_id = p.election_id
            LEFT JOIN candidates c ON c.candidate_id = v.candidate_id
            WHERE p.election_id = %s
            ORDER BY p.display_order, p.position_name
            """,
            (voter_id, election_id),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def results(election_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT p.position_id, p.position_name, p.display_order, p.max_winners,
                   c.candidate_id, c.full_name, c.party, c.grade_level, c.section,
                   COUNT(v.vote_id) AS votes
            FROM positions p
            JOIN candidates c ON c.position_id = p.position_id
            LEFT JOIN votes v
                   ON v.candidate_id = c.candidate_id
                  AND v.election_id = p.election_id
            WHERE p.election_id = %s
            GROUP BY p.position_id, p.position_name, p.display_order, p.max_winners,
                     c.candidate_id, c.full_name, c.party, c.grade_level, c.section
            ORDER BY p.display_order, p.position_name, votes DESC, c.full_name
            """,
            (election_id,),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def turnout(election_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT vt.grade_level,
                   COUNT(DISTINCT vt.voter_id) AS total_voters,
                   COUNT(DISTINCT v.voter_id) AS voted,
                   COUNT(DISTINCT vt.voter_id) - COUNT(DISTINCT v.voter_id) AS not_voted
            FROM voters vt
            LEFT JOIN votes v
                   ON v.voter_id = vt.voter_id
                  AND v.election_id = %s
            GROUP BY vt.grade_level
            ORDER BY vt.grade_level
            """,
            (election_id,),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def overall_turnout(election_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT (SELECT COUNT(*) FROM voters) AS total_voters,
                   (SELECT COUNT(DISTINCT voter_id) FROM votes WHERE election_id = %s) AS voters_who_voted,
                   (SELECT COUNT(*) FROM votes WHERE election_id = %s) AS total_votes_cast,
                   (SELECT COUNT(*) FROM positions WHERE election_id = %s) AS total_positions
            """,
            (election_id, election_id, election_id),
        )
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
