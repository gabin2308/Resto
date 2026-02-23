from app.models.UserDAO import UserSqliteDAO as UserDAO
class UserService():

    def __init__(self):
        self.udao = UserDAO()
    
    def getUserByUsername(self, username):

        res =self.udao.findByUsername(username)

        if type(res) is not list:
            res = [res]
        return res
    
    def getUsers(self):

        res = self.udao.findAll()

        return res  
    
    def login(self, username, password):

        res = self.udao.verifyUser(username, password)

        return res
    
    def register(self, username, password):

        res = self.udao.createUser(username, password)

        return res


    def getUserById(self, user_id):
        return self.udao.getUserById(user_id)

    def deleteUser(self, user_id):
        return self.udao.deleteUser(user_id)