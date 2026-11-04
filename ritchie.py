# File 3 of 4 : election_app.py - menu ug validation
import mysql.connector

import db_election

MENU = """
  ==== STUDENT ELECTION ====
  [1] Add (Create)   [2] View (Read)
  [3] Update         [4] Delete
  [0] Exit
"""


def ask(prompt, number=False):
    """number=False -> text; number=True -> numero lang."""
    while True:
        value = input(prompt).strip()
        if number and value.isdigit():
            return int(value)
        if not number and value != "":
            return value
        print("  * Numero lang." if number else "  * Dili pwede blangko.")


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


def add():
    print("\n  --- ADD ---")
    name = ask("  Name     : ")
    position = ask("  Position : ")
    try:
        new_id = db_election.add_candidate(name, position)
        print(f"  [SAVED] Bag-ong ID = {new_id}")
    except mysql.connector.Error as err:
        print(f"  [ERROR] {err}")


def update():
    print("\n  --- UPDATE ---")
    cid = ask("  ID           : ", number=True)
    name = ask("  New name     : ")
    position = ask("  New position : ")
    try:
        if db_election.update_candidate(cid, name, position):
            print("  [UPDATED]")
        else:
            print("  [WALA] Wala'y ID nga ingon ana.")
    except mysql.connector.Error as err:
        print(f"  [ERROR] {err}")


def delete():
    print("\n  --- DELETE ---")
    cid = ask("  ID           : ", number=True)
    answer = input(f"  Papason ang ID {cid}? (oo/hindi): ").strip().lower()
    if answer not in ("oo", "o", "yes", "y"):
        print("  [CANCELLED]")
        return
    try:
        if db_election.delete_candidate(cid):
            print("  [DELETED]")
        else:
            print("  [WALA] Wala'y ID nga ingon ana.")
    except mysql.connector.Error as err:
        print(f"  [ERROR] {err}")


def main():
    try:
        db_election.get_candidates()
    except mysql.connector.Error as err:
        print(f"\n  [ERROR] {err}")
        print("  Check: nagdagan ba ang MySQL? Na-import ba ang SQL?")
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
