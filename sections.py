from db import db
from flask import session
from sqlalchemy import text
import users

def get_sections():
    role = users.get_role()
    print("KÄYTTÄJÄN ROOLI ON: --", role)
    if role == 2:
        sql = text("SELECT name, id FROM sections ORDER BY name")
    else:
        sql = text("SELECT name, id FROM sections WHERE access = 1 ORDER BY name")
    result = db.session.execute(sql)
    sections = result.fetchall()
    return sections

def get_section(id):
    sql = text("SELECT id, name FROM sections WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    section = result.fetchone()
    return section
