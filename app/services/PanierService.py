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

    def ajouterRepas(self, id, nom, prix, quantite):
        self.pdao.ajouterRepas(id, nom, prix, quantite)

    def supprimerRepas(self, id):
        self.pdao.supprimerRepas(id)

    def viderPanier(self):
        self.pdao.viderPanier()

    def getPanierByCount(self, count):
        res = self.pdao.findByCount(count)  
        if len(res) > 0:
            return res
        return [{}]