from werkzeug.security import (check_password_hash, generate_password_hash)
import sqlite3

db = sqlite3.connect("dbBP.db")

def reg(login, psw):
    ''' Эта функция добавляет в таблицу usersBP пользователей '''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT `login` FROM `usersBP` WHERE `login` = '{login}'
        '''
    )
    res = cur.fetchall()
    db.commit()
    if len(res) == 0:
        cur.execute(
            f'''
                INSERT INTO `usersBP`(`login`, `password`)
                VALUES (
                    '{login}',
                    '{generate_password_hash(psw)}'
                )
            '''
        )
        db.commit()
        return {
            "msg": "Вы успешно зарегистрировались!",
            "status": True,
            "id": get_user_id(login)["id"]
        }
    return {
        "msg": "Такой логин занят!",
        "status": False
    }


def get_user_id(login):
    ''' Эта функция возвращает id '''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT `id` FROM `usersBP` WHERE `login` = '{login}'
        '''
    )
    res = cur.fetchall()
    db.commit()
    return {
        "id": res[0]["id"]
    }


def log(login, psw):
    ''' Эта функция логинит юзера '''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(f'''SELECT `id`, `login`, `password` FROM `usersBP`''')
    res = cur.fetchall()
    db.commit()
    for row in res:
        if row["login"] == login and check_password_hash(
            row['password'],
            psw
        ):
            return {
                "msg": "Вы успешно вошли",
                "status": True,
                "id": row["id"]
            }
    else:
        return {
            "msg": "Неверный логин/пароль!",
            "status": False
        }


def chek_psw(user_id, psw):
    ''' Эта функция проверяет пароли '''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(f'''SELECT `id`, `password` FROM `usersBP`''')
    res = cur.fetchall()
    db.commit()
    for row in res:
        if row["id"] == int(user_id) and check_password_hash(
            row["password"],
            psw
        ):
            return {
                "msg": "Пароли совпали",
                "status": True,
            }
    else:
        return {
            "msg": "Пароли не совпали",
            "status": False
        }