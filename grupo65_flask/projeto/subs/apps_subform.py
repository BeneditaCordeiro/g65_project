from flask import render_template, request, session

from classes.agency import Agency
from classes.project import Project
from classes.officer import Officer
from classes.transaction import Transaction
from classes.userlogin import Userlogin

# Dict per cname so different subforms don't share state
prev_option = {}

def get_fk_att(sbl, cl):
    """Find the attribute in sbl that is the FK pointing to cl's id."""
    cl_name = cl.__name__.lower()
    for att in sbl.att[1:]:
        if cl_name in att:
            return att
    # fallback: last attribute that ends in _id
    for att in reversed(sbl.att):
        if att.endswith('_id'):
            return att
    return sbl.att[1]

def apps_subform(cname=""):
    global prev_option
    tlist  = cname.split('_')
    cnames = tlist[0]
    scname = tlist[1]

    ulogin = session.get("user")
    if ulogin is not None:
        cl  = eval(cnames)
        sbl = eval(scname)
        cl_header  = cl.header
        sbl_header = sbl.header
        butshow = "enabled"
        butedit = "disabled"
        option  = request.args.get("option")
        prev    = prev_option.get(cname, "")

        # FK attribute in sub-class that links to parent class
        fk_att = get_fk_att(sbl, cl)

        if prev == 'insert' and option == 'save':
            strobj = request.form[cl.att[0]]
            for i in range(1, len(cl.att)):
                strobj += ";" + request.form[cl.att[i]]
            obj = cl.from_string(strobj)
            cl.insert(getattr(obj, cl.att[0]))
            cl.last()
        elif prev == 'edit' and option == 'save':
            obj = cl.current()
            for i in range(1, len(cl.att)):
                setattr(obj, cl.att[i], request.form[cl.att[i]])
            cl.update(getattr(obj, cl.att[0]))
        else:
            if option == "edit":
                butshow = "disabled"
                butedit = "enabled"
            elif option == "delete":
                obj = cl.current()
                lines = sbl.getlines(fk_att, getattr(obj, cl.att[0]))
                for line in lines:
                    sbl.remove(line)
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
            elif option is not None and option[:6] == "delrow":
                row = int(option.split("_")[1])
                obj = cl.current()
                lines = sbl.getlines(fk_att, getattr(obj, cl.att[0]))
                sbl.remove(lines[row])
            elif option == "addrow":
                butshow = "disabled"
                butedit = "disabled"
            elif option == "saverow":
                obj = cl.current()
                strobj = '0'
                for i in range(1, len(sbl.att)):
                    strobj += ";" + request.form[sbl.att[i]]
                objl = sbl.from_string(strobj)
                sbl.insert(objl.id)
            elif option == 'exit':
                return render_template("index.html", ulogin=session.get("user"))
            else:
                # First visit: go to first record
                cl.first()

        prev_option[cname] = option
        obj  = cl.current()
        objl = list()

        if option == 'insert' or len(cl.lst) == 0:
            dobj = {cl.att[0]: 0}
            for i in range(1, len(cl.att)):
                dobj[cl.att[i]] = ""
        else:
            dobj = {}
            for att in cl.att:
                dobj[att] = getattr(obj, att)

            # Use correct FK attribute to fetch sub-records
            lines = sbl.getlines(fk_att, getattr(obj, cl.att[0]))
            for line_id in lines:
                objl.append(sbl.obj[line_id])

        return render_template("subform.html",
                               cl_header=cl_header, sbl_header=sbl_header,
                               butshow=butshow, butedit=butedit,
                               cname=cname, obj=dobj,
                               att=cl.att, des=cl.des,
                               ulogin=session.get("user"),
                               objl=objl, desl=sbl.des, attl=sbl.att)
    else:
        return render_template("index.html", ulogin=ulogin)
