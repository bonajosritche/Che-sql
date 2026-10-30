# Student Election Voting System

Kini nga sistema maoy CLI nga botohanan sa eskuylahan. Naa kini election,
posisyon, kandidato, voter masterlist, ug boto. Ang database mismo maoy
mopugong sa **doble nga boto** pinaagi sa unique key, ug naa kini tally,
percentage, winner detection, ug turnout matag grade level.

## Unsa ang kinahanglan

- **Python 3.8 o mas bag-o**
- **XAMPP** (MySQL/MariaDB)
- **mysql-connector-python**

## 1) I-install ang MySQL connector

```powershell
pip install mysql-connector-python
```

## 2) Sugdi ang XAMPP

1. Ablihi ang **XAMPP Control Panel**.
2. Pindota ang **Start** tapad sa **MySQL**.
3. Siguroha nga **green** ang kolor sa MySQL.

## 3) I-import ang database

1. Ablihi ang `http://localhost/phpmyadmin`.
2. Pindota ang **Import** tab.
3. Pilia ang `schema_election.sql` (naa sa sama nga folder).
4. Pindota ang **Go** o **Import**.
5. Siguroha nga makita ang `school_election_db` sa lista sa wala.

## 4) Koneksyon sa database

| Variable | Default |
| --- | --- |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `3306` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | *(walay password)* |
| `DB_NAME` | `school_election_db` |

Kung lahi ang setup:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
$env:DB_NAME = "school_election_db"
```

## 5) Padagana ang sistema

```powershell
cd "C:\Users\suete\Documents\system for sale\ritchie=election=student_election_system"
python main_election.py
```

> Kung ibalhin ang folder sa lain nga computer, ilisi ang `cd` path sa
> aktwal nga lokasyon sa folder.


Dapat makita nimo ang **"Koneksyon sa Student Election database ay OK na."**

## Mga file

| File | Tumong |
| --- | --- |
| `schema_election.sql` | Naghimo sa `elections`, `positions`, `candidates`, `voters`, `votes` |
| `el_db.py` | SQL sa election, posisyon, kandidato, voter, boto, ug tally |
| `ballot_desk.py` | Flow sa menu ug validation sa boto |
| `main_election.py` | Ang CLI menu |
| `test_compile.py` | Pagsusi kung walay syntax error |

## Menu

| Numero | Aksyon |
| --- | --- |
| `1` | Paghimo og bag-ong election |
| `2` | Pagdugang og posisyon |
| `3` | Pagdugang og kandidato |
| `4` | Pagdugang og estudyante (voter masterlist) |
| `5` | Pagboto |
| `6` | Tan-awa ang mga kandidato |
| `7` | Results / tally matag posisyon |
| `8` | Voter turnout (matag grade level) |
| `9` | Status sa pagboto sa estudyante |
| `10` | Isara ang election |
| `11` | Listahan sa elections |
| `0` | Gula |

## Unsaon paggamit

1. Paghimo og election (`1`). Kini **OPEN** dayon.
2. Pagdugang og mga posisyon (`2`), pananglitan President, Vice President,
   Secretary.
3. Pagdugang og kandidato (`3`) sa matag posisyon.
4. Pagdugang og voters sa masterlist (`4`).
5. Pagboto (`5`). Pilia ang election ug posisyon, dayon ang kandidato.
6. Tan-awa ang tally (`7`) ug turnout (`8`).
7. Kung tapos na, isara ang election (`10`). Dili na makaboto pag-usab.

## Importante nga lagda

- **Usa ka boto ra** ang usa ka voter sa matag posisyon. Gibantayan kini sa
  `UNIQUE (election_id, voter_id, position_id)`.
- Dili makaboto kung **CLOSED** na ang election.
- Kung patas ang boto, ang sistema magpakita sa tanan nga naay pinakataas nga
  boto isip tie, dili ra usa ka winner.
- Ang `max_winners` sa posisyon nagtugot og labaw sa usa ka winner kung gikinahanglan.

## Giunsa pagtipig ang datos

Ang tanan naa sa MySQL sa `school_election_db`:

- `elections` — titulo, school year, status (`OPEN`, `CLOSED`)
- `positions` — posisyon ug `max_winners`
- `candidates` — kandidato matag posisyon
- `voters` — masterlist sa mga botante
- `votes` — matag boto, may petsa ug oras

## Troubleshooting

| Sayop / Mensahe | Solusyon |
| --- | --- |
| `Can't connect to MySQL server on 'localhost:3306'` | Wala nagdagan ang MySQL. Pindota ang **Start** sa XAMPP. |
| `Unknown database 'school_election_db'` | Wala pa na-import ang `schema_election.sql`. |
| `Table 'school_election_db.votes' doesn't exist` | I-import pag-usab ang schema. |
| `Access denied for user 'root'@'localhost'` | I-set ang `DB_PASSWORD`. |
| `ModuleNotFoundError: No module named 'mysql'` | `pip install mysql-connector-python` |
| `Duplicate entry` sa boto | Nakaboto na ang voter sa maong posisyon. |
| `Duplicate entry` sa posisyon | Naa nay parehas nga posisyon sa election. |

## Backup sa datos

1. Adto sa phpMyAdmin.
2. Pilia ang `school_election_db`.
3. **Export** → **Go**.
4. Tipigi ang `.sql` file.

## Sulayi ang code

```powershell
python test_compile.py
```

Dapat `OK` ang mogawas.
