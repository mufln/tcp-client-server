import datetime
import logging
import asyncio
import os

import flask
from cfg import *
from hash import *
from DBWorker import Worker
from flask import Flask
from uuid import uuid4
from flask import render_template, request, flash, redirect, url_for
from flask_socketio import SocketIO, emit, send
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import *
from flask_socketio import join_room, leave_room

app = Flask(__name__)
app.secret_key = SECRET_KEY
socketio = SocketIO(app)
login_manager = LoginManager(app)
from hash import *
from werkzeug.datastructures import CombinedMultiDict
# moment = Moment(app)
from werkzeug.utils import secure_filename

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
        username = request.form.get("username").lower()
        password = request.form.get("password")
        db_user = db.getUserbyUsername(username)
        if db_user and CheckPasswordHash(db_user['password'],password):
            user = UserMixin()
            # socketio.emit()
            user.__setattr__("id",db_user[0])
            login_user(user)
            return redirect('chats/')
        flash("Неверные учетные данные")
        return redirect('login')
    return render_template("login.html", title='Sign In', form=form)



@app.route('/register', methods=['POST','GET'])
def register():
    logging.log(level=logging.INFO,msg="Got registration request")
    if current_user.is_authenticated:
        return redirect('chats/')
    form = RegisterForm(CombinedMultiDict((request.files, request.form)))
    # print(form.is_submitted())
    if form.validate_on_submit():
        logging.log(logging.INFO,msg='Validating form')
        username = request.form.get('username').lower()
        # imagefile = request.files.get('docpicker')
        # logging.log(logging.INFO, msg=f"image {imagefile}")
        f = form.docpicker.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('static', filename))

        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = db.isUserExist(username)
        # print(user)
        if user:
            logging.log(logging.INFO, msg='Username already used')
            flash('юзернейм уже используется')
            return redirect('register')
        if password1!=password2:
            logging.log(logging.INFO, msg='Password mismatch')
            flash('пароли не совпадают')
            return redirect('register')
        db.registerUser(username,GeneratePasswordHash(password1),filename)
        return redirect('login')
    return render_template("register.html", title='Sign up', form=form)


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
    thisuser = db.getUserbyID(current_user.get_id())
    # print(thisuser)
    if thisuser==None:
        logout_user()
        redirect('login')
    chats = db.getUserChats(id = current_user.get_id())
    logging.log(logging.INFO,f'got chats {chats}')
    return render_template("chats.html",users=chats,thisuser=thisuser)


@app.route('/chats/<chat_id>', methods=['POST', 'GET'])
@login_required
def messages(chat_id):
    # print(chat_id)
    text = request.form.get('message_text')
    chat = db.getChatById(chat_id)
    # print(chat)
    if chat==None or int(current_user.get_id()) not in chat['users']:
        # print(int(current_user.get_id()),chat['users'])
        return redirect("/chats/")
    if text:
        db.handleMessagePost(chat_id,current_user.get_id(),text)
    thisuser = db.getUserbyID(current_user.get_id())
    chats = db.getUserChats(id=current_user.get_id())
    chat = [i for i in chats if i['id']==int(chat_id)][0]
    messages = db.handleMessageGet(chat_id)
    print(messages)
    if messages:
        messages=messages[::-1]
    return render_template("chat.html", messages = messages, users=chats, thisuser=thisuser, chat = chat)




@app.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
    form = SettingsForm(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit():
        f = form.docpicker.data
        print(f"file {f}")
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(os.getcwd(),'static', filename))
            db.setProfilePic(filename,int(current_user.get_id()))
            flash('фото профиля изменено')
        # filename = secure_filename(f.filename)
        # f.save(os.path.join('static', filename))
        username = request.form.get('username')
        print(f"username {username}")
        if username:
            db.setUserName(current_user.get_id(),username.lower())
            flash('юзернейм изменен')
    user = db.getUserbyID(current_user.get_id())
    return render_template('settings.html',form=form,user=user)


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    user = db.getUserbyID(current_user.get_id())
    return render_template('search.html', user = user)


@socketio.on('message_post')
def handle_message(data):
    logging.log(level=logging.INFO,msg= f'received message: {data}')
    db.handleMessagePost(data['chat_id'],current_user.get_id(),data['message_text'])
    data.__setitem__('from_user', db.getUserbyID(current_user.get_id()))
    data['from_user'].__setitem__('profile_pic_path',url_for('static',filename=data['from_user']['profile_pic_path']))
    data.__setitem__('send_date', datetime.datetime.now().strftime('%H:%M'))
    # join_room(data['room'])
    emit('message_recieve',data,broadcast=True, to=data['chat_id'])


@socketio.on('connection')
def connect(data):
    logging.log(level=logging.INFO,msg= f'recieved connection request for chat: {data}')
    join_room(data['chat_id'])
    pass


@socketio.on('finduser')
def finduser(data):
    logging.log(level=logging.INFO,msg= f'recieved find user request for username: {data}')
    # join_room(data['chat_id'])
    users = db.getUsersByName(data['username'])
    print(users)
    if users:
        for user in users:
            user['profile_pic_path'] = url_for('static',filename=user['profile_pic_path'])
    emit('founduser', users if users else False)


@socketio.on('createchat')
def createchat(data):
    logging.log(level=logging.INFO,msg= f'recieved create chat request for user_id: {data}')
    # join_room(data['chat_id'])
    if data['is_direct']:
        chats = db.getUserChatsCheck(current_user.get_id())
        if not int(data['user_id'][0])==int(current_user.get_id()):
            logging.log(level=logging.INFO,msg='Creating chat')
        else:
            return redirect('createchat')
        for i in chats:
            if data['user_id'][0] in i['users'] and i['is_direct']:
                emit('redirect_to_chat', i['id'], JSON=False)
                return
    else:
        if int(current_user.get_id()) in data['user_id']:
            data['user_id'].remove(int(current_user.get_id()))
    print(data['user_id'])
    chat_id = db.addChat([int(current_user.get_id())]+data['user_id'],data['is_direct'],data['chatname'] if not data['is_direct'] else None)
    emit('redirect_to_chat', chat_id, JSON=False)




if __name__ == "__main__":
    socketio.run(app,allow_unsafe_werkzeug=True)