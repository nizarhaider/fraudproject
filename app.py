from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

app = Flask(__name__)
app.config['DEBUG']= True

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['LoanBuddy']
# Home page route
@app.route('/', methods=['GET','POST'])
def home():
    bank_assets = db['bank'].find_one()['assets']
    return render_template('home.html', bank_assets=bank_assets)

# Customers page route
@app.route('/customers', methods=['GET','POST'])
def customers():
    bank_assets = db['bank'].find_one()['assets']
    # Retrieve the list of customers from the database
    customer_list = db['customers'].find()
    return render_template('customers.html', customers=customer_list, bank_assets=bank_assets)

# Decision route
@app.route('/decision', methods=['POST','GET'])
def decision():
    # Retrieve the customer ID and decision from the form submission
    bank_assets=request.form.get('bank_assets')
    customer_asking = request.form['customer_asking']
    decision = request.form['decision']

    # Find the customer in the database (for example)

    # Calculate the updated bank asset value based on the decision
    if decision == 'approve':
        bank_assets = int(bank_assets) - int(customer_asking)
    else:
        bank_assets = int(bank_assets) + int(customer_asking)

    # Return the updated bank asset value as a JSON response
    return jsonify({'bank_assets': bank_assets})


if __name__ == '__main__':
    app.run()
