# STUDENT ELECTION - CANDIDATE MANAGER (CRUD)
# PURPOSO: Pagtipig ug pag-manage sa mga kandidato sa election.
# PROBLEMA: Manwal ang listahan nya need paka mangutana og kinsay tresurer og kinsay secretary which is hussle so tungud ani 
# nga system mahibawan na nimo og kinsa ang president og vice deli naka need mangutana pa -> dali madoble, lisod usbon/papason.
# SOLUSYON: MySQL + CRUD (Add, View, Update, Delete).
# ============================================================
import mysql.connector
import db_election
MENU = """
  ==== STUDENT ELECTION ====
  [1] Add (Create)   [2] View (Read)
  [3] Update         [4] Delete
  [0] Exit
"""
# ask(): mangayo og input. Kung number=True, numero lang ang dawaton.
def ask(prompt, number=False):
    while True:
        value = input(prompt).strip()
        if number and value.isdigit():
            return int(value)
        if not number and value != "":
            return value
        print("  * Numero lang." if number else "  * Dili pwede blangko.")

# show_all(): READ - ipakita ang tanang record.
def show_all():
    try:
        rows = db_election.get_candidates()
    except mysql.connector.Error as err:
        print(f"  [ERROR] {err}")
        return
    if not rows:
        print("\n  Wala pay record.")
        return
    print(f"\n  --- CANDIDATES ({len(rows)}) ---")
    for row in rows:
        print(f"  [{row['id']}] {row['name']} - {row['position_name']}")

# add(): CREATE - mangayo og data ug mo-save og bag-ong record.
def add():
    print("\n  --- ADD ---")
    name = ask("  Name     : ")
    position = ask("  Position : ")
    try:
        new_id = db_election.add_candidate(name, position)
        print(f"  [SAVED] Bag-ong ID = {new_id}")
    except mysql.connector.Error as err:
        print(f"  [ERROR] {err}")

# update(): UPDATE - usbon ang record nga naay ID.
def update():
    print("\n  --- UPDATE ---")
    cid = ask("  ID           : ", number=True)
    name = ask("  New name     : ")
    position = ask("  New position : ")
    try:
        ok = db_election.update_candidate(cid, name, position)
        print("  [UPDATED]" if ok else "  [WALA] Wala'y ID.")
    except mysql.connector.Error as err:
        print(f"  [ERROR] {err}")

# delete(): DELETE - papason ang record, pero mangutana una.
def delete():
    print("\n  --- DELETE ---")
    cid = ask("  ID           : ", number=True)
    answer = input(f"  Papason ang ID {cid}? (oo/hindi): ").strip().lower()
    if answer not in ("oo", "o", "yes", "y"):
        print("  [CANCELLED]")
        return
    try:
        ok = db_election.delete_candidate(cid)
        print("  [DELETED]" if ok else "  [WALA] Wala'y ID.")
    except mysql.connector.Error as err:
        print(f"  [ERROR] {err}")

# main(): ang menu loop. Diri magsugod ang program.
def main():
    try:
        db_election.get_candidates()
    except mysql.connector.Error as err:
        print(f"\n  [ERROR] {err} - Check kung nagdagan ang MySQL.")
        return
    actions = {"1": add, "2": show_all, "3": update, "4": delete}
    while True:
        print(MENU)
        choice = input("  Pili: ").strip()
        if choice == "0":
            print("\n  Goodbye!")
            break
        if choice in actions:
            actions[choice]()
        else:
            print("  * Sayop nga pili.")
if __name__ == "__main__":
    main()
# ============================================
# SUMMARY: MENU ug input sa user; SQL naa sa db_election.py.
# SYNTAX: def=function | import=module | return=value
#         while=loop | if/else=kondisyon
#         try/except=dakpon error | finally=close
# ============================================
