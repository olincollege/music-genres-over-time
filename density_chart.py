"""
Produces a density chart.
"""
import pandas as pd
from count_genres_per_year import *
import matplotlib as plt

def density_chart():
    genres_per_year = count_genres_per_year(1946,2020)
    genres = ['Pop', 'Rock', 'Hip Hop', 'Funk / Soul', 'Electronic', 'Folk World & Country', 'Jazz', 'Stage & Screen', 'Blues', 'Latin']

    genre_dict_list = {'Pop':[], 'Rock':[], 'Hip Hop':[], 'Funk / Soul':[], 'Electronic':[], 'Folk World & Country':[], 'Jazz':[], 'Stage & Screen':[], 'Blues':[], 'Latin':[]}
    for genre in genres:
        for year_key in genres_per_year:
            try:
                genre_dict_list[genre].append(genres_per_year[year_key][genre])
            except:
                genre_dict_list[genre].append(0)

    df = pd.DataFrame({
        'Pop': genre_dict_list['Pop'],
        'Rock': genre_dict_list['Rock'],
        'Hip Hop': genre_dict_list['Hip Hop'],
        'Funk/Soul': genre_dict_list['Funk / Soul'],
        'Electronic': genre_dict_list['Electronic'],
        'Folk World & Country': genre_dict_list['Folk World & Country'],
        'Jazz': genre_dict_list['Jazz'],
        'Stage & Screen': genre_dict_list['Stage & Screen'],
        'Blues': genre_dict_list['Blues'],
        'Latin': genre_dict_list['Latin'],
    }, index=pd.date_range(start='1946',end='2021', freq='Y'))

    ax = df.plot.area(stacked=False)
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

def density_chart_cumulative():
    genres_per_year = accumulative_genre(1946,2020)
    genres = ['Pop', 'Rock', 'Hip Hop', 'Funk / Soul', 'Electronic', 'Folk World & Country', 'Jazz', 'Stage & Screen', 'Blues', 'Latin']

    genre_dict_list = {'Pop':[], 'Rock':[], 'Hip Hop':[], 'Funk / Soul':[], 'Electronic':[], 'Folk World & Country':[], 'Jazz':[], 'Stage & Screen':[], 'Blues':[], 'Latin':[]}
    for genre in genres:
        for year_key in genres_per_year:
            try:
                genre_dict_list[genre].append(genres_per_year[year_key][genre])
            except:
                genre_dict_list[genre].append(0)

    df = pd.DataFrame({
        'Pop': genre_dict_list['Pop'],
        'Rock': genre_dict_list['Rock'],
        'Hip Hop': genre_dict_list['Hip Hop'],
        'Funk/Soul': genre_dict_list['Funk / Soul'],
        'Electronic': genre_dict_list['Electronic'],
        'Folk World & Country': genre_dict_list['Folk World & Country'],
        'Jazz': genre_dict_list['Jazz'],
        'Stage & Screen': genre_dict_list['Stage & Screen'],
        'Blues': genre_dict_list['Blues'],
        'Latin': genre_dict_list['Latin'],
    }, index=pd.date_range(start='1946',end='2021', freq='Y'))

    ax = df.plot.area(stacked=False)
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

def density_chart_decades():
    genres_per_year = count_genres_per_year()
    genres = ['Pop', 'Rock', 'Hip Hop', 'Funk / Soul', 'Electronic', 'Folk World & Country', 'Jazz', 'Stage & Screen', 'Blues', 'Latin']
    genre_dict_list = {'Pop':[], 'Rock':[], 'Hip Hop':[], 'Funk / Soul':[], 'Electronic':[], 'Folk World & Country':[], 'Jazz':[], 'Stage & Screen':[], 'Blues':[], 'Latin':[]}
    for genre in genres:
        for year_key in genres_per_year:
            try:
                genre_dict_list[genre].append(genres_per_year[year_key][genre])
            except:
                genre_dict_list[genre].append(0)
    