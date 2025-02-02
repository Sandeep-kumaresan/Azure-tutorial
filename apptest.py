from flask import Flask, render_template, request, jsonify, make_response,redirect
from flask_bcrypt import Bcrypt
import db1  # Ensure this is your custom module for database connection

app = Flask(__name__)
bcrypt = Bcrypt(app)
upload = '/home/sandeep/Documents/authent/files'

@app.route('/')
def index():
    username = request.cookies.get('username')
    if username:
        return render_template('test.html',username = username)        
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = db1.db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT pass FROM users WHERE username = %s", (uname,))
                content = cur.fetchone()
        finally:
            conn.close()
        if content is None:
            return jsonify({"msg": "User not found"}), 404

        dpwd = content[0]  
        is_valid = bcrypt.check_password_hash(dpwd, pwd)
        
        if is_valid:
            resp = make_response(render_template('test.html'))
            resp.set_cookie('username', uname,max_age=10)
            return resp
        else:
            return jsonify({"msg": "Invalid credentials"}), 401
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            return jsonify({"msg": "Passwords do not match"}), 400

        uname = request.form['username']
        pwd = request.form['password1']
        epwd = bcrypt.generate_password_hash(pwd).decode('utf-8')

        conn = db1.db_connection()
        cur = conn.cursor()

        cur.execute("SELECT username FROM users WHERE username = %s", (uname,))
        exist = cur.fetchone()
        if exist:
            conn.close()
            return jsonify({"msg": "User already exists"}), 400

        cur.execute("INSERT INTO users (username, pass) VALUES (%s, %s)", (uname, epwd))
        conn.commit()
        conn.close()
        return jsonify({"msg": "User registered successfully"}), 201

    return render_template("signup.html")

@app.route('/logout')
def logout():
    resp = make_response('deleted cookie')
    resp.delete_cookie('username')
    return resp

@app.route('/dashboard',methods = ['POST','GET'])
def dash():
    if request.method == 'POST':
        f = request.files['file']
        filename =  f.filename
        f.save(upload+"/"+filename)
        return "uploaded successfully"
    return render_template('test.html')



if __name__ == "__main__":
    app.run(debug=True)
