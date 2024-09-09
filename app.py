import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering

from flask import Flask, jsonify
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
from bson.json_util import dumps
import io
import base64

app = Flask(__name__)

# MongoDB connection
try:
    client = MongoClient(host='localhost', port=27017, serverSelectionTimeoutMS = 1000)
    client.server_info() # trigger exception if cannot connnect to the database
except:
    print("Error, cannot connect to the database.")

db = client['Steams_data']  # Replace with your database name

print(db.list_collection_names())

games = db['Games']  # Replace with your collection name

@app.route('/')
def index():
    return "Welcome to the Flask and MongoDB app!"

# Example route to retrieve data
# @app.route('/data', methods=['GET'])
# def get_data():
#     data = list(games.find({"Release_year": 2015}))
#     print(data)  # Debugging: Print the data to see what’s being retrieved
#     return dumps(data)

@app.route('/top-games/<int:year>')
def top_games(year):
    #query the data for plotting
    data = list(games.find({"Release_year":year}).sort("Metacritic_score", -1).limit(10))

    #prepare data for plotting:
    game_names = [each["Name"] for each in data]
    popularity = [each['Metacritic_score'] for each in data]

    # Create the plot
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=popularity, y=game_names, hue=game_names, palette='viridis', legend=False)
    plt.title(f'Top 10 Games of {year} by the highest Metacritic score')
    plt.xlabel('Metacritic Score')
    plt.ylabel('Game Name')

    # Adjust layout
    plt.tight_layout()
    
    # Save plot to a string buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    # Return the image as a response
    return f'<img src="data:image/png;base64,{img_base64}"/>'

if __name__ == '__main__':
    app.run(debug=True)

