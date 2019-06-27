import sqlite3
import os
from contextlib import suppress
from config import config
from tournament import simple_product

def init_db():
    with suppress(FileNotFoundError):
        os.remove(config["database"])
    conn = sqlite3.connect(config["database"])
    c = conn.cursor()
    for table in config["tables"]:
        print(f"CREATE TABLE {table} ({', '.join(column for column in config[f'{table}_columns'])})")
        c.execute(f"CREATE TABLE {table} ({', '.join(column for column in config[f'{table}_columns'])})")
        conn.commit()
    conn.close()


def save_user(user_data: dict):
    conn = sqlite3.connect(config["database"])
    c = conn.cursor()
    c.execute(f"select * from player where id = \'{user_data['from']['id']}\'")
    if len(c.fetchall()) != 0:
        return False

    c.execute(
        f"INSERT INTO player VALUES (\'{user_data['from']['id']}\', \'{user_data['from']['name'].split(' ')[0][:-1]}\' , "
        f"'{user_data['from']['name'].split(' ')[1]}\', null)")

    conn.commit()
    conn.close()
    return True


def tournament(user_data: dict, sport: str):
    conn = sqlite3.connect(config["database"])
    c = conn.cursor()
    c.execute(f"select * from tournament where id = \'{user_data['from']['id']}\' and sport = \'{sport}\' ")
    if len(c.fetchall()) != 0:
        return False

    save_user(user_data)
    c.execute(f"INSERT INTO tournament VALUES (\'{user_data['from']['id']}\', null, null, \'{sport}\' )")

    conn.commit()
    conn.close()
    return True


def waitlist(user_data: dict, sport: str):
    conn = sqlite3.connect(config["database"])
    c = conn.cursor()
    save_user(user_data)

    c.execute(f"select * from waitlist where sport = \'{sport}\'")
    player2 = c.fetchall()
    if len(player2) == 0:

        c.execute(f"INSERT INTO waitlist VALUES (\'{user_data['from']['id']}\', \'{sport}\' ,null, null)")
        conn.commit()
        conn.close()
        return False
    else:
        c.execute(f"select * from waitlist where player_id = \'{user_data['from']['id']}\' and sport = \'{sport}\'")
        if len(c.fetchall()) != 0:
            return 5
        c.execute(f"delete from waitlist where player_id = \'{player2[-1][0]}\'")
        conn.commit()
        c.execute(f"select name, surname from player where id = \'{player2[-1][0]}\'")
        return ", ".join(c.fetchone())


def remove_user(user_data: dict, sport: str):
    conn = sqlite3.connect(config["database"])
    c = conn.cursor()
    c.execute(
        f"DELETE FROM tournament where id = \'{user_data['from']['id']}\' and sport = \'{sport}\'")
    conn.commit()
    conn.close()


def get_users():
    conn = sqlite3.connect(config["database"])
    c = conn.cursor()
    c.execute(f"SELECT * FROM player")
    users = c.fetchall()
    conn.close()
    return users


def get_users_tournament(sport):
    conn = sqlite3.connect(config["database"])
    c = conn.cursor()
    c.execute(f"SELECT * FROM tournament where sport = \'{sport}\'")
    users = c.fetchall()
    conn.close()
    return users


def get_tournament(sport):
    ids = get_users_tournament(sport)
    conn = sqlite3.connect(config["database"])
    c = conn.cursor()
    c.execute(f"SELECT * FROM player")
    print(c.fetchall())
    users = []
    for id in ids:
        c.execute(f"SELECT name, surname FROM player where id = '{id[0]}'")
        users.append(", ".join(c.fetchone()))
    return simple_product(users)