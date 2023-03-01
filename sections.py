from db import db
from flask import session
from sqlalchemy import text
import users


#Palauttaa aihealueet etusivulle ketjujen lukumäärän kanssa
def get_sections_num():
    sql = text("SELECT S.id, S.name, S.access, COUNT(T.id) FROM sections S LEFT JOIN threads T ON S.id = T.section_id AND T.visible = 1 GROUP BY S.id")
    result = db.session.execute(sql)
    sections = result.fetchall()
    return sections

#Hakee tietyn ketjun
def get_section(id):
    sql = text("SELECT id, name FROM sections WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    section = result.fetchone()
    return section



#Luo uuden aihealueen
def add_section(name, access):
    sql = text("INSERT INTO sections (name, access) VALUES (:name, :access)")
    db.session.execute(sql, {"name":name, "access":access})
    db.session.commit()
    return True

#Poistaa aihealueen
def remove_section(id):
    if users.get_role() == 2:
        sql = text("UPDATE sections SET access=0 WHERE id=:id")
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    return False
