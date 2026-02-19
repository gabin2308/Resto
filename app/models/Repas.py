class Repas:

    def __init__(self, dico):
        self.id = dico["id"]
        self.nom = dico["nom"]
        self.description = dico["description"]
        self.pays = dico["pays"]
        self.vegetarien = dico["vegetarien"]
        self.prix = dico["prix"]

    def getPrix(self):
        return self.prix
    
    def getDescription(self):
        return self.description
    