import pandas as pd
from datetime import datetime
import os

INPUT_FILE = "weather_data.csv"
OUTPUT_FOLDER = "weather_reports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------------------
# LOAD
# -----------------------------------------
def load_weather():
    df = pd.read_csv(INPUT_FILE)
    print(f"[INFO] Loaded {len(df)} weather records.")
    return df

# -----------------------------------------
# PROCESS
# -----------------------------------------
def summarize_weather(df):

    summary = {
        "total_rows": len(df),

        "temperature_summary": df["temperature_c"].describe().to_dict(),
        "humidity_summary": df["humidity_pct"].describe().to_dict(),
        "wind_summary": df["wind_kmh"].describe().to_dict(),
        "rainfall_summary": df["rainfall_mm"].describe().to_dict(),

        "avg_temp_by_city": df.groupby("city")["temperature_c"].mean().round(2).to_dict(),
        "total_rain_by_city": df.groupby("city")["rainfall_mm"].sum().round(2).to_dict(),
        "conditions_count": df["condition"].value_counts().to_dict(),
    }

    return summary

# -----------------------------------------
# EXPORT
# -----------------------------------------
# def export_report(summary):
#     ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     file = f"{OUTPUT_FOLDER}/weather_report_{ts}.xlsx"

#     with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
#         pd.DataFrame([summary["total_rows"]], columns=["total_rows"]).to_excel(
#             writer, sheet_name="Summary", index=False
#         )

#         pd.DataFrame(summary["temperature_summary"]).to_excel(writer, sheet_name="Temperature Summary")
#         pd.DataFrame(summary["humidity_summary"]).to_excel(writer, sheet_name="Humidity Summary")
#         pd.DataFrame(summary["wind_summary"]).to_excel(writer, sheet_name="Wind Summary")
#         pd.DataFrame(summary["rainfall_summary"]).to_excel(writer, sheet_name="Rainfall Summary")

#         pd.DataFrame.from_dict(summary["avg_temp_by_city"], orient="index",
#                                columns=["avg_temp"]).to_excel(writer, sheet_name="Avg Temp by City")

#         pd.DataFrame.from_dict(summary["total_rain_by_city"], orient="index",
#                                columns=["total_rainfall"]).to_excel(writer, sheet_name="Rain by City")

#         pd.DataFrame.from_dict(summary["conditions_count"], orient="index",
#                                columns=["count"]).to_excel(writer, sheet_name="Conditions Breakdown")

#     print(f"[SUCCESS] Weather report saved → {file}")


def export_report(summary):
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file = f"{OUTPUT_FOLDER}/weather_report_{ts}.xlsx"

    with pd.ExcelWriter(file) as writer:

        # 1. Summary rows
        pd.DataFrame({"total_rows": [summary["total_rows"]]}).to_excel(
            writer, sheet_name="Summary", index=False
        )

        # 2. Temperature Summary
        pd.DataFrame.from_dict(summary["temperature_summary"], orient="index",
                               columns=["value"]).to_excel(writer, sheet_name="Temperature Summary")

        # 3. Humidity Summary
        pd.DataFrame.from_dict(summary["humidity_summary"], orient="index",
                               columns=["value"]).to_excel(writer, sheet_name="Humidity Summary")

        # 4. Wind Summary
        pd.DataFrame.from_dict(summary["wind_summary"], orient="index",
                               columns=["value"]).to_excel(writer, sheet_name="Wind Summary")

        # 5. Rainfall Summary
        pd.DataFrame.from_dict(summary["rainfall_summary"], orient="index",
                               columns=["value"]).to_excel(writer, sheet_name="Rainfall Summary")

        # 6. Average Temp by City
        pd.DataFrame.from_dict(summary["avg_temp_by_city"], orient="index",
                               columns=["avg_temp"]).to_excel(writer, sheet_name="Avg Temp by City")

        # 7. Total Rainfall by City
        pd.DataFrame.from_dict(summary["total_rain_by_city"], orient="index",
                               columns=["total_rainfall"]).to_excel(writer, sheet_name="Rain by City")

        # 8. Weather Condition Counts
        pd.DataFrame.from_dict(summary["conditions_count"], orient="index",
                               columns=["count"]).to_excel(writer, sheet_name="Conditions Breakdown")

    print(f"[SUCCESS] Weather report saved → {file}")


# -----------------------------------------
# MAIN
# -----------------------------------------
def main():
    df = load_weather()
    summary = summarize_weather(df)
    export_report(summary)

if __name__ == "__main__":
    main()
