from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import generate_password_hash, check_password_hash
from database_and_tables_file import User, Expense

app = Flask(__name__)
app.secret_key="hkiojo"

@app.route('/' , methods=["GET", "POST"])
def register():  # put application's code here
    if request.method == "POST":
        userName = request.form["u_name"]
        userEmail = request.form["u_email"]
        userPassword = request.form["u_pass"]
        encryptedUserPassword = generate_password_hash(userPassword)
        User.create(name=userName, email=userEmail, password=encryptedUserPassword)
        flash("User created successfully")
    return render_template("register.html")

@app.route('/login' , methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userEmail = request.form["u_email"]
        userPassword = request.form["u_pass"]
        try:
            user = User.get(User.email == userEmail)
            encryptedPassword = user.password
            if check_password_hash(encryptedPassword, userPassword):
                flash("Login sucessful")
                session["loggedIn"]= True
                session["userName"] = user.name
                #redirect the user to home.html
                return redirect(url_for("home"))
        except:
            flash("wrong email or password")

    return render_template("login.html")

@app.route("/home")
def home():
    if not session["loggedIn"]:
        return redirect(url_for(login))
    return render_template("home.html")

@app.route("/add_expense", methods=['GET', 'POST'])
def addExpense(): 
    if not session["loggedIn"]:
        return redirect(url_for(login))
    if request.method == "POST":
        expenseName = request.form["name"]
        expenseCost = request.form["cost"]
        Expense.create(name=expenseName, cost= expenseCost)
        flash("Expense created successfully") 
    return render_template("add_expense.html")

@app.route("/expenses")
def expenses():
    if not session["loggedIn"]:
        return redirect(url_for(login))
    expenses = Expense.select()
    return render_template("expenses.html", expenses= expenses)

@app.route("/delete/<int:id>")
def delete(id):
    if not session["loggedIn"]:
        return redirect(url_for(login))
    Expense.delete().where(Expense.id ==id).execute()
    flash("Expense deleted successfully")
    return redirect(url_for("expenses"))

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    if not session["loggedIn"]:
        return redirect(url_for(login))
    expense = Expense.get(Expense.id == id)
    if request.method == 'POST':
        updatedName = request.form['name']
        updatedCost = request.form['cost']
        expense.name = updatedName
        expense.cost = updatedCost
        expense.save()
        flash('Expense updated successfully')
        return redirect(url_for("expenses"))
    return render_template("update_expense.html", expense = expense)

if __name__ == '__main__':
    app.run()
