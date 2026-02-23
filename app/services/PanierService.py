from app.models.PanierDAO import PanierSqliteDAO as PanierDAO
from flask import session
class PanierService:

    def __init__(self):
        self.pdao = PanierDAO()

    def getAllPanier(self):
        res = self.pdao.findAll(self._getUserId())
        return res  

    def getPanierByTotal(self, total):
        res = self.pdao.findByTotal(total)
        if len(res) > 0:
            return res
        return [{}]

    def getPanierCount(self):
        res = self.pdao.findCount()  
        if res > 0:
            return res
        return 0

    def ajouterRepas(self, id, nom, prix, quantite):
        self.pdao.ajouterRepas(self._getUserId(),id, nom, prix, quantite)

    def supprimerRepas(self, id):
        self.pdao.supprimerRepas(self._getUserId(),id)

    def viderPanier(self):
        self.pdao.viderPanier(self._getUserId())

    def getPanierByCount(self, count):
        res = self.pdao.findByCount(count)  
        if len(res) > 0:
            return res
        return [{}]
    
    def getByUserId(self, user_id):
        return self.pdao.findByUserId(user_id)
    
    def _getUserId(self):
        return session.get('user_id', 0)