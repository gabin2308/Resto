from app.models.CommandesDAO import CommandesSqliteDAO as CommandesDAO


class CommandesService:

    def __init__(self):
        self.cdao = CommandesDAO()

    def getAllCommande(self):
        res = self.cdao.findAllCommande()

        return res
    
    def getByTotal(self, total):
        res = self.cdao.findByTotal(total)
        if len(res) > 0:
            return res
        return [{}]
    
    def getByStatut(self, statut):
        res = self.cdao.findByStatut(statut)
        if len(res) > 0:
            return res
        return []
    
    def ajouter(self,date, items,total, statut ):
        commande = {
            "date": date,
            "items": items,
            "total": total,
            "statut": statut
        }
        return self.cdao.ajouter(commande)
    
    def supprimer(self, id):

        return self.cdao.supprimer(id)
    
    def vider(self):
        return self.cdao.vider()
    
