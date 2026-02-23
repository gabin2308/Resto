class Commandes:
    def __init__(self, dico):
        self.id          = dico.get('id', None)
        self.user_id    = dico.get('user_id', 0)
        self.date        = dico.get('date', None)       
        self.items       = dico.get('items', [])         
        self.total       = dico.get('total', 0.0)
        self.statut      = dico.get('statut', 'en attente') 
        #self.nom_client  = dico.get('nom_client', '')
        #self.adresse     = dico.get('adresse', '')       
        #self.telephone   = dico.get('telephone', '')     