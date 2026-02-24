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
    
    def ajouter(self,date, items,total, statut,user_id = 0 ):
        commande = {
            'user_id': user_id,
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
    
    def getByUserId(self, user_id):
        return self.cdao.findByUserId(user_id)

    def getByUserIdAndStatut(self, user_id, statut):
        return self.cdao.findByUserIdAndStatut(user_id, statut)
    
    def getUpdateByStatut(self, user_id, statut,id):
        return self.cdao.updateByStatut(user_id, statut,id)
        
