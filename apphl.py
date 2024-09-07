from flask import Flask, send_file
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load cleaned data
df_cleaned = pd.read_csv('cleaned_data.csv')

def create_plot_with_names(x_col, y_col, title, filename):
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    plt.scatter(df_cleaned[x_col], df_cleaned[y_col])
    plt.title(title)
    plt.xlabel('Price')
    plt.ylabel(y_col)
    
    # Annotate each point with game names
    for i, name in enumerate(df_cleaned['Name']):
        ax.annotate(name, (df_cleaned[x_col][i], df_cleaned[y_col][i]), fontsize=8, ha='right')

    plt.savefig(filename)
    plt.close()

@app.route('/plot/positive_vs_price')
def positive_vs_price():
    create_plot_with_names('Price', 'Positive_ratings', 'Positive Reviews vs Price', 'positive_vs_price_with_names.png')
    return send_file('positive_vs_price_with_names.png', mimetype='image/png')

@app.route('/plot/negative_vs_price')
def negative_vs_price():
    create_plot_with_names('Price', 'Negative_ratings', 'Negative Reviews vs Price', 'negative_vs_price_with_names.png')
    return send_file('negative_vs_price_with_names.png', mimetype='image/png')

@app.route('/plot/rating_difference_vs_price')
def rating_difference_vs_price():
    create_plot_with_names('Price', 'Rating_difference', 'Rating Difference vs Price', 'rating_difference_vs_price_with_names.png')
    return send_file('rating_difference_vs_price_with_names.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)