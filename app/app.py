import flask
print(flask.__version__)
from cfg import *
from hash import *
from DBWorker import Worker
from flask import Flask
from uuid import uuid4
from flask import render_template, request, flash, redirect, url_for
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
app = Flask(__name__)

socketio = SocketIO(app)
login_manager = LoginManager(app)
# moment = Moment(app)


db = Worker(DB_HOST,DB_PORT,DB_USER,DB_PASSWORD,DB_NAME)
login_manager.login_view = 'login'


#App view routes
@app.route("/")
def index():
    return render_template("login.html")


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username').lower()
    password = request.form.get('password')
    user = db.isUserExist(username)
    if not user or not CheckPasswordHash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('messages'))


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