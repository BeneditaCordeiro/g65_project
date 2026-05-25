from flask import Flask, render_template, request, session
from datafile import filename

# 1. IMPORTAR AS TUAS CLASSES
from classes.agency import Agency
from classes.officer import Officer
from classes.project import Project
from classes.transaction import Transaction
from classes.userlogin import Userlogin

# 2. IMPORTAR AS APPS GENÉRICAS DA PASTA SUBS
from subs.apps_gform import apps_gform
from subs.apps_subform import apps_subform
from subs.apps_userlogin import apps_userlogin

app = Flask(__name__)
app.secret_key = 'CHAVE_SECRETA_DO_GRUPO'  # Altera se quiseres, necessária para as sessões

# 3. LER OS DADOS DE TODAS AS TABELAS (Garante que o nome do ficheiro .db está correto)
db_path = filename + 'projeto_grupo5.db'
Agency.read(db_path)
Officer.read(db_path)
Project.read(db_path)
Transaction.read(db_path)
Userlogin.read(db_path)

# --- ROTA PRINCIPAL: MENU INICIAL ---
@app.route("/", methods=["POST", "GET"])
def index():
    # Verifica se há um utilizador logado na sessão
    ulogin = session.get("user")
    return render_template("index.html", ulogin=ulogin)

# --- ROTAS FORMULÁRIOS GENÉRICOS (GFORM) ---
@app.route("/agency", methods=["POST", "GET"])
def agency():
    return apps_gform("Agency")

@app.route("/project", methods=["POST", "GET"])
def project():
    return apps_gform("Project")

# --- ROTAS FORMULÁRIOS MESTRE-DETALHE (SUBFORM) ---
# Relação: Uma Agência tem vários Trabalhadores (Officers)
@app.route("/agency_officer", methods=["POST", "GET"])
def agency_officer():
    return apps_subform("Agency_Officer")

# Relação: Um Projeto tem várias Transações/Pagamentos
@app.route("/project_transaction", methods=["POST", "GET"])
def project_transaction():
    return apps_subform("Project_Transaction")

# --- ROTA DE GESTÃO DE UTILIZADORES ---
@app.route("/userlogin", methods=["POST", "GET"])
def userlogin():
    return apps_userlogin()

# --- ROTAS DE AUTENTICAÇÃO (LOGIN / LOGOUT) ---
@app.route("/login", methods=["POST", "GET"])
def login():
    message = ""
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]
        
        # Validação genérica usando o método da classe Userlogin
        res = Userlogin.chk_password(user, password)
        if res == True:
            session["user"] = user  # Guarda o utilizador na sessão
            return render_template("index.html", ulogin=user)
        else:
            message = "Utilizador ou Palavra-passe incorretos!"
            
    return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    session.pop("user", None)  # Limpa o utilizador da sessão
    return render_template("index.html", ulogin=None)

if __name__ == "__main__":
    app.run()#(debug=True)