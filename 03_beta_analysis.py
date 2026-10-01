import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/vikrantjamwal/Desktop/ERA5_cleaned_2024.csv")
df = df[["pressure", "temperature", "geopotential_height"]]
df = df.groupby("pressure", as_index=False).mean().sort_values("pressure", ascending=False)

P1, P2 = df["pressure"][:-1].values, df["pressure"][1:].values
T1, T2 = df["temperature"][:-1].values, df["temperature"][1:].values

beta_obs = np.log(P2 / P1) / np.log(T2 / T1)
beta_theory_val = 9.80665 / (0.0065 * 287.05)
beta_theory = np.full_like(beta_obs, beta_theory_val)
beta_diff = beta_obs - beta_theory

pairs = [f"{int(a)}–{int(b)}" for a, b in zip(P1, P2)]
result = pd.DataFrame({
    "Pressure Pair (hPa)": pairs,
    "Mid Pressure": (P1 + P2) / 2,
    "P1": P1, "P2": P2, "T1": T1, "T2": T2,
    "β Observed": beta_obs,
    "β Theoretical": beta_theory,
    "Difference": beta_diff
})

result.to_csv("/Users/vikrantjamwal/Desktop/beta_combined_output.csv", index=False)

plt.figure(figsize=(12, 5))
plt.plot(result["Pressure Pair (hPa)"], result["β Observed"], "o-",
         label="Observed β", color="royalblue", linewidth=2)
plt.plot(result["Pressure Pair (hPa)"], result["β Theoretical"], "s-",
         label="Theoretical β", color="mediumseagreen", linewidth=2)
plt.plot(result["Pressure Pair (hPa)"], result["Difference"], "^-",
         label="Difference", color="indianred", linewidth=2)
plt.xlabel("Pressure Pair (hPa)")
plt.ylabel("β Value")
plt.title("Line Plot: β Comparison vs Pressure Pair")
plt.xticks(rotation=45, ha="right")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

def plot_beta_bar(s, title, xlim):
    plt.figure(figsize=(9, 5))
    w, y = 0.25, np.arange(len(s))
    plt.barh(y-w, s["β Observed"], w, label="Observed β", color="teal")
    plt.barh(y, s["β Theoretical"], w, label="Theoretical β", color="goldenrod")
    plt.barh(y+w, s["Difference"], w, label="Difference", color="indianred")
    plt.yticks(y, s["Pressure Pair (hPa)"])
    plt.xlabel("β Value")
    plt.ylabel("Pressure Pair")
    plt.title(title)
    plt.legend(loc="upper right")
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.xlim(xlim)
    plt.tight_layout()
    plt.show()

subset1 = result[(result["Mid Pressure"] <= 1000) & (result["Mid Pressure"] >= 100)]
subset2 = result[(result["Mid Pressure"] < 100) & (result["Mid Pressure"] >= 10)]

plot_beta_bar(subset1, "Bar Chart: β (1000 hPa to 100 hPa)", (-2, 11))
plot_beta_bar(subset2, "Bar Chart: β (100 hPa to 10 hPa)", (-25, 130))
