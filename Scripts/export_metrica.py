import requests
import pandas as pd
from dotenv import load_dotenv
import os
import calendar
import time

# ============================================
# ENV
# ============================================

load_dotenv()

TOKEN = os.getenv("YANDEX_TOKEN")
COUNTER_ID = os.getenv("COUNTER_ID")

# ============================================
# API
# ============================================

url = "https://api-metrika.yandex.net/stat/v1/data"

headers = {
    "Authorization": f"OAuth {TOKEN}"
}

# ============================================
# PERIOD
# ============================================

start_year = 2025
start_month = 3

end_year = 2026
end_month = 5

# ============================================
# RESULT STORAGE
# ============================================

all_rows = []

# ============================================
# DEVICE MAP
# ============================================

device_map = {
    "desktop": "desktop",
    "smartphone": "mobile",
    "tablet": "tablet",
    "tv": "tv"
}

# ============================================
# DIMENSIONS
# ============================================

dimensions = ",".join([
    "ym:s:date",
    "ym:s:regionArea",
    "ym:s:deviceCategory",
    "ym:s:trafficSource",
    "ym:s:searchEngine"
])

# ============================================
# METRICS
# ============================================

metrics = ",".join([

    "ym:s:visits",
    "ym:s:users",
    "ym:s:pageviews",
    "ym:s:bounceRate",
    "ym:s:avgVisitDurationSeconds",
    "ym:s:pageDepth",
    "ym:s:newUsers",
    "ym:s:percentNewVisitors",
    "ym:s:visitsPerUser"
])

# ============================================
# PERIOD LOOP
# ============================================

year = start_year
month = start_month

while (year < end_year) or (year == end_year and month <= end_month):

    # Первый день месяца
    date1 = f"{year}-{month:02d}-01"

    # Последний день месяца
    last_day = calendar.monthrange(year, month)[1]
    date2 = f"{year}-{month:02d}-{last_day}"

    print(f"\nВыгружаем: {date1} → {date2}")

    # ============================================
    # REQUEST PARAMS
    # ============================================

    params = {
        "ids": COUNTER_ID,
        "dimensions": dimensions,
        "metrics": metrics,
        "date1": date1,
        "date2": date2,
        "accuracy": "full",
        "limit": 100000
    }

    # ============================================
    # REQUEST
    # ============================================

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    # ============================================
    # ERROR CHECK
    # ============================================

    if response.status_code != 200:

        print(f"Ошибка для периода {date1} → {date2}")
        print(response.status_code)
        print(response.text)

    else:

        data = response.json()

        rows_count = len(data.get("data", []))

        print(f"Получено строк: {rows_count}")

        # ============================================
        # PROCESS ROWS
        # ============================================

        for item in data.get("data", []):

            dimensions_data = item["dimensions"]
            metrics_data = item["metrics"]

            # Device normalize
            device_raw = dimensions_data[2]["name"] if len(dimensions_data) > 2 else None
            device_clean = device_map.get(device_raw, device_raw)

            row = {

                # Dimensions
                "date": dimensions_data[0]["name"] if len(dimensions_data) > 0 else None,

                "region_area": (
                    dimensions_data[1]["name"]
                    if len(dimensions_data) > 1
                    else None
                ),

                "device_category": device_clean,

                "traffic_source": (
                    dimensions_data[3]["name"]
                    if len(dimensions_data) > 3
                    else None
                ),

                "source_engine": (
                    dimensions_data[4]["name"]
                    if len(dimensions_data) > 4
                    else None
                ),

                # Metrics
                "visits": metrics_data[0],
                "users": metrics_data[1],
                "pageviews": metrics_data[2],
                "bounce_rate": metrics_data[3],
                "avg_visit_duration_sec": metrics_data[4],
                "page_depth": metrics_data[5],
                "new_users": metrics_data[6],
                "percent_new_visitors": metrics_data[7],
                "visits_per_user": metrics_data[8]
            }

            all_rows.append(row)

    # ============================================
    # API PAUSE
    # ============================================

    time.sleep(1)

    # ============================================
    # NEXT MONTH
    # ============================================

    month += 1

    if month > 12:
        month = 1
        year += 1

# ============================================
# DATAFRAME
# ============================================

df = pd.DataFrame(all_rows)

# ============================================
# SAVE CSV
# ============================================

df.to_csv(
    "metrica_main.csv",
    index=False,
    encoding="utf-8-sig"
)

# ============================================
# FINAL INFO
# ============================================

print("\n===================================")
print("Выгрузка завершена")
print(f"Всего строк: {len(df)}")
print("Файл: metrica_main.csv")

