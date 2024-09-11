import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import matplotlib.ticker as ticker

matplotlib.use('Agg')  # Use the Agg backend for rendering

# Create an app
app = Flask(__name__)

# MongoDB connection
try:
    client = MongoClient(host='localhost', port=27017, serverSelectionTimeoutMS = 1000)
    client.server_info()
except: # print the message in case of issues connecting to databse
    print("Error, cannot connect to the database.")

db = client['Steams_data']  # Using same Database name

print(db.list_collection_names())

games_collection = db['Games_collection']  # Using collections which has updated csv data updated_steam_data.csv
# updated_steam_data.csv - this csv file contains total ratings and positive ratings percentage column

# Define the home route
@app.route('/')
def home():
    return (
        "<h1>Welcome to the Steam Data Analysis App API</h1>"
        "<p>Available Routes:</p>"
        "<li><a href='/about'>About</a></li>"
        "<li><a href='/api/v1.0/publishers-vs-positive-ratings'>Top 10 Publishers with highest Positive Ratings</a></li>"
        "<li><a href='/api/v1.0/publishers-vs-positive-rating-percentage'>Top 10 Publishers with highest Positive Rating Percentage (Total Ratings > 40,000)</a></li>"
        "<li><a href='/api/v1.0/publishers-vs-negative-rating'>Top 10 Publishers with highest Negative Ratings</a></li>"
        "</ul>"
    )


# Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return """
<!DOCTYPE html>
<html>
<head>
	<title>Game Ratings Analysis Dashboard</title>
	<style>
		body {
			font-family: Arial, sans-serif;
		}
		h2 {
			color: #337ab7;
		}
	</style>
</head>
<body>
	<h1>About</h1>
	<p>Welcome to the Game Ratings Analysis Dashboard! This platform provides detailed analytics about game publishers and their ratings, based on data collected from the Steam site.</p>
	
	<h2>API Features</h2>
	<ul>
		<li>
			<h3>Top 10 Publishers by Highest Positive Ratings</h3>
			<p>Endpoint: <a href='/api/v1.0/publishers-vs-positive-ratings'>Top 10 Publishers with highest Positive Ratings</a></p>
			<p>This endpoint returns a bar chart visualizing the top 10 game publishers based on their highest positive ratings for a single game. It helps identify which publishers have developed highly acclaimed games within the gaming community.</p>
		</li>
		<li>
			<h3>Top 10 Publishers by Positive Rating Percentage</h3>
			<p>Endpoint: <a href='/api/v1.0/publishers-vs-positive-rating-percentage'>Top 10 Publishers with highest Positive Rating Percentage (Total Ratings > 40,000)</a></p>
			<p>This endpoint showcases the top 10 publishers with the highest positive rating percentage. The visualization filters out publishers with fewer than 40,000 total ratings. This plot gives you information about the publishers that consistently deliver games with high community approval.</p>
		</li>
		<li>
			<h3>Top 10 Publishers by Highest Negative Ratings</h3>
			<p>Endpoint: <a href='/api/v1.0/publishers-vs-negative-rating'>Top 10 Publishers with highest Negative Ratings</a></p>
			<p>This endpoint presents the top 10 publishers whose games received the highest number of negative ratings. It helps users to filter out Publishers which received high negative ratings for a Game.</p>
		</li>
	</ul>
	
	<h2>Contact</h2>
	<ul>
		<li>Project 3 : Group 3 Team</li>
	</ul>
</body>
</html>
    """

@app.route('/api/v1.0/publishers-vs-positive-ratings', methods=['GET'])
def publishers_vs_positive_ratings():
    # Query the Games collection to get the top 10 publishers with the highest positive ratings
    top_publishers = games_collection.aggregate([
        {"$group": {"_id": "$Publishers", "max_positive": {"$max": "$Positive_ratings"}}},
        {"$sort": {"max_positive": -1}},
        {"$limit": 10}
    ])
    
    # Extract publisher names and ratings
    publishers = []
    ratings = []
    for publisher in top_publishers:
        publishers.append(publisher["_id"])
        ratings.append(publisher["max_positive"])
    
    # Create a bar plot with publisher names on the x-axis
    sns.set(style="whitegrid")
    plt.figure(figsize=(18, 10))
    sns.barplot(x=publishers, y=ratings, palette='viridis')
    
    # Customize the plot
    plt.title('Top 10 Publishers by Highest Positive Ratings', fontsize=14, fontweight='bold')
    plt.xlabel('Publishers', fontsize=14, fontweight='bold')
    plt.ylabel('Highest Positive Ratings', fontsize=14, fontweight='bold')
    plt.xticks(rotation=20, ha='right')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    # Save plot to a PNG image in memory
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return f'<img src="data:image/png;base64,{plot_url}"/>'


@app.route('/api/v1.0/publishers-vs-positive-rating-percentage', methods=['GET'])
def publishers_vs_positive_rating_percentage():
    # Query the Games collection to get the top 10 publishers with the highest positive rating percentage
    # Aggregate top 10 publishers by negative ratings
    top_publishers = games_collection.aggregate([
        {"$match": {"Total_ratings": {"$gt": 40000}}},
        {"$group": {"_id": "$Publishers", "positive_rating_percentage": {"$max": "$Positive_Rating_Percentage"}}},
        {"$sort": {"positive_rating_percentage": -1}},
        {"$limit": 10}
    ])

    # Extract publisher names and percentages
    publishers = []
    percentages = []
    for publisher in top_publishers:
        publishers.append(publisher["_id"])
        percentages.append(publisher["positive_rating_percentage"])

    # Create a line plot with publisher names on the x-axis
    sns.set(style="whitegrid")
    plt.figure(figsize=(18, 10))
    sns.lineplot(x=publishers, y=percentages, marker='o', palette='viridis')

    # Customize the plot
    plt.title('Top 10 Publishers by Highest Positive Rating Percentage (Total Ratings > 40,000)', fontsize=14, fontweight='bold')
    plt.xlabel('Publishers', fontsize=14, fontweight='bold')
    plt.ylabel('Positive Rating Percentage', fontsize=14, fontweight='bold')
    plt.xticks(rotation=20, ha='right')

    # Save plot to a PNG image in memory
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return f'<img src="data:image/png;base64,{plot_url}"/>'


@app.route('/api/v1.0/publishers-vs-negative-rating', methods=['GET'])
def publishers_vs_negative_ratings():
    # Query the Games collection to get the top 10 publishers with the highest Negative ratings
    top_publishers = games_collection.aggregate([
        {"$group": {"_id": "$Publishers", "max_negative": {"$max": "$Negative_ratings"}}},
        {"$sort": {"max_negative": -1}},
        {"$limit": 10}
    ])
    
    # Extract publisher names and ratings
    publishers = []
    ratings = []
    for publisher in top_publishers:
        publishers.append(publisher["_id"])
        ratings.append(publisher["max_negative"])
    
    # Create a bar plot with publisher names on the x-axis
    sns.set(style="whitegrid")
    plt.figure(figsize=(18, 10))
    sns.barplot(x=publishers, y=ratings, palette='viridis')
    
    # Customize the plot
    plt.title('Top 10 Publishers by Highest Negative Ratings', fontsize=14, fontweight='bold')
    plt.xlabel('Publishers', fontsize=14, fontweight='bold')
    plt.ylabel('Highest Negative Ratings', fontsize=14, fontweight='bold')
    plt.xticks(rotation=20, ha='right')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    # Save plot to a PNG image in memory
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return f'<img src="data:image/png;base64,{plot_url}"/>'


if __name__ == "__main__":
    app.run(debug=True)