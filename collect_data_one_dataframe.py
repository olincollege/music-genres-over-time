# Test file for Discogs API

import discogs_client
import pandas as pd
import wikipedia
import csv

def find_genre(songs,year_song):

    # Start a client to Discogs servers
    ds = discogs_client.Client('DiscogsClient/1.0', user_token='sWUMMBbXLhNtVbXxeXyimGXfkRAgYcZXUXtwvpkB')

    # Search for song
    songs["Artist(s)"] = list(songs["Artist(s)"].split(" "))[-1]
    result = ds.search(title= songs["Title"].strip(), artist=songs["Artist(s)"], year=year_song)
    # Search for first release object
    # Only finds the first usable object, may cause unexpected behavior!
    is_release = 0
    count = 0
    genres = None
    while is_release == 0:
        # Finds url for each object
        try:
            link = result[count].url
            # If url is a release object, find the genre
            if link.find('release') != -1:
                genres = result[count].genres
                is_release = 1
            count += 1
        except:
            break
    return genres

def find_top_songs():
    
    top_songs1950 = wikipedia.page("Billboard year-end top 30 singles of 1950")
    #gets a list of all the names of the articles for hot singles for each year
    top_per_year_wikis = top_songs1950.links[10:83]
    #makes sure we're accoutning for 1950, because that's the page we got all the links from
    top_per_year_wikis.append("Billboard year-end top 30 singles of 1950")


    list_all_years = []
    for year_wiki in top_per_year_wikis:
        #setting auto suggest to false avoids mistakes in title
        wikepedia_url = (wikipedia.page(year_wiki, auto_suggest = False)).url
        tables_in_article = pd.read_html(wikepedia_url)
        year = year_wiki[-4:]
        if year == "2012" or year == "2013":
            top_songs_data_frame = tables_in_article[1] 
        else:
            top_songs_data_frame = tables_in_article[0] 
        #gets rid of No. or '№' column
        if (top_songs_data_frame.columns)[0] == "No.":
            top_songs_data_frame = top_songs_data_frame.drop(["No."], axis=1)
        elif (top_songs_data_frame.columns)[0] == "№":
            top_songs_data_frame = top_songs_data_frame.drop(['№'], axis=1)

        top_songs_data_frame["Year"] = year
        #top_songs_data_frame["year"] = year
        top_songs_list = top_songs_data_frame.to_dict("records")
        for songs in top_songs_list:
            songs["Genre"] = find_genre(songs, year)
            songs.pop("Title", None)
            songs.pop("Artist(s)",None)
        list_all_years+= top_songs_list
        print(year)
    return list_all_years

def create_csv():
    list_all_years = find_top_songs()
    f = open("genre_year_data.csv", "w")
    writer = csv.DictWriter(
        f, fieldnames=["Genre", "Year"])
    writer.writeheader()
    writer.writerows(list_all_years)
    f.close()
    
create_csv()