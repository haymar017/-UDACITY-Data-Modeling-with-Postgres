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
songplays-
    Details: Records in log data associated with song plays i.e. records with page NextSong
    Fields : songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

#### Dimension Tables
- users
    Details: Users in the app
    Fields : user_id, first_name, last_name, gender, level

- songs
    Details: Songs in music database
    Fields : song_id, title, artist_id, year, duration

- artists 
    Details: Artists in music database
    Fields : artist_id, name, location, latitude, longitude

- time 
    Details: Timestamps of records in songplays broken down into specific units
    Fields : start_time, hour, day, week, month, year, weekday
