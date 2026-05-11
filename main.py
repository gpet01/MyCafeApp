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

@app.context_processor
def inject_globals():
    return { "now": datetime.datetime.now()}

def load_menu():
    with open(os.path.join(app.root_path, "data", "menu.json")) as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("index.html", menu=load_menu())

if __name__ == "__main__":
    app.run(debug=True)