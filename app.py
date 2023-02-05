from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route("/")
def index():
    sql = text("SELECT id, topic, created_at FROM threads ORDER BY id DESC")
    result = db.session.execute(sql)
    threads = result.fetchall()
    return render_template("index.html", threads=threads)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    message = request.form["message"]
    sql = text("INSERT INTO threads (topic, created_at, message) VALUES (:topic, NOW(), :message) RETURNING id")
    db.session.execute(sql, {"topic":topic, "message":message})
    db.session.commit()
    return redirect("/")

@app.route("/reply/<int:id>")
def reply(id):
    sql = text("SELECT topic FROM threads WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    return render_template("reply.html", id=id, topic=topic)

@app.route("/answer", methods=["POST"])
def answer():
    topic_id = request.form["id"]
    answer = request.form["message"]
    sql = text("INSERT INTO answers (topic_id, sent_at, answer) VALUES (:topic_id, NOW(), :answer)")
    db.session.execute(sql, {"topic_id": topic_id, "answer": answer})
    db.session.commit()
    return redirect("/thread/" + str(topic_id))

@app.route("/thread/<int:id>")
def thread(id):
    sql = text("SELECT topic, message FROM threads WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    row = result.fetchone()
    topic = row.topic
    message = row.message
    sql = text("SELECT sent_at, answer FROM answers WHERE topic_id=:topic_id")
    result = db.session.execute(sql, {"topic_id":id})
    answers = result.fetchall()
    return render_template("thread.html", topic=topic, message=message, answers=answers, id=id)