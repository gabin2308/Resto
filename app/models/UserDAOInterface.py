class UserDAOInterface:

    def createUser(seld, username, password, role = 'lecteur'):
        pass

    def findByUsername(self, username):
        pass    

    def findByEmail(self, email):
        pass

    def findByRole(self, role):
        pass

    def verifyUser(self, username, password):
        pass

    def findAll(self):
        pass