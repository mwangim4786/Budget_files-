from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


transactions_table_content = {
    "1": {
        "trans_No": "QSILKA3L7DX",
        "budget_Id": "bgt-001",
        "user": "Martin Kihungi",
        "date": "20-05-2024",
        "status": "Paid",
        "amount": "150",
        "description": "Shipping"
        },
    "2": {
        "trans_No": "QSI4XGH86FH",
        "budget_Id": "bgt-001",
        "user": "Martin Kihungi",
        "date": "20-05-2024",
        "status": "Paid",
        "amount": "200",
        "description": "Stationery"
        }
    }

approvals_table_content = {
    "1": {
        "request_id": "bgt-003",
        "user": "Martin Kihungi",
        "date": "25-05-2024",
        "status": "Pending",
        "amount": "150"
        },
    "2": {
        "request_id": "bgt-003",
        "user": "Martin Kihungi",
        "date": "25-05-2024",
        "status": "Pending",
        "amount": "150"
        }
    }


ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    #  connect to db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12king34pin@localhost/budget_db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create db object
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Text())
    password = db.Column(db.Text())
    date = db.Column(db.Date())

    def __init__(self, name, email, phone, role, password, date):
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.password = password
        self.date = date

class Transaction(db.Model):
    __tablename__ = 'transactions_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.String(30), unique=True, nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(20), nullable=False)
    merchant_req_id = db.Column(db.String(40),nullable=True)
    mpesa_ref = db.Column(db.String(20),nullable=True)

    def __init__(self, transaction_id, phone_no, amount, created_at, status, merchant_req_id, mpesa_ref):
        self.transaction_id = transaction_id
        self.phone_no = phone_no
        self.amount = amount
        self.created_at = created_at
        self.status = status
        self.merchant_req_id = merchant_req_id
        self.mpesa_ref = mpesa_ref

class Payment(db.Model):
    __tablename__ = 'payments_table'
    id = db.Column(db.Integer, primary_key=True)
    result_code = db.Column(db.Integer)
    phone_no = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    mpesa_ref = db.Column(db.String(20))
    created_at = db.Column(db.DateTime(timezone=True))
    merchant_req_id = db.Column(db.String(40),nullable=True)

    def __init__(self, result_code, phone_no, amount, mpesa_ref, created_at, merchant_req_id):
        self.result_code = result_code
        self.phone_no = phone_no
        self.amount = amount
        self.mpesa_ref = mpesa_ref
        self.created_at = created_at
        self.merchant_req_id = merchant_req_id

def create_db():
    with app.app_context():
        db.create_all()


@app.route('/home')
def hello_world():
    return 'Hello World!'

@app.route('/create')
def create_all():
    # return 'Hello World!'
    create_db()

    return 'ok'


@app.route('/transactions')
def hello():
    # return 'Hello World!'

    return render_template('transactions.html', data=transactions_table_content)


@app.route('/approvals', methods=['POST', 'GET'])
def submit():
    return render_template('approvals.html', data=approvals_table_content)


@app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    if request.method == 'GET':
        users = Users.query.all()
        return render_template('users.html', users=users)
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = "254"+request.form['phone']
        role = request.form['role']
        password = request.form['password']
        date = datetime.today().strftime('%d-%m-%Y')

        if name == '' or email == '' or phone == '' or role == '' or password == '':
            return render_template('users.html', message='Please enter required fields.') 
        
        data = Users(name, email, phone, role, password, date)
        db.session.add(data)
        db.session.commit()
        return render_template('users.html', message='User added successfully.')
        # return redirect("/users")


# @app.route('/users/<int:id>', methods=['GET', 'POST'])
# def edit_user(id):
#     id = request.form['edit_user_id']
#     data = Users.query.filter_by(id==id).first()
#     data.name = 

# @app.route('/submit', methods=['POST', 'GET'])
# def submit_user():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         role = request.form['role']
#         password = request.form['password']
#         date = datetime.today().strftime('%d-%m-%Y')

#         if name == '' or email == '' or phone == '' or role == '' or password == '':
#             return render_template('users.html', message='Please enter required fields.') 
        
#         data = Users(name, email, phone, role, password, date)
#         db.session.add(data)
#         db.session.commit()
#         # return render_template('success.html')
#         return render_template('users.html', message='User added successfully.')
#         # return redirect("/users")
#     elif request.method == 'GET':
#         users = Users.query.all()
#         return render_template('users.html', users=users)



# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         customer = request.form['customer']
#         dealer = request.form['dealer']
#         rating = request.form['rating']
#         comments = request.form['comments']
#         # print(customer, dealer, rating, comments)
#         if customer == '' or dealer == '':
#             return render_template('index.html', message='Please enter required fields.') 
#         if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
#             data = Feedback(customer, dealer, rating, comments)
#             db.session.add(data)
#             db.session.commit()
#             return render_template('success.html')
#         return render_template('index.html', message='Hello '+customer+', you have already submitted feedback.')
    










if __name__ == '__main__':
    app.run()
    