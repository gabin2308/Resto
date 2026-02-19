import sqlite3,json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "static" / "data" / "repas.json"
SCHEMA_PATH = BASE_DIR / "schema.sql"
DB_PATH = BASE_DIR / "database.db"

with open(json_path) as f:
    plats = json.load(f)

connection = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, encoding="utf-8") as f:
    connection.executescript(f.read())      

cur = connection.cursor()

for p in plats:
    cur.execute("INSERT INTO plats (id,nom, description,pays,vegetarien,prix) VALUES(?,?,?,?,?,?)", (p["id"], p["nom"], p["description"], p["pays"], p["vegetarien"], p["prix"]))


connection.commit()
connection.close()

print("Database initialized successfully.")