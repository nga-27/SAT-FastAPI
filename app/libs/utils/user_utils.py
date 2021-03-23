import os
import json
import datetime
import secrets

from app import main

from .classes import User


def serialize_users():
    users = []
    for username in main.USER:
        obj = dict(username=username,
                   name=main.USER[username]['name'], uuid=main.USER[username]['uuid'])
        users.append(obj)
    return users, 200


def serialize_user(username: str):
    obj = {}
    if username in main.USER:
        obj = User(username=username,
                   name=main.USER[username]['name'],
                   uuid=main.USER[username]['uuid'],
                   vq_key="<hidden>",
                   password_hash="<hidden>")
    return obj, 200


def check_user(username: str):
    if username in main.USER:
        return True
    return False


def add_user(user: User):
    if user.username in main.USER:
        return {"value": f"Username '{user.username}' already exists."}, 409

    main.USER[user.username] = {
        "name": user.name,
        "password_hash": user.password_hash,
        "username": user.username,
        "uuid": user.uuid,
        "vq_key": user.vq_key
    }
    update_user(main.USER)
    return {"value": f"User '{user.username}' added."}, 201


def remove_user(username: str, password):
    if username in main.USER:
        user_obj = main.USER[username]
        if user_obj['password_hash'] != '':
            correct_password = secrets.compare_digest(
                password, user_obj['password_hash'])
            if correct_password:
                main.USER.pop(username)
                update_user(main.USER)
                return {"value": f"User '{username}' deleted."}, 200
        else:
            main.USER.pop(username)
            update_user(main.USER)
            return {"value": f"User '{username}' deleted."}, 200
        return {"value": f"User '{username}' is unauthorized"}, 401
    return {"value": f"User '{username}' not found."}, 404


def update_user(user_obj):
    with open(main.USER_PATH, 'w') as usf:
        json.dump(user_obj, usf)
        usf.close()
    return
