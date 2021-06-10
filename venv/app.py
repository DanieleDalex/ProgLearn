from flask import Flask
from flask import render_template, request, session, redirect, url_for,jsonify,flash
from flask_pymongo import PyMongo
from pymongo import collection
from pymongo import MongoClient
from youtubesearchpython import VideosSearch
import quiz_c_base
import quiz_c_medium
import quiz_c_advanced
import quiz_cplusplus_base
import quiz_cplusplus_medium
import quiz_cplusplus_advanced
import quiz_java_base
import quiz_java_medium
import quiz_java_advanced
import quiz_python_base
import quiz_python_medium
import quiz_python_advanced
import bcrypt
import pymongo

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key="hello"
app.config["MONGO_DBNAME"] = "mg_db"
app.config["MONGO_URI"] = "mongodb://192.168.99.100:27017/mg_db"
mongo = PyMongo(app)
db = mongo.db


utenti = db["utenti"]


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/languages")
def languages():
    return render_template("languages.html")


@app.route("/data_structures")
def data_structures():
    return render_template("data_structures.html")


@app.route("/login")
def login():
    return render_template("Login.html")


@app.route("/register")
def register():
    return render_template("Register.html")

@app.route("/games")
def games():
    if "username" in session:
        user = session["username"]
        c_level= utenti.find_one({'username':user},{'C_level':1})
        cplusplus_level = utenti.find_one({'username': user}, {'Cplusplus_level': 1})
        java_level = utenti.find_one({'username': user}, {'Java_level': 1})
        python_level = utenti.find_one({'username': user}, {'Python_level': 1})
        c_level=c_level["C_level"]
        cplusplus_level=cplusplus_level["Cplusplus_level"]
        java_level=java_level["Java_level"]
        python_level=python_level["Python_level"]
        return render_template("games.html", c=c_level, cplusplus=cplusplus_level, java=java_level, python=python_level)
    else:
        return render_template("games.html")

@app.route("/quiz")
def quiz_id():
    if "username" in session:
        return render_template("quiz.html")
    else:
        return redirect(url_for("login"))

@app.route("/sign_in", methods=('GET', 'POST'))
def sign_in():
    req = request.form
    username = req.get('uname')
    pwd = req.get("psw")
    userlog = db.utenti.find_one({'username': username})
    if userlog:
        if bcrypt.hashpw(pwd.encode('utf-8'), userlog['password']) == userlog['password']:
            session["username"]=username
            return redirect(url_for("user"))
    flash ("Combinazione Nome utente/Password inesistente")
    return redirect(url_for("login"))


@app.route("/reg", methods=('GET', 'POST'))
def reg():
    req = request.form
    usname = req.get("username")
    pwd = req.get("psw")
    pwd2 = req.get("psw-repeat")
    em = req.get("email")
    if pwd != pwd2:
        flash("Inserite due password differenti")
        return redirect(url_for("register"))
    elif db.utenti.find_one({'username': usname}):
        flash("Il nome utente esiste già")
        return redirect(url_for("register"))
    else:
        hashpwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
        db.utenti.insert({'username': usname, 'password': hashpwd, 'email': em, 'C_level': 'base', 'Cplusplus_level': 'base', 'Java_level': 'base', 'Python_level': 'base'})
        return redirect(url_for("login"))
#@app.route("quiz")
#def quiz():

@app.route("/user")
def user():
    if "username" in session:
        return redirect(url_for("root"))
    else:
        return redirect(url_for("login"))


@app.route("/videos", methods=['GET'])
def search_video():
    url_youtube = "http://www.youtube.com/embed/"
    easy = request.args.get("easy", "")
    advanced = request.args.get("advanced", "")
    print(easy)
    print(advanced)
    videosSearch1 = VideosSearch(easy, limit=1)
    results1 = videosSearch1.result()
    id1 = results1["result"][0]["id"]
    url_video1 = url_youtube + id1
    videosSearch2 = VideosSearch(advanced, limit=1)
    results2 = videosSearch2.result()
    id2 = results2["result"][0]["id"]
    url_video2 = url_youtube + id2
    dict_url = {"url1": url_video1, "url2": url_video2}
    print(dict_url)
    return jsonify(dict_url)

@app.route("/user/profile")
def profile():
    pass;

@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("root"))
'''
@app.route("/quiz_form")
def quiz_form():
    if "username" in session:
        questions = quiz.quiz
        return render_template("quiz.html", q=questions)
    else:
        return redirect(url_for("login"))
'''

@app.route("/save_score", methods=['POST'])
def save_score():
    if request.method == 'POST':
        score = float(request.form.get("score","0"))
        lan = request.form.get("lan"," ")
        print(lan)
        if score > ((score*50)/100):
            user=session["username"]
            level = utenti.find_one({'username': user}, {lan: 1})
            level = level[lan]
            print(level)
            if level == "base":
                utenti.update({"username": user}, { "$set": {lan: "medium"}})
            elif level == "medium":
                utenti.update({"username": user}, {"$set": {lan: "advanced"}})
        return "ok"
    return "no"

@app.route("/quiz_c/<level>")
def quiz_c(level):
    lan="C_level"
    questions = quiz_c_base.quiz
    if level == "base":
        questions = quiz_c_base.quiz
    elif level == "medium":
        questions = quiz_c_medium.quiz
    elif level == "advanced":
        questions = quiz_c_medium.quiz
    return render_template("quiz.html",q=questions, lan=lan)

@app.route("/quiz_cplusplus/<level>")
def quiz_cplusplus(level):
    lan="Cplusplus_level"
    questions = quiz_cplusplus_base.quiz
    if level == "base":
        questions = quiz_cplusplus_base.quiz
    elif level == "medium":
        questions = quiz_cplusplus_medium.quiz
    elif level == "advanced":
        questions = quiz_cplsuplus_advanced.quiz
    return render_template("quiz.html",q=questions, lan=lan)

@app.route("/quiz_java/<level>")
def quiz_java(level):
    lan="Java_level"
    questions = quiz_java_base.quiz
    if level == "base":
        questions = quiz_java_base.quiz
    elif level == "medium":
        questions = quiz_java_medium.quiz
    elif level == "advanced":
        questions = quiz_java_advanced.quiz
    return render_template("quiz.html",q=questions, lan=lan)

@app.route("/quiz_python/<level>")
def quiz_python(level):
    lan="Python_level"
    questions = quiz_python_base.quiz
    if level == "base":
        questions = quiz_python_base.quiz
    elif level == "medium":
        questions = quiz_python_medium.quiz
    elif level == "advanced":
        questions = quiz_python_advanced.quiz
    return render_template("quiz.html",q=questions, lan=lan)












