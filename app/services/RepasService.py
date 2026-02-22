from app.models.RepasDAO import RepasSqliteDAO as RepasDAO
from app.models.RepasDAO import RepasDAOInterface

class RepasService:

    def __init__(self):
        self.rdao = RepasDAO()

    def getRepasAll(self):
        res = self.rdao.findAll()
        return res
    
    def getRepasByNom(self, name):
        res = self.rdao.findByNom(name)
        if type(res) is not list:
            res = [res]
        return res
    
    def getRepasByPrix(self, prix):
        res = self.rdao.findByPrix(prix)
        if len(res) > 0 :
            return res
        return [{}]
    
    def getRepasByCategorie(self, categorie):
        return self.rdao.findByCategorie(categorie)
    
    def getRepasByStatut(self, statut):
        
        res = self.rdao.findByStatut(statut)

        if len(res) > 0:
            return res
        return [{}]
    
    def getAllCategorie(self):

        tous = self.rdao.findAll()
        
        return list({r.categorie: 1 for r in tous}.keys())
    
    

    