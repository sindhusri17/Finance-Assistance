from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "finance123"

def get_db():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()

    if user:
        session['user_id'] = user['id']
        return redirect('/dashboard')

    return "Invalid Login"

@app.route('/dashboard')
def dashboard():

    conn = get_db()

    transactions = conn.execute(
        "SELECT * FROM transactions WHERE user_id=?",
        (session['user_id'],)
    ).fetchall()

    total = sum(t['amount'] for t in transactions)
    food_total = sum(t['amount'] for t in transactions if t['category'] == 'Food')
    transport_total = sum(t['amount'] for t in transactions if t['category'] == 'Transport')
    shopping_total = sum(t['amount'] for t in transactions if t['category'] == 'Shopping')
    entertainment_total = sum(t['amount'] for t in transactions if t['category'] == 'Entertainment')  
    budget = 10000

    remaining = budget - total
    recommendation = f"You can save ₹{remaining} this month."
    if remaining > 5000:
     health = "Excellent"
    elif remaining > 2000:
     health = "Good"
    else:
     health = "Needs Improvement"

    return render_template(
    "dashboard.html",
    transactions=transactions,
    total=total,
    budget=budget,
    remaining=remaining,
    recommendation=recommendation,
    health=health,
    food_total=food_total,
    transport_total=transport_total,
    shopping_total=shopping_total,
    entertainment_total=entertainment_total

    )
@app.route('/add_transaction', methods=['POST'])
def add_transaction():

    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']

    conn = get_db()

    conn.execute(
        "INSERT INTO transactions(user_id,amount,category,date) VALUES(?,?,?,?)",
        (session['user_id'], amount, category, date)
    )

    conn.commit()

    return redirect('/dashboard')
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

