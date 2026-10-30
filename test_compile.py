import py_compile

py_compile.compile('el_db.py', doraise=True)
py_compile.compile('ballot_desk.py', doraise=True)
py_compile.compile('main_election.py', doraise=True)
print('OK')
