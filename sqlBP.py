from werkzeug.security import (check_password_hash, generate_password_hash)
import sqlite3

db = sqlite3.connect("dbBP.db")


def reg(login, password):
    ''' Эта функция добавляет в таблицу usersBP пользователей '''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT `login` FROM `usersBP` WHERE `login` = '{login}';
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
                    '{generate_password_hash(password)}'
                )
            '''
        )
        db.commit()
        return {
            "msg": "Вы успешно зарегистрировались!",
            "status": True,
            "id": return_user_id(login)["id"]
        }
    return {
        "msg": "Такой логин занят!",
        "status": False
    }


def return_user_id(login):
    ''' Эта функция возвращает id '''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT `id` FROM `usersBP` WHERE `login` = '{login}';
        '''
    )
    res = cur.fetchall()
    db.commit()
    return {
        "id": res[0]["id"]
    }


def log(login, password):
    ''' Эта функция логинит юзера '''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT `id`, `login`, `password` FROM `usersBP`;
        '''
    )
    res = cur.fetchall()
    db.commit()
    for row in res:
        if row["login"] == login and check_password_hash(
                row['password'],
                password
        ):
            return {
                "msg": "Вы успешно вошли",
                "status": True,
                "id": row["id"]
            }
    else:
        return {
            "msg": "Неверный логин или пароль!",
            "status": False
        }


def check_password(user_id, password):
    ''' Эта функция проверяет ввод паролей на совпадение '''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT `id`, `password` FROM `usersBP`;
        '''
    )
    res = cur.fetchall()
    db.commit()
    for row in res:
        if row["id"] == int(user_id) and check_password_hash(
                row["password"],
                password
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


def del_profile(user_id):
    ''' Эта функция удаляет профиль пользователя '''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            DELETE FROM `usersBP` WHERE `id` = {user_id};
        '''
    )
    db.commit()
    return {
        "msg": "Профиль был успешно удалён",
        "status": True
    }


def count_seconds(user_id):
    '''Эта функция вносит общее число секунд в базу'''
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            UPDATE `usersBP` SET `seconds` = `seconds` + 1 WHERE `id` = {user_id};
        '''
    )
    db.commit()


def return_seconds(user_id):
    """Эта функция возвращает количество секунд"""
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT seconds FROM usersBP WHERE `id` = {user_id};
        '''
    )
    id_sec = cur.fetchall()
    db.commit()
    return {
        "seconds": id_sec[0][0]
    }


def return_place(user_id):
    """Эта функция сортирует пользователей по количеству секунд фокусировки"""
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT *, ROW_NUMBER() OVER(ORDER BY seconds DESC) AS place
            FROM usersBP
        '''
    )
    place_res = cur.fetchall()
    db.commit()
    for row in place_res:
        if row[0] == user_id:
            ind = place_res.index(row)
    return {
        "place": place_res[ind][4]
    }