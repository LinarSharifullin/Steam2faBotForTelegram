import sqlite3


def create_db():
    con = sqlite3.connect('files/main_base.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS accounts '
                '(login TEXT, shared_secret TEXT)')
    con.commit()
    cur.close()
    con.close()

def add_accounts(accounts):
    con = sqlite3.connect('files/main_base.db')
    cur = con.cursor()
    for account_data in accounts:
        login = list(account_data.keys())[0]
        shared_secret = account_data[login]
        cur.execute('INSERT OR IGNORE INTO accounts '
            'VALUES(?, ?)', (login, shared_secret))
    con.commit()
    cur.close()
    con.close()

def get_shared_secret(login):
    con = sqlite3.connect('files/main_base.db')
    cur = con.cursor()
    cur.execute('SELECT shared_secret FROM accounts WHERE login = ?', 
        (login, ))
    db_items = cur.fetchall()
    cur.close()
    con.close()
    return db_items


if __name__ == '__main__':
    create_db()