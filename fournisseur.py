import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('pharmacie.db')

# Création d'un curseur
cursor = conn.cursor()

# Commande SQL pour créer la table
create_table_query = """
CREATE TABLE IF NOT EXISTS medicaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
);
"""

# Exécution de la commande
try:
    cursor.execute(create_table_query)
    print("Table 'medicaments' créée avec succès.")
except sqlite3.Error as e:
    print(f"Erreur lors de la création de la table: {e}")

# Fermeture de la connexion
finally:
    conn.commit()  # Valider les changements
    conn.close()