from flask import Flask, render_template, request, session
from datafile import filename

# --- AS TUAS CLASSES ---
from classes.agency import Agency
from classes.officer import Officer
from classes.project import Project
from classes.transaction import Transaction
from classes.userlogin import Userlogin

prev_option = ""

def apps_subform(cname=""):
    global prev_option
    tlist = cname.split('_')
    cnames = tlist[0]
    scname = tlist[1]
    ulogin=session.get("user")
    if (ulogin != None):
        cl = eval(cnames)
        sbl = eval(scname)
        cl_header = cl.header
        sbl_header = sbl.header
        butshow = "enabled"
        butedit = "disabled"
        option = request.args.get("option")
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
            if option == "edit":
                butshow = "disabled"
                butedit = "enabled"
            elif option == "delete":
                obj = cl.current()
                cl.remove(obj.id)
                if not cl.previous():
                    cl.first()
            elif option == "insert":
                butshow = "disabled"
                butedit = "enabled"
            elif option == 'cancel':
                pass
            elif option == "first":
                cl.first()
            elif option == "previous":
                cl.previous()
            elif option == "next":
                cl.nextrec()
            elif option == "last":
                cl.last()
            elif option == 'insertl':
                strobj = '0'
                for i in range(1, len(sbl.att)):
                    strobj += ";" + request.form[sbl.att[i]]
                objl = sbl.from_string(strobj)
                sbl.insert(objl.id)
            elif option == 'exit':
                return render_template("index.html", ulogin=session.get("user"))
        prev_option = option
        obj = cl.current()
        headers = list()
        objl = list()
        if option == 'insert' or len(cl.lst) == 0:
            obj = dict()
            obj[cl.att[0]] = 0
            for i in range(1, len(cl.att)):
                obj[cl.att[i]] = ""
        else:
            for i in range(1, len(sbl.att)):
                    headers.append(sbl.att[i][1:])        
            lines = sbl.getlines(sbl.att[1],getattr(obj, cl.att[0]))
            for line in lines:
                objl.append(sbl.obj[line])
        return render_template("subform.html", butshow=butshow, butedit=butedit, cname=cname, obj=obj, cl=cl, \
                               headers=headers, objl=objl, sbl=sbl, ulogin=session.get("user"))
    else:
         return render_template("login.html")

