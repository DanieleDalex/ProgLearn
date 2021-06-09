from flask import Flask
from flask import render_template, request, session, redirect, url_for,jsonify,flash
from flask_pymongo import PyMongo
from pymongo import collection
from pymongo import MongoClient
from youtubesearchpython import VideosSearch
import quiz
import bcrypt
import pymongo
"""
domande=["Which function is the first function a C program calls?",
         "C is a:",
         "Which of these is not an existing type?",
         "Which of these is the correct syntax for comments?",
         "Most of C lines end with:",
         "Which operator compares 2 variables?",
         "Which function prints something on the console?",
         "Which function reads an input from the console?",
         'Select the output of the following code:\nint main() {\nint x=5;\nint y=3;\nx=x+y*x;\nprintf("%d",x);\nreturn 0;\n}'
         'Complete the code to print the value of x:\nint main() {\nint x=5;\nx=x+4;\n_____________;\nreturn 0;\n}']
risposte=[["printf()","scanf()","start()","main()"],
          ["Low level programming language","High level programming language","Markup Language","Not a language"],
          ["Float","Char","Word","Int"],
          ["/*comment*/","#comment","<!--comment-->","**comment**"],
          [".","^","?",";"],
          ["--","=","==","++"],
          ["scanf()","printf()","system()","main()"],
          ["printf()","push()","start()","scanf()"],
          ["5","40","20","35"],
          ['printf("%d,&x")','printf("%d,x")','scanf("%d",&x)',"push(x)"]
          ]
soluzioni= [3,0,2,0,3,2,1,3,2,1]
"""
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key="hello"
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

@app.route("/quiz")
def quiz_id():
    return render_template("quiz.html")

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
        db.utenti.insert({'username': usname, 'password': hashpwd, 'email': em})
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
@app.route("/quiz_form")
def quiz_form():
    questions = quiz.quiz
    return jsonify(questions)







