# Project: Data Modeling with Postgres
## Project Summary
Postgres database for Song data that is designed to optimize queries for song play analysis created using the JSON logs from user activity and JSON metadata of the songs.

## Purpose
Sparkify(startup) company wants to have a optimzed database that they can use easily to do song play analysis. They have been collected the required data using their new music streaming app.
Currently the data collected are in form of JSON logs file collected from user activity on the app and Json metadata that is used for the songs stored in the app. The current form of data does not facilitates Sparkify team to perform anlaysis directly and understand what song users are listening.

To simplify the process for Sparkify team, we performed Data modeling using Postgres and created a Relational Database.

## Schema Design
This project follows star schema to optimize the queires for the required analysis. As part of star schema, see below for the Facts and Dimensions.
#### Fact Table
- songplays-
    - Details: Records in log data associated with song plays i.e. records with page NextSong
    - Fields : songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
#### Dimension Tables
- users
    - Details: Users in the app
    - Fields : user_id, first_name, last_name, gender, level
- songs
    - Details: Songs in music database
    - Fields : song_id, title, artist_id, year, duration
- artists 
    - Details: Artists in music database
    - Fields : artist_id, name, location, latitude, longitude
- time 
    - Details: Timestamps of records in songplays broken down into specific units
    - Fields : start_time, hour, day, week, month, year, weekday

## ETL Pipeline
The ETL flow has been created using Python script.
- Extract  : Raw data has been extracted from the Data folder which contains Json files (user activity and Songs meta data)
- Transform: Transformation has been done for the required fields such as timestamp and and break down to multiple fields, Also for easier availability of data multiple dataset are joined and fetched and then loaded into the fact table
- Load     : The finalized data gets loaded into the postgres database in above mentoned tables for easier availability.

## Repository Details
Below are the files that are present in the repository:
- *data*            : Contain below datasets.
    - *Song Dataset*: The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID.
    - *Log Dataset*  : The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.
- *test.ipynb*      : Displays the first few rows of each table to let you check your database.
- *create_tables.py*: Drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts.
- *etl.ipynb*       : Reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.
- *etl.py*          : Reads and processes files from song_data and log_data and loads them into your tables. You can fill this out based on your work in the ETL notebook.
- *sql_queries.py*  : Contains all your sql queries, and is imported into the last three files above.

### How to run the code
- To set up Database      : Run **create_tables.py** for creating tables and database from fresh or dropping all the table and database.\
Note: **create_tables.py** needs to be excecute once before doing any analysis.
- To load data in Database: run **etl.py** to trigger the etl process and load the data in the database.


