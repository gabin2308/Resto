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
    
    def findByName(self, name):
        import unicodedata
        import re

        def normalize(text):

            text = unicodedata.normalize('NFD',text)
            text = ''.join(char for char in text if unicodedata.cathegory(char) != 'Mn')
            text = re.sub(r'[^a-z0-9\s]', '', text.lower())

            prefixes_suffixes =[
                "le", "la", "les", "un", "une", "des", "du", "de", "d'", "et", "en", "au", "aux"
            ]
            words = text.split()
            words = [word for word in words if word not in prefixes_suffixes]
            return " ".join(words)
        normalized_name = normalize(name)
        for repas in self.repas:
            for r in repas:
                if normalize(r["nom"]) == normalized_name:
                    return Repas(r)
        return []
    

    
    def findByPays(self, pays):
        repas_found = []
        for repas in self.repas:
            for r in repas:
                if r.get("pays", "").lower() == pays.lower():
                    repas_found.append(Repas(r))
        return repas_found
    
    def findByPrix(self, prix):
        repas_found = []
        for repas in self.repas:
            for r in repas:
                if r.get("prix", 0) <= prix:
                    repas_found.append(Repas(r))
        return repas_found

class RepasSqliteDAO(RepasDAOInterface):

    def __init__(self):
        self.databasename = current_app.root_path + "/database.db"

    def getDbconnection(self):

        connection = sqlite3.connect(self.databasename)
        connection.row_factory = sqlite3.Row
        return connection
    
    def findAll(self):
        connection = self.getDbconnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM plats")
        rows = cursor.fetchall()
        connection.close()
        repas_list = []
        for row in rows:
            repas = Repas(row)
            repas_list.append(repas)
        return repas_list
    
    def findByName(self, name):
        connection = self.getDbconnection()

        cursor = connection.cursor()

        query = "SELECT * FROM plats WHERE nom LIKE ?"

        rows = cursor.execute(query, (f"%{name}%",)).fetchall()
        connection.close()

        return  [Repas(dict(row)) for row in rows]
    
    def findByPrix(self, prix):
        connection = self.getDbconnection()
        cursor = connection.cursor()
        query = "SELECT * FROM plats WHERE prix <= ?"
        rows = cursor.execute(query, (prix,)).fetchall()
        connection.close()
        repas_list = []
        for row in rows:
            repas = Repas(row["id"], row["nom"], row["description"], row["pays"], row["vegetarien"], row["prix"])
            repas_list.append(repas)
        return repas_list
    
    def findByVegetarien(self, vegetarien):
        connection = self.getDbconnection()
        cursor = connection.cursor()
        query = "SELECT * FROM plats WHERE vegetarien = ?"
        rows = cursor.execute(query, (vegetarien,)).fetchall()
        connection.close()
        repas_list = []
        for row in rows:
            repas = Repas(row["id"], row["nom"], row["description"], row["pays"], row["vegetarien"], row["prix"])
            repas_list.append(repas)
        return repas_list
    
    def findByPays(self, pays):
        connection = self.getDbconnection()
        cursor = connection.cursor()
        query = "SELECT * FROM plats WHERE pays = ?"
        rows = cursor.execute(query, (pays,)).fetchall()
        connection.close()
        repas_list = []
        for row in rows:
            repas = Repas(row["id"], row["nom"], row["description"], row["pays"], row["vegetarien"], row["prix"])
            repas_list.append(repas)
        return repas_list
