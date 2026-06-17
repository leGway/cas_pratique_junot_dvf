import duckdb

con = duckdb.connect(database=':memory:')

query = """
WITH transactions_brutes AS (
    SELECT 
        "Nature mutation",
        TRY_CAST(REPLACE("Valeur fonciere", ',', '.') AS FLOAT) AS valeur_fonciere,
        "Code postal",
        "No voie",
        "Voie",
        "Type local",
        "Code type local",
        TRY_CAST("Surface reelle bati" AS FLOAT) AS surface_bati,
        TRY_CAST("Nombre pieces principales" AS INTEGER) AS nb_pieces
    FROM read_csv_auto('data/ValeursFoncieres-*.txt', sep='|', all_varchar=true)
),

transactions_filtrees AS (
    SELECT *
    FROM transactions_brutes
    WHERE "Nature mutation" = 'Vente' 
      AND surface_bati > 0 
      AND "Type local" IN ('Appartement', 'Maison')
),

transactions_dedoublonnees AS (
    SELECT 
        valeur_fonciere,
        "Code postal",
        "No voie",
        "Voie",
        "Type local",
        MAX(surface_bati) AS surface_lot_principal,
        MAX(nb_pieces) AS nb_pieces
    FROM transactions_filtrees
    GROUP BY 
        valeur_fonciere, 
        "Code postal", 
        "No voie", 
        "Voie", 
        "Type local"
)

SELECT 
    *,
    (valeur_fonciere / surface_lot_principal) AS prix_m2
FROM transactions_dedoublonnees
WHERE (valeur_fonciere / surface_lot_principal) BETWEEN 3000 AND 30000
"""

print("Nettoyage des 3 fichiers DVF en cours via DuckDB...")
# Modification du chemin de destination
con.execute(f"COPY ({query}) TO 'data/dvf_clean.parquet' (FORMAT PARQUET);")
print("✅ Fichier 'dvf_clean.parquet' généré avec succès dans le dossier data/ !")