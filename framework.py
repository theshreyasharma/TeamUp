from flask import Flask, request, render_template, url_for, redirect, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "#d\xdd_\t2pD*?d\xd8\xb1\x90\x88d\x07g\x87\xc7\xfco\xf0\x88\x18L"

@app.route("/")
@app.route("/projects", methods=["GET"])
def projects():
    if request.method == "GET":
        conn = mysql.connector.connect(host='teamup.czuxuaxnpu3e.us-east-2.rds.amazonaws.com',
                                            database='innodb',
                                            user='root',
                                            password='rootroot')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM project")
            rows = cursor.fetchall()

            print("Total Rows: ", cursor.rowcount)

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()
    
    return render_template("layout.html", projects=rows)

@app.route("/join", methods=["GET"])
def join():
    if request.method == "GET":
        conn = mysql.connector.connect(host='teamup.czuxuaxnpu3e.us-east-2.rds.amazonaws.com',
                                            database='innodb',
                                            user='root',
                                            password='rootroot')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM project")
            rows = cursor.fetchall()

            print("Total Rows: ", cursor.rowcount)

        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    return render_template("jointeam.html", projects=rows)

# Used to verify user upon logging in
@app.route("/sign_in_get", methods=["POST"])
def sign_in_get():
    if request.method == "POST":
        print("entered post")
        conn = mysql.connector.connect(host='teamup.czuxuaxnpu3e.us-east-2.rds.amazonaws.com',
                                            database='innodb',
                                            user='root',
                                            password='rootroot')
        cursor = conn.cursor()
        try:
            sign_in_name = request.form.get("signInName", False)
            sign_in_email = request.form.get("signInEmail", False)
            sign_in_password = request.form.get("signInPassword", False)

            print(sign_in_email)

            cursor.execute("SELECT * FROM web_users WHERE user_name = %s AND user_password = %s", (sign_in_name, sign_in_password))
            row = cursor.fetchall()
            print(row)

            # if user found, this info is now accesible on all other templates in session
            if len(row) != 0:
                print("is a user")
                session["email"] = sign_in_email
                session["name"] = sign_in_name
                return redirect("/")
            else:
                print("Not a user")
                return redirect("/signin")
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    print("didnt enter get")
    return redirect("/")
                

@app.route("/submit")
def submit():
    return render_template("project-form.html")


@app.route("/details", methods=['GET'])
def details():
    return redirect(url_for("individual"))

@app.route("/signin")
def signin():
    
    return render_template("signin.html")

@app.route("/individual")
def individual():
    if(request.method == 'GET'):
        print("Button")
    return render_template("individual-project.html")
    
@app.route("/account")
def new_account():
    return render_template("createaccount.html")

@app.route("/create_project_post", methods=['POST'])
def insert_new_project():
    if request.method == "POST":
        project_name = request.form['projectName']
        project_description = request.form['projectDescription']
        project_time = request.form['projectTime']
        project_language = request.form['projectLanguages']

        # TEMPORARILY REMOVED OWNER ID TO TEST CONNECTION
        # ADD BACK WHEN USERS IMPLEMENTED
        query = "INSERT INTO project(project_name,project_time,project_description,project_language)" \
                "VALUES(%s,%s,%s,%s)"
        args = (project_name, project_time, project_description, project_language)

        conn = None
        try:
            conn = mysql.connector.connect(host='teamup.czuxuaxnpu3e.us-east-2.rds.amazonaws.com',
                                        database='innodb',
                                        user='root',
                                        password='rootroot')
            cursor = conn.cursor()
            cursor.execute(query, args)

            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')

            conn.commit()
            
            #if conn.is_connected():
            #    print('Connected to MySQL database')

        except Error as e:
            print(e)

        finally:
            print("Connection closed")
            cursor.close()
            conn.close()
    return redirect(url_for("projects"))

@app.route("/create_web_user_post", methods=['POST'])
def insert_new_web_user():
    if request.method == "POST":
        new_user_name = request.form.get("newUserName", False)
        new_user_email = request.form.get("newUserEmail", False)
        new_user_password = request.form.get("newUserPassword", False)

        query = "INSERT INTO web_users(user_name, user_email, user_password)" \
                "VALUES(%s, %s, %s)"
        args = (new_user_name, new_user_email, new_user_password)
        conn = None
        try:
            conn = mysql.connector.connect(host='teamup.czuxuaxnpu3e.us-east-2.rds.amazonaws.com',
                                        database='innodb',
                                        user='root',
                                        password='rootroot')
            cursor = conn.cursor()
            cursor.execute(query, args)
            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')

            conn.commit()
        except Error as e:
            print(e)
        finally:
            print("Connection closed")
            cursor.close()
            conn.close()
    return redirect(url_for("projects"))

@app.route("/jointeam")
def join_team():
    if request.method == "GET":
        conn = mysql.connector.connect(host='teamup.czuxuaxnpu3e.us-east-2.rds.amazonaws.com',
                                            database='innodb',
                                            user='root',
                                            password='rootroot')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM project")
            rows = cursor.fetchall()

            print("Total Rows: ", cursor.rowcount)

        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    return render_template("jointeam.html", projects=rows)


