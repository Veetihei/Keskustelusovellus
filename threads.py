from db import db
from flask import session
from sqlalchemy import text
import users


##EI KÄYTÖSSÄ, ANTAA KAIKKI UUSIMMAT KETJUT ETUSIVULLE
def get_threads():
    if session.role == 2:
        sql = text("SELECT T.topic, T.id, T.created_at, U.name FROM ")
    else:
        sql = text("SELECT name, id FROM sections WHERE access = 1 ORDER BY name")
    result = db.session.execute(sql, {"role":session.role})
    sections = result.fetchall()
    return sections

def section_threads(id):
    sql = text("SELECT T.id, T.topic, T.created_at, T.visible, T.section_id, U.username, T.user_id FROM threads T, users U " \
        "WHERE T.user_id = U.id AND T.section_id = :id ORDER BY T.id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def create(topic, message, section):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO threads (topic, created_at, message, user_id, section_id) " \
        "VALUES (:topic, NOW(), :message, :user_id, :section_id)")
    db.session.execute(sql, {"topic":topic, "message":message, "user_id":user_id, "section_id":section})
    db.session.commit()
    sql = text("SELECT id FROM threads WHERE topic=:topic ORDER BY created_at DESC")
    result = db.session.execute(sql, {"topic":topic})
    id = result.fetchone()
    return True, id

def get_thread(id):
    sql = text("SELECT T.topic, T.id, T.created_at, T.message, T.section_id, T.user_id, U.username FROM threads T, Users U " \
        "WHERE T.user_id=U.id AND T.id=:id AND T.visible=1")
    result = db.session.execute(sql, {"id":id})
    section = result.fetchone()
    return section

def search(query):
    role = users.get_role()
    if role == 2:
        sql = text("SELECT T.topic, T.id, T.created_at, U.username FROM threads T, Users U " \
            "WHERE T.user_id = U.id AND T.topic like :query")
    else:
        sql = text("SELECT T.topic, T.id, T.created_at, U.username FROM threads T, Users U, " \
            "sections S WHERE T.user_id = U.id AND T.section_id = S.id AND S.access = 1 AND T.topic like :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    threads = result.fetchall()
    return threads
    
def delete_thread(id):
    sql = text("SELECT user_id FROM threads WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user_id = result.fetchone()[0]
    if users.get_role() == 2 or users.user_id() == user_id:
        sql = text("UPDATE threads SET visible=0 WHERE id=:id")
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    return False
