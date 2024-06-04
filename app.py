import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta, datetime
from flask_mail import Mail, Message
from helpers import apology, login_required, validate_password, validate_email, validate_username, validate_age, admin_required
from db_conn import conn

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    if request.method == "POST":
        return redirect("/admin")
    else:
        return render_template("admin.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if request.method == "POST":
        
        if not request.form.get("username"):
            return apology("must provide username", 400)
        
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        # Query database for username
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (request.form.get("username"),))
        user = cursor.fetchone()
        cursor.close()

        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user["password_hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = user["id"]
    
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        age = request.form.get("age")
        email = request.form.get("email")

# validate user input

        # check for empty fields
        if not username or not password or not age or not email:
            return apology("One or more fields were left empty")
        
        username_validation_result = validate_username(username)
        password_validation_result = validate_password(password)
        email_validation_result = validate_email(email)
        age_validation_result = validate_age(age)

        # Check validation results
        if username_validation_result is not None:
            return apology(username_validation_result)

        if password_validation_result is not None:
            return apology(password_validation_result)

        if email_validation_result is not None:
            return apology(email_validation_result)

        if age_validation_result is not None:
            return apology(age_validation_result)
        
        # confirm password
        if password != confirm_password:
            return apology("Passwords must match")
        
        # check for unique email
        query = conn.cursor(dictionary=True)
        query.execute("SELECT email FROM users WHERE email = %s", (request.form.get("email"),))
        user = query.fetchone()
        query.close()
        if user:
            return apology("There is already an account with that email")
            
# ready INSERT
  
        # create the hash for storage
        password = generate_password_hash(password)
        
        # store the users data
        query = conn.cursor(dictionary=True)
        query.execute("INSERT INTO users (username, password_hash, age, email) VALUES (%s, %s, %s, %s)", (username, password, age, email))
        conn.commit()
        query.close()
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/map", methods=["GET", "POST"])
@login_required
def map():
    if request.method == "POST":

        playerName = request.form.get("playerName")
        playerAge = request.form.get("playerAge")
        playerColor = request.form.get("ColorRadios")
        playerAvatar = request.form.get("playerAvatar")

        if not playerName or not playerAge: # or not playerAvatar or not playerColor
            return apology("Oops! Some fields were left empty Please try Again")
        
        playerName_validation = validate_username(playerName)
        if playerName_validation is not None:
            return apology(playerName_validation)
        
        playerAge_validation = validate_age(playerAge)
        if playerAge_validation is not None:
            return apology(playerAge_validation)

        validate_age(playerAge)
        # check db for existing player
        query = conn.cursor(dictionary=True)
        query.execute("SELECT name FROM players WHERE user_id = %s AND name = %s LIMIT 1", (session["user_id"], playerName))
        existing_player = query.fetchone()
        query.close()

        if existing_player:
            return apology("A player with the same name already exists. Please choose a different name.")
        
        # insert data onto the table
        query = conn.cursor(dictionary=True)
        query.execute("INSERT INTO players (user_id, name, age) VALUES (%s, %s, %s) ;", (session["user_id"], playerName, playerAge))
        conn.commit()
        query.close()

        return redirect("/map")  
    else:
        # render each player on the list
        query = conn.cursor(dictionary=True)
        query.execute("SELECT name, age FROM players WHERE user_id = %s", (session["user_id"],))
        players = query.fetchall()
        query.close()
        return render_template("map.html", players=players )
    
@app.route("/credits", methods=["GET"])
@login_required
def credits():
        # here 
        # is 
        # credits
        # page
        # lol
        return render_template("credits.html")
    
@app.route("/account", methods=["GET"])
@login_required
def account():
        # get player info for the playerModal
        query = conn.cursor(dictionary=True)
        query.execute("SELECT name, age FROM players WHERE user_id = %s", (session["user_id"],))
        players = query.fetchall()
        query.close()
        return render_template("account.html", players=players)


@app.route("/managePlayers", methods=["GET","POST"])
@login_required
def managePlayers():
    if request.method == "POST": 
        
        return render_template("managePlayers.html")
       # return redirect("/account",)
    else:
        return apology("Test")
#    if players:
        



@app.route("/deleteAccount", methods=["POST"])
@login_required
def deleteAccount():
    query = conn.cursor(dictionary=True) 
    query.execute("SELECT username FROM users WHERE id = %s", (session["user_id"],))
    players = query.fetchone()
    query.close()

    if players:
        query = conn.cursor(dictionary=True)
        # delete players first to rid users of foreign key dependencies
        query.execute("DELETE FROM players WHERE user_id = %s", (session["user_id"],))
        query.execute("DELETE FROM users WHERE id = %s;", (session["user_id"],))
        conn.commit()
        query.close()
        #clear session so if redirect fails the @login_required will redirect to login
        session.clear()
        return redirect("/logout")
    else:
        session.clear()
        return redirect("/logout")
        
@app.route("/manageEmail", methods=["POST"])
@login_required
def manageEmail():
    newEmail = request.form.get("changeEmail")
    today = datetime.now()

    if newEmail:
        if validate_email(newEmail) is not None:
            return apology("That is an invalid email format. PLease try Again")
        
        # check db for existing email
        query = conn.cursor(dictionary=True)
        query.execute("SELECT email FROM users WHERE email = %s LIMIT 1", (newEmail,))
        existingEmail = query.fetchone()
        query.close()

        if existingEmail:
            return apology("That email is already in use!")
        
        # get back a timestamp
        query = conn.cursor(dictionary=True)
        query.execute("SELECT email_change FROM users WHERE id = %s ORDER BY email_change DESC LIMIT 1", (session["user_id"],))
        emailChange = query.fetchone()
        query.close()

        if emailChange["email_change"]:

            ChangeTimeStr = emailChange["email_change"]
            changeTime = datetime.strptime(ChangeTimeStr, "%Y-%m-%d %H:%M:%S")
            timeDifference = today - changeTime

            if timeDifference < timedelta(days=30):
                return apology("You have already made an Email change in the last 30 days!")
            else:
                # handle email change
                query = conn.cursor(dictionary=True)
                query.execute("UPDATE users SET email = %s WHERE id = %s", (newEmail, session["user_id"]))
                query.execute("UPDATE users SET email_change = %s WHERE id = %s", (today.strftime("%Y-%m-%d %H:%M:%S"), session["user_id"],))
                conn.commit()
                query.close()
                return redirect("/account")
        else:
            # first time change
            query = conn.cursor(dictionary=True)
            query.execute("UPDATE users SET email = %s WHERE id = %s", (newEmail, session["user_id"],))
            query.execute("UPDATE users SET email_change = %s WHERE id = %s", (today.strftime("%Y-%m-%d %H:%M:%S"), session["user_id"],))
            conn.commit()
            query.close()
            return redirect("/account")
    
    else:
        return apology("The field was left empty! Please enter the correct value.")


@app.route("/manageUsername", methods=["POST"])
@login_required
def manageUsername():
    newName = request.form.get("changeUsername")
    today = datetime.now()
    if newName:
        if validate_username(newName) is not None:
            return apology("The value you entered is invalid!")
        
        # check db for existing username
        query = conn.cursor(dictionary=True)
        query.execute("SELECT username FROM users WHERE username = %s LIMIT 1", (newName,))
        existingUsername = query.fetchone()
        query.close()

        if existingUsername:
            return apology("That Username has been taken already")
        
        # check db for timestamp
        query = conn.cursor(dictionary=True)
        query.execute("SELECT name_change FROM users WHERE id = %s ORDER BY name_change DESC LIMIT 1", (session["user_id"],))
        nameChange = query.fetchone()
        query.close()

        if nameChange["name_change"] == None:
              # 1st time change
            query = conn.cursor(dictionary=True)
            query.execute("UPDATE users SET username = %s WHERE id = %s",  (newName, session["user_id"]))
            query.execute("UPDATE users SET name_change = %s WHERE id = %s",  (today.strftime("%Y-%m-%d %H:%M:%S"), session["user_id"],))
            conn.commit()
            query.close()
            return redirect("/account")
        else:
            # parse string to a datetime
            ChangeTimeStr = nameChange["name_change"]
            changeTime = datetime.strptime(ChangeTimeStr, "%Y-%m-%d %H:%M:%S")

            timeDifference = today - changeTime

            if timeDifference < timedelta(days=30):
                return apology("You have already made a Name change in the last 30 days!")
            else:
                # handle name change
                query = conn.cursor(dictionary=True)
                query.execute("UPDATE users SET username = %s WHERE id = %s",  (newName, session["user_id"]))
                query.execute("UPDATE users SET name_change = %s WHERE id = %s", (today.strftime("%Y-%m-%d %H:%M:%S"),session["user_id"]))
                conn.commit()
                query.close()
                return redirect("/account") 
           
    else:
        return apology("The field was left empty! Please enter the correct value")



    
@app.route("/support", methods=["GET", "POST"])
@login_required
def support():
    if request.method == "POST":
        subjectInput = request.form.get("subjectText")
        describeInput = request.form.get("descriptionText")

        if describeInput and subjectInput:

            if len(subjectInput) > 45:
                flash("Limit to 45 characters")
                return redirect("/support")
            
            if len(describeInput) > 1500:
                flash("The description is to long")
                return redirect("/support")
            
            #TODO: insert Ticket information and get admin view of the ticket
            flash("Support request submitted successfully!", "success")
            return redirect("/support")
        else:
            flash("Both subject and description fields are required.", "danger")
            return redirect("/support")
    else:

        return render_template("support.html")

if (__name__) == ("__main__"):
    app.run(debug = True)


