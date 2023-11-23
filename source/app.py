from flask import Flask, render_template, request, redirect, jsonify
from models import db, OrderssModel
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)

env_name = 'TEST'

if env_name == 'TEST':
    load_dotenv(".env.dev")
elif env_name == 'ACC':
    load_dotenv(".env.acc")
elif env_name == 'PROD':
    load_dotenv(".env")

server=os.getenv('server')
database=os.getenv('database')
user=os.getenv('user')
password=os.getenv('password')
port=os.getenv('port')

DB_URL = f"postgresql://{user}:{password}@{server}:{port}/{database}"

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.app_context().push()
db.init_app(app)
db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
        return render_template("home.html")


@app.route("/orders")
def RetrieveList():
    orders = OrderssModel.query.all()
    json_data = [
        dict(
            order_id=order.order_id,
            order_date_time=order.order_date_time,
            order_type=order.order_type,
            order_status=order.order_status,
            gmv=order.gmv,
        )
        for order in orders
    ]
    return jsonify(json_data)


@app.route("/UpdateOrderStatus", methods=["POST"])
def UpdateOrderStatus():
    if request.method == "POST":
        req = json.loads(request.data)
        print(req)
        row = OrderssModel.query.filter_by(order_id=req["order_id"]).first()
        prev_status = row.order_status
        row.order_status = req["order_status"]
        db.session.commit()
        return f"Order status updated from {prev_status} to {req['order_status']}"


@app.route("/CreateOrder", methods=["POST"])
def CreateOrder():
    if request.method == "POST":
        req = json.loads(request.data)
        order = OrderssModel(**req)
        db.session.add(order)
        db.session.commit()
        return "Order Created Successfully"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
