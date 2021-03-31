"""
Create two dictionaries that count the genres per year.
count_genres_per_year counts the number of songs per genre in
each year. accumulative_genre adds the number of songs per genre
in each year to the amount of songs per genre for the years before
it.
"""

import csv
import ast


def count_genres_per_year():
    """
    Returns a dictionary of the number of songs per genre in each year.

    Returns a dictionary that has the year as the key and a dictionary
    as the value. The inner dictionaries have genres as keys, and the
    number of songs in each genre as the values.

    RETURNS:
        counted_genres: A dictionary with the value being an int representing
        the year, and the key being another dictionary. This dictionary's key
        has strings representing the genre, and ints representing the number
        of songs in each genre for respective year.
    """
    counted_genres = {}
    total_genres_each_year = {}
    for year in range(1946, 2021):
        counted_genres[year] = {}

    with open('genre_year_data.csv', 'r') as data:
        # goes through each song
        for song in csv.DictReader(data):
            # if there is no genre listed, skip to the next song
            if song['Genre'] == '':
                continue
            year = int(song['Year'])
            # getting rid of commas avoids creating two different list items for the one genre
            song['Genre'] = song['Genre'].replace(
                'Folk, World, & Country', 'Folk World & Country')
            # makes string list into list. i.e. turns '['a','b']' to ['a','b']
            song['Genre'] = ast.literal_eval(song['Genre'])
            # adds one for each genre when it appears
            for genre in song['Genre']:
                counted_genres[year][genre] = counted_genres[year].get(
                    genre, 0) + 1
                
            #get rid of genres that represent less than 5% of the year's songs
            total_songs = sum(counted_genres[year].values(), 0.0)
            for genre, number in counted_genres[year].copy().items():
                if number/total_songs <0.05:
                    counted_genres[year].pop(genre, None)
            
            #normalize each year so the total coutn for each genre adds up to 100
            counted_genres[year]= {genre: number *100/ total_songs for genre, number in counted_genres[year].items()}
    return counted_genres


def accumulative_genre():
    """
    Returns a dictionary of the cumulative number of songs per genre in each year.

    Returns a dictionary that has the year as the key and a dictionary
    as the value. The inner dictionaries have genres as keys, and the
    cumulative number of songs in each genre as the values.

    RETURNS:
        accumulated_genres: A dictionary with the value being an int representing
        the year, and the key being another dictionary. This dictionary's key
        has strings representing the genre, and ints representing the cumulative
        number of songs in each genre for respective year. i.e. if 1946 has 10 pop
        songs, and 1947 has 15 pop songs, the cumulative number for 1947 is 25 pop
        songs.
    """
    counted_genres = count_genres_per_year()
    accumulated_genres = {}
    # copying the dictionary key instead of setting it equal as to not change the original
    # dictionary python does not implicitly copy objects, meaning that if I set them equal,
    # both dictionaries would point to the same object
    accumulated_genres[1946] = counted_genres[1946].copy()
    for year in range(1947, 2021):
        accumulated_genres[year] = accumulated_genres[year - 1].copy()
        # add all genres from past year and current year
        for genre in counted_genres[year]:
            genre_count = accumulated_genres[year - 1].get(genre, 0)
            accumulated_genres[year][genre] = genre_count + \
                counted_genres[year][genre]
    return accumulated_genres

