# ===== PROBLEMA =====
# Manwal ang botohan sa Student Election. Madaling madoble ang boto, hindi
# malinaw ang tally, at matagal bago malaman kung sino ang panalo. May duda
# rin kung tunay na isang boto lang ang bawat estudyante sa bawat posisyon.
#
# ===== SOLUSYON =====
# CLI system na may one-vote-per-position protection sa database, tally na may
# percentage at winner detection, turnout per grade level, at history ng
# pagboto ng bawat estudyante.
import el_db
import ballot_desk


def el_menu():
    print("\n" + "="*56)
    print("        STUDENT ELECTION - VOTING SYSTEM")
    print("="*56)
    print("  [1] Gumawa ng Bagong Election")
    print("  [2] Magdagdag ng Posisyon")
    print("  [3] Magdagdag ng Kandidato")
    print("  [4] Magdagdag ng Estudyante (Voter Masterlist)")
    print("  [5] Bumoto (Cast Vote)")
    print("  [6] Tingnan ang mga Kandidato")
    print("  [7] Results / Tally Bawat Posisyon")
    print("  [8] Voter Turnout (per Grade Level)")
    print("  [9] Status ng Pagboto ng Estudyante")
    print("  [10] Isara ang Election (Close)")
    print("  [11] Listahan ng Elections")
    print("  [0] Lumabas")
    print("="*56)


def el_cli():
    ok, msg = el_db.test_connection()
    print(f"\n  {msg}")
    if not ok:
        print("  Paki-import muna ang 'schema_election.sql' sa XAMPP/MySQL.")
        return
    while True:
        el_menu()
        ch = input("\n  Ano'ng aksyon ang gagawin? : ").strip()
        if ch == "1":
            ballot_desk.open_election()
        elif ch == "2":
            ballot_desk.create_position()
        elif ch == "3":
            ballot_desk.nominate_candidate()
        elif ch == "4":
            ballot_desk.register_voter()
        elif ch == "5":
            ballot_desk.lodge_vote()
        elif ch == "6":
            ballot_desk.show_candidates()
        elif ch == "7":
            ballot_desk.show_tally()
        elif ch == "8":
            ballot_desk.show_turnout()
        elif ch == "9":
            ballot_desk.show_voter_status()
        elif ch == "10":
            ballot_desk.seal_election()
        elif ch == "11":
            ballot_desk.show_elections()
        elif ch == "0":
            print("\n  Sarado na ang botohan. Salamat sa pagboto!")
            break
        else:
            print("\n  * Hindi tamang pagpili.")


if __name__ == "__main__":
    el_cli()
