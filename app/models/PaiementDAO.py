import json
import sqlite3
from flask import current_app
from app.models.Paiement import Paiement
from app.models.PaiementDAOInterface import PaiementDAOInterface
class PaiementSqliteDAO(PaiementDAOInterface):

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
            CREATE TABLE IF NOT EXISTS paiements (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                id_commande INTEGER NOT NULL,
                stripe_id   TEXT    NOT NULL,
                montant     REAL    NOT NULL DEFAULT 0.0,
                statut      TEXT    NOT NULL DEFAULT 'en attente',
                date        TEXT    NOT NULL
            )
        """)
        connection.commit()
        connection.close()

    #  Crée un paiement
    def ajouter(self, paiement):
        connection = self._getDbConnection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO paiements (id_commande, stripe_id, montant, statut, date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                paiement.get('id_commande'),
                paiement.get('stripe_id'),
                paiement.get('montant', 0.0),
                paiement.get('statut', 'en attente'),
                paiement.get('date')
            ))
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    #  Tous les paiements
    def findAll(self):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM paiements").fetchall()
        connection.close()
        return [Paiement(dict(row)) for row in rows]

    #  Paiement par id
    def findById(self, id):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        row = cursor.execute("SELECT * FROM paiements WHERE id = ?", (id,)).fetchone()
        connection.close()
        if row:
            return Paiement(dict(row))
        return None

    #  Paiements d'une commande
    def findByCommande(self, id_commande):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("""
            SELECT * FROM paiements WHERE id_commande = ?
        """, (id_commande,)).fetchall()
        connection.close()
        return [Paiement(dict(row)) for row in rows]

    #  Paiements par statut
    def findByStatut(self, statut):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        rows = cursor.execute("""
            SELECT * FROM paiements WHERE statut = ?
        """, (statut,)).fetchall()
        connection.close()
        return [Paiement(dict(row)) for row in rows]

    #  Paiement par stripe_id (pour vérifier après callback Stripe)
    def findByStripeId(self, stripe_id):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        row = cursor.execute("""
            SELECT * FROM paiements WHERE stripe_id = ?
        """, (stripe_id,)).fetchone()
        connection.close()
        if row:
            return Paiement(dict(row))
        return None

    #  Met à jour le statut (payé / annulé)
    def updateStatut(self, id, statut):
        connection = self._getDbConnection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE paiements SET statut = ? WHERE id = ?
            """, (statut, id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    # Supprime un paiement
    def supprimer(self, id):
        connection = self._getDbConnection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM paiements WHERE id = ?", (id,))
        connection.commit()
        connection.close()
