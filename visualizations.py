"""
Contains code to produce visualizations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import bar_chart_race as bcr
import count_genres_per_year


def area_chart_decades():
    """
    Plots an area chart for the genres of top songs from 1950 to 2020
    by the decade.

    Args:
        None

    Returns:
        None
    """
    genres_per_year = count_genres_per_year.count_genres_per_year_normalized(
        'genre_year_data.csv', 1946, 2020)
    every_decade = {}
    for year in genres_per_year.copy():
        if year % 10 == 0:
            every_decade[year] = genres_per_year[year]

    genres = ['Pop', 'Rock', 'Hip Hop', 'Funk / Soul', 'Electronic',
              'Folk World & Country', 'Jazz', 'Stage & Screen']

    genre_dict_list = {'Pop': [], 'Rock': [], 'Hip Hop': [], 'Funk / Soul': [],
                       'Electronic': [], 'Folk World & Country': [],
                       'Jazz': [], 'Stage & Screen': []}

    for genre in genres:
        for year_key in every_decade:
            try:
                genre_dict_list[genre].append(every_decade[year_key][genre])
            except KeyError:
                genre_dict_list[genre].append(0)

    genre_dataframe = pd.DataFrame({
        'Pop': genre_dict_list['Pop'],
        'Rock': genre_dict_list['Rock'],
        'Hip Hop': genre_dict_list['Hip Hop'],
        'Funk/Soul': genre_dict_list['Funk / Soul'],
        'Electronic': genre_dict_list['Electronic'],
        'Folk World & Country': genre_dict_list['Folk World & Country'],
        'Jazz': genre_dict_list['Jazz'],
        'Stage & Screen': genre_dict_list['Stage & Screen'],
    }, index=pd.date_range(start='1950', end='2020', periods=8))

    axes = genre_dataframe.plot.area(stacked=False,
                                     title='Top Genres by the Decades from 1950' +
                                     ' to 2020', xlabel='Years', ylabel='Normalized' +
                                     'Number of Songs')
    axes.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    # uncomment this line to save the area chart plot
    # plt.savefig('visualizations/Area_Chart.png',bbox_inches='tight')


def create_dataframe():
    """
    Creates a dataframe with the year as the index and genres as headers.

    Args:
        None

    Returns:
        genre_year_dataframe: A dataframe with the index being ints that
        represent the years 1946 to 2020 and the headers being strings
        that represent the most popular genres. In each column are ints
        that represent the cumulative number of songs for each genre/year.

    """
    accumulated_genres = count_genres_per_year.accumulative_genre(
        'genre_year_data.csv', 1946, 2020)
    genre_year_dataframe = pd.DataFrame(accumulated_genres)
    # switch rows and columns so that the columns are genres and the
    # rows are the years
    genre_year_dataframe = genre_year_dataframe.T
    genre_year_dataframe.index.name = 'Year'
    # fill any NaN with 0 instead
    genre_year_dataframe.fillna(0, inplace=True)
    return genre_year_dataframe


def create_bar_chart_race():
    """
    Creates a bar chart race of the genres for the top songs over the years.

    Creates a bar chart race that animates bars that represent the cumulative
    number of top songs per genre over the years 1946 to 2020.

    Args:
        None

    Returns:
        race.data: An html object representing the bar chartt race animation.
    """

    genre_year_dataframe = create_dataframe()
    race = bcr.bar_chart_race(
        df=genre_year_dataframe,
        # uncomment this line to save the bar plot race
        #filename= 'visualizations/popular_genres_over_time.mp4',
        n_bars=10,
        period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
        period_fmt='Year{x:10.0f}',
        dpi=400,
        title='Genres of the Top Songs from 1946 to 2020',
        title_size='',
        shared_fontdict={'family': 'DejaVu Sans', 'color': '.1'},
        filter_column_colors=True)
    # comment this line if saving the bar plot race
    return race.data


def total_genre(year_start, year_end):
    """
    Returns a dictionary of the total count of each genre from year start to year end.

    Returns a dictionary that has genres as keys, and the total number of songs from
    year start to year end in each genre as the values.

    Args:
        year_start: An int representing the first year that we start counting songs.
        year_end: An int representing the last year we count the songs.

    Returns:
        total_genre: A dictionary with the keys being strings representing each genre,
        and the values being ints representing the total number of songs in each genre
        from year start to year end.
    """
    counted_genres = count_genres_per_year.count_genres_per_year_normalized(
        'genre_year_data.csv', 1946, 2020)
    total_genre_dic = {}
    # copying the dictionary key instead of setting it equal as to not change the original
    # dictionary python does not implicitly copy objects, meaning that if I set them equal,
    # both dictionaries would point to the same object
    total_genre_dic = counted_genres[year_start].copy()
    for year in range(year_start+1, year_end+1):
        # add all genres from past year and current year
        for genre in counted_genres[year]:
            total_genre_dic[genre] = total_genre_dic.get(
                genre, 0) + counted_genres[year][genre]

    # get rid of genres that make up less than 5% of the genres
    total_songs = sum(total_genre_dic.values(), 0.0)
    for genre, number in total_genre_dic.copy().items():
        if number/total_songs < 0.05:
            total_genre_dic.pop(genre, None)
    return total_genre_dic


def create_pichart(year_start, year_end):
    """
    Plots and saves pie charts for genres over a certain timeframe.

    Plots and saves pie charts based on a year start and a year end.
    Each slice of the pie chart represents a genre, and its size is
    determined by the prevelence of the genre in a certain time period
    compared to other genres.

    Args:
        year_start: an int representing the first year that we start counting songs.
        year_end: an int representing the last year we count the songs.

    Returns:
        None
    """
    total_genre_dic = total_genre(year_start, year_end)
    labels = []
    sizes = []

    for genre, number in total_genre_dic.items():
        labels.append(genre)
        sizes.append(number)

    # Plot
    plt.clf()
    plt.pie(sizes, autopct='%1.1f%%')
    plt.title(f'Top Genres from {year_start} to {year_end}')
    plt.legend(labels,
               title="Genres",
               loc="center left",
               bbox_to_anchor=(0.8, 0, 1, 1.3))
    plt.axis('equal')
    #uncomment this line to save the pie plots
    #plt.savefig(f'visualizations/{year_start}_to_{year_end}_genre_pie_chart.png', \
               #bbox_inches='tight')


def generate_pies():
    """
    Creates pie charts for 5 different time periods.

    Creates pie charts that break down the percantage of the genres in
    the top charts for the time periods throughout 1946 to 2020.

    Args:
        None

    Returns:
        None
    """

    create_pichart(1946, 1964)
    create_pichart(1965, 1980)
    create_pichart(1981, 1996)
    create_pichart(1997, 2015)
    create_pichart(2016, 2020)

# uncomment this line to save the plots.
# area_chart_decades()
# create_bar_chart_race()
# generate_pies()
