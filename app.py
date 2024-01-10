
### calling libaryes ###
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
import re

app = Flask(__name__)

### Session ###
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

### Configure CS50 Library to use SQLite database ###
db = SQL("sqlite:///kunto.db")


### HOME PAGE ###
@app.route("/", methods=["GET", "POST"])
def Home():
    if request.method == "POST":
        return render_template("home.html")
    else:
        return render_template("home.html")

### PROFILE PAGE ###
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    ### GET DAY COUNTER FROM MYSQL ###
    dayCount = str(db.execute("SELECT ID FROM DAYs;"))
    dayCount = dayCount.replace("[{'ID': ","")
    dayCount = dayCount.replace("}]","")
    dayCount = int(dayCount) -1

    ### GET USERNAME FROM DATABASE WITHOUT HEADER NAME ###
    username = str(db.execute("SELECT username FROM users WHERE id = ?", session["user_id"]))
    username = username.replace("[{'username': '","")
    username = username.replace("'}]","")

    ### IF BUTTEN WAS CLICKED THIS ACTION WILL START ###
    if request.method == "POST":
        ### Username1, DayNum is placeholder in profile.html ###
        return render_template("profile.html",username1 = username, DayNum = dayCount)
    ### IF BUTTEN WASN'T CLICKED THIS ACTION WILL BE VISUPLE ###
    else:
        ### Username1, DayNum is placeholder in profile.html ###
        return render_template("profile.html",username1 = username, DayNum = dayCount)


### LOGIN PAGE ###
@app.route("/login", methods=["GET", "POST"])
def login():
    ### Forget any user_id ###
    session.clear()
    ### User reached route via POST (as by submitting a form via POST) ###
    if request.method == "POST":
        ### Ensure username was submitted ###
        if not request.form.get("username"):
            return render_template("login.html", Place1 = "must provide username")

        ### Ensure password was submitted ###
        elif not request.form.get("password"):
            return render_template("login.html", Place1 =  "must provide password")

        ### Query database for username ###
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        ### Ensure username exists and password is correct ###
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("login.html", Place1 = "invalid username and/or password")

        ### remember whish user loged in ###
        session["user_id"] = rows[0]["id"]
        ### redirect user to home page ###
        return redirect("/")

    ### User reached route via GET (as by clicking a link or via redirect) ###
    else:
        return render_template("login.html")




### REGISTER PAGE ###
@app.route("/register", methods=["GET", "POST"])
def register():
    ### Forget any user_id ###
    session.clear()
    if request.method == "POST":
        ### Ensure username was submitted ###
        if not request.form.get("username"):
            return render_template("register.html", Place1 = "must provide username")

        ### Ensure password was submitted ###
        elif not request.form.get("password"):
            return render_template("register.html", Place1 = "must provide password")

        ### Ensure password confirmation was submited ###
        elif not request.form.get("confir"):
            return render_template("register.html", Place1 = "must repeat the password")

        ### Ensure password is equal to confirmation ###
        elif request.form.get("password") != request.form.get("confir"):
            return render_template("register.html", Place1 = "passwprd is not match")

        ### Query database for username ###
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        ### Ensure username is not exists ###
        if len(rows) != 0:
            return render_template("register.html", Place1 = "username already exist")

        ### insert user to database ###
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password"),))
        ### Query database for username ###
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        ### remember whish user loged in ###
        session["user_id"] = rows[0]["id"]
        ### redirect user to home page ###
        return redirect("/")
    ### User reached route via GET (as by clicking a link or via redirect) ###
    else:
        return render_template("register.html")

### ENTER ACHIVMENT PAGE ###
@app.route("/MyDocument", methods=["GET", "POST"])
@login_required
def MyDocument():
    ### CALL DAY COUNT FROM DB ###
    dayCount = str(db.execute("SELECT ID FROM DAYs;"))
    dayCount = dayCount.replace("[{'ID': ","")
    dayCount = dayCount.replace("}]","")
    if request.method == "POST":
        return render_template("MyDocument.html", dayCount = dayCount)
    else:
        return render_template("MyDocument.html", dayCount = dayCount)

