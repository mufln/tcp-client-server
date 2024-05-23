import datetime
import json
import datetime
import psycopg2
import psycopg2.extras
import logging
from cfg import *
logging.basicConfig(level=logging.INFO)
class Worker():
    #-----------------------INIT---------------------------
    def __init__(self, address, port, user, password, name):
        self.address = address
        self.port = port
        self.user = user
        self.password = password
        self.name = name
        self.base = self.connect()


    def makeTables(self):
        logging.log(logging.INFO,msg="Trying to make tables")
        try:
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Users(
                        ID SERIAL PRIMARY KEY,
                        username TEXT,
                        profile_pic_path TEXT,
                        password TEXT,
                        chats JSON)""")
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Chats(
                        ID SERIAL PRIMARY KEY,
                        chatname TEXT,
                        chat_pic_path TEXT,
                        tags JSON,
                        users JSON,
                        is_direct BOOLEAN)""")
            # cur.execute("""
            #             CREATE TABLE IF NOT EXISTS FlaskSessions(
            #             ID INT PRIMARY KEY,
            #             user_id BIGINT,
            #             CONSTRAINT fk_user
            #                 FOREIGN KEY(user_id)
            #                     REFERENCES Users(ID))""")
            self.base.commit()
            cur.close()
            logging.log(logging.INFO,msg="Success")
        except Exception as e:
            logging.log(logging.ERROR,msg=e)


    def dropTables(self):
        try:
            logging.log(level=logging.INFO, msg="Trying to drop tables")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
            self.base.commit()
            cur.close()
            logging.log(level=logging.INFO,msg="Dropped all tables")
        except Exception as e:
            logging.log(logging.ERROR,msg=e)


    def makeChat(self, chatid, cur):
        try:
            chatTableName = f"Chat_{chatid}"
            cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS """+ chatTableName +"""(
                        ID SERIAL PRIMARY KEY,
                        from_user BIGINT,
                        message_text TEXT,
                        send_date TIME,
                        captions JSON)""")
            cur.execute("INSERT INTO "+ chatTableName +" (from_user, message_text, send_date) VALUES (%s,%s,%s)",(1,"say hello!",datetime.datetime.now()))
            self.base.commit()
            logging.log(level=logging.INFO, msg=f"Made table Chats_{chatid}")
        except Exception as e:
            logging.log(logging.ERROR, msg=e)


    def makeCaptions(self, chatid,cur):
        try:
            logging.log(level=logging.INFO,msg=f"Trying to make captions table for chat {chatid}")
            chatTable = f"ChatMedia_{chatid}"
            cur.execute(f"""
                            CREATE TABLE IF NOT EXISTS """+chatTable+"""(
                            ID SERIAL PRIMARY KEY,
                            path TEXT,
                            type INT)""")
            self.base.commit()
            logging.log(level=logging.INFO,msg="Success")
        except Exception as e:
            logging.log(logging.ERROR,msg=e)


    def connect(self):
        try:
            logging.log(level=logging.INFO, msg=f"Trying to connect to DB {self.name}")
            base = psycopg2.connect(dbname=self.name, host=self.address, user=self.user, password=self.password, port=self.port)
            logging.log(level=logging.INFO,msg="Connected")
            logging.log(level=logging.INFO, msg=f"Success")
            return base
        except Exception as e:
            logging.log(level=logging.INFO, msg=f"Trying to connect to DB again, caught {e}")
            self.connect()


    def close(self):
        try:
            logging.log(level=logging.INFO,msg="Closing DB connection")
            self.base.close()
            logging.log(level=logging.INFO, msg="Success")
        except Exception as e:
            logging.log(level=logging.ERROR,msg=e)
    #---------------------------------------------------------


    #----------------------AUTH-------------------------------
    def getPasswordHash(self, username):
        try:
            logging.log(level=logging.INFO,msg=f"Getting password hash for {username}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT password FROM Users WHERE username = %s",(username,))
            password = cur.fetchone()[0]
            logging.log(level=logging.INFO, msg=f"Successm res = {password}")
            cur.close()
            return password
        except Exception as e:
            logging.log(level=logging.ERROR,msg=e)


    def isUserExist(self, username):
        try:
            logging.log(level=logging.INFO, msg=f"Checking user existance for {username}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM Users WHERE username = %s",(username,))
            res = cur.fetchone()
            logging.log(logging.INFO,msg=f"Checked User {username} existance = {res if res else False}")
            cur.close()
            return res if res else False
        except Exception as e:
            logging.log(level=logging.ERROR,msg=e)


    def registerUser(self, username, password):
        try:
            logging.log(logging.INFO, msg=f"Signing up new user with username = {username} and password hash = {password}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("INSERT INTO Users (username, password, profile_pic_path, chats) VALUES (%s, %s, %s, %s)",(username,password,DEFAULT_PROFILE_PIC_PATH,json.dumps([])))
            self.base.commit()
            cur.close()
            logging.log(logging.INFO,msg=f"Registered new user {username}")
        except Exception as e:
            logging.log(logging.ERROR,msg=e)


    # def addSession(self,username,session_id):
    #     try:
    #         cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #         cur.execute("SELECT ID FROM Users WHERE username=%s",(username,))
    #         user_id = cur.fetchone()[0]
    #         cur.execute("INSERT INTO FlaskSessions (ID,user_id) VALUES (%s,%s)",(session_id,user_id))
    #     except Exception as e:
    #         logging.log(level=logging.ERROR, msg=e)


    # def getSessions(self,username):
    #     try:
    #         logging.log(level=logging.INFO,msg=f"Trying to get sessions for {username}")
    #         cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #         cur.execute("SELECT ID FROM Users WHERE username = %s",(username,))
    #         user_id = cur.fetchone()[0]
    #         cur.execute("SELECT ID FROM Flask_Sessions WHERE user_id",(user_id,))
    #         sessions = cur.fetchall()
    #         # print(sessions)
    #         logging.log(level=logging.INFO,msg=f"Got {sessions}")
    #     except Exception as e:
    #         logging.log(level=logging.ERROR, msg=e)


    # def getUserIDBySessionID(self,session_id):
    #     try:
    #         logging.log(level=logging.INFO,msg=f"trying to get user_id for session {session_id}")
    #         cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #         cur.execute("SELECT user_id FROM FlaskSessions WHERE session_id = %s", (session_id,))
    #         user_id = cur.fetchone()[0]
    #         logging.log(level=logging.INFO, msg=f"trying to get user_id for session {user_id}")
    #         return user_id
    #     except Exception as e:
    #         logging.log(level=logging.ERROR, msg=e)


    def getUserbyID(self,id):
        try:
            logging.log(level=logging.INFO, msg=f"trying to get user by id {id}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM Users WHERE ID = %s", (id,))
            user = dict(cur.fetchone())
            cur.close()
            logging.log(level=logging.INFO, msg=f"Got user {user}")
            return user
        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)


    def getUserbyUsername(self, username):
        try:
            logging.log(level=logging.INFO, msg=f"trying to get user by username {username}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM Users WHERE username = %s", (username,))
            user = cur.fetchone()
            logging.log(level=logging.INFO, msg=f"Got user {user}")
            cur.close()
            return user
        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)


    def setProfilePic(self,path, id = None, username = None):
        try:
            logging.log(level=logging.INFO, msg=f"trying to get user by id {id} with username {username}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if id:
                cur.execute("UPDATE Users SET profile_pic_path%s WHERE id = %s", (path,id))
            else:
                cur.execute("UPDATE Users SET profile_pic_path=%s WHERE username = %s", (path,username))
            self.base.commit()
            cur.close()
            logging.log(level=logging.INFO, msg=f"Updated profile_pic_path for user {username} with id {id} to {path}")
        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)

    # ---------------------------------------------------------


    # -------------------CHATS--------------------------------
    def addChat(self,user_ids, is_direct, name = None ):
        try:
            logging.log(level=logging.INFO,msg=f"Trying to make chat for {user_ids}, is_direct = {is_direct}, chat_name = {name}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if name:
                cur.execute("INSERT INTO Chats (chatname, chat_pic_path, users, is_direct) VALUES (%s,%s,%s,%s) RETURNING ID",(name,'logo2.png',json.dumps(user_ids),is_direct))
            else:
                cur.execute("INSERT INTO Chats (users, chat_pic_path, is_direct) VALUES (%s,%s,%s) RETURNING ID", (json.dumps(user_ids),'logo2.png',is_direct))
            chat_id = cur.fetchone()['id']
            logging.log(level=logging.INFO,msg=f"Added to Chats chat with id {chat_id}")
            self.base.commit()
            self.makeChat(chat_id, cur)
            self.makeCaptions(chat_id,cur)
            for user_id in user_ids:
                cur.execute("SELECT chats FROM Users WHERE id=%s", (user_id,))
                chats = json.dumps(cur.fetchone()['chats'] + [chat_id])
                cur.execute("UPDATE Users SET chats=%s WHERE ID=%s", (chats, user_id))
            self.base.commit()
            cur.close()
            logging.log(level=logging.INFO,msg="Success")
        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)


    def delChat(self, chat_id):
        try:
            logging.log(level=logging.INFO,msg=f"Trying to delete chat {chat_id}")
            cur = self.base.cursor()
            chatTable = f"Chat_{chat_id}"
            chatMediaTable = f"ChatMedia_{chat_id}"
            cur.execute("DROP TABLE "+chatTable)
            cur.execute("DROP TABLE "+chatMediaTable)
            cur.execute("DELETE FROM chats WHERE ID=%s RETURNING users",(chat_id,))
            users = cur.fetchone()[0]
            for user in users:
                cur.execute("SELECT chats FROM Users WHERE ID=%s",(user,))
                chats = cur.fetchone()[0]
                chats.remove(chat_id)
                cur.execute("UPDATE Users SET chats = %s WHERE ID=%s",(json.dumps(chats),user))
            self.base.commit()
            cur.close()
            logging.log(level=logging.INFO,msg="Success")
        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)

    def getChatById(self,chat_id):
        try:
            logging.log(level=logging.INFO,msg=f"Trying to get info about chat {chat_id}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM Chats WHERE ID= %s",(chat_id,))
            chat = dict(cur.fetchone())
            cur.close()
            return chat
        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)

    def getUserChats(self, id=None,username=None):
        try:
            logging.log(level=logging.INFO,msg=f"Trying to get chats for user {id} {username}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if id:
                cur.execute("SELECT * FROM Users WHERE ID = %s",(id,))
            else:
                cur.execute("SELECT * FROM Users WHERE username = %s", (username,))
            user = dict(cur.fetchone())
            chat_ids = user['chats']
            chats = []
            for i in chat_ids:
                inst = {"id":i}
                cur.execute("SELECT * FROM Chats WHERE ID = %s",(i,))
                chat = cur.fetchone()
                if chat['is_direct']:
                    users = chat['users']
                    users.remove(user['id'])
                    to_user_id = users[0]
                    to_user = self.getUserbyID(to_user_id)
                    inst.__setitem__('chat_pic_path',to_user['profile_pic_path'])
                    inst.__setitem__('chatname',to_user['username'])
                    inst.__setitem__('last_message','sample_message_direct')
                else:
                    inst.__setitem__('chat_pic_path',chat['chat_pic_path'])
                    inst.__setitem__('chatname', chat['chatname'])
                    inst.__setitem__('last_message','sample_message_group')
                chats.append(inst)
            cur.close()
            return chats
        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)


    # --------------------MESSAGE------------------------------
    def handleMessagePost(self, chat_id, from_user, message_text = None, captions = None):
        try:
            logging.log(level=logging.INFO,msg=f'trying to post msg to chat {chat_id} from user {from_user}')
            cur = self.base.cursor()
            cur.execute("INSERT INTO Chat_"+chat_id+" (from_user, message_text, send_date, captions) VALUES (%s,%s,%s,%s)",(from_user,message_text,datetime.datetime.now(),captions))
            self.base.commit()
            cur.close()
        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)
        pass


    def handleMessageGet(self, chat_id):
        try:
            logging.log(level=logging.INFO,msg=f'Getting messages from chat {chat_id}')
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM Chats WHERE ID =%s", (chat_id,))
            chat = cur.fetchone()
            cur.execute("SELECT * FROM Chat_"+chat_id+ " ORDER BY ID DESC LIMIT 100")
            messages = [dict(i) for i in cur.fetchall()]
            users = {user_id:self.getUserbyID(user_id) for user_id in chat['users']}
            for message in messages:
                message.__setitem__('from_user', users[message['from_user']])
                message.__setitem__("send_date",message['send_date'].strftime("%H:%M"))
            logging.log(level=logging.INFO, msg=f'Success')
            cur.close()
            return messages
        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)

    # ---------------------------------------------------------


    #-------------------------MEDIA------------------------
    def getMedia(self, name):
        try:
            logging.log(level=logging.INFO, msg=f"Getting {name} from DB")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT path FROM Storage WHERE name = %s", (name,))
            res = cur.fetchone()
            cur.close()
        except Exception as e:
            logging.log(logging.ERROR,msg=e)


if __name__=="__main__":
    import hash
    from cfg import *
    db = Worker(DB_HOST,DB_PORT,DB_USER,DB_PASSWORD,DB_NAME)
    while(True):
        action = input()
        if action=="exit":
            exit(0)
        elif action=="make tables":
            db.makeTables()
        elif action=="register":
            name = input("enter name: ")
            password = input("enter password: ")
            if not db.isUserExist(name):
                print("USER DOESNT EXISTS")
                db.registerUser(name,hash.GeneratePasswordHash(password))
            else:
                print("USER ALREADY EXISTS")
        elif action=="exist":
            name = input("for user: ")
            print(db.isUserExist(name))
        elif action=="login":
            name = input("enter name: ")
            password = input("enter password: ")
            if hash.CheckPasswordHash(db.getPasswordHash(name),password):
                print("Logged in")
            else:
                print("Worng password")
        elif action=="drop":
            db.dropTables()
        elif action=="updatepic":
            path = input("new path: ")
            db.setProfilePic(username='user',path=path)
        elif action=="getuser":
            name = input("username: ")
            print(db.getUserbyUsername(name))
        elif action == "getchats":
            name = input("username: ")
            print(db.getUserChats(username=name))
        elif action == "addchat":
            user_ids = [int(i) for i in input("enter user_ids separate by space ").split()]
            name = input("Enter name or nothing ")
            is_direct = bool(int(input("Is chat direct? 0/1 ")))
            db.addChat(user_ids,is_direct,name if name!="" else None)
        elif action == "delchat":
            id = int(input("enter id "))
            db.delChat(id)
        elif action == "listchats":
            cur = db.base.cursor()
            cur.execute("SELECT * FROM Chats")
            res = cur.fetchall()
            for i in res:
                print(i)
        elif action=="send message":
            pass
        elif action=="fix":
            pass
