import json
import os
import datetime

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Boolean
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mycafe.db'
db.init_app(app)



class Order(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(120))
    item: Mapped[str] = mapped_column(String(100))
    pickup_time: Mapped[str] = mapped_column(String(10))
    notes: Mapped[str] = mapped_column(String(300))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

with app.app_context():
    db.create_all()

@app.context_processor
def inject_globals():
    return { "now": datetime.datetime.now()}

def load_menu():
    with open(os.path.join(app.root_path, "data", "menu.json")) as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("index.html", menu=load_menu())

@app.route("/place_order", methods=["POST"])
def place_order():
    order = Order(
        name = request.form['name'],
        phone = request.form['phone'],
        email = request.form.get('email', ""),
        item = request.form['item'],
        pickup_time = request.form['pickup_time'],
        notes = request.form.get('notes', "")
    )
    db.session.add(order)
    db.session.commit()
    flash("Order placed! We'll inform you by phone.", "success")
    return redirect(url_for("home") + "#order-section")

if __name__ == "__main__":
    app.run(debug=True)