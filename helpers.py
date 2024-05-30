import re
from flask import redirect, render_template, session
from functools import wraps
from db_conn import conn


def apology(message, code=400):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")  # Redirect unauthenticated users to the login page
        elif not is_admin(session["user_id"]):  # Check if the user is an admin 
            return apology("Unauthorized access")  # Redirect non-admin users to an "unauthorized" page
        return f(*args, **kwargs)
    return decorated_function

def is_admin(user):
     # Query database for username
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT isAdmin FROM USERS WHERE id = %s LIMIT 1", (user,))
    admin = cursor.fetchone()
    cursor.close()
    if admin:
        return True
    else:
        return False
    

def validate_password(password):
    if len(password) < 8:
        return("Password must be at least 8 characters long.")
    
    if not re.search("[A-Z]", password):
        return ("Password must contain at least one uppercase character.")

    if not re.search("[0-9]", password):
        return ("Password must contain at least one digit.")
    
def validate_username(username):
    if not re.match("^[A-Za-z0-9]*$", username):
        return ("Invalid username. Only alphanumeric characters are allowed.")
    return None

def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return ("Invalid email format.")
    return None

def validate_age(age):
    try:
        age = int(age)
        if age < 0:
            return("Please enter a valid age")
    except ValueError:
        return ("Please enter a valid age")
    return None
        