### ADD BUTTEN IN MYDOCUMENT PAGE ###
@app.route("/ADD", methods=["GET", "POST"])
def ADD():
    ### CALL DAY COUNT FROM DB ###
    dayCount = str(db.execute("SELECT ID FROM DAYs;"))
    dayCount = dayCount.replace("[{'ID': ","")
    dayCount = dayCount.replace("}]","")

    if request.method == "POST":
        ### IF ADD BUTTEN WAS CLICKED ALL FORMS WILL BE ADD TO DATABASE ###
        str(db.execute("INSERT INTO achive (ID,big,ashive,problem,problemsolve) VALUES(?,?,?,?,?)",
                    int(dayCount),
                    request.form.get("big"),
                    request.form.get("achive"),
                    request.form.get("problem"),
                    request.form.get("problemsolve")))
        ### UPDATE DAT COUNT TABLE ###
        db.execute("UPDATE DAYs SET ID = ID + 1")
        return redirect("/MyDocument")
    else:
        return redirect("/MyDocument")


### RESTART BUTTEN IN MYDOCUMENT PAGE ###
@app.route("/RESTART", methods=["GET", "POST"])
def RESTART():
    ### IF ADD BUTTEN WAS CLICKED ALL DATA OF THE TABLE IN THE DATABASE WILL BE DELETED ###
    if request.method == "POST":
        ### DELET EVERY THING FROM ACHIVE TABLE ###
        db.execute("DELETE FROM achive")
        ### UPDATE DAY TABLE ###
        db.execute("UPDATE DAYs SET ID = ?","1")
        return redirect("/MyDocument")
    return redirect("/MyDocument")

### LOG OUT ###
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()  # Forget any user_id
    return redirect("/")


@app.route("/changePass", methods=["GET", "POST"])
def changePass():
    ### GET PASSWORD FROM DATABASE WITHOUT HEADER NAME ###
    password = str(db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"]))
    password = password.replace("[{'hash': '","")
    password = password.replace("'}]","")

    if request.method == "POST":
        ### UPDATE PASSWORD ###
        db.execute("UPDATE users SET hash = ? WHERE hash = ?",generate_password_hash(request.form.get("password")),password)
        return redirect("/profile")
    else:
        return redirect("/profile")



@app.route("/changeUser", methods=["GET", "POST"])
def changeUser():
    ### GET USERNAME FROM DATABASE WITHOUT HEADER NAME ###
    username = str(db.execute("SELECT username FROM users WHERE id = ?", session["user_id"]))
    username = username.replace("[{'username': '","")
    username = username.replace("'}]","")

    ### CHECK IF USERNAME IN THE DATEBASE ###
    rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
    if request.method == "POST":
    ### UPDATE USERNAME ###
        ### ENSURE USER NAME IS NOT EXIST ###
        if len(rows) != 0:
            return render_template("profile.html", place1 = "username already exist",username1 = username)
        db.execute("UPDATE users SET username = ? WHERE username = ?",request.form.get("username"),username)
        return redirect("/profile")
    else:
        return redirect("/profile")




@app.route("/history", methods=["GET", "POST"])
def history():
    ### GET DAY COUNTER ###
    dayCount = str(db.execute("SELECT ID FROM DAYs;"))
    dayCount = dayCount.replace("[{'ID': ","")
    dayCount = dayCount.replace("}]","")
    dayCount = int(dayCount) -1

    ### GET BIG COLUMEN ###
    big = str(db.execute("SELECT big FROM achive WHERE ID = ?",request.form.get("Day1")))
    big = big.replace("[{'big': ","")
    big = big.replace("}]","")

    ### GET ASHIVE COLUMEN ###
    ashive = str(db.execute("SELECT ashive FROM achive WHERE ID = ?",request.form.get("Day1")))
    ashive = ashive.replace("[{'ashive': ","")
    ashive = ashive.replace("}]","")

    ### GET PROBLEM COLUMEN ###
    problem = str(db.execute("SELECT problem FROM achive WHERE ID = ?",request.form.get("Day1")))
    problem = problem.replace("[{'problem': ","")
    problem = problem.replace("}]","")

    ### GET PROBLEMSOLVE COLUMEN ###
    problemsolve = str(db.execute("SELECT problemsolve FROM achive WHERE ID = ?",request.form.get("Day1")))
    problemsolve = problemsolve.replace("[{'problemsolve': ","")
    problemsolve = problemsolve.replace("}]","")

    ### THE NUMBER WAS ENTERD IN THE FORM ###
    Day = request.form.get("Day1")

    ### SHOW ALL DATA ON THE PAGE ###
    if request.method == "POST":
        return render_template("history.html",Day = Day, big = big, ashive = ashive, problem = problem, problemsolve = problemsolve, DayNum = dayCount)
    else:
        return render_template("history.html",Day = Day, DayNum = dayCount)



#### project title : KUNTO
#### my name : ali sulaiman
#### country, city : oman, suhar