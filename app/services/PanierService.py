from app.models.PanierDAO import PanierSqliteDAO as PanierDAO

class PanierService:

    def __init__(self):
        self.pdao = PanierDAO()

    def getAllPanier(self):
        res = self.pdao.findAll()
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

    def ajouter(self, id, nom, prix, quantite):
        self.pdao.ajouter(id, nom, prix, quantite)

    def supprimer(self, id):
        self.pdao.supprimer(id)

    def vider(self):
        self.pdao.vider()

    def getPanierByCount(self, count):
        res = self.pdao.findByCount(count)  
        if len(res) > 0:
            return res
        return [{}]