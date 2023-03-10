from app import app
from flask import redirect, render_template, request, session
from sqlalchemy import text
#import kaikki python filet
import answers
import sections
import threads
import users
from db import db


#Etusivu
@app.route("/")
def index():
    section_list = sections.get_sections_num()
    return render_template("index.html", sections=section_list)

#Tietyn aihealueen sivu
@app.route("/section/<int:id>")
def section(id):
    section = sections.get_section(id)
    section_threads = threads.section_threads(id)
    return render_template("section.html", section=section, threads=section_threads)

#Sisäänkirjautuminen
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")

#Uloskirjautuminen
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

#Ohjeet sivu
@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

#Rekisteröitymis sivu ja uuden käyttäjän luonti
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        role = request.form["role"]
        if len(username) > 20:
            return render_template("error.html", message="Käyttäjänimi on liian pitkä, sen täytyy olla korkeintaan 20 merkkiä")
        if len(username) < 3:
            return render_template("error.html", message="Käyttäjänimi on liian lyhyt, sen täytyy olla vähintään 3 merkkiä")
        if len(password1) < 5:
            return render_template("error.html", message="Salasana on liian lyhyt, sen täytyy olla vähintään 5 merkkiä")
        if len(password1) > 20:
            return render_template("error.html", message="Salasana on liian pitkä, sen täytyy olla korkeintaan 20 merkkiä")
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if password1 == "":
            return render_template("error.html", message="Salasana ei voi olla tyhjä")
        if users.register(username, password1, role):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

#Hakukonesivu
@app.route("/search", methods=["GET"])
def search():
    query = request.args["query"]
    list = threads.search(query)
    print(list)
    return render_template("search.html", threads=list, query=query)

#Uuden ketjun luomissivu
@app.route("/new/<int:id>")
def new(id):
    section = sections.get_section(id)
    return render_template("new.html", section=section)

#Uuden ketjun luominen
@app.route("/create/<int:id>", methods=["POST"])
def create(id):
    topic = request.form["topic"]
    message = request.form["message"]
    section = request.form["section"]
    if len(topic) > 100:
        return render_template("error.html", message="Otsikko on liian pitkä")
    if len(topic) < 3:
        return render_template("error.html", message="Otsikko on liian lyhyt, sen pitää olla vähintään 3 merkkiä")
    if len(message) > 5000:
        return render_template("error.html", message="Viesti on liian pitkä")
    values = threads.create(topic, message, section)
    thread_id = str(values[1][0])
    if values[0]:
        return redirect("/thread/"+thread_id)
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

#Ketjuun vastaaminen
@app.route("/answer/<int:id>", methods=["POST"])
def answer(id):
    thread_id = request.form["thread"]
    answer = request.form["message"]
    if len(answer) > 5000:
        render_template("error.html", message="Viesti on liian pitkä")
    if answers.answer(thread_id, answer):
        return redirect("/thread/"+thread_id)
    else:
        return render_template("error.html", message="Vastaaminen ei onnistunut")

#Viestin äänestäminen
@app.route("/vote/<int:id>", methods=["POST"])
def vote(id):
    thread_id = request.form["thread_id"]
    vote = int(request.form["up_down"])
    user = request.form["user_id"]
    if answers.vote(id, vote, user):
        return redirect("/thread/"+thread_id)
    else:
        return redirect("/thread/"+thread_id)

#Viestin poistaminen
@app.route("/delete_message/<int:id>", methods=["POST"])
def delete_message(id):
    thread_id = request.form["thread_id"]
    if answers.delete_message(id):
        return redirect("/thread/"+thread_id)
    else:
        return render_template("error.html", message="Vastauksen poistaminen ei onnistunut")

#Tietyn ketjun sivu
@app.route("/thread/<int:id>")
def thread(id):
    row = threads.get_thread(id)
    thread_answers = answers.get_answers_votes(id)
    return render_template("thread.html", thread=row, answers=thread_answers)

#Ketjun poistaminen
@app.route("/delete_thread/<int:id>", methods=["POST"])
def delete_thread(id):
    section_id = request.form["section_id"]
    if threads.delete_thread(id):
        return redirect("/section/"+section_id)
    else:
        return render_template("error.html", message="Poistaminen ei onnistunut")

#Aihealueen poistaminen
@app.route("/remove_section/<int:id>", methods=["POST"])
def remove_section(id):
    if sections.remove_section(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Poistaminen ei onnistunut")

#Uuden aihealueen luominen
@app.route("/new_section", methods=["GET", "POST"])
def new_section():
    if request.method == "GET":
        return render_template("new_section.html")
    if request.method == "POST":
        topic = request.form["topic"]
        access = request.form["access"]
        if sections.add_section(topic, access):
            return redirect("/")
        else:
            return render_template("error.html", message="Aihealueen lisäys ei onnistunut")
        
