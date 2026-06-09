import pandas as pd
from sqlalchemy import create_engine

# ============================================
# PostgreSQL connection
# ============================================
DB_USER = "postgres"
DB_PASSWORD = "12345678"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "analytics_db"

# ============================================
# SQLAlchemy engine
# ============================================
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ============================================
# LOAD GOALS TABLE ONLY
# ============================================
print("Loading 'metrica_goals.csv' into PostgreSQL...")

# Read CSV file
df_goals = pd.read_csv("metrica_goals.csv")

# Optional: inspect first rows
print(df_goals.head())

# Upload to PostgreSQL (replace table if exists)
df_goals.to_sql(
    name="fact_metrica_goals_1",
    con=engine,
    if_exists="replace",
    index=False
)

print("Table 'fact_metrica_goals' has been successfully loaded into PostgreSQL.")

print("===================================")
print("All done.")