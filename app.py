from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import plotly
import json

app = Flask(__name__)

# Load your processed data
df_top_300 = pd.read_csv('processed_data.csv')

@app.route('/')
def index():
    return render_template('hl_index.html')

@app.route('/plot/<plot_type>')
def plot(plot_type):
    if plot_type == 'positive_vs_price':
        fig = px.scatter(
            df_top_300,
            x='Price',
            y='Positive_ratings',
            hover_name='Name',
            hover_data={'Name': True, 'Positive_ratings': True, 'Price': True},
            title="Positive Reviews vs Price"
        )
    elif plot_type == 'negative_vs_price':
        fig = px.scatter(
            df_top_300,
            x='Price',
            y='Negative_ratings',
            hover_name='Name',
            hover_data={'Name': True, 'Negative_ratings': True, 'Price': True},
            title="Negative Reviews vs Price"
        )
    elif plot_type == 'rating_difference_vs_price':
        fig = px.scatter(
            df_top_300,
            x='Price',
            y='Rating_difference',
            hover_name='Name',
            hover_data={'Name': True, 'Rating_difference': True, 'Price': True},
            title="Rating Difference vs Price"
        )
    else:
        return jsonify({'error': 'Invalid plot type'})

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

if __name__ == '__main__':
    app.run(debug=True)