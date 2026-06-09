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
# LOAD MAIN TABLE
# ============================================

print("Загружаем metrica_main.csv")

df_main = pd.read_csv("metrica_main.csv")

print(df_main.head())

df_main.to_sql(
    name="fact_metrica_main_1",
    con=engine,
    if_exists="replace",
    index=False
)

print("fact_metrica_main загружена")
print("===================================")
print("ВСЕ ТАБЛИЦЫ УСПЕШНО ЗАГРУЖЕНЫ")