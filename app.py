from flask import Flask, render_template, request,redirect,session
import sqlite3
import random


app = Flask(__name__)

app.secret_key="okuhira"

@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route('/good')
def good():
    name = "Good"
    return name 

@app.route("/greet/<name>")
def greet(name):
    return name + "さん、こんにちは！！"

@app.route("/tpl")
def tpl():
    name = "台風一過の快晴"
    return render_template("weather.html",tpl_name=name)

@app.route("/coler")
def coler():
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("select name from coler")
    coler = c.fetchall()
    c.close()
    print(coler)
    coler_choice = random.choice(coler)
    return render_template("coler.html", html_coler=coler_choice[0])

@app.route("/add_get")
def add_get():
    if "user_id" in session:
        return render_template("add.html")
    else:
        return redirect("/login_get")

@app.route("/add_post",methods=["post"])
def add_post():
    py_task = request.form.get("html_task")
    print(py_task)
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("insert into task values(null,?)",(py_task,))
    conn.commit()
    c.close()

    return redirect("/list")

@app.route("/list")
def list():
    if "user_id" in session:
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("select id,name from task")
        py_task = c.fetchall()
        c.close()
        print(py_task)
        task_list=[]
        for item in py_task:
            task_list.append({"id": item[0], "name": item[1]})

        return render_template("list.html", html_task=task_list)

    else:
        return redirect("/login_get")

@app.route("/delete/<task_id>")
def delete(task_id):
    if "user_id" in session:
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("delete from task where id = ?",(task_id,))
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/login_get")

@app.route("/regist_get")
def regist_get():
    return render_template("regist.html")

@app.route("/regist_post",methods=["post"])
def regist_post():
    py_name=request.form.get("html_name")
    py_pass=request.form.get("html_pswd")
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("insert into account values(null,?,?)",(py_name,py_pass))
    conn.commit()
    c.close()
    return render_template("login.html")

@app.route("/login_get")
def login_get():
    return render_template("login.html")

@app.route("/login_post",methods=["post"])
def login_post():
    py_name=request.form.get("html_name")
    py_pass=request.form.get("html_pswd")
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("select id from account where name=? and password=?",(py_name,py_pass))
    py_id = c.fetchone()
    c.close()

    if py_id is None:
        return render_template("login.html")
    else:
        session["user_id"]=py_id[0]
        return redirect("/list")
        
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login_get")


@app.errorhandler(404)
def not_found(error):
    return "お探しのページは見つかりません"

@app.route("/edit_get/<task_id>")
def edit_get(task_id):
    if "user_id" in session:
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("select name from task where id = ?",(task_id,))
        py_task = c.fetchone()[0]
        c.close()
        return render_template("edit.html",html_id=task_id, html_task=py_task)
    else:
        return redirect("/login_get")

@app.route("/edit_post",methods=["post"])
def edit_post():
    py_id=request.form.get("html_id")
    py_name=request.form.get("html_task")

    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("update task set name=? where id = ?",(py_name,py_id))
    conn.commit()
    c.close()
    return redirect("/list")



    
    # return render_template("dbtest.html",html_name=user_info[0], html_ago=user_info[1], html_address=user_info[2])

# @app.route("dbtest")
# def dbtest():
#     conn = sqlite3.connect("flasktest.db")
#     c = conn.cursor()
#     c.execute("select name,age,address from user where id = 2")
#     user_info = c.fetchone()
#     c.close()
#     print(user_info)

## おまじない
if __name__ == "__main__":
    app.run(debug=True)

