from flask import Flask, request, render_template, url_for, redirect
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

    return redirect(url_for("projects"))


@app.route("/projects")
def projects():
    return render_template("layout.html")


@app.route("/submit")
def submit():
    return render_template("project-form.html")
