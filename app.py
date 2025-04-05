import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import datetime

app = Dash(__name__)
app.title = "Bitcoin Tracker"

def load_data():
    df = pd.read_csv("data/prices.csv", names=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# App layout avec du style
app.layout = html.Div(style={
    "backgroundColor": "#1e1e1e",
    "color": "#f1f1f1",
    "fontFamily": "Arial, sans-serif",
    "padding": "40px",
    "minHeight": "100vh"
}, children=[
    html.H1("💸 Bitcoin Price Tracker (CryptoCompare)", style={
        "textAlign": "center",
        "color": "#00FFAB",
        "marginBottom": "40px"
    }),
    
    html.Div(id="latest-price", style={
        "fontSize": "30px",
        "textAlign": "center",
        "marginBottom": "30px"
    }),

    dcc.Graph(id="price-graph", config={"displayModeBar": False}),
    
    dcc.Interval(id="interval", interval=30*1000, n_intervals=0)
])

@app.callback(
    [Output("latest-price", "children"),
     Output("price-graph", "figure")],
    [Input("interval", "n_intervals")]
)
def update_graph(n):
    df = load_data()
    latest_price = df["price"].iloc[-1]

    price_text = f"Dernier prix : {latest_price:.2f} $"
    fig = go.Figure(
        data=go.Scatter(
            x=df["timestamp"],
            y=df["price"],
            mode="lines",
            line=dict(color="#00FFAB")
        )
    )
    fig.update_layout(
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        font=dict(color="#f1f1f1"),
        margin=dict(l=40, r=40, t=20, b=40),
        xaxis_title="Heure",
        yaxis_title="Prix ($)"
    )
    return price_text, fig

if __name__ == "__main__":
    app.run(debug=True)

