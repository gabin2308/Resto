
class User:

    def __init__(self,dico):
        self.id = dico["id"]
        self.username = dico["username"]
        self.password = dico["password"]  
        self.role = dico["role"]      

    def to_dict(self):
        return {
            "id":       self.id,
            "username": self.username,
            "role":     self.role
            # password intentionnellement exclu pour la sécurité
        }