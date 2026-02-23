import json
import sqlite3
from flask import current_app, session
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS commandes (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL DEFAULT 0,
                date    TEXT    NOT NULL,
                items   TEXT    NOT NULL DEFAULT '[]',
                total   REAL    NOT NULL DEFAULT 0.0,
                statut  TEXT    NOT NULL DEFAULT 'en attente'
            )
        """)
        connection.commit()
        connection.close()

    ##ef createCommande(self, form):
        ##connection = self._getDbConnection()
        ##try:
            ##cursor = connection.cursor()
            ##user_id = session["user_id"]
            ##cursor.execute("""
                #INSERT INTO commandes (user_id, date, items, total, statut)
                #VALUES (?, ?, ?, ?, ?)
            #""",(
                ##user_id,
                ##form.get('date'),
                ##form.get('items'),
                ##float(form.get('total', 0.0)),
                ##form.get('statut', 'en attente')
            #))
            ##connection.commit()
            ##return cursor.lastrowid
        ##except Exception as e:
            ##connection.rollback()
            ##raise e
        ##finally:
            ##connection.close()

    def findAllCommande(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM commandes ORDER BY date DESC").fetchall()
        connection.close()
        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'     : row['id'],
                'user_id': row['user_id'],
                'date'   : row['date'],
                'items'  : json.loads(row['items']),
                'total'  : row['total'],
                'statut' : row['statut']
            }))
        return resultat

    #  Nouvelle méthode — commandes d'un utilisateur
    def findByUserId(self, user_id):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("""
            SELECT * FROM commandes WHERE user_id = ? ORDER BY date DESC
        """, (user_id,)).fetchall()
        connection.close()
        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'     : row['id'],
                'user_id': row['user_id'],
                'date'   : row['date'],
                'items'  : json.loads(row['items']),
                'total'  : row['total'],
                'statut' : row['statut']
            }))
        return resultat

    #  Commandes d'un utilisateur filtrées par statut
    def findByUserIdAndStatut(self, user_id, statut):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("""
            SELECT * FROM commandes WHERE user_id = ? AND statut = ? ORDER BY date DESC
        """, (user_id, statut)).fetchall()
        connection.close()
        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'     : row['id'],
                'user_id': row['user_id'],
                'date'   : row['date'],
                'items'  : json.loads(row['items']),
                'total'  : row['total'],
                'statut' : row['statut']
            }))
        return resultat

    def findByTotal(self, total):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM commandes WHERE total = ?", (total,)).fetchall()
        connection.close()
        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'     : row['id'],
                'user_id': row['user_id'],
                'date'   : row['date'],
                'items'  : json.loads(row['items']),
                'total'  : row['total'],
                'statut' : row['statut']
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
                'id'     : row['id'],
                'user_id': row['user_id'],
                'date'   : row['date'],
                'items'  : json.loads(row['items']),
                'total'  : row['total'],
                'statut' : row['statut']
            }))
        return resultat

    def findAllStatut(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("SELECT DISTINCT statut FROM commandes").fetchall()
        connection.close()
        return [row['statut'] for row in rows]

    def findByDate(self, date):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM commandes WHERE date = ?", (date,)).fetchall()
        connection.close()
        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'     : row['id'],
                'user_id': row['user_id'],
                'date'   : row['date'],
                'items'  : json.loads(row['items']),
                'total'  : row['total'],
                'statut' : row['statut']
            }))
        return resultat

    def findByMois(self, mois):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM commandes WHERE date LIKE ?", (f"%{mois}%",)).fetchall()
        connection.close()
        resultat = []
        for row in rows:
            resultat.append(Commandes({
                'id'     : row['id'],
                'user_id': row['user_id'],
                'date'   : row['date'],
                'items'  : json.loads(row['items']),
                'total'  : row['total'],
                'statut' : row['statut']
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
                'id'     : row['id'],
                'user_id': row['user_id'],
                'date'   : row['date'],
                'items'  : json.loads(row['items']),
                'total'  : row['total'],
                'statut' : row['statut']
            }))
        return resultat

    def ajouter(self, commande):
        connection = self._getDbConnection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO commandes (user_id, date, items, total, statut)
                VALUES (?, ?, ?, ?, ?)
            """, (
                commande.get('user_id'),           #  user_id ajouté
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
        cursor.execute("DELETE FROM commandes WHERE id = ?", (id,))
        connection.commit()
        connection.close()

    def vider(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM commandes")
        connection.commit()
        connection.close()