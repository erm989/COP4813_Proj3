from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, DecimalField
from flask import Flask, render_template, request

app = Flask(__name__)

app.config["SECRET_KEY"] = "cop4813_a3"
app.config["MONGO_URI"] = "mongodb+srv://erm989:cop4813_a3@project3.n5qt8.mongodb.net/db?ssl=true&ssl_cert_reqs=CERT_NONE"
# app.config["MONGO_URI"] = "mongodb+srv://erm989:cop4813_a3@project3.n5qt8.mongodb.net/db?retryWrites=true&w=majority"

mongo = PyMongo(app)


class Expenses(FlaskForm):

    description = StringField('Description')
    category = SelectField('Category', choices=[('rent', 'Rent'),
                                                ('electricity', 'Electricity'),
                                                ('car', 'Car'),
                                                ('insurance', 'Insurance'),
                                                ('gas', 'Gas'),
                                                ('restaurants', 'Restaurants'),
                                                ('cell', 'Cell'),
                                                ('clothing', 'Clothing'),
                                                ('travel', 'Travel')])
    cost = DecimalField('Cost')
    date = DateField('Date', format='%m-%d-%Y')


def get_total_expenses(category):

    total_expenses = 0

    query = {"category": category}
    records = mongo.db.expenses.find(query)

    for i in records:
        total_expenses += float(i["cost"])
    return total_expenses


@app.route('/')
def index():

    my_expenses = mongo.db.expenses.find()
    total_cost = 0

    for i in my_expenses:
        total_cost += float(i["cost"])

    expensesByCategory = [("rent", get_total_expenses("rent")),
                          ("electricity", get_total_expenses("electricity")),
                          ("car", get_total_expenses("car")),
                          ("insurance", get_total_expenses("insurance")),
                          ("gas", get_total_expenses("gas")),
                          ("restaurants", get_total_expenses("restaurants")),
                          ("cell", get_total_expenses("cell")),
                          ("clothing", get_total_expenses("clothing")),
                          ("travel", get_total_expenses("travel"))]

    return render_template("index.html", expenses=total_cost, expensesByCategory=expensesByCategory)

@app.route('/addExpenses', methods=['GET', 'POST'])
def addExpenses():

    expensesForm = Expenses(request.form)

    if request.method == 'POST':

        description = request.form['description']
        category = request.form['category']
        cost = request.form['cost']
        date = request.form['date']

        document = {'description': description, 'category': category, 'cost': float(cost), 'date': date}

        mongo.db.expenses.insert_one(document)

        return render_template("expenseAdded.html")
    return render_template("addExpenses.html", form=expensesForm)


app.run()
