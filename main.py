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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin_login"

class Order(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(120))
    item: Mapped[str] = mapped_column(String(100))
    size: Mapped[str] = mapped_column(String(50))
    pickup_time: Mapped[str] = mapped_column(String(10))
    notes: Mapped[str] = mapped_column(String(300))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

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
        size = request.form.get('size', ""),
        pickup_time = request.form['pickup_time'],
        notes = request.form.get('notes', ""),
    )
    db.session.add(order)
    db.session.commit()
    flash("Order placed! We'll inform you by phone.", "success")
    return redirect(url_for("home") + "#order-section")

@app.route('/admin/login', methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin'))
        flash("Wrong username or password.", "error")
        return redirect(url_for('admin_login'))

    return render_template("admin_login.html")

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin():
    orders = db.session.execute(
        db.select(Order).order_by(Order.created_at.desc())
    ).scalars().all()
    return render_template("admin.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)