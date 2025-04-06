import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from generate_daily_report import generate_daily_report
import json

app = Dash(__name__)
app.title = "Crypto Tracker"

# App layout
app.layout = html.Div(style={
    "backgroundColor": "#1e1e1e",
    "color": "#f1f1f1",
    "fontFamily": "Arial, sans-serif",
    "padding": "40px"
}, children=[
    html.H1("Suivi du prix des cryptos", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="crypto-dropdown",
        options=[
            {"label": "Bitcoin", "value": "btc"},
            {"label": "Ethereum", "value": "eth"}
        ],
        value="btc",
        style={"width": "50%", "margin": "auto", "color": "#000"}
    ),

    dcc.Graph(id="price-graph"),

    # Afficher le rapport quotidien
    html.Div(id="daily-report", style={"textAlign": "center", "marginTop": "20px"})
])

# Callback pour mettre à jour le graphe et le rapport quotidien selon la crypto choisie
@app.callback(
    [Output("price-graph", "figure"),
     Output("daily-report", "children")],
    [Input("crypto-dropdown", "value")]
)
def update_graph_and_report(crypto):
    # Charger les prix pour le graphique
    if crypto == "btc":
        filepath = "data/prices.csv"
    else:
        filepath = "data/eth_prices.csv"

    df = pd.read_csv(filepath, names=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["price"], mode="lines+markers", name=crypto.upper()))
    fig.update_layout(
        title=f"Prix de {crypto.upper()}",
        xaxis_title="Date",
        yaxis_title="Prix en USD",
        template="plotly_dark"
    )

    # Générer le rapport quotidien
    report = generate_daily_report(crypto)
    if "error" in report:
        daily_report = f"Aucun rapport disponible pour {crypto.upper()} aujourd'hui."
    else:
        daily_report = [
            html.H3(f"Rapport quotidien pour {crypto.upper()}:"),
            html.P(f"Date: {report['date']}"),
            html.P(f"Prix d'ouverture: ${report['open']}"),
            html.P(f"Prix de clôture: ${report['close']}"),
            html.P(f"Prix maximum: ${report['max']}"),
            html.P(f"Prix minimum: ${report['min']}"),
            html.P(f"Volatilité: {report['volatility']} USD"),
            html.P(f"Évolution: {report['evolution_percent']}%")
        ]

    return fig, daily_report

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
