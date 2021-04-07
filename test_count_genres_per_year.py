"""
Unit tests for count_genres_per_year
"""

import pytest
from collect_genre_data import (find_genre, find_top_songs, create_csv)
from count_genres_per_year import (count_genres_per_year,
    count_genres_per_year_normalized, accumulative_genre)
from visualizations import (area_chart_decades, create_dataframe,
    create_bar_chart_race, total_genre, create_pichart, generate_pies)

# Unit test for data collection
find_top_songs = [
    # Test that there is no year that is missing
]


# Unit test for data cleaning and structuring
count_genres_per_year_cases = [
    # Test that genres are separated correctly if the input is a string rather than a list.
    ('data_test/count_genres_per_year_1.csv', 1960, 1960,
        {1960: {'Funk / Soul': 1, 'Rock': 1}}),
    # Test that songs with no genres are filtered out.
    ('data_test/count_genres_per_year_2.csv', 1962, 1962, {1962: {}}),
    # Test that all genres of songs in a year is counted.
    ('data_test/count_genres_per_year_3.csv', 1958, 1958,
        {1958: {'Rock': 4,'Pop': 4}}),
    # Test that songs in different years do not get mixed together
    ('data_test/count_genres_per_year_4.csv', 1959, 1960,
        {1959: {'Funk / Soul': 4, 'Pop':4}, 1960: {'Funk / Soul': 4, 'Pop':4}})
]

count_genres_per_year_normalized_cases = [
    # Test that normalized values in a year are correct.
    ('data_test/count_genres_per_year_normalized_1.csv', 1960, 1960, {1960:
        {'Folk World & Country': 14.285714285714286, 'Pop': 42.857142857142854,
        'Rock': 28.571428571428573, 'Stage & Screen': 14.285714285714286}}),
    # Test that normalized values in mulitple years are correct.
    ('data_test/count_genres_per_year_normalized_2.csv', 1960, 1961, {1960:
        {'Pop': 50.0,'Rock': 50.0},1961: {'Blues': 25.0,
        'Folk World & Country': 25.0,'Jazz': 25.0,'Pop': 25.0},})
]

accumulative_genre_cases = [
    # Test that it behaves correctly when given an empty dictionary.
    ('data_test/accumulative_genre_1.csv', 1960, 1961, {1960: {}, 1961: {}}),
    # Test that genres are added to next year even if the next year does not
    # have that genre. For example a popular song in 1960 is Pop but is not
    # one in 1961.
    ('data_test/accumulative_genre_2.csv', 1960, 1961, {1960: {'Pop': 100.0},
        1961: {'Pop': 100.0}}),
    # Test that it behaves correctly when a year is skipped.
    ('data_test/accumulative_genre_3.csv', 2000, 2002, {2000: {'Pop': 100.0},
        2001: {'Pop': 100.0}, 2002: {'Pop': 200.0}}, )
]

# Define standard testing functions to check functions' outputs given certain
# inputs defined above.

@pytest.mark.parametrize("path, year_start, year_end, processed_data",
    count_genres_per_year_cases)
def test_count_genres_per_year(path, year_start, year_end, processed_data):
    """
    Test that the raw data is formatted and cleaned properly.

    Args:
        path: A string representing the path the .csv file.
        year_start: An integer representing the start year.
        year_end: An integer representing the end year.
        processed_data: A dictionary in which the keys are the years and the
        values is a dictionary in which the keys are the genre and the value
        is a number.
    """
    assert count_genres_per_year(path, year_start, year_end) == processed_data

@pytest.mark.parametrize("path, year_start, year_end, processed_data",
    count_genres_per_year_normalized_cases)
def test_count_genres_per_year_normalized(path, year_start, year_end,
    processed_data):
    """
    Test that the genre values are normalized correctly.

    Args:
        path: A string representing the path the .csv file.
        year_start: An integer representing the start year.
        year_end: An integer representing the end year.
        processed_data: A dictionary in which the keys are the years and the
        values is a dictionary in which the keys are the genre and the value
        is a number.
    """
    assert count_genres_per_year_normalized(path, year_start, year_end) == \
        processed_data

@pytest.mark.parametrize("path, year_start, year_end, processed_data",
    count_genres_per_year_normalized_cases)
def test_count_genres_per_year_normalized_add(path, year_start, year_end,
    processed_data):
    """
    Test that the genre values in a given year add up to 100.

    Args:
        path: A string representing the path the .csv file.
        year_start: An integer representing the start year.
        year_end: An integer representing the end year.
        processed_data: A dictionary in which the keys are the years and the
        values is a dictionary in which the keys are the genre and the value
        is a number.
    """
    normalized_genre_values = count_genres_per_year_normalized(path,
        year_start, year_end)
    total = 0
    for value in normalized_genre_values.values():
        total += sum(value.values())
    assert  total == 100 * (year_end - year_start + 1)

@pytest.mark.parametrize("path, year_start, year_end, processed_data",
    accumulative_genre_cases)
def test_accumulative_genre(path, year_start, year_end, processed_data):
    """
    Test genres in the previous year are added to the next year in the
    dictionary.

    Args:
        path: A string representing the path the .csv file.
        year_start: An integer representing the start year.
        year_end: An integer representing the end year.
        processed_data: A dictionary in which the keys are the years and the
        values is a dictionary in which the keys are the genre and the value
        is a number.
    """
    assert accumulative_genre(path, year_start, year_end) == processed_data
    