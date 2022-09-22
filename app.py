import sqlite3
import random
from flask import Flask, session, flash, redirect, render_template, request, g
from cs50 import SQL

app = Flask(__name__)
app.secret_key = "select_a_COMPLEX_secret_key_please"
app.config["SESSION_COOKIE_NAME"] = "958&"

db = SQL("sqlite:///todo_db.db")


# === Index === #
@app.route("/", methods=["POST", "GET"])
def index():
    session["all_items"], session["all_task"] = get_db()
    return render_template("index.html", all_items=session["all_items"], all_task=session["all_task"])



# === Adding tasks for check === #
@app.route("/add_items", methods=["POST"])
def add_items():
    if request.form["select_items"] in session["all_task"]:
        flash("You cannot add one task twice!", "info")
    elif len(session["all_task"]) > 9:
        flash("You cannot add more task!", "info")
    else:
        session["all_task"].append(request.form["select_items"])
        session.modified = True

    return render_template("index.html", all_items=session["all_items"], all_task=session["all_task"])



# === Adding new tasks to the DB === #
@app.route("/add_new", methods=["GET", "POST"])
def add_new():
    new = request.form.get("new")
    check_task = db.execute("SELECT name FROM todo WHERE name = ? COLLATE NOCASE", new)

    special_characters = "!@#$%^&*()-+?_=,<>/'"""

    if not new:
        flash("This field cannot be empty!", "info")
    elif check_task:
        flash(new + " has already been added!", "info")
    elif any(c in special_characters for c in new):
        flash("Text cannot contain special characters!", "info")
    else:
        db.execute("INSERT INTO todo (name) VALUES (?)", new)
        flash(new + " has been added!", "info")

    return render_template("index.html", all_items=session["all_items"], all_task=session["all_task"])



# === Removing items from checking stage === #
@app.route("/remove_items", methods=["POST"])
def remove_items():
    check_boxes = request.form.getlist("check")

    for item in check_boxes:
        if item in session["all_task"]:
            idx = session["all_task"].index(item)
            session["all_task"].pop(idx)
            session.modified = True

    return render_template("index.html", all_items=session["all_items"], all_task=session["all_task"])



# === Reset the page & the checking items === #
@app.route("/reset", methods=["GET", "POST"])
def reset_task():
    session["all_items"], session["all_task"] = get_db()
    return render_template("index.html", all_items=session["all_items"], all_task=session["all_task"])



# === Getting the DB === #
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('todo_db.db')
        cursor = db.cursor()
        cursor.execute("SELECT name FROM todo ORDER BY name ASC")
        all_data = cursor.fetchall()
        all_data = [str(val[0]) for val in all_data]

        todo_list = all_data.copy()
        random.shuffle(todo_list)
        todo_list = todo_list[:4]
    return all_data, todo_list

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()