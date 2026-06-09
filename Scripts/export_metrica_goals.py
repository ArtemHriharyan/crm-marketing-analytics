import requests
import pandas as pd
from dotenv import load_dotenv
import os
import calendar
import time

# ============================================
# Load environment variables
# ============================================
load_dotenv()
TOKEN = os.getenv("YANDEX_TOKEN")
COUNTER_ID = os.getenv("COUNTER_ID")

# ============================================
# API URL and headers
# ============================================
url = "https://api-metrika.yandex.net/stat/v1/data"
headers = {"Authorization": f"OAuth {TOKEN}"}

# ============================================
# Period
# ============================================
start_year = 2025
start_month = 3
end_year = 2026
end_month = 5

# ============================================
# Result storage
# ============================================
all_rows = []

# ============================================
# Device mapping
# ============================================
device_map = {
    "desktop": "desktop",
    "smartphone": "mobile",
    "tablet": "tablet",
    "tv": "tv"
}

# ============================================
# Dimensions
# ============================================
dimensions = ",".join([
    "ym:s:date",
    "ym:s:regionArea",
    "ym:s:deviceCategory",
    "ym:s:trafficSource",
    "ym:s:searchEngine",
    "ym:s:firstTrafficSource"
])

# ============================================
# Metrics
# ============================================
metrics = ",".join([
    # Phone goals
    "ym:s:goal371484907users",
    "ym:s:goal371490044users",
    "ym:s:goal371498463users",
    "ym:s:goal414675455users",

    # Form goals
    "ym:s:goal371487439users",
    "ym:s:goal371488074users",
    "ym:s:goal371488804users",
    "ym:s:goal371496728users",
    "ym:s:goal371497083users",
    "ym:s:goal371497275users",
    "ym:s:goal371696603users",
    "ym:s:goal371498025users",

    # New users metrics
    "ym:s:upToDaySinceFirstVisitPercentage",   # New users 1 day
    "ym:s:upToWeekSinceFirstVisitPercentage", # New users 1-7 days
    "ym:s:upToMonthSinceFirstVisitPercentage", # New users 8-31 days

    # Unique users
    "ym:s:users",   # Total unique users
    "ym:s:visits"   # Total visits
])

# ============================================
# Loop through months
# ============================================
year = start_year
month = start_month

while (year < end_year) or (year == end_year and month <= end_month):
    date1 = f"{year}-{month:02d}-01"
    last_day = calendar.monthrange(year, month)[1]
    date2 = f"{year}-{month:02d}-{last_day}"

    print(f"\nExporting goals: {date1} → {date2}")

    params = {
        "ids": COUNTER_ID,
        "dimensions": dimensions,
        "metrics": metrics,
        "date1": date1,
        "date2": date2,
        "accuracy": "full",
        "limit": 100000
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"Error for period {date1} → {date2}")
        print(response.status_code)
        print(response.text)
    else:
        data = response.json()
        print(f"Rows retrieved: {len(data.get('data', []))}")

        for item in data.get("data", []):
            dimensions_data = item.get("dimensions", [])
            metrics_data = item.get("metrics", [])

            # Device normalization
            device_raw = dimensions_data[2]["name"] if len(dimensions_data) > 2 else None
            device_clean = device_map.get(device_raw, device_raw)

            # Build row dictionary
            row = {
                # Dimensions
                "date": dimensions_data[0]["name"] if len(dimensions_data) > 0 else None,
                "region_area": dimensions_data[1]["name"] if len(dimensions_data) > 1 else None,
                "device_category": device_clean,
                "traffic_source": dimensions_data[3]["name"] if len(dimensions_data) > 3 else None,
                "source_engine": dimensions_data[4]["name"] if len(dimensions_data) > 4 else None,

                # Phone goals
                "tel_click": metrics_data[0],
                "tel_cont_click": metrics_data[1],
                "tel_fut_click": metrics_data[2],
                "all_tel_click": metrics_data[3],

                # Form goals
                "call_click": metrics_data[4],
                "call_send": metrics_data[5],
                "offer_send": metrics_data[6],
                "form_cont_send": metrics_data[7],
                "order_click": metrics_data[8],
                "order_send": metrics_data[9],
                "fast_order_send": metrics_data[10],
                "banner_send": metrics_data[11],

                # New users metrics
                "new_users_1d": metrics_data[12], 
                "new_users_1_7d": metrics_data[13],
                "new_users_8_31d": metrics_data[14],

                # Unique users
                "unique_users": metrics_data[15],

                # Visits
                "visits": metrics_data[16]
            }

            all_rows.append(row)

    time.sleep(1)
    month += 1
    if month > 12:
        month = 1
        year += 1

# ============================================
# Create DataFrame and save CSV
# ============================================
df = pd.DataFrame(all_rows)
df.to_csv("metrica_goals.csv", index=False, encoding="utf-8-sig")

print("\n===================================")
print("Goals export completed")
print(f"Total rows: {len(df)}")
print("File: metrica_goals.csv")