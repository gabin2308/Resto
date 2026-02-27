import app
import json
import sqlite3
from flask import current_app
from app.models.Repas import Repas
from app.models.RepasDAOInterface import RepasDAOInterface

class RepasJsonDAO(RepasDAOInterface):

    def __init__(self):
        self.repas = current_app.root_path + "/repas.json"

    def findAll(self):
      repas_instances = []
      for repas in self.repas:
          for r in repas:
              repas_instances.append(Repas(r))
      return repas_instances
    
    def findByNom(self, nom):
        import unicodedata
        import re

        def normalize(text):

            text = unicodedata.normalize('NFD',text)
            text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
            text = re.sub(r'[^a-z0-9\s]', '', text.lower())

            prefixes_suffixes =[
                "le", "la", "les", "un", "une", "des", "du", "de", "d'", "et", "en", "au", "aux"
            ]
            words = text.split()
            words = [word for word in words if word not in prefixes_suffixes]
            return " ".join(words)
        normalized_name = normalize(nom)
        for repas in self.repas:
            for r in repas:
                if normalize(r["nom"]) == normalized_name:
                    return Repas(r)
        return []
    

    
    def findByCategorie(self, c):
        repas_found = []
        for repas in self.repas:
            for r in repas:
                if r.get("categorie", "").lower() == c.lower():
                    repas_found.append(Repas(r))
        return repas_found
    
    def findByPrix(self, prix):
        repas_found = []
        for repas in self.repas:
            for r in repas:
                if r.get("prix", 0) <= prix:
                    repas_found.append(Repas(r))
        return repas_found
    
    def findStatut(self, s):
        repas_found = []
        for repas in self.repas:
            for r in repas:
                if r.get("statut", "").lower()== s.lower():
                    repas_found.append(Repas(r))
        return repas_found
    
    def findQuatite(self, q):
        repas_found = []
        for repas in self.repas:
            for r in repas:
                if r.repas("quantité", "") <= q :
                    repas_found.append(Repas(r))


    def ajouterRepas(self, nom, description, categorie, prix, statut, quantite):
   

    # Charger le fichier JSON
        with open(self.repas, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Générer un nouvel id automatiquement
        nouvel_id = max((r.get("id", 0) for repas in data for r in repas), default=0) + 1

        # Créer le nouveau repas
        nouveau = {
            "id": nouvel_id,
            "nom": nom,
            "description": description,
            "categorie": categorie,
            "prix": prix,
            "statut": statut,
            "quantite": quantite
        }

        # Ajouter dans la première liste (ou créer une nouvelle)
        if data:
            data[0].append(nouveau)
        else:
            data.append([nouveau])

        # Sauvegarder
        with open(self.repas, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class RepasSqliteDAO(RepasDAOInterface):

    def __init__(self):
        self.databasename = current_app.root_path + "/database.db"

    def _getDbconnection(self):

        connection = sqlite3.connect(self.databasename)
        connection.row_factory = sqlite3.Row
        return connection
    
    def findAll(self):
        connection = self._getDbconnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM repas ORDER BY  prix ASC")
        rows = cursor.fetchall()
        connection.close()
        repas_list = []
        for row in rows:
            repas = Repas(dict(row))
            repas_list.append(repas)
        return repas_list
    
    def findByNom(self, nom):
        connection = self._getDbconnection()

        cursor = connection.cursor()

        query = "SELECT * FROM repas WHERE nom LIKE ?"

        rows = cursor.execute(query, (f"%{nom}%",)).fetchall()
        connection.close()

        return  [Repas(dict(row)) for row in rows]
    
    def findByPrix(self, prix):
        connection = self._getDbconnection()
        cursor = connection.cursor()
        query = "SELECT * FROM repas WHERE prix <= ? ORDER BY prix ASC"
        rows = cursor.execute(query, (prix,)).fetchall()
        connection.close()
        return [Repas(dict(row)) for row in rows]
    
    def findByCategorie(self, categorie):
        connection = self._getDbconnection()
        cursor = connection.cursor()
        query = "SELECT * FROM repas WHERE categorie = ? ORDER BY prix ASC"
        rows = cursor.execute(query, (categorie,)).fetchall()
        connection.close()
        return [Repas(dict(row)) for row in rows]
    
    def findByStatut(self, statut):
        connection = self._getDbconnection()
        cursor = connection.cursor()
        query = "SELECT * FROM repas WHERE statut = ? ORDER BY prix ASC"
        rows = cursor.execute(query, (statut,)).fetchall()
        connection.commit()
        connection.close()
        return [Repas(dict(row)) for row in rows]
    
    def ajouterRepas(self,nom, description, categorie, prix, statut, quantite,photo=None):
        
        connection = self._getDbconnection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO repas ( nom, description, categorie, prix, statut,quantite,photo) VALUES (?,?,?,?,?,?,?)
                       """, ( nom, description, categorie, prix,statut, quantite,photo))
        
        connection.commit()
        connection.close()

    def deleteRepas(self,id):
        
        connection = self._getDbconnection()
        cursor = connection.cursor()
        try:
            connection.execute("DELETE FROM repas WHERE id = :id", {"id": id})
            connection.commit()
        finally:
            connection.close()


    def updateRepas(self, id, n, desc, cat, p, s, q, photo=None):  
        
        connection = self._getDbconnection()
        cursor = connection.cursor()
        if photo:
            query = "UPDATE repas SET nom=?, description=?, categorie=?, prix=?, statut=?, quantite=?, photo=? WHERE id=?"
            cursor.execute(query, (n, desc, cat, p, s, q, photo, id))  
        else:
            query = "UPDATE repas SET nom=?, description=?, categorie=?, prix=?, statut=?, quantite=? WHERE id=?"
            cursor.execute(query, (n, desc, cat, p, s, q, id)) 
        connection.commit()
        connection.close()

    
    