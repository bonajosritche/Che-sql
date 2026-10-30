# ===== PROBLEMA =====
# Manwal ang botohan sa Student Election. Madaling madoble ang boto, hindi
# malinaw ang tally, at matagal bago malaman kung sino ang panalo. May duda
# rin kung tunay na isang boto lang ang bawat estudyante sa bawat posisyon.
#
# ===== SOLUSYON =====
# Ang UNIQUE (election_id, voter_id, position_id) sa database ang pumipigil sa
# doble at maramihang boto. Ang tally ay COUNT() per kandidato, may percentage,
# winner detection, at turnout per grade level.

import mysql.connector

import el_db


def demand_text(msg):
    while True:
        v = input(msg).strip()
        if v == "":
            print("  * Hindi puwede blangko.")
            continue
        return v


def demand_optional(msg):
    return input(msg).strip()


def demand_number(msg, minimum=1, default=None):
    while True:
        v = input(msg).strip()
        if v == "":
            if default is not None:
                return default
            print("  * Hindi puwede blangko.")
            continue
        try:
            val = int(v)
        except ValueError:
            print("  * Numero lang dapat.")
            continue
        if val < minimum:
            print(f"  * Dapat {minimum} pataas.")
            continue
        return val


def get_open_election():
    try:
        e = el_db.get_active_election()
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return None
    if not e:
        print("  [WALA] Walang OPEN election. Gumawa muna sa [1].")
        return None
    return e


def render_election_card(e):
    print("\n" + "="*44)
    print(f"  ELECTION ID : {e['election_id']}")
    print("="*44)
    print(f"  Pangalan     : {e['title']}")
    print(f"  School Year  : {e['school_year']}")
    print(f"  Kalagayan    : {e['status']}")
    if e.get('date_created'):
        print(f"  Ginawa noong : {e['date_created']}")
    print("="*44)


def render_position_card(p):
    print("\n" + "="*44)
    print(f"  POSITION ID : {p['position_id']}")
    print("="*44)
    print(f"  Posisyon     : {p['position_name']}")
    print(f"  Bilang Panalo: {p['max_winners']}")
    print(f"  Order sa Ballot: {p['display_order']}")
    print("="*44)


def render_candidate_card(c):
    print("\n" + "="*44)
    print(f"  CANDIDATE ID : {c['candidate_id']}")
    print("="*44)
    print(f"  Pangalan   : {c['full_name']}")
    print(f"  Grade/Section: {c['grade_level']} - {c['section']}")
    print(f"  Partido    : {c['party'] or '--- INDEPENDENT ---'}")
    if c.get('position_name'):
        print(f"  Posisyon   : {c['position_name']}")
    print("="*44)


def render_voter_card(v):
    print("\n" + "="*44)
    print(f"  STUDENT ID : {v['voter_id']}")
    print("="*44)
    print(f"  Buong Pangalan : {v['full_name']}")
    print(f"  Grade Level    : {v['grade_level']}")
    print(f"  Seksyon        : {v['section']}")
    print("="*44)


# ELECTIONS
def open_election():
    print("\n--- GUMAWA NG BAGONG ELECTION ---")
    existing = get_open_election()
    if existing:
        print(f"  [PAALALA] May OPEN pa: #{existing['election_id']} {existing['title']}")
        print(f"             ({existing['school_year']}). Isara muna sa [10] kung tapos na.")
    title = demand_text("  Pangalan ng Election (hal. SSG Election 2026): ")
    sy = demand_text("  School Year (hal. 2026-2027): ")
    try:
        eid = el_db.add_election(title, sy)
        print(f"\n  [TAPOS NA] Nagawa na ang election. Election ID: {eid}")
        render_election_card(el_db.find_election(eid))
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")


def show_elections():
    try:
        tally_rows = el_db.list_elections()
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not tally_rows:
        print("\n  Wala pang election. Gumawa sa [1].")
        return
    print(f"\n--- LISTAHAN NG ELECTIONS ({len(tally_rows)}) ---")
    for r in tally_rows:
        mark = " <== AKTIBO" if r['status'] == 'OPEN' else ""
        print(
            f"  [#{r['election_id']}] {r['title']} | SY {r['school_year']} "
            f"| {r['status']}{mark}"
        )


