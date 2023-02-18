from db import db
from flask import session
from sqlalchemy import text
import users

def get_sections():
    sql = text("SELECT * FROM sections ORDER BY name")
    result = db.session.execute(sql)
    sections = result.fetchall()
    return sections

def get_section(id):
    sql = text("SELECT id, name FROM sections WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    section = result.fetchone()
    return section

#EI KÄYTETÄ
def add_section(name, access):
    sql = text("INSERT INTO sections (name, access) VALUES (:name, :access)")
    db.session.execute(sql, {"name":name, "access":access})
    db.session.commit()
    return True

def remove_section(id):
    if users.get_role() == 2:
        sql = text("UPDATE sections SET access=0 WHERE id=:id")
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    return False
