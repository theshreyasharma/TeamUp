from flask import Flask, request, render_template, url_for, redirect
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)

@app.route("/")
@app.route("/home", methods=['POST'])
def home():
    if(request.method == 'POST'):
        print(request.get_json())
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


@app.route("/submit")
def submit():
    return render_template("project-form.html")


@app.route("/details", methods=['GET'])
def details():
    return redirect(url_for("individual"))


@app.route("/individual")
def individual():
    if(request.method == 'GET'):
        print("Button")
    return render_template("individual-project.html")
    
@app.route("/account")
def new_account():
    if(request.method == 'POST'):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
    return redirect(url_for("made"))

@app.route("/accountconfirmation")
def account_confirmation():
    render_template("accountconfirmation")
