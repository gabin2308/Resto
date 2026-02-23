from app.models.PaiementDAO import PaiementSqliteDAO as PaiementDAO

class PaiementService:

    def __init__(self):
        self.pdao = PaiementDAO()

    #  Crée un paiement
    def ajouter(self, id_commande, stripe_id, montant, statut, date):
        paiement = {
            'id_commande': id_commande,
            'stripe_id'  : stripe_id,
            'montant'    : montant,
            'statut'     : statut,
            'date'       : date
        }
        return self.pdao.ajouter(paiement)

    #  Tous les paiements
    def getAllPaiement(self):
        return self.pdao.findAll()

    #   Paiement par id
    def getById(self, id):
        res = self.pdao.findById(id)
        if res:
            return res
        return None

    #  Paiements d'une commande
    def getByCommande(self, id_commande):
        res = self.pdao.findByCommande(id_commande)
        if len(res) > 0:
            return res
        return []

    #  Paiements par statut
    def getByStatut(self, statut):
        res = self.pdao.findByStatut(statut)
        if len(res) > 0:
            return res
        return []

    #  Paiement par stripe_id
    def getByStripeId(self, stripe_id):
        res = self.pdao.findByStripeId(stripe_id)
        if res:
            return res
        return None

    #  Met à jour le statut
    def updateStatut(self, id, statut):
        return self.pdao.updateStatut(id, statut)

    #  Supprime un paiement
    def supprimer(self, id):
        return self.pdao.supprimer(id)