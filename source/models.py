from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class OrderssModel(db.Model):
    __tablename__ = "order_table"

    order_id = db.Column(db.String(50), unique=True, primary_key=True)
    order_date_time = db.Column(
        db.DateTime(), server_default=datetime.now().strftime("%D %T")
    )
    order_type = db.Column(db.String(30))
    order_status = db.Column(db.String(80), server_default="PENDING")
    gmv = db.Column(db.Float())

    def __repr__(self):
        return f"{self.order_id}"
