import sqlite3

conn = sqlite3.connect("app/database.db")  # adapte le chemin
conn.execute("ALTER TABLE repas ADD COLUMN photo TEXT;")
conn.commit()
conn.close()
print("✅ Colonne photo ajoutée !")