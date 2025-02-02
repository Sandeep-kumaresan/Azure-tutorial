from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
upload = '/home/sandeep/Documents/authent/files'
@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        f = request.files['file']
        filename =  f.filename
        f.save(upload+"/"+filename)
        return "uploaded successfully"
    return render_template('test.html')
if __name__ == "__main__":
    app.run(debug=True)
