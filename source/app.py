from flask import Flask,render_template,request,redirect,jsonify
from models import db,EmployeeModel
from flask_sqlalchemy import SQLAlchemy
import json
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://default:default1@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db.init_app(app)

db.create_all()

@app.route('/' , methods = ['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        return render_template('home.html')
 
@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    print(employees)
    return jsonify(employees)

@app.route('/add_employee', methods = ['POST'])
def insert_record():
    if request.method == 'POST':
        req = json.loads(request.data)
        employee = EmployeeModel(**req)
        db.session.add(employee)
        db.session.commit()
        return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

