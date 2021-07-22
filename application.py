import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


def trade_table():
    """
    function to check if trade table exists, and create it otherwise
    """
    # check if table exists
    trades_ind = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trades';")
    if len(trades_ind) == 0: # create new table if does not exist
        db.execute(
            """
            CREATE TABLE trades
              (
                 user_id  TEXT NOT NULL,
                 symbol   TEXT NOT NULL,
                 quantity NUMERIC NOT NULL,
                 price    NUMERIC NOT NULL,
                 time     TEXT NOT NULL
              );
            """,
            )
    # reset table
    # $ cp finance.db.bak finance.db


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # retrieve user information
    users0 = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])[0]
    del users0["hash"] # delete password hash

    # retrieve user portfolio information
    trade_table()
    user_port = db.execute(
        """
        SELECT *
        FROM   (SELECT symbol,
                       Sum(quantity)                         AS quantity,
                       Sum(quantity * price) / Sum(quantity) AS average_price
                FROM   trades
                WHERE  user_id = ?
                GROUP  BY symbol)
        WHERE  quantity > 0
               AND symbol <> 'CASH_DEPOSIT';
        """,
        session["user_id"]
        )

    # compute total portfolio value
    total_value = users0["cash"]
    # loop through each security in the the portfolio table
    for security1 in user_port:
        # add total value to portfolio
        total_value += security1["quantity"] * security1["average_price"]

    return render_template("index.html", users_info=users0, total_value=total_value, user_port=user_port)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # retrieve user inputs
        input_symbol = request.form.get("symbol")
        input_quantity = request.form.get("shares")

        # Ensure symbol, shares, was submitted
        if (
            not input_symbol
            or not input_quantity
            ):
            return apology("fill in all required fields", 400)
        # Ensure shares is an integer
        if not input_quantity.isdigit():
            return apology("input positive integer", 400)
        # convert quantity to int
        input_quantity = int(input_quantity)

        # use api to get information
        lookup_r = lookup(input_symbol)
        # if there is no return, ask user input again
        if lookup_r == None:
            return apology("Symbol Not Found", 400)

        # get time
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # retrieve user information
        users0 = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])[0]

        # cash balance after tx
        tx_cash_balance = users0["cash"] - lookup_r["price"] * input_quantity

        # check if user has sufficient cash
        if (tx_cash_balance < 0):
            return apology("not enough cash", 789)

        # update cash balance in database
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?;",
            tx_cash_balance, session["user_id"]
            )

        # add entry to trades table
        db.execute(
            "INSERT INTO trades (user_id, symbol, quantity, price, time) VALUES(?, ?, ?, ?, ?);",
            session["user_id"], lookup_r["symbol"], input_quantity, lookup_r["price"], time_str
            )

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html", gui_prompt="input buy order")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_trades = db.execute(
        """
        SELECT symbol, quantity, price, time FROM trades WHERE user_id = ?;
        """,
        session["user_id"]
        )

    return render_template("history.html", user_trades=user_trades)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # retrieve user inputs
        input_symbol = request.form.get("symbol")
        # use api to get information
        lookup_r = lookup(input_symbol)
        # print(lookup_r)

        # if there is no return, ask user input again
        if lookup_r == None:
            return apology("Symbol Not Found", 400)

        # else return symbol information
        return render_template("quote.html", name_q=lookup_r["name"], symbol_q=lookup_r["symbol"], price_q=lookup_r["price"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html", name_q="Enter a Security Symbol", symbol_q="", price_q="")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # starting cash
    cash_bonus = 10000

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # retrieve user inputs
        input_username = request.form.get("username")
        input_password = request.form.get("password")
        input_confirmation = request.form.get("confirmation")

        # Ensure username, password, and confirmation was submitted
        if (
            not input_username
            or not input_password
            or not input_confirmation
            ):
            return apology("fill in all required fields", 400)
        # ensure that password == confirmation
        if (input_password != input_confirmation):
            return apology("passwords do not match", 400)
        # ensure that username does not exist
        all_users = db.execute("SELECT username FROM users WHERE username = ?;", str(input_username))
        if (len(all_users) != 0):
            return apology("user already exists", 400)

        # generate password_hash
        password_hash = generate_password_hash(input_password)

        # insert into database
        db.execute(
            "INSERT INTO users (username, hash, cash) VALUES(?, ?, ?);",
            input_username, password_hash, cash_bonus
            )

        # go to login page
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # retrieve user inputs
        input_symbol = request.form.get("symbol")
        input_quantity = request.form.get("shares")

        # Ensure symbol, shares, was submitted
        if (
            not input_symbol
            or not input_quantity
            ):
            return apology("fill in all required fields", 403)
        # Ensure shares is an integer
        if not input_quantity.isdigit():
            return apology("input positive integer", 403)
        # convert quantity to int
        input_quantity = int(input_quantity)

        # use api to get information
        lookup_r = lookup(input_symbol)
        # if there is no return, ask user input again
        if lookup_r == None:
            return render_template("sell.html", gui_prompt="symbol not found")

        # get time
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # retrieve user information
        users0 = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])[0]
        # retrieve portfolio information of security
        security_q = db.execute(
            "SELECT Sum(quantity) AS quantity FROM trades WHERE user_id = ? AND symbol = ?;",
            session["user_id"], input_symbol
            )
        # quantity of security
        if len(security_q) == 0:
            security_q = 0
        else:
            security_q = security_q[0]["quantity"]

        # security balance after tx
        security_balance = security_q - input_quantity

        # cash balance after tx
        tx_cash_balance = users0["cash"] + lookup_r["price"] * input_quantity

        # check if user has sufficient quantity of security
        if (security_balance < 0):
            return apology("insufficient quantity of security", 987)

        # update cash balance in database
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?;",
            tx_cash_balance, session["user_id"]
            )

        # add entry to trades table
        db.execute(
            "INSERT INTO trades (user_id, symbol, quantity, price, time) VALUES(?, ?, ?, ?, ?);",
            session["user_id"], lookup_r["symbol"], -input_quantity, lookup_r["price"], time_str
            )

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", gui_prompt="input sell order")


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """deposit or withdraw cash"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # retrieve user inputs
        input_deposit = request.form.get("deposit")

        # Ensure deposit was submitted
        if (
            not input_deposit
            ):
            return render_template("deposit.html", gui_prompt="fill in all required fields")
        # Ensure deposit is a number
        try:
            input_deposit = float(input_deposit)
        except ValueError:
            return render_template("deposit.html", gui_prompt="input a float")

        # get time
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # retrieve user information
        users0 = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])[0]

        # cash balance after tx
        tx_cash_balance = users0["cash"] + input_deposit

        # check if user has sufficient cash
        if (tx_cash_balance < 0):
            return render_template("deposit.html", gui_prompt="not enough cash")

        # update cash balance in database
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?;",
            tx_cash_balance, session["user_id"]
            )

        # add entry to trades table
        db.execute(
            "INSERT INTO trades (user_id, symbol, quantity, price, time) VALUES(?, ?, ?, ?, ?);",
            session["user_id"], "CASH_DEPOSIT", input_deposit, 1, time_str
            )

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("deposit.html", gui_prompt="Deposit Cash")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# $ .schema
# CREATE TABLE users (id INTEGER, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00, PRIMARY KEY(id));
# CREATE UNIQUE INDEX username ON users (username);

