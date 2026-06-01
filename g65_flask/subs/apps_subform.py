from flask import Flask, render_template, request, session
from classes.agency import Agency
from classes.project import Project
from classes.officer import Officer
from classes.transaction import Transaction
from classes.userlogin import Userlogin

prev_option = ""

def apps_subform(cname=""):
    global prev_option
    # cname virá como "Agency_Officer" ou "Project_Transaction"
    tlist = cname.split('_')
    cnames = tlist[0] # Classe Principal
    scname = tlist[1] # Classe Sub (Detalhes)
    
    ulogin=session.get("user")
    if (ulogin != None):
        cl = eval(cnames)
        sbl = eval(scname)
        cl_header, sbl_header = cl.header, sbl.header
        butshow, butedit = "enabled", "disabled"
        option = request.args.get("option")

        # Lógica de gravação igual ao gform
        if prev_option == 'insert' and option == 'save':
            strobj = request.form[cl.att[0]]
            for i in range(1,len(cl.att)):
                strobj += ";" + request.form[cl.att[i]]
            obj = cl.from_string(strobj)
            cl.insert(getattr(obj, cl.att[0]))
            cl.last()
        elif prev_option == 'edit' and option == 'save':
            obj = cl.current()
            for i in range(1,len(cl.att)):
                setattr(obj, cl.att[i], request.form[cl.att[i]])
            cl.update(getattr(obj, cl.att[0]))
        else:
            # Navegação e Linhas do Subform
            if option == "edit":
                butshow, butedit = "disabled", "enabled"
            elif option == "delete":
                obj = cl.current()
                # Apaga as linhas dependentes (ex: apaga officers da agência)
                lines = sbl.getlines(sbl.att[1], getattr(obj, cl.att[0]))
                for line in lines:
                    sbl.remove(line.id)
                cl.remove(obj.id)
                cl.first()
            elif option == "insert":
                butshow, butedit = "disabled", "enabled"
            elif option[:6] == "delrow": # Apaga uma linha específica da tabela de baixo
                row = int(option.split("_")[1])
                obj = cl.current()
                lines = sbl.getlines(sbl.att[1], getattr(obj, cl.att[0]))
                sbl.remove(lines[row].id)
            elif option == "saverow": # Adiciona uma linha na tabela de baixo
                obj = cl.current()
                # O primeiro campo do subform deve ser o ID da classe principal
                strobj = '0;' + str(getattr(obj, cl.att[0])) 
                for i in range(2, len(sbl.att)):
                    strobj += ";" + request.form[sbl.att[i]]
                objl = sbl.from_string(strobj)
                sbl.insert(objl.id)
            # ... (outras opções: first, last, next) ...
            elif option == 'exit':
                return render_template("index.html", ulogin=session.get("user"))

        prev_option = option
        obj = cl.current()
        objl = list()
        if option == 'insert' or len(cl.lst) == 0:
            obj = {a: "" for a in cl.att}
            obj[cl.att[0]] = 0
        else:
            # Puxa as linhas que pertencem a este registo (ex: Officers desta Agência)
            lines = sbl.getlines(sbl.att[2], getattr(obj, cl.att[0]))
            for line in lines:
                objl.append(line)

        return render_template("subform.html", cl_header=cl_header, sbl_header=sbl_header, butshow=butshow, butedit=butedit, cname=cname, obj=obj, att=cl.att, des=cl.des, ulogin=session.get("user"), objl=objl, desl=sbl.des, attl=sbl.att)
    else:
        return render_template("index.html", ulogin=ulogin)
    

