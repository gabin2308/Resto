import json
import sqlite3
from flask import current_app
from app.models.Commandes import Commandes
from app.models.CommandesDAOInterface import CommandesDAOInterface

class CommandesSqliteDAO(CommandesDAOInterface):

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
            CREATE TABLE IF NOT EXISTS commandes (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                date   TEXT    NOT NULL,
                items  TEXT    NOT NULL DEFAULT '[]',
                total  REAL    NOT NULL DEFAULT 0.0,
                statut TEXT    NOT NULL DEFAULT 'en attente'
            )
        """
        cursor.execute(query)  
        connection.commit()
        connection.close()

    def createCommande(self, form):
        connection = self._getDbConnection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO commandes (date, items, total, statut)
                VALUES (?, ?, ?, ?)
            """, (
                form.get('date'),
                form.get('items'),
                float(form.get('total', 0.0)),
                form.get('statut', 'en attente')
            ))
            connection.commit()
            return cursor.lastrowid

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            connection.close()

    def findAllCommande(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM commandes ORDER BY date DESC").fetchall()  
        connection.close()
        resultat = []
        for row in rows:                                             
            resultat.append(Commandes({
                'id'    : row['id'],
                'date'  : row['date'],
                'items' : json.loads(row['items']),
                'total' : row['total'],
                'statut': row['statut']
            }))
        return resultat     
   
    def findByTotal(self, total):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("""
            SELECT * FROM commandes WHERE total = ?
        """, (total,)).fetchall()
        connection.close()
        resultat = []
        for row in rows:
            resultat.append(Commandes({ 
                'id'    : row['id'],
                'date'  : row['date'],
                'items' : json.loads(row['items']),
                'total' : row['total'],
                'statut': row['statut']  
            }))
        return resultat
    
    def findByStatut(self, statut):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("""
            SELECT * FROM commandes WHERE statut = ? ORDER BY date DESC
        """, (statut,)).fetchall()
        connection.close()
        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'    : row['id'],
                'date'  : row['date'],
                'items' : json.loads(row['items']),
                'total' : row['total'],
                'statut': row['statut']
            }))
        return resultat
    
    def findAllStatut(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()

      
        rows = cursor.execute("""
            SELECT DISTINCT statut FROM commandes
        """).fetchall()

        connection.close()

        
        return [row['statut'] for row in rows]
    
    
    def findByDate(self, date):
        connection = self._getDbConnection()
        cursor = connection.cursor()

        rows = cursor.execute("""
            SELECT * FROM commandes WHERE date = ?
        """, (date,)).fetchall()

        connection.close()

        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'    : row['id'],
                'date'  : row['date'],
                'items' : json.loads(row['items']),
                'total' : row['total'],
                'statut': row['statut']
            }))
        return resultat
    
   
    def findByMois(self, mois):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("""
            SELECT * FROM commandes WHERE date LIKE ?
        """, (f"%{mois}%",)).fetchall()
        connection.close()  
        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'    : row['id'],
                'date'  : row['date'],
                'items' : json.loads(row['items']),
                'total' : row['total'],
                'statut': row['statut']
            }))
        return resultat  

    def findByPeriode(self, date_debut, date_fin):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("""
            SELECT * FROM commandes WHERE date BETWEEN ? AND ?
        """, (date_debut, date_fin)).fetchall()
        connection.close()  
        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'    : row['id'],
                'date'  : row['date'],
                'items' : json.loads(row['items']),
                'total' : row['total'],
                'statut': row['statut']
            }))
        return resultat  
    
    def ajouter(self, commande):
        connection = self._getDbConnection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO commandes (date, items, total, statut)
                VALUES (?, ?, ?, ?)
            """, (
                commande.get('date'),
                json.dumps(commande.get('items', [])),
                commande.get('total', 0.0),  
                commande.get('statut', 'en attente')
            ))
            connection.commit()
            return cursor.lastrowid  

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            connection.close()

    def supprimer(self, id):
        connection = self._getDbConnection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM commandes WHERE id = ?
        """, (id,))

        connection.commit()
        connection.close()

    def vider(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM commandes")  
        connection.commit()
        connection.close()
