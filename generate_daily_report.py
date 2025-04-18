import pandas as pd
import json
from datetime import datetime

def generate_daily_report(crypto: str):
    # Charger les données en fonction de la crypto
    if crypto == "btc":
        filepath = "data/prices.csv"
    elif crypto == "eth":
        filepath = "data/eth_prices.csv"
    
    # Charger les prix depuis le fichier CSV
    df = pd.read_csv(filepath, names=["timestamp", "price"])

    # Convertir en datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Garder uniquement les données d'aujourd'hui
    today = pd.Timestamp.now().normalize()
    df_today = df[df["timestamp"].dt.normalize() == today]

    if not df_today.empty:
        open_price = df_today.iloc[0]["price"]
        close_price = df_today.iloc[-1]["price"]
        max_price = df_today["price"].max()
        min_price = df_today["price"].min()
        volatility = df_today["price"].std()
        evolution = ((close_price - open_price) / open_price) * 100

        report = {
            "date": str(today.date()),
            "open": round(open_price, 2),
            "close": round(close_price, 2),
            "min": round(min_price, 2),
            "max": round(max_price, 2),
            "volatility": round(volatility, 2),
            "evolution_percent": round(evolution, 2)
        }

        # Sauvegarder dans un fichier JSON
        with open(f"data/{crypto}_daily_report.json", "w") as f:
            json.dump(report, f, indent=2)

        return report
    else:
        return {"error": "No data for today"}
