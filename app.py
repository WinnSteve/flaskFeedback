"""routes for FlaskFeedback"""

# standard flask imports
from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

# connect DB and access forms
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = "thereAreNoSecrets"

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def homepage():
    """homepage redirect to register as per instructed"""

    return redirect("/register")


@app.route("register", methods=['GET', 'POST'])
def register():
    """register user and handle form submit / if user in currently in session redirect"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """create login form / handle login"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = [
                "Incorrect username/password.... Please Try Again"]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route('/secret', methods=['GET'])
def secret():
    """secret route part 3....."""

    return f{"You Made It!"}
