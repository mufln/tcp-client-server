import logging

import flask
from cfg import *
from hash import *
from DBWorker import Worker
from flask import Flask
from uuid import uuid4
from flask import render_template, request, flash, redirect, url_for
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import *

app = Flask(__name__)
app.secret_key = SECRET_KEY
socketio = SocketIO(app)
# login_manager = LoginManager(app)
# moment = Moment(app)


db = Worker(DB_HOST,DB_PORT,DB_USER,DB_PASSWORD,DB_NAME)
# login_manager.login_view = 'login'


#App view routes
@app.route("/")
def index():
    return render_template("base.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        if db.isUserExist(username) and CheckPasswordHash(db.getPasswordHash(username),password):
            return redirect('/messages')
        flash("Неверные учетные данные")
        redirect('login')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username').lower()
    password = request.form.get('password')
    user = db.isUserExist(username)
    if user:
        flash('Email address already exists')
        return redirect(url_for('register'))
    db.registerUser(username,GeneratePasswordHash(password))
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/messages/', methods=['POST', 'GET'])
@login_required
def messages():
    pass


if __name__ == "__main__":
    socketio.run(app)