import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Add the user's entry into the database

        # retrieve input data
        input_name = request.form.get("name")
        input_month = request.form.get("month")
        input_day = request.form.get("day")

        # not all fields filled
        if (
            not input_name
            or not input_month
            or not input_day
            ):
            return redirect("/")

        # insert into database
        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)",
            input_name, input_month, input_day
            )
        # reset database
        # $ cp birthdays.db.bak birthdays.db

        return redirect("/")


    else:

        # Display the entries in the database on index.html
        # read from database
        birthdays_d = db.execute("SELECT * FROM birthdays")

        # loop through all rows
        for birthday_entry in birthdays_d:
            # create birthday string into "birthday" key
            birthday_entry["birthday"] = str(birthday_entry["month"]) + "/" + str(birthday_entry["day"])
            # delete redundant keys
            del birthday_entry["month"]
            del birthday_entry["day"]

        # return database to html
        return render_template("index.html", birthdays_t=birthdays_d)
