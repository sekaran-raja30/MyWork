import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------------------
# GENERATE 1000+ WEATHER SAMPLES
# -----------------------------------------
def generate_weather_data(output_file="weather_data.csv", rows=1200):

    start_date = datetime(2025, 1, 1)
    data = []

    cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Hyderabad",
              "Kolkata", "Pune", "Jaipur", "Lucknow", "Ahmedabad"]

    for i in range(rows):
        date = start_date + timedelta(minutes=i * 30)  # every 30 mins
        city = random.choice(cities)

        temperature = round(random.uniform(10, 45), 1)         # Celsius
        humidity = random.randint(20, 95)                      # %
        wind_speed = round(random.uniform(1, 40), 1)           # km/h
        rainfall = round(random.uniform(0, 20), 1)             # mm
        condition = random.choice([
            "Sunny", "Cloudy", "Rain", "Thunderstorm",
            "Fog", "Haze", "Drizzle", "Windy"
        ])

        data.append([date, city, temperature, humidity, wind_speed, rainfall, condition])

    df = pd.DataFrame(data, columns=[
        "date", "city", "temperature_c", "humidity_pct",
        "wind_kmh", "rainfall_mm", "condition"
    ])

    df.to_csv(output_file, index=False)
    print(f"[SUCCESS] Generated {rows} rows → {output_file}")

generate_weather_data()
