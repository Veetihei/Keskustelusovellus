from app import app
from flask import redirect, render_template, request, session
from sqlalchemy import text
#import kaikki python filet
import answers
import sections
import threads
import users


#TEHTY so far
@app.route("/")
def index():
    section_list = sections.get_sections()
    return render_template("index.html", sections=section_list)

#TEHTY so far
@app.route("/section/<int:id>")
def section(id):
    section = sections.get_section(id)
    section_threads = threads.section_threads(id)
    return render_template("section.html", section=section, threads=section_threads)

###EN TIIÄ
    sql = text("SELECT topic, message FROM threads WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    row = result.fetchone()
    topic = row.topic
    message = row.message
    sql = text("SELECT sent_at, answer FROM answers WHERE topic_id=:topic_id")
    result = db.session.execute(sql, {"topic_id":id})
    answers = result.fetchall()
    return render_template("thread.html", topic=topic, message=message, answers=answers, id=id)
###

#TEHTY
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")

#TEHTY
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

#TEHTY
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        role = request.form["role"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if password1 == "":
            return render_template("error.html", message="Salasana ei voi olla tyhjä")
        if users.register(username, password1, role):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

#TEHTY
@app.route("/search", methods=["GET"])
def search():
    query = request.args["query"]
    list = threads.search(query)
    return render_template("search.html", threads=list, query=query)

#TEHTY
@app.route("/new/<int:id>")
def new(id):
    section = sections.get_section(id)
    return render_template("new.html", section=section)

#TEHTY
@app.route("/create/<int:id>", methods=["POST"])
def create(id):
    topic = request.form["topic"]
    message = request.form["message"]
    section = request.form["section"]
    if threads.create(topic, message, section):
        return redirect("/") #MUOKKAA MENEMÄÄN KETJUUN
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

#TEHTY
@app.route("/answer/<int:id>", methods=["POST"])
def answer(id):
    thread_id = request.form["thread"]
    answer = request.form["message"]
    if answers.answer(thread_id, answer):
        return redirect("/thread/"+thread_id) #MUOKKAA MENEMÄÄN KETJUUN
    else:
        return render_template("error.html", message="Vastaaminen ei onnistunut")

#ABOUT THETY
@app.route("/thread/<int:id>")
def thread(id):
    row = threads.get_thread(id)
    thread_answers = answers.get_answers(id)
    return render_template("thread.html", thread=row, answers=thread_answers)

