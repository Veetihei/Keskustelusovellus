from db import db
from flask import session
from sqlalchemy import text
import users

#PALAUTTAA ilman votes
def get_answers(id):
    sql = text("SELECT A.id, A.user_id, A.sent_at, A.answer, U.username FROM answers A, users U WHERE " \
        "A.user_id = U.id AND A.topic_id=:id AND A.visible=1 ORDER BY A.sent_at")
    results = db.session.execute(sql, {"id":id})
    answers = results.fetchall()
    return answers

def get_answers_votes(id):
    sql = text("SELECT A.id, A.user_id, A.sent_at, A.answer, U.username, SUM(V.vote) FROM answers A LEFT JOIN " \
               "votes V ON A.id = V.answer_id LEFT JOIN users U ON U.id = A.user_id WHERE A.visible=1 AND " \
                "A.topic_id=:id GROUP BY A.id, U.id ORDER BY A.sent_at")
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

def delete_message(id):
    sql = text("SELECT user_id FROM answers WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user_id = result.fetchone()[0]
    print(user_id)
    print(users.user_id())
    if users.get_role() == 2 or users.user_id() == user_id:
        sql = text("UPDATE answers SET visible=0 WHERE id=:id")
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    return False

def vote(id, vote, user):
    sql = text("SELECT * FROM votes WHERE answer_id=:answer_id AND user_id=:user_id")
    result = db.session.execute(sql, {"answer_id":id, "user_id":user})
    check = result.fetchone()
    if check and check.vote == vote:
        return False
    elif check and check.vote != vote:
        sql = text("UPDATE votes SET vote=:vote WHERE user_id=:user_id AND answer_id=:answer_id")
        db.session.execute(sql, {"vote":vote, "user_id":user, "answer_id":id})
        db.session.commit()
        return True        
    else:
        sql = text("INSERT INTO votes (answer_id, user_id, vote) VALUES (:id, :user, :vote)")
        db.session.execute(sql, {"id":id, "user":user, "vote":vote})
        db.session.commit()
        return True