def seal_election():
    print("\n--- ISARA ANG ELECTION ---")
    e = get_open_election()
    if not e:
        return
    render_election_card(e)
    confirm = input("  Kumpirmahin na ISARA ang election? (oo/hindi): ").strip().lower()
    if confirm not in ("oo", "o", "yes", "y"):
        print("  Kinansela.")
        return
    try:
        changed = el_db.close_election(e['election_id'])
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if changed:
        print("\n  [TAPOS NA] Sarado na ang election. Hindi na tumatanggap ng boto.")
        print("  Tingnan ang Results sa [7] at Turnout sa [8].")
    else:
        print("\n  [PAALALA] Sarado na ang election na ito.")


# POSITIONS
def create_position():
    print("\n--- MAGDAGDAG NG POSISYON ---")
    e = get_open_election()
    if not e:
        return
    print(f"  Election: {e['title']} ({e['school_year']})")
    try:
        positions = el_db.list_positions(e['election_id'])
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    next_order = len(positions) + 1
    name = demand_text("  Pangalan ng Posisyon (hal. Presidente): ")
    winners = demand_number("  Ilang panalo (Enter = 1): ", default=1)
    order = demand_number(f"  Order sa ballot (Enter = {next_order}): ", default=next_order)
    try:
        pid = el_db.add_position(e['election_id'], name, winners, order)
        print(f"\n  [TAPOS NA] Naidagdag na ang posisyon. Position ID: {pid}")
        render_position_card(el_db.find_position(pid))
    except mysql.connector.Error as err:
        if "Duplicate entry" in str(err) or "uniq_el_position_name" in str(err):
            print("  [PAALALA] May ganito nang posisyon sa election na ito.")
        else:
            print(f"  [MALI] {err}")


# CANDIDATES
def nominate_candidate():
    print("\n--- MAGDAGDAG NG KANDIDATO ---")
    e = get_open_election()
    if not e:
        return
    try:
        positions = el_db.list_positions(e['election_id'])
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not positions:
        print("  [WALA] Wala pang posisyon. Magdagdag muna sa [2].")
        return
    print("\n  Mga Posisyon:")
    for p in positions:
        print(f"  [{p['position_id']}] {p['position_name']} (panalo: {p['max_winners']})")
    pid = demand_number("\n  Position ID: ")
    pos = next((p for p in positions if p['position_id'] == pid), None)
    if not pos:
        print("  [WALA] Hindi kabilang sa aktibong election ang posisyong iyon.")
        return
    render_position_card(pos)
    name = demand_text("  Buong Pangalan ng Kandidato: ")
    grade = demand_text("  Grade Level: ")
    section = demand_text("  Seksyon: ")
    party = demand_optional("  Partido (Enter kung independent): ")
    try:
        cid = el_db.add_candidate(pid, name, grade, section, party or None)
        print(f"\n  [TAPOS NA] Naidagdag na ang kandidato. Candidate ID: {cid}")
        render_candidate_card(el_db.find_candidate(cid))
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")


def show_candidates():
    print("\n--- TINGNAN ANG MGA KANDIDATO ---")
    e = get_open_election()
    if not e:
        return
    try:
        positions = el_db.list_positions(e['election_id'])
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not positions:
        print("  [WALA] Wala pang posisyon. Magdagdag muna sa [2].")
        return
    print(f"\n  Election: {e['title']} ({e['school_year']})")
    for p in positions:
        try:
            cands = el_db.list_candidates(p['position_id'])
        except mysql.connector.Error as err:
            print(f"  [MALI] {err}")
            return
        print(f"\n  [{p['position_id']}] {p['position_name']} (panalo: {p['max_winners']})")
        if not cands:
            print("      --- WALA PANG KANDIDATO ---")
            continue
        for c in cands:
            print(
                f"      #{c['candidate_id']} {c['full_name']} "
                f"| {c['grade_level']} - {c['section']} | {c['party'] or 'Independent'}"
            )


