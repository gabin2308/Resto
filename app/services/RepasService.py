from app.models.RepasDAO import RepasSqliteDAO as RepasDAO
from app.models.RepasDAO import RepasDAOInterface

class RepasService:

    def __init__(self):
        self.rdao = RepasDAO()

    def getRepasdAll(self):
        res = self.rdao.findAll()
        return res
    
    def getRepasByName(self, name):
        res = self.rdao.findByName(name)
        if type(res) is not list:
            res = [res]
        return res
    
    def getRepasByPrix(self, prix):
        res = self.rdao.findByPrix(prix)
        if len(res)>0 :
            return res
        return [{}]
    
    def getRepasByVegetarien(self, vegetarien):
        return self.rdao.findByVegetarien(vegetarien)
    
    def getRepasByPays(self, pays):
        
        res = self.rdao.findByPays(pays)

        if len(res) > 0:
            return res
        return [{}]
    
    def getAllPays(self):

        tous = self.rdao.findAll()
        return list({r.pays:1 for r in tous}.values())
    