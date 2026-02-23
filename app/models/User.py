
class User:

    def __init__(self,dico):
        self.id = dico["id"]
        self.username = dico["username"]
        self.password = dico["password"]  
        self.role = dico["role"]      