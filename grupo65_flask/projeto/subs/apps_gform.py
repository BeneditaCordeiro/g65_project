from flask import render_template, request, session

from classes.agency import Agency
from classes.project import Project
from classes.officer import Officer
from classes.transaction import Transaction
from classes.userlogin import Userlogin

prev_option = {}

def apps_gform(cname=''):
    global prev_option
    ulogin = session.get("user")
    if ulogin is not None:
        cl = eval(cname)
        butshow = "enabled"
        butedit = "disabled"
        option = request.args.get("option")
        prev = prev_option.get(cname, "")

        if prev == 'insert' and option == 'save':
            strobj = request.form[cl.att[0]]
            for i in range(1, len(cl.att)):
                strobj += ";" + request.form[cl.att[i]]
            obj = cl.from_string(strobj)
            cl.insert(getattr(obj, cl.att[0]))
            cl.last()
        elif prev == 'edit' and option == 'save':
            obj = cl.current()
            if obj is not None:
                for i in range(1, len(cl.att)):
                    setattr(obj, cl.att[i], request.form[cl.att[i]])
                cl.update(getattr(obj, cl.att[0]))
        else:
            if option == "edit":
                butshow = "disabled"
                butedit = "enabled"
            elif option == "delete":
                obj = cl.current()
                if obj is not None:
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
            elif option == 'exit':
                return render_template("index.html", ulogin=session.get("user"))
            else:
                # First visit or unknown option: go to first record
                cl.first()

        prev_option[cname] = option
        obj = cl.current()

        if option == 'insert' or obj is None or len(cl.lst) == 0:
            dobj = {cl.att[0]: 0}
            for i in range(1, len(cl.att)):
                dobj[cl.att[i]] = ""
        else:
            dobj = {}
            for att in cl.att:
                dobj[att] = getattr(obj, att)

        return render_template("gform.html", butshow=butshow, butedit=butedit,
                               cname=cname, obj=dobj, att=cl.att, des=cl.des,
                               ulogin=session.get("user"))
    else:
        return render_template("index.html", ulogin=ulogin)
