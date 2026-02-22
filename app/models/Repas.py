class Repas:

    def __init__(self, dico):
        self.id = dico["id"]
        self.nom = dico["nom"]
        self.description = dico["description"]
        self.categorie = dico["categorie"]
        self.prix = dico["prix"]
        self.statut = dico["statut"]
        self.quantite = dico["quantite"]
        
    def getPrix(self):
        return self.prix
    
    def getDescription(self):
        return self.description
    
    def getNom(self):
        return self.nom
    
    def getStatut(self):
        return self.statut
    
    def getCategorie(self):
        return self.categorie
    
    def getQuantite(self):
        return self.quantite
    
    