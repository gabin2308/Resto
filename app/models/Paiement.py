class Paiement:
    def __init__(self, dico):
        self.id             = dico.get('id', None)
        self.id_commande    = dico.get('id_commande', None)
        self.stripe_id      = dico.get('stripe_id', '')   # id session Stripe
        self.montant        = dico.get('montant', 0.0)
        self.statut         = dico.get('statut', 'en attente')  # en attente / payé / annulé
        self.date           = dico.get('date', None)

    def getMontant(self):    return self.montant
    def getStatut(self):     return self.statut
    def getStripeId(self):   return self.stripe_id