from flask import Flask, send_file
from pymongo import MongoClient
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Use Agg backend for non-GUI rendering
matplotlib.use('Agg')

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['steamdb']  # Replace with your database name
collection = db['games']  # Replace with your collection name

# Helper function to fetch and preprocess data
def fetch_and_prepare_data():
    games_data = pd.DataFrame(list(collection.find({}, {'Genres': 1, 'Price': 1, 'Positive_ratings': 1, 'Average_playtime': 1, '_id': 0})))
    games_data['genres_split'] = games_data['Genres'].str.split(',')
    games_exploded = games_data.explode('genres_split')
    games_exploded['genres_split'] = games_exploded['genres_split'].str.strip()
    return games_exploded

# Helper function to create a chart based on the chart type
def create_chart(chart_type, data):
    fig, ax = plt.subplots(figsize=(8, 6))

    if chart_type == "popularity":
        genre_popularity = data['genres_split'].value_counts()
        sns.barplot(x=genre_popularity.index, y=genre_popularity.values, palette="viridis", ax=ax)
        ax.set_title("Genre Popularity (Total Games)")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Number of Games")

        # Rotate x-axis labels to prevent cutting off
        plt.xticks(rotation=45, ha='right', fontsize=8)

    elif chart_type == "avg_ratings":
        avg_ratings = data.groupby('genres_split')['Positive_ratings'].mean().sort_values(ascending=False)
        sns.barplot(x=avg_ratings.index, y=avg_ratings.values, palette="Blues_d", ax=ax)
        ax.set_title("Average Positive Ratings by Genre")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Average Positive Ratings")

        # Rotate x-axis labels to prevent cutting off
        plt.xticks(rotation=45, ha='right', fontsize=8)

    elif chart_type == "avg_playtime":
        avg_playtime = data.groupby('genres_split')['Average_playtime'].mean().sort_values(ascending=False)
        sns.barplot(x=avg_playtime.index, y=avg_playtime.values, palette="magma", ax=ax)
        ax.set_title("Average Playtime by Genre")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Average Playtime (minutes)")

        # Rotate x-axis labels to prevent cutting off
        plt.xticks(rotation=45, ha='right', fontsize=8)

    elif chart_type == "ratings_vs_playtime":
        # Calculate the average positive ratings and average playtime by genre
        genre_stats = data.groupby('genres_split').agg({
            'Positive_ratings': 'mean',
            'Average_playtime': 'mean'
        }).reset_index()

        # Scatterplot: Average Positive Ratings vs. Average Playtime by Genre
        scatter = ax.scatter(genre_stats['Average_playtime'], genre_stats['Positive_ratings'],
                             c=genre_stats['Positive_ratings'], cmap='viridis', s=100, alpha=0.75)
        ax.set_title("Average Positive Ratings vs Average Playtime by Genre")
        ax.set_xlabel("Average Playtime (minutes)")
        ax.set_ylabel("Average Positive Ratings")

        # Add genre labels as a legend
        handles = []
        for i, genre in enumerate(genre_stats['genres_split']):
            handles.append(ax.scatter([], [], label=genre, color=scatter.cmap(scatter.norm(genre_stats['Positive_ratings'][i])), s=30, alpha=0.5))

        # Create legend for genres
        ax.legend(handles=handles, title="Genres", bbox_to_anchor=(0.90, 1.1), loc='upper left')

    elif chart_type == "revenue":
        data['Revenue'] = data['Price'] * data['Positive_ratings']
        revenue = data.groupby('genres_split')['Revenue'].sum().sort_values(ascending=False)
        sns.barplot(x=revenue.index, y=revenue.values, palette="viridis", ax=ax)
        ax.set_title("Total Revenue by Genre")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Total Revenue (USD)")

        # Rotate x-axis labels to prevent cutting off
        plt.xticks(rotation=45, ha='right', fontsize=8)

    # Save chart to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return img

# Dynamic route to generate charts based on the chart type in the URL
@app.route('/chart/<string:chart_type>', methods=['GET'])
def genre_chart(chart_type):
    if chart_type not in ['popularity', 'avg_ratings', 'avg_playtime', 'ratings_vs_playtime', 'revenue']:
        return "Invalid chart type! Valid options: popularity, avg_ratings, avg_playtime, ratings_vs_playtime, revenue", 400

    # Fetch and prepare data
    games_exploded = fetch_and_prepare_data()

    # Generate the requested chart
    img = create_chart(chart_type, games_exploded)

    # Return the image as a PNG response
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)