import json

import psycopg2
import psycopg2.extras
import logging
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
                        users JSON)""")
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS FlaskSessions(
                        ID INT PRIMARY KEY,
                        user_id BIGINT,
                        CONSTRAINT fk_user
                            FOREIGN KEY(user_id)
                                REFERENCES Users(ID))""")
            self.base.commit()
            cur.close()
            logging.log(logging.INFO,msg="Success")
        except Exception as e:
            logging.log(logging.ERROR,msg=e)


    def dropTables(self):
        logging.log(level=logging.INFO, msg="Trying to drop tables")
        cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        self.base.commit()
        cur.close()
        logging.log(level=logging.INFO,msg="Dropped all tables")


    def makeChat(self, chatid):
        cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS Chat_{chatid}(
                    ID SERIAL PRIMARY KEY,
                    from_user BIGINT,
                    message_text TEXT,
                    send_date DATE,
                    captions JSON)""")
        self.base.commit()


    def makeCaptions(self, chatid):
        try:
            logging.log(level=logging.INFO,msg=f"Trying to make captions table for chat {chatid}")
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(f"""
                            CREATE TABLE IF NOT EXISTS ChatMedia_{chatid}(
                            ID SERIAL PRIMARY KEY,
                            path TEXT,
                            type INT)""")
            self.base.commit()
            cur.close()
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
            cur.execute("INSERT INTO Users (username, password, profile_pic_path) VALUES (%s, %s, %s)",(username,password,DEFAULT_PROFILE_PIC_PATH))
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
            user = cur.fetchone()
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
    def getUserChats(self, id=None,username=None):
        try:
            cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if id:
                cur.execute("SELECT chats FROM Users WHERE ID = %s",(id,))
            else:
                cur.execute("SELECT chats FROM Users WHERE username = %s", (username,))
            chats = json.loads(cur.fetchone()[0])

        except Exception as e:
            logging.log(level=logging.ERROR, msg=e)


    # --------------------MESSAGE------------------------------
    def handleMessagePost(self):
        pass


    def handleMessageGet(self):
        pass

    # ---------------------------------------------------------


    #-------------------------MEDIA------------------------
    def getMedia(self, name):
        logging.log(level=logging.INFO, msg=f"Getting {name} from DB")
        cur = self.base.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT path FROM Storage WHERE name = %s", (name,))
        res = cur.fetchone()


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
            pass
        elif action=="":
            pass
