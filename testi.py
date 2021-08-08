from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
	return "Heipparallaa!"

@app.route("/numerot")
def numerot():
	content = ""
	for i in range(100):
		content += str(i + 1) + " "
	return content

@app.route("/parametri/<int:nbr>")
def parametri(nbr):
	return "Sivulla on numero " + str(nbr)

@app.route("/template")
def template():
	return render_template("index.html")

@app.route("/jinja")
def jinja():
	words = ["heiippa", "moikka", "tere"]
	return render_template("index.html", name="Jami", items=words)

@app.route("/form")
def form():
	return render_template("form.html")

@app.route("/form", methods=["POST"])
def result():
	return render_template("form.html", name=request.form["name"])

@app.route("/redir")
def redir():
	return redirect(url_for("index"))
	
@app.route("/print")
def printText():
	result = db.session.execute("SELECT msg FROM messages")
	messages = result.fetchall()
	return render_template("db.html", count=len(messages), messages=messages)

@app.route("/new")
def newMessageForm():
	return render_template("new.html")

@app.route("/send", methods=["POST"])
def sendMessage():
	content = request.form["content"]
	sql = "INSERT INTO messages (msg) VALUES (:content)"
	db.session.execute(sql, {"content":content})
	db.session.commit()
	return redirect("/print")