import xarray as xr
import pandas as pd
import os

grib_file = "/Users/vikrantjamwal/Downloads/data.grib"
if not os.path.exists(grib_file):
    raise FileNotFoundError(f"File not found: {grib_file}")

ds = xr.open_dataset(grib_file, engine="cfgrib")
print(ds)

level_dim = next((x for x in ["level", "isobaricInhPa", "plev"] if x in ds.dims), None)
if level_dim is None:
    raise ValueError("Pressure-level dimension not found.")

lat, lon = 31.53, 78.27
t = ds["t"].sel(latitude=lat, longitude=lon, method="nearest")
z = ds["z"].sel(latitude=lat, longitude=lon, method="nearest")

print("Pressure levels:", t[level_dim].values)

daily_t = t.resample(time="1D").mean()
daily_z = z.resample(time="1D").mean()
monthly_t = t.resample(time="1M").mean()
monthly_z = z.resample(time="1M").mean()

def save_csv(t, z, filename):
    a = t.to_dataframe().reset_index()
    b = z.to_dataframe().reset_index()
    df = pd.merge(a, b, on=["time", level_dim])
    df.rename(columns={"t": "temperature", "z": "geopotential_height"}, inplace=True)
    df.to_csv(filename, index=False)
    print(f"Saved: {filename}")

save_csv(daily_t, daily_z, "/Users/vikrantjamwal/Desktop/ERA5_daily_2024.csv")
save_csv(monthly_t, monthly_z, "/Users/vikrantjamwal/Desktop/ERA5_monthly_2024.csv")
