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
        cursor.execute("SELECT * FROM repas")
        rows = cursor.fetchall()
        connection.close()
        repas_list = []
        for row in rows:
            repas = Repas(row)
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
        query = "SELECT * FROM repas WHERE prix <= ?"
        rows = cursor.execute(query, (prix,)).fetchall()
        connection.close()
        return [Repas(dict(row)) for row in rows]
    
    def findByCategorie(self, categorie):
        connection = self._getDbconnection()
        cursor = connection.cursor()
        query = "SELECT * FROM repas WHERE categorie = ?"
        rows = cursor.execute(query, (categorie,)).fetchall()
        connection.close()
        return [Repas(dict(row)) for row in rows]
    
    def findByStatut(self, statut):
        connection = self._getDbconnection()
        cursor = connection.cursor()
        query = "SELECT * FROM repas WHERE statut = ?"
        rows = cursor.execute(query, (statut,)).fetchall()
        connection.close()
        return [Repas(dict(row)) for row in rows]
    
    