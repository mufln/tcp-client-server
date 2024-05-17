import psycopg2
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
            cur = self.base.cursor()
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
            self.base.commit()
            logging.log(logging.INFO,msg="Success")
        except Exception as e:
            logging.log(logging.ERROR,msg=e)



    def makeChat(self, chatid):
        cur = self.base.cursor()
        cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS Chat_{chatid}(
                    ID SERIAL PRIMARY KEY,
                    from_user BIGINT,
                    message_text TEXT,
                    send_date DATE,
                    captions JSON)""")
        self.base.commit()


    def makeCaptions(self, chatid):
        cur = self.base.cursor()
        cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS ChatMedia_{chatid}(
                        ID SERIAL PRIMARY KEY,
                        path TEXT,
                        type INT)""")
        self.base.commit()


    def connect(self):
        try:
            logging.log(level=logging.INFO, msg=f"Trying to connect to DB {self.name}")
            base = psycopg2.connect(dbname=self.name, host=self.address, user=self.user, password=self.password, port=self.port)
            logging.log(level=logging.INFO,msg="Connected")
            return base
        except Exception as e:
            logging.log(level=logging.INFO, msg=f"Trying to connect to DB again, caught {e}")
            self.connect()


    def close(self):
        logging.log(level=logging.INFO,msg="Closed DB connection")
        self.base.close()
    #---------------------------------------------------------


    #----------------------AUTH-------------------------------
    def getPasswordHash(self, username):
        cur = self.base.cursor()
        cur.execute("SELECT password FROM Users WHERE username = %s",(username,))
        return cur.fetchone()[0]


    def isUserExist(self, username):
        cur = self.base.cursor()
        logging.log(level=logging.INFO, msg=f"Checking user existance for {username}")
        try:
            cur.execute("SELECT * FROM Users WHERE username = %s",(username,))
            res = cur.fetchone()
            logging.log(logging.INFO,msg=f"Checked User {username} existance = {res if res else False}")
            return res if res else False
        except Exception as e:
            logging.log(level=logging.ERROR,msg=e)


    def registerUser(self, username, password):
        cur = self.base.cursor()
        print(username,password)
        logging.log(logging.INFO, msg=f"Signing up new user with username = {username} and password hash = {password}")
        try:
            cur.execute("INSERT INTO Users (username, password, profile_pic_path) VALUES (%s, %s, %s)",(username,password,DEFAULT_PROFILE_PIC_PATH))
            self.base.commit()
            logging.log(logging.INFO,msg=f"Registered new user {username}")
        except Exception as e:
            logging.log(logging.ERROR,msg=e)
    # ---------------------------------------------------------


    # --------------------MESSAGE------------------------------
    def handleMessagePost(self, ):
        pass


    def handleMessageGet(self, request):
        pass

    # ---------------------------------------------------------


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
            name = input("enter name ")
            password = input("enter password ")
            if not db.isUserExist(name):
                print("USER DOESNT EXISTS")
                db.registerUser(name,hash.GeneratePasswordHash(password))
                print("REGISTERED USER")
            else:
                print("USER ALREADY EXISTS")
        elif action=="exist":
            name = input("for user ")
            print(db.isUserExist(name))
        elif action=="login":
            name = input("enter name ")
            password = input("enter password ")
            if hash.CheckPasswordHash(db.getPasswordHash(name),password):
                print("Logged in")
            else:
                print("Worng password")
        elif action=="":
            pass
