from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from os import getenv

#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False