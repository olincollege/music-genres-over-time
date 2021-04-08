"""
Create a CSV of the genre and year of the top
songs from 1946 to 2020.
"""

import csv
import time
import discogs_client
from keys.api_keys import token
import pandas as pd
import wikipedia


def find_genre(songs):
    """
    Finds the genre(s) of a song by using the Discogs API.

    ARGS:
        songs: A dictionary containing the artist and title of each song.
    RETURNS:
        genres: A list of strings representing the genres of a song.
    """
    # Start a client to Discogs servers
    client = discogs_client.Client(
        'DiscogsClient/1.0', user_token=token)

    # Takes only the last name so unexpected words like "featuring" does not mess up discogs API
    artist_last_name = list(songs['Artist(s)'].split(' '))[-1]

    # Strips apostrophes produced by wikipedia API.
    title_processed = songs['Title'].strip('"')

    # Search for song using the title, and artist's last name.
    result = client.search(title=title_processed, artist=artist_last_name)

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
        except IndexError:
            break

    # For testing purposes
    # print(songs['Title'].strip('"') + ' ' + songs["Artist(s)"])
    # print(genres)
    return genres


def find_top_songs():
    """
    Returns list of dictionaries with genre/year of the top songs from 1946-2020.

    Scrapes the wikipedia articles for the top singles of each year from `1946 to
    2020 to find the artist and title of the top songs. Then finds the genre and
    puts it into a list of dictionaries with the format, {"Genre": "some genre",
    "Year": "Current Year"}.

    RETURNS:
        list_all_years: A list of dictionaries with strings representing the genre
            and year of each of the top songs from 1946 to 2020.
    """
    top_songs1950 = wikipedia.page('Billboard year-end top 30 singles of 1950')
    # Gets a list of all the names of the articles for hot singles for each year.
    top_per_year_wikis = top_songs1950.links[9:83]
    # Makes sure we're accoutning for 1950, because that's the page we got all the links from.
    top_per_year_wikis.append('Billboard year-end top 30 singles of 1950')

    list_all_years = []
    request_global = 0
    for year_wiki in top_per_year_wikis:
    # for year_wiki in ["Billboard Year-End Hot 100 singles of 1959"]:
        # Setting auto suggest to false avoids mistakes in title look up
        wikepedia_url = (wikipedia.page(year_wiki, auto_suggest=False)).url
        # Get all the tables in the site.
        tables_in_article = pd.read_html(wikepedia_url)
        # Set the year for the data.
        year = year_wiki[-4:]

        # 2012 and 2013 both had one extra table in the article that had to be avoided
        if year in ('2012', '2013'):
            top_songs_data_frame = tables_in_article[1]
        else:
            top_songs_data_frame = tables_in_article[0]

        # Gets rid of No. or '№' (articles have one or the other to represent the rank of songs).
        if (top_songs_data_frame.columns)[0] == 'No.':
            top_songs_data_frame = top_songs_data_frame.drop(['No.'], axis=1)
        elif (top_songs_data_frame.columns)[0] == '№':
            top_songs_data_frame = top_songs_data_frame.drop(['№'], axis=1)

        top_songs_data_frame['Year'] = year

        # Convert dataframe into a list of dictionaries
        top_songs_list = top_songs_data_frame.to_dict('records')

        # Start Getting Genres for a certain year.
        print('Flushing Request Window...', end='\r', flush=True)
        time.sleep(75)
        request_local = 0
        for songs in top_songs_list:
            songs['Genre'] = find_genre(songs)
            songs.pop('Title', None)
            songs.pop('Artist(s)', None)

            request_local += 1
            #allows user to keep track of how many requests has been made
            print(f'{request_local+request_global} requests has been made!{" " * 20}',
                  end='\r', flush=True)
            time.sleep(1)
            #creates delay because requests are capped at 30 requests per minute
            if request_local == 30:
                seconds = 75
                while seconds > 0:
                    print(f'Discogs Request Limit Reached! Please Wait {seconds}! ',
                          end='\r', flush=True)
                    seconds -= 1
                    time.sleep(1)
                request_global += request_local
                request_local = 0
        print(f'{year} is done!{" " * 35}')
        list_all_years += top_songs_list
    return list_all_years


def create_csv():
    """
    Creates a CSV from the list of dictionaries of all top songs.

    Writes the list of dictionaries of all top songs to a CSV file.
    The CSV file has two headers of Genre and Year, and each row has
    the genre and year of each top song.
    """

    list_all_years = find_top_songs()
    with open('genre_year_data1959.csv', 'w') as file:
        writer = csv.DictWriter(
            file, fieldnames=['Genre', 'Year'])
        writer.writeheader()
        writer.writerows(list_all_years)
    file.close()
    