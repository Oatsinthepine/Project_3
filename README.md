# Project 3 Group 3

## Data Visualisation Track (custom): Steam platform games data visualistion

## Introduction:

This group project is about performing data analysis and visualisations about the Steam games data. The source data was
obtained from the Kaggle website, for details of the data please see the references below. 
The purpose of this project is to present users about some insignts in Steam games data accross multiple years. 
As we are interested in exploring and gaining more information on the world most popular digital distribution platfrom developed by Valve Coorpation. Steam enables users to download, purchase, discuss, publish, recreate, and many more. Therefore, through this project, we would like to show the users about our findings and representing in visual ways via static and dynamic plots.

Here are the main questions we are going to explore in this project:

- What are the most popular 10 games from 2014 to 2024?
- Is there any relationship between users' review and games price?
- Which publishers have the highest positive ratings?
- Do games with certain genre or descriptors tend to be more popular?

## The approach for this project:

1: Download the source data from the kaggle website. Use Pandas to read csv and perform data cleanning. (please noticed
in this step two csv files are being merged together for this group project)
for seeing all the data cleaning and df merging details, please refer to 'Steam_dataset_cleaning.ipynb'

2: save the output file locally in csv and json format. Imported all the cleaned data to MongoDB database.
Please use the 'output_file.json', run the mongo import command: mongoimport -- type json --db Steam_data -c Games --drop --jsonArray output_file.json

3: Peform analysis & visualsations using pymongo to query data and plots using Matplotlib and Seaborn.

4: Create html page and visualise more graph using D3.js and Plotly.js, and interactive webpage for user to interact.
Please refer to the js folder to see the app.js and index.html for details.

5: Using Flask to serve the app.route and enable users to see differnet graphs.
Please refer to app.py file for details.

## Reasons for certain techniques & opeations we done for this project:

- For data frame merging, as upon inspection from source data, there are some data missing in both side of source data, so merged data better suits the project.
- For using NoSQL db of MongoDB. As the cleaned data contains some nested columns which are hard to seperate and store in relational db, so NoSQL is more suitable for storing the data for this project.

## Instruction of viewing & interact with this project:

please git clone to your local, then either you enabling local server or using live server that can open the index.html to see the  JS plots. use the dropdown panel to see different chart based on differnt year. You can view the other charts using the app.py file when running the localhost, enter the designed app route to see per plot.

## Ethical considerations for this project:

The original source data contains some information about Steam game developer/publishers company email. But for this project all these data were removed and it were not used for the entire project. After careful inspection, there are no personal identifiable information(PPI) in the project data. This project conatins plots that all given information are subject to per user's own interpretation. Hereby this project is only for educational & practical purpose only. All the data including all analysis and visualisations, will not be using for any commercial purpose under any circumstances. 

## Data Source: 

1: Kaggle.com, Martin Bustos, Steam Games Dataset
url: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
Licence: MIT (url: https://www.mit.edu/~amini/LICENSE.md)
Hereby according to the author said: All data has been collected thanks to the Web API provided by Steam (Steam Spy). Only games (no DLCs, episodes, music, videos, etc) currently released have been added.

2: Kaggle.com, Nik Davis, Steam Store Games (Clean dataset)
url: https://www.kaggle.com/datasets/nikdavis/steam-store-games
Licence: Attribution 4.0 International (CC BY 4.0) (url: https://creativecommons.org/licenses/by/4.0/)
Hereby according to the author said: data gathered via using Steam Store and SteamSpy API.



# References:

Martin Bustos Roman. (2022). Steam Games Dataset [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DS/2109585

Nik Davis. (2019). Steam Store Games (Clean dataset) [Data set]. Kaggle. https://www.kaggle.com/nikdavis/steam-store-games



