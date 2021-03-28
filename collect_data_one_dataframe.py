# Test file for Discogs API

import discogs_client
import pandas as pd
import wikipedia
import csv
import time
import os

def find_genre(songs,year_song):
    """
    Finds the genre(s) of a song by using the Discogs API.

    ARGS:
        songs: A dictionary containing the artist and title.
        year_song: A string representing the year of a song. Currently not in
        use because some songs only came to popularity afterwards.
    RETURNS:
        genres: A list of strings representing the genres of a song.
    """
    # Start a client to Discogs servers
    ds = discogs_client.Client('DiscogsClient/1.0', user_token='sWUMMBbXLhNtVbXxeXyimGXfkRAgYcZXUXtwvpkB')

    # Takes only the last name
    artist_last_name = list(songs["Artist(s)"].split(" "))[-1]

    # Strips apostrophes produced by wikipedia API.
    title_processed = songs["Title"].strip('"')

    # Search for song using the title, artist's last name, and year.
    result = ds.search(title=title_processed, artist=artist_last_name)
    
    # Search for first release object.
    # Note: Only finds the first usable object, may cause unexpected behavior!
    is_release = 0
    count = 0
    genres = None
    while is_release == 0:
        # Set up catch in case if Discogs Client does not find a result.
        try:
            # Finds url for each object.
            link = result[count].url
            # If url is a release object, find the genre.
            if link.find('release') != -1:
                genres = result[count].genres
                is_release = 1
            count += 1
        except:
            break

    # For testing purposes
    # print(songs['Title'].strip('"') + ' ' + songs["Artist(s)"])
    # print(genres)
    return genres

def find_top_songs():
    top_songs1950 = wikipedia.page("Billboard year-end top 30 singles of 1950")
    # Gets a list of all the names of the articles for hot singles for each year.
    top_per_year_wikis = top_songs1950.links[10:83]
    # Makes sure we're accoutning for 1950, because that's the page we got all the links from.
    top_per_year_wikis.append("Billboard year-end top 30 singles of 1950")

    list_all_years = []
    request_global = 0
    for year_wiki in top_per_year_wikis:
    # for year_wiki in ['Billboard Year-End Hot 100 singles of 1960']:
        # Setting auto suggest to false avoids mistakes in title
        wikepedia_url = (wikipedia.page(year_wiki, auto_suggest = False)).url
        # Get the data from the site.
        tables_in_article = pd.read_html(wikepedia_url)
        # Set the year for the data.
        year = year_wiki[-4:]


        if year == "2012" or year == "2013":
            top_songs_data_frame = tables_in_article[1] 
        else:
            top_songs_data_frame = tables_in_article[0] 
        
        # Gets rid of No. or '№' column.
        if (top_songs_data_frame.columns)[0] == "No.":
            top_songs_data_frame = top_songs_data_frame.drop(["No."], axis=1)
        elif (top_songs_data_frame.columns)[0] == "№":
            top_songs_data_frame = top_songs_data_frame.drop(['№'], axis=1)
        # Note: Note sure what causes "№" name!

        top_songs_data_frame["Year"] = year

        # Convert dataframe into a dictionary
        top_songs_list = top_songs_data_frame.to_dict("records")
        
        # Start Getting Genres for a certain year.

        print('Flushing Request Window...',end='\r',flush=True)
        time.sleep(75)
        request_local = 0
        for songs in top_songs_list:
            songs["Genre"] = find_genre(songs, year)
            songs.pop("Title", None)
            songs.pop("Artist(s)", None)
            
            request_local += 1
            print(f"{request_local+request_global} requests has been made!{' ' * 20}",end='\r',flush=True)
            time.sleep(1)
            if request_local == 30: # Not Sure why it is capped at 30?
                              # Can't get authenticated request
                              # Will use 30 for now
                seconds = 75
                while seconds > 0:
                    print(f'Discogs Request Limit Reached! Please Wait {seconds}! ',end='\r',flush=True)
                    seconds -= 1
                    time.sleep(1)
                request_global += request_local
                request_local = 0
        print(f"{year} is done!{' ' * 15}")
        list_all_years+= top_songs_list
    return list_all_years

# Original Code
""" def create_csv():
    list_all_years = find_top_songs()
    f = open("genre_year_data.csv", "w")
    writer = csv.DictWriter(
        f, fieldnames=["Genre", "Year"])
    writer.writeheader()
    writer.writerows(list_all_years)
    f.close() """

def create_csv():
    # May want to filter out Nones before entering file?
    # May be better to process after?
    # Adding all the data to file at once might be a bad idea?
    list_all_years = find_top_songs()
    with open('genre_year_data.csv', 'w') as f:
        writer = csv.DictWriter(
            f, fieldnames=["Genre", "Year"])
        writer.writeheader()
        writer.writerows(list_all_years)
    f.close()
    
create_csv()