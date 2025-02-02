from flask import Flask, render_template, request, jsonify, make_response,redirect,url_for,session,flash
from flask_bcrypt import Bcrypt
from admin.second import second
import db1  # Ensure this is your custom module for database connection

app = Flask(__name__)
bcrypt = Bcrypt(app)
upload = '/home/sandeep/Documents/authent/files'
app.secret_key = "reallysecret"
app.register_blueprint(second,url_prefix = "/admin")

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        session["user"] = uname
        conn = db1.db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT pass FROM users WHERE username = %s", (uname,))
                content = cur.fetchone()
        finally:
            conn.close()
        if content is None:
            flash('Are you Drunk? 😵‍💫 Give correct credentials! 😪',"error")
            return redirect(url_for("login"))

        dpwd = content[0]  
        is_valid = bcrypt.check_password_hash(dpwd, pwd)
        
        if is_valid :
            return redirect(url_for("user"))
        else:
            flash("Bad User Credentials,Please Try Again 😶‍🌫️","error")
            return render_template('login.html')
    else:
        return render_template('login.html')
    
@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        return redirect(url_for("dash"))
    else:
        flash('Login First! 😡🤬','warning')
        return redirect(url_for("login"))
    
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            return jsonify({"msg": "Passwords do not match"}), 400
        elif request.form['password1'] == "" or request.form['password2'] == "" or request.form['username'] == "":
            flash("Please enter details to signup","error")
            return render_template('signup.html')

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
        flash("User registered successfully","success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop("user",None)
    flash("You have been logged out!","info")
    return redirect(url_for("login"))

@app.route('/dashboard',methods = ['POST','GET'])
def dash():
    user = session.get('user')
    return render_template('dash.html',user=user)



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
