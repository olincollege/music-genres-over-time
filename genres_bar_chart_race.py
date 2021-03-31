"""
Creates bar chart race of the genres for the
top songs from 1946 to 2020.
"""

import pandas as pd
import bar_chart_race as bcr
import count_genres_per_year

def create_dataframe():
    """
    Creates a dataframe with the year as the index and genres as headers.

    RETURNS:
        genre_year_dataframe: A dataframe with the index being ints that
        represent the years 1946 to 2020 and the headers being strings
        that represent the most popular genres. In each column are ints
        that represent the cumulative number of songs for each genre/year.

    """
    accumulated_genres = count_genres_per_year.accumulative_genre(1946, 2020)
    genre_year_dataframe = pd.DataFrame(accumulated_genres)
    #switch rows and columns so that the columns are genres and the
    #rows are the years
    genre_year_dataframe = genre_year_dataframe.T
    genre_year_dataframe.index.name = 'Year'
    #fill any NaN with 0 instead
    genre_year_dataframe.fillna(0, inplace = True)
    return genre_year_dataframe


def create_bar_chart_race():
    """
    Creates a bar chart race of the genres for the top songs over the years.

    Creates a bar chart race that animates bars that represent the cumulative
    number of top songs per genre over the years 1946 to 2020.
    """

    genre_year_dataframe = create_dataframe()
    bcr.bar_chart_race(
        df=genre_year_dataframe,
        filename='popular_genres_over_time.mp4',
        orientation='h',
        sort='desc',
        n_bars=10,
        fixed_order=False,
        fixed_max=False,
        steps_per_period=10,
        interpolate_period=False,
        label_bars=True,
        bar_size=.95,
        period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
        period_fmt= 'Year{x:10.0f}',
        period_length=500,
        figsize=(5, 3),
        dpi=144,
        cmap='dark12',
        title='Genres of the Top Songs from 1946 to 2020',
        title_size='',
        bar_label_size=7,
        tick_label_size=7,
        shared_fontdict={'family' : 'DejaVu Sans', 'color' : '.1'},
        scale='linear',
        writer=None,
        fig=None,
        bar_kwargs={'alpha': .7},
        filter_column_colors=True)

create_bar_chart_race()