# VOTERS
def register_voter():
    print("\n--- MAGDAGDAG NG ESTUDYANTE (VOTER MASTERLIST) ---")
    vid = demand_text("  Student ID: ").upper()
    try:
        exist = el_db.find_voter(vid)
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if exist:
        print("  [PAALALA] Nasa masterlist na ang estudyanteng ito.")
        render_voter_card(exist)
        return
    name = demand_text("  Buong Pangalan (Apelyido, Pangalan): ")
    grade = demand_text("  Grade Level (hal. Grade 10): ")
    section = demand_text("  Seksyon: ")
    try:
        el_db.add_voter(vid, name, grade, section)
        print("\n  [TAPOS NA] Naidagdag na sa voter masterlist.")
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")


def show_voters():
    try:
        tally_rows = el_db.list_voters()
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not tally_rows:
        print("\n  Wala pang voter sa masterlist.")
        return
    print(f"\n--- VOTER MASTERLIST ({len(tally_rows)}) ---")
    for r in tally_rows:
        print(f"  [{r['voter_id']}] {r['full_name']} | {r['grade_level']} - {r['section']}")


# VOTING
def lodge_vote():
    print("\n--- BUMOTO (CAST VOTE) ---")
    e = get_open_election()
    if not e:
        return
    vid = demand_text("  Student ID ng boboto: ").upper()
    try:
        v = el_db.find_voter(vid)
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not v:
        print("  [WALA] Hindi nasa voter masterlist. Idagdag muna sa [4].")
        return
    render_voter_card(v)

    try:
        status = el_db.voter_status(e['election_id'], vid)
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not status:
        print("  [WALA] Wala pang posisyon ang election na ito. Magdagdag sa [2].")
        return

    print("\n  Kalagayan ng Pagboto:")
    for s in status:
        if s['voted']:
            print(f"  [{s['position_id']}] {s['position_name']}: NAKABOTO -> {s['voted_for']}")
        else:
            print(f"  [{s['position_id']}] {s['position_name']}: HINDI PA")
    open_positions = [s for s in status if not s['voted']]
    if not open_positions:
        print("\n  [PAALALA] Nakaboto na ang estudyanteng ito sa lahat ng posisyon.")
        return

    pid = demand_number("\n  Position ID na bobotoan: ")
    chosen = next((s for s in status if s['position_id'] == pid), None)
    if not chosen:
        print("  [WALA] Hindi kabilang sa aktibong election ang posisyong iyon.")
        return
    if chosen['voted']:
        print(f"  [PAALALA] Nakaboto na siya sa {chosen['position_name']} ({chosen['voted_for']}).")
        return

    try:
        cands = el_db.list_candidates(pid)
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not cands:
        print("  [WALA] Walang kandidato sa posisyong ito. Magdagdag muna sa [3].")
        return
    print(f"\n  Mga Kandidato para sa {chosen['position_name']}:")
    for c in cands:
        print(f"  [{c['candidate_id']}] {c['full_name']} | {c['party'] or 'Independent'}")

    cid = demand_number("\n  Candidate ID na iboboto: ")
    cand = next((c for c in cands if c['candidate_id'] == cid), None)
    if not cand:
        print("  [WALA] Wala sa posisyong ito ang kandidatong iyon.")
        return

    print("\n  --- KUMPIRMASYON NG BOTO ---")
    print(f"  Botante   : [{vid}] {v['full_name']}")
    print(f"  Posisyon  : {chosen['position_name']}")
    print(f"  Kandidato : [{cid}] {cand['full_name']} ({cand['party'] or 'Independent'})")
    confirm = input("  Kumpirmahin ang boto? (oo/hindi): ").strip().lower()
    if confirm not in ("oo", "o", "yes", "y"):
        print("  Kinansela. Walang naitalang boto.")
        return

    try:
        vote_id = el_db.cast_vote(e['election_id'], pid, cid, vid)
        print(f"\n  [TAPOS NA] Naitala ang boto. Vote ID: {vote_id}")
        print("  Salamat sa boto! Bawal nang baguhin ito.")
    except ValueError as err:
        print(f"  [HINDI PWEDE] {err}")
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")


