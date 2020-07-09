import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process all the json files present in the song folder.  
    After processing the json files use to enter data in song and artist table. 
    Parameters: 
    arg1 : cursor for the databse connected 
    arg2 : filepath of the songfile  
    Returns: 
    None
    """
    # open song file
    df = pd.read_json(filepath,lines = True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude','artist_longitude']].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process all the json log files present in the log folder.  
    After processing the json files and transformation use to enter data in songplay, user and time table  
    Parameters: 
    arg1 : cursor for the databse connected 
    arg2 : filepath of the songfile  
    Returns: 
    None
    """
    # open log file
    df = pd.read_json(filepath,lines = True) 

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit="ms")
    t = df['ts']
    
    # insert time data records
    time_data = [(x, x.hour, x.day, x.week, x.month, x.year, x.dayofweek) for x in t]
    #time_data = [(x, x.hour, x.day, x.week, x.month, x.year, x.dayofweek) for x in [pd.to_datetime(row, unit="ms") for row in t]]
    column_labels = ('timestamp', 'hour', 'day', 'weekofyear', 'month', 'year','weekday')
    time_df = pd.DataFrame(time_data,columns= column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId,row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Read all the files present in the provided folder.  
    
    Parameters: t
    arg1 : cursor for the databse connected 
    arg2 : connection created for the database  
    arg3 : filepath of the folder
    arg4 : function based on the required files 
    Returns: 
    None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()