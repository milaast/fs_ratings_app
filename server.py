"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template
from flask import redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""
    # a = jsonify([1,3])
    # return a

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html",
                           users=users)


@app.route("/registration")
def reg_form():
    """Shows user account registration form."""

    return render_template("registration.html")


@app.route("/registration", methods=["POST"])
def create_account():
    """Create user account.

        Checks database and, if e-mail does not exist there yet, creates a
        new user account."""

    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    email = request.form.get("email")

    existing_user = User.query.filter(User.email == email).first()

    if not existing_user:

        new_user = User(email=email,
                        password=password,
                        age=age,
                        zipcode=zipcode)

        db.session.add(new_user)
        db.session.commit()

        flash("You successfully created an account")
        return redirect("/")

    else:
        flash("That e-mail address is already in use!")
        return redirect("/registration")


@app.route("/login")
def show_login():

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def log_user_in():

    email = request.form.get("email")
    form_password = request.form.get("password")

    existing_user = User.query.filter(User.email == email).first()

    if not existing_user:

        flash("You must create an account first")
        return redirect("/login")

    else:

        user_password = existing_user.password

        if form_password != user_password:

            flash("The password you entered does not match your account")
            return redirect("/login")

        else:

            session["email"] = email

            flash("You've successfully logged in")
            return redirect("/")


@app.route("/logout")
def log_user_out():

    session.clear()
    flash("You've successfully logged out")

    return redirect("/")

    # not sure if should redirect or render homepage template


@app.route("/users/*?*")
def show_profile():

    user_id = request.args.get("user_id")

    user_info = User.query.filter(User.user_id == user_id).one()

    user_age = user_info.age
    user_zipcode = user_info.zipcode
    user_email = user_info.email

    ratings_list = db.session.query(Movie.title,
                                    Rating.score).join(Rating).filter(Rating.user_id == user_id).all()

    return render_template("user_profile.html",
                           ratings_list=ratings_list,
                           user_id=user_id,
                           user_age=user_age,
                           user_zipcode=user_zipcode,
                           user_email=user_email)

    # need to fix route to get to requested user by user id


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")
