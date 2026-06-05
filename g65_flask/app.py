from flask import Flask, render_template, request, session
import sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.chdir(BASE_DIR)

from datafile import filename

from classes.agency import Agency
from classes.officer import Officer
from classes.project import Project
from classes.transaction import Transaction
from classes.userlogin import Userlogin

from subs.apps_gform import apps_gform
from subs.apps_subform import apps_subform
from subs.apps_userlogin import apps_userlogin
from subs.apps_dashboard import apps_dashboard

app = Flask(__name__)
app.secret_key = 'CHAVE_SECRETA_GRUPO5'

Agency.read(filename + 'projeto_grupo5.db')
Officer.read(filename + 'projeto_grupo5.db')
Project.read(filename + 'projeto_grupo5.db')
Transaction.read(filename + 'projeto_grupo5.db')
Userlogin.read(filename + 'projeto_grupo5.db')

@app.route("/")
def index():
    return render_template("index.html", ulogin=session.get("user"))

@app.route("/login")
def login():
    return render_template("login.html", user="", password="",
                           ulogin=session.get("user"), resul="")

@app.route("/logoff")
def logoff():
    session.pop("user", None)
    return render_template("index.html", ulogin=session.get("user"))

@app.route("/chklogin", methods=["post", "get"])
def chklogin():
    user     = request.form["user"]
    password = request.form["password"]
    resul    = Userlogin.chk_password(user, password)
    if resul == "Valid":
        session["user"] = user
        return render_template("index.html", ulogin=session.get("user"))
    return render_template("login.html", user=user, password=password,
                           ulogin=session.get("user"), resul=resul)

@app.route("/dashboard")
def dashboard():
    return apps_dashboard()

@app.route("/gform/<cname>", methods=["post", "get"])
def gform(cname):
    return apps_gform(cname)

@app.route("/subform/<cname>", methods=["post", "get"])
def subform(cname):
    return apps_subform(cname)

@app.route("/Userlogin", methods=["post", "get"])
def userlogin():
    return apps_userlogin()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
