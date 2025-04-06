import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from generate_daily_report import generate_daily_report

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

    # Champ pour afficher le prix actuel en USD
    html.Div(id="current-price-usd", style={"textAlign": "center", "marginTop": "20px"}),

    # Champ pour entrer le montant en BTC
    html.Div([
        html.Label(id="amount-label"),  # Utilise l'ID dynamique pour l'étiquette
        dcc.Input(id='btc-amount', type='number', value=0, min=0, step=0.01, style={"width": "50%"}),
        html.Button("Convertir", id="convert-button", style={"marginLeft": "10px"}),
        html.Div(id='conversion-result', style={"marginTop": "20px"})
    ], style={"textAlign": "center", "marginTop": "40px"}),

    # Afficher le rapport quotidien
    html.Div(id="daily-report", style={"textAlign": "center", "marginTop": "20px"})
])

# Callback pour mettre à jour le graphe, le prix actuel et le rapport quotidien
@app.callback(
    [Output("price-graph", "figure"),
     Output("current-price-usd", "children"),
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

    # Récupérer le prix actuel (dernier prix dans la série)
    current_price = df['price'].iloc[-1]  # Dernier prix du DataFrame

    # Générer le rapport quotidien
    report = generate_daily_report(crypto)
    if "error" in report:
        daily_report = f"Aucun rapport disponible pour {crypto.upper()} aujourd'hui."
    else:
        daily_report = [
            html.H3(f"Rapport quotidien pour {crypto.upper()} :"),
            html.P(f"Date: {report['date']}"),
            html.P(f"Prix maximum: ${report['max']}"),
            html.P(f"Prix minimum: ${report['min']}"),
            html.P(f"Volatilité: {report['volatility']} USD"),
            html.P(f"Évolution: {report['evolution_percent']}%")
        ]

    return fig, f"Prix actuel : ${current_price:.2f} USD", daily_report

# Callback pour la conversion de BTC en USD
@app.callback(
    Output('conversion-result', 'children'),
    Input('convert-button', 'n_clicks'),
    State('btc-amount', 'value'),
    State('current-price-usd', 'children'),
    State('crypto-dropdown', 'value')  # Ajouter cet état pour vérifier la crypto sélectionnée
)
def convert_crypto_to_usd(n_clicks, amount, current_price_text, selected_crypto):
    if n_clicks is None:
        return ""
    try:
        # Extraire le prix actuel depuis le texte affiché et nettoyer la chaîne
        price_str = current_price_text.split(":")[1].strip().split(" ")[0]
        
        # Retirer le symbole '$' et convertir en float
        price = float(price_str.replace('$', '').replace(',', ''))

        # Conversion basée sur la crypto sélectionnée
        if selected_crypto == "btc":
            result = amount * price
            return f"{amount} BTC = {result:.2f} USD"
        elif selected_crypto == "eth":
            result = amount * price
            return f"{amount} ETH = {result:.2f} USD"
    except Exception as e:
        return f"Erreur de conversion : {e}"
@app.callback(
    Output('amount-label', 'children'),  # Met à jour l'étiquette du montant
    Input('crypto-dropdown', 'value')  # Écoute le changement de la crypto sélectionnée
)
def update_amount_label(selected_crypto):
    if selected_crypto == "btc":
        return "Montant en BTC:"
    elif selected_crypto == "eth":
        return "Montant en ETH:"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
