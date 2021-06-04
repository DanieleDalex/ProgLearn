import bcrypt
from flask import Flask
from flask import render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_pymongo import PyMongo
from youtubesearchpython import VideosSearch
from pymongo import collection
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

app.config["MONGO_DBNAME"] = "mg_db"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mg_db"
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
    return render_template("games.html")


@app.route("/sign_in", methods=('GET', 'POST'))
def sign_in():
    req = request.form
    username = req.get('uname')
    pwd = req.get("psw")
    userlog = db.utenti.find_one({'username': username})
    if userlog:
        if bcrypt.hashpw(pwd.encode('utf-8'), userlog['password']) == userlog['password']:
            return "Login avvenuto con successo"
    return "Combinazione Nome utente/Password inesistente"


@app.route("/reg", methods=('GET', 'POST'))
def reg():
    req = request.form
    usname = req.get("username")
    pwd = req.get("psw")
    pwd2 = req.get("psw-repeat")
    em = req.get("email")
    if pwd != pwd2:
        return "Inserite due password differenti"
    elif db.utenti.find_one({'username': usname}):
        return "Il nome utente esiste già"
    else:
        hashpwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
        db.utenti.insert({'username': usname, 'password': hashpwd, 'email': em})
        return "Registrazione avvenuta con successo"


@app.route("/videosc", methods=["GET"])
def videosc():
    url_youtube = "http://www.youtube.com/embed/"
    facile = request.args.get("easy", "facile")
    medio = request.args.get("medium", "facile")
    difficile = request.args.get("hard", "facile")
    videosSearch1 = VideosSearch(facile, limit=1)
    results1 = videosSearch1.result()
    id = results1["result"][0]["id"]
    url_video1 = url_youtube + id
    videosSearch2 = VideosSearch(medio, limit=1)
    results2 = videosSearch2.result()
    id1 = results2["result"][0]["id"]
    url_video2 = url_youtube + id1
    videosSearch3 = VideosSearch(difficile, limit=1)
    results3 = videosSearch3.result()
    id2 = results3["result"][0]["id"]
    url_video3 = url_youtube + id2
    dict_url = {"url1": url_video1,"url2": url_video2,"url3": url_video3}
    print(dict_url)
    return jsonify(dict_url)