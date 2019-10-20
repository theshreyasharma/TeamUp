from flask import Flask, request, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/home", methods=['POST'])
def home():
    if(request.method == 'POST'):
        project_name = request.files['projectName']
        project_description = request.values['projectDescription']
        project_time = request.form['projectTime']
        project_language = request.form['projectLanguages']
            
    return "render_template("")"