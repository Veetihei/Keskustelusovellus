from db import db
from flask import session
from sqlalchemy import text
import users

#TÄMÄ VAIN MALLINA
def get_thread(id):
    sql = text("SELECT * FROM threads WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    section = result.fetchone()
    return section

def get_answers(id):
    sql = text("SELECT A.sent_at, A.answer, U.username FROM answers A, users U WHERE " \
        "A.user_id = U.id AND A.topic_id=:id AND A.visible=TRUE ORDER BY A.sent_at")
    results = db.session.execute(sql, {"id":id})
    answers = results.fetchall()
    return answers

def answer(thread_id, answer):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO answers (topic_id, sent_at, answer, user_id) "\
        "VALUES (:thread_id, NOW(), :answer, :user_id)")
    db.session.execute(sql, {"thread_id":thread_id, "answer":answer, "user_id":user_id})
    db.session.commit()
    return True



#MALLI
def create(topic, message, section):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO threads (topic, created_at, message, user_id, section_id) " \
        "VALUES (:topic, NOW(), :message, :user_id, :section_id)")
    db.session.execute(sql, {"topic":topic, "message":message, "user_id":user_id, "section_id":section})
    db.session.commit()
    return True