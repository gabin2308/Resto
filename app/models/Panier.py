class Panier:

    def __init__(self, dico):
        self.id = dico.get("id", None)
        self.user_id = dico.get('user_id', 0)
        self.items = dico.get("items", [])
        self.total = dico.get("total", 0.0)
        self.count = dico.get("count", 0)

    
    def getItems(self):
        return self.items
    
    def getTotal(self):
        return self.total
    
    def getCount(self):
        return self.count