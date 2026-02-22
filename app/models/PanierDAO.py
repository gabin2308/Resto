import json
import sqlite3
from flask import current_app
from app.models.Panier import Panier
from app.models.PanierDAOInterface import PanierDAOInterface

class PanierSqliteDAO(PanierDAOInterface):

    def __init__(self):
        self.databasename = current_app.root_path + "/database.db"
        self._initTable()

    def _getDbConnection(self):
        connection = sqlite3.connect(self.databasename)
        connection.row_factory = sqlite3.Row
        return connection

    def _initTable(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS paniers (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                items  TEXT    NOT NULL DEFAULT '[]',
                total  REAL    NOT NULL DEFAULT 0.0,
                count  INTEGER NOT NULL DEFAULT 0
            )
        """
        cursor.execute(query)
        connection.commit()
        connection.close()

    def findAll(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM paniers")
        row = cursor.fetchone()
        connection.close()
        if row:
            return Panier({
                'id'   : row['id'],
                'items': json.loads(row['items']),
                'total': row['total'],
                'count': row['count']
            })
        return Panier({'id': None, 'items': [], 'total': 0.0, 'count': 0})

    def findByTotal(self, total):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM paniers WHERE total <= ?", (total,)).fetchall()
        connection.close()
        resultat = []
        for row in rows:
            resultat.append(Panier({
                'id'   : row['id'],
                'items': json.loads(row['items']),
                'total': row['total'],
                'count': row['count']
            }))
        return resultat

    def findCount(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        result = cursor.execute("SELECT SUM(count) FROM paniers").fetchone()
        connection.close()
        return result[0] or 0
    
    def findByCount(self, count):
        connection = self._getDbConnection()
        cursor = connection.cursor()

        # Filtre les paniers dont le count est supérieur ou égal à count
        rows = cursor.execute("""
            SELECT * FROM paniers WHERE count >= ?
        """, (count,)).fetchall()

        connection.close()

        resultat = []
        for row in rows:
            resultat.append(Panier({
                'id'   : row['id'],
                'items': json.loads(row['items']),
                'total': row['total'],
                'count': row['count']
            }))
        return resultat

    def ajouter(self, id, nom, prix, quantite):
        connection = self._getDbConnection()
        cursor = connection.cursor()

        # Récupère le panier existant
        row = cursor.execute("SELECT * FROM paniers LIMIT 1").fetchone()

        if row:
            # Charge les items existants
            items = json.loads(row['items'])

            # Vérifie si l'article est déjà dans le panier
            for item in items:
                if item['id'] == id:
                    item['quantite'] += quantite
                    break
            else:
                # Sinon on l'ajoute
                items.append({'id': id, 'nom': nom, 'prix': prix, 'quantite': quantite})

            # Recalcule total et count
            total = round(sum(i['prix'] * i['quantite'] for i in items), 2)
            count = sum(i['quantite'] for i in items)

            cursor.execute("""
                UPDATE paniers SET items = ?, total = ?, count = ?
                WHERE id = ?
            """, (json.dumps(items), total, count, row['id']))

        else:
            # Crée un nouveau panier
            items = [{'id': id, 'nom': nom, 'prix': prix, 'quantite': quantite}]
            total = round(prix * quantite, 2)
            count = quantite

            cursor.execute("""
                INSERT INTO paniers (items, total, count)
                VALUES (?, ?, ?)
            """, (json.dumps(items), total, count))

        connection.commit()
        connection.close()

    def supprimer(self, id):
        connection = self._getDbConnection()
        cursor = connection.cursor()

        # Récupère le panier existant
        row = cursor.execute("SELECT * FROM paniers LIMIT 1").fetchone()

        if row:
            # Charge les items
            items = json.loads(row['items'])

            # Retire l'article dont l'id correspond
            items = [item for item in items if item['id'] != id]

            # Recalcule total et count après suppression
            total = round(sum(i['prix'] * i['quantite'] for i in items), 2)
            count = sum(i['quantite'] for i in items)

            cursor.execute("""
                UPDATE paniers SET items = ?, total = ?, count = ?
                WHERE id = ?
            """, (json.dumps(items), total, count, row['id']))

        connection.commit()
        connection.close()

    def vider(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM paniers")  
        connection.commit()
        connection.close()
