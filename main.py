from flask import Blueprint, Flask, render_template, url_for, redirect, request, flash
from sql_all import check_person, check_person_real
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from models import *


db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'adbdgdjgjdg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('rememder') else False
    if not check_person([email, password]):
        flash('Пожалуйста проверьте свой логин и попробуйте снова')
        return redirect(url_for('login'))
    return redirect(url_for('profile'))


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    if check_person_real(email):
        print(1)
        flash('Email address already exists')
        return redirect(url_for('signup'))
    new_user = User(email=email, name=name, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    return 'Logout'


if __name__ == "__main__":
    db.create_all(app)
    app.run(debug=True)

