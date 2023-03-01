from db import db
from sqlalchemy import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

#Kirjautuu sisään
def login(username, password):
    sql = text("SELECT id, username, password, role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = user.username
            session["role"] = user.role
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16) #EI VIELÄ KÄYTÖSSÄ
            return True
        else:
            return False

#Kirjautuu ulos
def logout():
    del session["username"]
    del session["role"]
    del session["user_id"]

#Lisää uuden käyttäjän sovellukseen
def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)")
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)


def get_role():
    return session.get("role", 0)

def user_id():
    return session.get("user_id", 0)