# REPORTS
def show_voter_status():
    print("\n--- STATUS NG PAGBOTO NG ESTUDYANTE ---")
    e = get_open_election()
    if not e:
        return
    vid = demand_text("  Student ID: ").upper()
    try:
        v = el_db.find_voter(vid)
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not v:
        print("  [WALA] Wala sa voter masterlist ang estudyanteng ito.")
        return
    render_voter_card(v)
    try:
        status = el_db.voter_status(e['election_id'], vid)
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not status:
        print("\n  Wala pang posisyon ang election.")
        return
    voted = 0
    print(f"\n--- STATUS | {e['title']} ---")
    for s in status:
        if s['voted']:
            voted += 1
            print(f"  [{s['position_id']}] {s['position_name']}: NAKABOTO -> {s['voted_for']}")
        else:
            print(f"  [{s['position_id']}] {s['position_name']}: HINDI PA")
    print("-" * 44)
    print(f"  Nakaboto sa {voted} / {len(status)} posisyon")
    print("-" * 44)


def show_tally():
    print("\n--- RESULTS / TALLY BAWAT POSISYON ---")
    e = get_open_election()
    if not e:
        return
    try:
        tally_rows = el_db.results(e['election_id'])
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not tally_rows:
        print("  [WALA] Wala pang kandidato sa election na ito.")
        return

    groups = []
    for r in tally_rows:
        if not groups or groups[-1]['position_id'] != r['position_id']:
            groups.append({
                'position_id': r['position_id'],
                'position_name': r['position_name'],
                'max_winners': r['max_winners'],
                'candidates': [],
            })
        groups[-1]['candidates'].append(r)

    print(f"\n  Election: {e['title']} ({e['school_year']}) | Status: {e['status']}")
    for g in groups:
        total = sum(c['votes'] for c in g['candidates'])
        print(f"\n--- {g['position_name']} | Panalo: {g['max_winners']} | Kabuuang boto: {total} ---")
        if total == 0:
            print("  Wala pang boto sa posisyong ito.")
            continue
        prev_votes = None
        rank = 0
        for i, c in enumerate(g['candidates']):
            if c['votes'] != prev_votes:
                rank = i + 1
                prev_votes = c['votes']
            pct = (c['votes'] / total) * 100
            label = "  <== PANALO" if (c['votes'] > 0 and rank <= g['max_winners']) else ""
            print(
                f"  #{rank} [{c['candidate_id']}] {c['full_name']} "
                f"| {c['party'] or 'Independent'} | {c['votes']} boto ({pct:.1f}%){label}"
            )


def show_turnout():
    print("\n--- VOTER TURNOUT ---")
    e = get_open_election()
    if not e:
        return
    try:
        tally_rows = el_db.turnout(e['election_id'])
        overall = el_db.overall_turnout(e['election_id'])
    except mysql.connector.Error as err:
        print(f"  [MALI] {err}")
        return
    if not tally_rows:
        print("  [WALA] Wala pang voter sa masterlist.")
        return
    print(f"\n  Election: {e['title']} ({e['school_year']})")
    print(f"  {'GRADE LEVEL':<16}{'TOTAL':>8}{'BUMOTO':>9}{'HINDI':>8}")
    print("  " + "-" * 40)
    for r in tally_rows:
        print(
            f"  {r['grade_level']:<16}{r['total_voters']:>8}{r['voted']:>9}{r['not_voted']:>8}"
        )
    print("  " + "-" * 40)
    total = overall['total_voters'] or 0
    voted = overall['voters_who_voted'] or 0
    pct = (voted / total * 100) if total else 0
    print(f"  Kabuuang Voter      : {total}")
    print(f"  Bumoto              : {voted} ({pct:.1f}%)")
    print(f"  Hindi pa bumoboto   : {total - voted}")
    print(f"  Kabuuang boto naitala: {overall['total_votes_cast']} sa {overall['total_positions']} posisyon")
