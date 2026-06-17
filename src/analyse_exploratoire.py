import duckdb

con = duckdb.connect()

query = """
SELECT 
    "Code postal",
    COUNT(*) AS volume_ventes,
    MEDIAN(prix_m2) AS prix_median_m2,
    MIN(prix_m2) AS prix_min_m2,
    MAX(prix_m2) AS prix_max_m2
FROM 'data/dvf_clean_v3.parquet'
GROUP BY "Code postal"
ORDER BY volume_ventes DESC
"""

print("=== ANALYSE DU MARCHÉ PARISIEN (EXTRAIT JUNOT) ===")
df_result = con.execute(query).df()
print(df_result.to_string(index=False))

con.close()