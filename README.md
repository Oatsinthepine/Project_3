# Project 3 Group 3

## Data Visualisation Track (custom): Steam games data visualistion

## Introduction:

This group project is about performing data analysis and visualisations about the Steam games data. The source data was
obtained from the Kaggle website, for details of the data please see the references below. 
The purpose of this project is to present users about some insignts in Steam games data accross multiple years. 
As we are interested in exploring and gaining more information on the world most popular digital distribution platfrom developed by Valve Coorpation. Steam enables users to download, purchase, discuss, publish, recreate, and many more. Therefore, through this project, we would like to show the users about our findings and representing in visual ways via static and dynamic plots.

Here are the main questions we are going to explore in this project:

- Q1: What are the most popular 10 games from 2014 to 2024?
- Q2: Is there any relationship between users' review and games price?
- Q3: Which publishers have the highest positive ratings?
- Q4: Do games with certain genre or descriptors tend to be more popular?

## The approach for this project:

1: Download the source data from the kaggle website. Use Pandas to read csv and perform data cleanning. (please noticed
in this step two csv files are being merged together for this group project)
for seeing all the data cleaning and df merging details, please refer to 'Steam_dataset_cleaning.ipynb'

2: save the output file locally in csv and json format. Imported all the cleaned data to MongoDB database.
Please use the 'output_file.json' for this.
run the mongo import command: mongoimport -- type json --db 'Your_db_name' -c 'Your_collection_name' --drop --jsonArray output_file.json

3: Peform analysis & visualsations using pymongo to query data and plots using Matplotlib and Seaborn.

4: Create html page and visualise more graph using D3.js and Plotly.js, and interactive webpage for user to interact.
Please refer to the js folder to see the app.js and index.html for details.

5: Using Flask to serve the app.route and enable users to see differnet graphs.
Please refer to app.py file for details.

## Reasons for certain techniques & opeations we done for this project:

- For data frame merging, as upon inspection from source data, there are some data missing in both side of source data, so merged data better suits the project.
- For using NoSQL db of MongoDB. As the cleaned data contains some nested columns which are hard to seperate and store in relational db, so NoSQL is more suitable for storing the data for this project.

## Instruction of viewing & interact with this project:

Please git clone the whole project_3 repository to your local site. Then either you enabling a local server or using live server extension which provided in your chosen IDE. 

For viewing the interactive JS plot. Please click 'index.html' file, after you done the step mentioned above. You can going to the web page and by seleting the year in the dropdown bar to view the specific chart based on the year. Be noticed that the source javascript file is located as: '/js/app.js'

- For viewing other charts or seeing the details of analysis. After you clone the whole repo. You noticed that there are 3 sub-folders 'HLim_part','JChia_part', and 'RSingh_part'. So these folders contains the essential files about the Flask app, analysis and plotting perfromed by using jupyter notebook. 

- For viewing individual's work. Please move all the contents from the selecting folder out from its folder, then put them into the 'Project_3'. Then you can execute all the files respectively to see the details. Also, for viewing individual's work, please also follow per code annotations as instructed to ensure successful viewing.

The Reason for the 3 sub-folders is that as Project_3 is a group work and this 'main' branch combined all the team members' work together. buddling into sub-folders is just to tidy it up. As the individual's work were built on top of using the 'cleaned_steam_data.csv'. Therefore, please ensure they are in the same folder for all their code executing successfully.


## Project_3 group task allocation:

Team Leader:

- Ziyue Zhou (Jacky), Tasks: project repo set-up, responsible for question 1, initial data cleaning & merging. creating JS plotting of index.html and app.js.

Contributors: (All of the contributors works are in the corresponding sub-folders)

- Hung Lim (Hansen), Tasks: responsible for question 2, perform analysis and plotting on price / ratings. Flask dynamic app route creation.

- Rakhi Singh, Tasks: responsible for question 3, perform analysis on publishers and ratings. Flask dynamic app route creation. Presentation sildes set-up.

- Jordan Chia, Tasks: responsible for question 4, perform analysis on game genres and popularities. Flask dynamic app route creation.

## Ethical considerations for this project:

The original source data contains some information about Steam game developer/publishers company email. But for this project all these data were removed and it were not used for the entire project. After careful inspection, there are no personal identifiable information(PPI) in the project data. This project conatins plots that all given information are subject to per user's own interpretation. Hereby this project is only for educational & practical purpose only, which is for fullfilling the course requirement of Monash/edx Data visualisation bootcamp. All the data including all analysis and visualisations, will not be using for any commercial purpose under any circumstances. 

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

Wentao Li (Clarmy). mplfonts. https://github.com/Clarmy/mplfonts

Seaborn Document. User guide and Tutorial. https://seaborn.pydata.org/tutorial/introduction.html

Coders Page. Python Flask MongoDB complete CRUD in one video. https://www.youtube.com/watch?v=o8jK5enu4L4&t=796s

Bek Brace. Build a Flask fullstack App with MongoDB. https://www.youtube.com/watch?v=FVVOaCOAMFU

teclado. How to add graphs EASILY to your Flask apps. https://www.youtube.com/watch?v=E2hytuQvLlE





