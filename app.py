from flask import Flask, flash, request, render_template
from models.users import User, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "clave"
db.init_app(app)

@app.route("/crear")
def createTables():
    db.create_all()
    return "creadas"

@app.route("/signup", methods = ['POST', 'GET'])
def createUser():
    if request.method == "POST":
        print("HOla")
        print(request.form)
        print(request.form.get("email"))
        print(request.form["email"])
        email = request.form["email"]
        print(email)
        name = request.form["name"]
        print(name)
        lastname = request.form["lastname"]
        print(lastname)
        password = request.form["password"]
        print(password)
        confirm_pass = request.form["confirm_pass"]
        print(confirm_pass)
        print(confirm_pass != password)
        if email == None or name == None or lastname == None or password == None:
            flash("Missing fields.", 'danger')
            return render_template("signup.html")
        
        if confirm_pass != password:
            flash("Passwords does not match.", 'danger')
            return render_template("signup.html")
        
        new_user = User(
            email=email,
            name=name,
            lastname=lastname
        )
        new_user.set_and_hash_pass(password)

        db.session.add(new_user)
        db.session.commit()
        flash("Account created.", 'success')
        return render_template("login.html")
    else:
        return render_template("signup.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        return ""
    else:
        return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)
