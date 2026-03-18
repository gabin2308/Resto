import sqlite3 
from app import app 
from app.models.User import User
from app.models.UserDAOInterface import UserDAOInterface

from flask_bcrypt import bcrypt

class UserSqliteDAO(UserDAOInterface):

    def __init__(self):
        self.databasename = app.root_path + "/database.db"
        self._initTable()

    def _getDbConnection(self):
        
        connection = sqlite3.connect(self.databasename)
        connection.row_factory = sqlite3.Row
        return connection
    
    def _initTable(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'lecteur'
            )
        '''
        cursor.execute(query)
        connection.commit()
        connection.close()

    def _generatePawdHash(self, password):
        password_bytes = password.encode('utf-8')
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        password_hash = hashed_bytes.decode('utf-8')
        return password_hash
    
    def createUser(self, username, password, role='lecteur'):
        connection = self._getDbConnection()
        hashed_password = self._generatePawdHash(password)
        try:
            query = """
                INSERT INTO users (username, password, role)
                VALUES (:username, :password, :role)
            """
            connection.execute(query, {"username": username, "password": hashed_password, "role": role})
            connection.commit()
        except sqlite3.IntegrityError:
            return None  
        finally:
            connection.close()
        return self.findExactByUsername(username)  
    
    def findByUsername(self, username):
        connection = self._getDbConnection()
        query = "SELECT * FROM users WHERE username LIKE :username"
        user = connection.execute(query, {"username":f"%{username}%"}).fetchone()
        connection.close()
        if user: 
            user = User(user)
        return user
    
    def findExactByUsername(self, username):
        connection = self._getDbConnection()
        query = "SELECT * FROM users WHERE username = :username"
        user = connection.execute(query, {"username": username}).fetchone()
        connection.close()
        if user: 
            user = User(user)
        return user
     
    def verifyUser(self, username, password):
        connection = self._getDbConnection()
        query = "SELECT * FROM users WHERE username = :username"
        user = connection.execute(query, {"username": username}).fetchone()
        connection.close()
        if user: 
            password_bytes = password.encode('utf-8')
            stored_hash_bytes = user["password"].encode('utf-8')
            if bcrypt.checkpw(password_bytes, stored_hash_bytes):
                return User(user)
        return None
    
    def findAll(self):
        connection = self._getDbConnection()
        query = "SELECT * FROM users"
        users = connection.execute(query).fetchall()

        instances = list()

        for user in users:
            instances.append(User(user))
        connection.close()
        return instances
            
        
    def getUserById(self, user_id):
        connection = self._getDbConnection()
        user = connection.execute("SELECT * FROM users WHERE id = :id", {"id": user_id}).fetchone()
        connection.close()
        return User(dict(user)) if user else None

    def deleteUser(self, user_id):
        connection = self._getDbConnection()
        try:
            connection.execute("DELETE FROM users WHERE id = :id", {"id": user_id})
            connection.commit()
        finally:
            connection.close()

    def findByRole(self, role):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        users = cursor.execute("SELECT * FROM users WHERE role = ?", (role,)).fetchall()
        connection.close()
        return [User(dict(user)) for user in users]
    
    def updateByRole(self,id,role):

        connection = self._getDbConnection()
        cursor = connection.cursor()
        query = "UPDATE users SET role = ? WHERE  id = ?"
        cursor.execute(query, (role,id))
        connection.commit()
        connection.close()