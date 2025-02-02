from flask import Flask,render_template,Blueprint

second = Blueprint("second",__name__,static_folder="statics",template_folder="template")
@second.route('/')
@second.route('/user')
def home():
    return render_template("test.html") 