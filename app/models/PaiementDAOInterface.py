

class PaiementDAOInterface():

    
    def ajouter(self, paiement):
        pass

    def findAll(self):
        pass

    def findById(self, id):
        pass

    def findByCommande(self, id_commande):
        pass

    def findByStatut(self, statut):
        pass

    def findByStripeId(self, stripe_id):
        pass

    def updateStatut(self, id, statut):
        pass
    
    def supprimer(self, id):
        pass