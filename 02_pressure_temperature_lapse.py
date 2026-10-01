import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("/Users/vikrantjamwal/Desktop/ERA5_daily_2024.csv")
df = df[["time", "isobaricInhPa", "latitude_x", "longitude_x", "temperature", "geopotential_height"]]
df.rename(columns={"time": "date", "isobaricInhPa": "pressure",
                   "latitude_x": "lat", "longitude_x": "lon"}, inplace=True)
df["date"] = pd.to_datetime(df["date"])
df["geopotential_height"] /= 9.81

day15 = df[df["date"].dt.day == 15]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

plt.figure(figsize=(10, 6))
for m in range(1, 13):
    s = day15[day15["date"].dt.month == m]
    if not s.empty:
        plt.plot(s["pressure"], s["geopotential_height"], marker="o", label=months[m-1])
plt.xlabel("Pressure (hPa)")
plt.ylabel("Geopotential Height (m)")
plt.title("Pressure vs Geopotential Height (15th of each month, 2024)")
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
for m in range(1, 13):
    s = day15[day15["date"].dt.month == m]
    if not s.empty:
        plt.plot(s["temperature"], s["geopotential_height"], marker="o", label=months[m-1])
plt.xlabel("Temperature (K)")
plt.ylabel("Geopotential Height (m)")
plt.title("Temperature vs Geopotential Height (15th of each month, 2024)")
plt.legend()
plt.show()

def daily_lapse_rate(s):
    s = s.sort_values("geopotential_height")
    dT = np.diff(s["temperature"])
    dz = np.diff(s["geopotential_height"])
    return np.nanmean((-dT / dz) * 1000)

daily_lapse = df.groupby("date").apply(daily_lapse_rate)
daily_lapse.plot(figsize=(12, 4), title="Daily Mean Lapse Rate (2024)")
plt.ylabel("Lapse Rate (K/km)")
plt.show()

monthly_lapse = daily_lapse.resample("M").mean()
monthly_lapse.plot(figsize=(12, 4), marker="o", title="Monthly Mean Lapse Rate (2024)")
plt.ylabel("Lapse Rate (K/km)")
plt.show()

df.to_csv("/Users/vikrantjamwal/Desktop/ERA5_cleaned_2024.csv", index=False)
daily_lapse.to_csv("/Users/vikrantjamwal/Desktop/ERA5_daily_lapse_2024.csv")
monthly_lapse.to_csv("/Users/vikrantjamwal/Desktop/ERA5_monthly_lapse_2024.csv")
print("All analysis complete.")
