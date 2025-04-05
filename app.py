import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import datetime

app = Dash(__name__)

def load_data():
    df = pd.read_csv("data/prices.csv", names=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

app.layout = html.Div([
    html.H1("💸 Bitcoin Price Tracker (CryptoCompare)"),
    html.Div(id="latest-price", style={"fontSize": 28, "marginBottom": "20px"}),
    dcc.Graph(id="price-graph"),
    dcc.Interval(id="interval", interval=30*1000, n_intervals=0)  # Refresh every 30s
])

@app.callback(
    [Output("latest-price", "children"),
     Output("price-graph", "figure")],
    [Input("interval", "n_intervals")]
)
def update_dashboard(n):
    df = load_data()
    latest = df.iloc[-1]
    latest_price = f"Last price: ${latest['price']:.2f} at {latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"

    fig = go.Figure(data=go.Scatter(x=df["timestamp"], y=df["price"], mode="lines+markers"))
    fig.update_layout(title="Bitcoin Price over Time", xaxis_title="Time", yaxis_title="USD")

    return latest_price, fig

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)

