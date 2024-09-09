import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

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

games = db['Games']  # Using same collections name

# Define the home route
@app.route('/')
def home():
    return (
        "<h1>Welcome to the Streams Data Analysis App API</h1>"
        "<p>Available Routes:</p>"
        "<li><a href='/about'>About</a></li>"
        "<li><a href='/api/v1.0/publishers-vs-positive-ratings'>Top 10 Publishers with highest Positive Ratings</a></li>"
        "<li><a href='/api/v1.0/publishers-vs-positive-rating-percentage'>Top 10 Publishers with highest Positive Rating Percentage</a></li>"
        "<li><a href='/api/v1.0/publishers-vs-negative-rating'>Top 10 Publishers with highest Negative Ratings</a></li>"
        "</ul>"
    )


# Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

@app.route('/api/v1.0/publishers-vs-positive-ratings', methods=['GET'])
def publishers_vs_positive_ratings():
    # Query the Games collection to get the top 10 publishers with the highest positive ratings
    # Code

    # Return the result as JSON
    return jsonify({'top_publishers': result})

@app.route('/api/v1.0/publishers-vs-positive-rating-percentage', methods=['GET'])
def publishers_vs_positive_rating_percentage():
    # Query the Games collection to get the top 10 publishers with the highest positive rating percentage
    # Code

    # Return the result as JSON
    return jsonify({'top_publishers': result})


@app.route('/api/v1.0/publishers-vs-negative-rating', methods=['GET'])
def publishers_vs_negative_ratings():
    # Query the Games collection to get the top 10 publishers with the highest Negative ratings
    # Code

    # Return the result as JSON
    return jsonify({'top_publishers': result})

if __name__ == "__main__":
    app.run(debug=True)