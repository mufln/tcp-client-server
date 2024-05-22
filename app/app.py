import logging
import asyncio
import flask
from cfg import *
from hash import *
from DBWorker import Worker
from flask import Flask
from uuid import uuid4
from flask import render_template, request, flash, redirect, url_for
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user, \
    AnonymousUserMixin
from forms import *
from flask_socketio import join_room, leave_room

app = Flask(__name__)
app.secret_key = SECRET_KEY
socketio = SocketIO(app)
login_manager = LoginManager(app)
# moment = Moment(app)


db = Worker(DB_HOST,DB_PORT,DB_USER,DB_PASSWORD,DB_NAME)
# login_manager.login_view = 'login'


#App view routes
@login_manager.user_loader
def load_user(id):
    logging.log(level=logging.INFO,msg=f"loading user {id}")
    user = UserMixin()
    user.__setattr__("id",id)
    return user


@app.route("/")
def index():
    return redirect("login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    logging.log(level=logging.INFO,msg=f"Logging in {current_user}")
    if current_user.is_authenticated:
        return redirect('chats/')
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        db_user = db.getUserbyUsername(username)
        if db_user and CheckPasswordHash(db_user['password'],password):
            user = UserMixin()
            socketio.emit()
            user.__setattr__("id",db_user[0])
            login_user(user)
            return redirect('chats/')
        flash("Неверные учетные данные")
        redirect('login')
    return render_template("login.html", title='Sign In', form=form)


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username').lower()
    password = request.form.get('password')
    user = db.isUserExist(username)
    if user:
        flash('username already exists')
        return redirect('register')
    db.registerUser(username,GeneratePasswordHash(password))
    return redirect('login')


@app.route('/logout')
@login_required
def logout():
    logging.log(level=logging.INFO,msg=f"Logging out {current_user}")
    logout_user()
    return redirect('login')


@app.route('/chats/', methods=['POST', 'GET'])
@login_required
def chats():
    logging.log(logging.INFO,msg=f'Got request for listing main page from user {current_user.get_id()}')
    chats = db.getUserChats(id = current_user.get_id())
    logging.log(logging.INFO,f'got chats {chats}')
    thisuser = db.getUserbyID(current_user.get_id())
    return render_template("chats.html",users=chats,thisuser=thisuser)


@app.route('/chats/<chat_id>', methods=['POST', 'GET'])
@login_required
def messages(chat_id):
    print(chat_id)
    text = request.form.get('message_text')
    print(text)
    if text:
        db.handleMessagePost(chat_id,current_user.get_id(),text)
    thisuser = db.getUserbyID(current_user.get_id())
    chats = db.getUserChats(id=current_user.get_id())
    chat = [i for i in chats if i['id']==int(chat_id)][0]
    messages = db.handleMessageGet(chat_id)[::-1]
    return render_template("chat.html", messages = messages, users=chats, thisuser=thisuser, chat = chat)


@socketio.on('message')
def handle_message(data):
    print(f'received message: {data}')
    return {'status':200}


if __name__ == "__main__":
    socketio.run(app)