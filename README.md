# Student Election - Simple CRUD

4 ka file. Usa ka table. Kada function mag-close sa connection.

## Setup (4 steps)

1. `pip install mysql-connector-python`
2. Ablihi ang XAMPP -> **Start** ang **MySQL**
3. Adto `http://localhost/phpmyadmin` -> **Import** -> pili
   `schema_election.sql` -> **Go**
4. Padagana:

```powershell
cd "C:\Users\suete\Documents\SYSTEM--HUHUa\ritchie=election=student_election_system\simple_version"
python election_app.py
```

## Table

```
candidates
├── id             INT (auto, primary key)
├── name           VARCHAR(100)
└── position_name  VARCHAR(50)
```

## Menu

| # | Operation | Function |
| --- | --- | --- |
| 1 | Create | `add_candidate()` |
| 2 | Read | `get_candidates()` |
| 3 | Update | `update_candidate()` |
| 4 | Delete | `delete_candidate()` |
| 0 | Exit | `break` |

## Files

| File | Lines | Trabaho |
| --- | --- | --- |
| `schema_election.sql` | 54 | Database + table + sample data |
| `db_election.py` | 88 | Tanang SQL |
| `election_app.py` | 100 | Menu + validation |
| `README.md` | 100 | Kini |

## Paliwanag sa code (Bisaya)

| Function | Paliwanag |
| --- | --- |
| `connect()` | Mohimo og koneksyon sa MySQL |
| `ask()` | Mangayo og input; numero ra kung `number=True` |
| `add_candidate()` / `add()` | CREATE - mopasulod og bag-ong record |
| `get_candidates()` / `show_all()` | READ - mokuha ug ipakita ang record |
| `update_candidate()` / `update()` | UPDATE - usbon ang record pinaagi sa ID |
| `delete_candidate()` / `delete()` | DELETE - papason, mangutana una |
| `main()` | Menu loop; `0` = exit |

## Syntax glossary (Bisaya)

| Syntax | Meaning |
| --- | --- |
| `def` | Mohimo og function |
| `import` | Mogamit og laing module/file |
| `return` | Mobalik sa value ug matapos ang function |
| `while True` / `if / else` | Loop ug kondisyon (kung / dili) |
| `try / except / finally` | Dakpon ang error; sigurohon ma-close |
| `%s` | Parameterized query (safe sa SQL injection) |
| `commit()` / `rollback()` | I-save / i-cancel ang SQL |

## Requirements checklist

- Python + MySQL only — `mysql.connector`
- Database + table — `school_election_db.candidates`
- Functions — kada operation naay function
- Menu — `while True` + `input`
- Validation — `ask()` (text ug numero)
- Exception handling — `try / except` + `rollback()`
- Parameterized — `%s` sa tanan
- Delete confirmation — `oo/hindi`
- Exit — `[0]`

## Kung naay error

| Error | Solusyon |
| --- | --- |
| `Can't connect to MySQL server` | Wala nagdagan ang MySQL. Start sa XAMPP. |
| `Unknown database` | Wala pa na-import ang SQL file. |
| `Access denied for 'root'` | Butangi og password ang `DB` sa `db_election.py`. |
| `No module named 'mysql'` | `pip install mysql-connector-python` |

## Q&A (3 ra ka importante)

**Ngano `%s`?** — Parameterized query. Dili ma-hack ang database pinaagi sa
pag-type og SQL sa input.

**Ngano `commit()`?** — Para ma-save gyud ang data. Kung naay error, ang
`rollback()` mo-cancel.

**Ngano `finally`?** — Para siguro nga ma-close ang cursor ug connection,
bisan naay error.
