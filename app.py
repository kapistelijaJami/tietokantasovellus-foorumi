from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
uri = str(getenv("DATABBASE_URL"))
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = uri
db = SQLAlchemy(app)

@app.route("/")
def index():
	result = db.session.execute("SELECT * FROM area")
	
	areas = result.fetchall()
	return render_template("listAreas.html", count = len(areas), areas = areas)

@app.route("/area/<int:areaId>")
def area(areaId):
	sql = "SELECT * FROM thread WHERE area_id = :AREA_ID"
	result = db.session.execute(sql, {"AREA_ID": areaId})
	
	threads = result.fetchall()
	return render_template("listThreads.html", count = len(threads), threads = threads, areaId = areaId)

@app.route("/thread/<int:threadId>")
def thread(threadId):
	sql = "SELECT * FROM message WHERE thread_id = :THREAD_ID"
	result = db.session.execute(sql, {"THREAD_ID": threadId})
	
	messages = result.fetchall()
	return render_template("listMessages.html", count = len(messages),
		messages = messages,
		threadId = threadId)

@app.route("/send/<int:threadId>", methods=["POST"])
def sendMessage(threadId):
	content = request.form["content"]
	sql = "INSERT INTO message (msg, sent_at, thread_id) VALUES (:content, NOW(), :THREAD_ID)"
	
	db.session.execute(sql, {"content": content, "THREAD_ID": threadId})
	db.session.commit()
	return redirect("/thread/" + str(threadId))


@app.route("/createThread/<int:areaId>")
def createThreadForm(areaId):
	return render_template("createThread.html", areaId=areaId)

@app.route("/createThread/<int:areaId>", methods=["POST"])
def createThread(areaId):
	topic = request.form["topic"]
	sql = "INSERT INTO thread (topic, created_at, area_id) VALUES (:TOPIC, NOW(), :AREA_ID)"
	
	db.session.execute(sql, {"TOPIC": topic, "AREA_ID": areaId})
	db.session.commit()
	
	sql = "SELECT id FROM thread WHERE area_id = :AREA_ID ORDER BY id DESC LIMIT 1"
	result = db.session.execute(sql, {"AREA_ID": areaId})
	
	newThreadId = result.fetchone()
	
	content = request.form["content"]
	
	sql = "INSERT INTO message (msg, sent_at, thread_id) VALUES (:content, NOW(), :THREAD_ID)"
	
	db.session.execute(sql, {"content": content, "THREAD_ID": newThreadId.id})
	db.session.commit()
	
	return redirect("/area/" + str(areaId))

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/register")
def register():
	return render_template("register.html")
