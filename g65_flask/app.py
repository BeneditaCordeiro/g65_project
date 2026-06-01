from flask import Flask, render_template, request, session
import os

app = Flask(__name__)
app.secret_key = 'CHAVE_SECRETA_DO_GRUPO'

# --- CORREÇÃO DE CAMINHO ---
# Isto obriga o Python a encontrar a base de dados na mesma pasta deste ficheiro app.py
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'data\\projeto_grupo5.db')

# 1. IMPORTAR AS TUAS CLASSES
from classes.agency import Agency
from classes.officer import Officer
from classes.project import Project
from classes.transaction import Transaction
from classes.userlogin import Userlogin

# 2. IMPORTAR AS APPS DA PASTA SUBS
from subs.apps_gform import apps_gform
from subs.apps_subform import apps_subform
from subs.apps_userlogin import apps_userlogin

# 3. LER OS DADOS (Agora com o db_path seguro)
# Se o ficheiro não existir, o .read() do professor cria os objetos vazios em memória
Agency.read(db_path)
Officer.read(db_path)
Project.read(db_path)
Transaction.read(db_path)
#Userlogin.read(db_path)

# --- ROTA PRINCIPAL ---
@app.route("/", methods=["POST", "GET"])
def index():
    ulogin = session.get("user")
    return render_template("index.html", ulogin=ulogin)

# --- FORMULÁRIOS GFORM ---
@app.route("/agency", methods=["POST", "GET"])
def agency():
    return apps_gform("Agency")

@app.route("/project", methods=["POST", "GET"])
def project():
    return apps_gform("Project")

# --- FORMULÁRIOS SUBFORM ---
@app.route("/agency_officer", methods=["POST", "GET"])
def agency_officer():
    return apps_subform("Agency_Officer")

@app.route("/project_transaction", methods=["POST", "GET"])
def project_transaction():
    return apps_subform("Project_Transaction")

# --- GESTÃO DE UTILIZADORES ---
@app.route("/userlogin", methods=["POST", "GET"])
def userlogin():
    return apps_userlogin()

# --- LOGIN / LOGOUT ---
@app.route("/login", methods=["POST", "GET"])
def login():
    message = ""
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        
        res = Userlogin.chk_password(user, password)
        if res == "Valid": 
            session["user"] = user
            return render_template("index.html", ulogin=user)
        else:
            message = res # Ex: "Wrong password" ou "No existent user"
            
    return render_template("login.html", message=message, ulogin=session.get("user"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return render_template("index.html", ulogin=None)

if __name__ == "__main__":
    # use_reloader=False é CRUCIAL para não dar SystemExit no Spyder
    app.run(debug=True, use_reloader=False)

    
