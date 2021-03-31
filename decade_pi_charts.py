import count_genres_per_year
import matplotlib.pyplot as plt

def total_genre(year_start, year_end):
    """
    Returns a dictionary of the total count of each genre from year start to year end.

    Returns a dictionary that has genres as keys, and the total number of songs from
    year start to year end in each genre as the values.
    
    ARGS:
        year_start: an int representing the first year that we start counting songs.
        year_end: an int representing the last year we count the songs.
    RETURNS:
        total_genre: A dictionary with the keys being strings representing each genre, 
        and the values being ints representing the total number of songs in each genre
        from year start to year end.
    """
    counted_genres = count_genres_per_year.count_genres_per_year(1946, 2020)
    total_genre_dic = {}
    # copying the dictionary key instead of setting it equal as to not change the original
    # dictionary python does not implicitly copy objects, meaning that if I set them equal,
    # both dictionaries would point to the same object
    total_genre_dic = counted_genres[year_start].copy()
    for year in range(year_start+1, year_end+1):
        # add all genres from past year and current year
        for genre in counted_genres[year]:
            total_genre_dic[genre]= total_genre_dic.get(genre,0) + counted_genres[year][genre]
     
    #get rid of genres that make up less than 5% of the genres
    total_songs = sum(total_genre_dic.values(), 0.0)
    for genre, number in total_genre_dic.copy().items():
        if number/total_songs <0.05:
            total_genre_dic.pop(genre, None)
    return total_genre_dic


def create_pichart(year_start,year_end):
    total_genre_dic = total_genre(year_start,year_end)
    labels = []
    sizes = []

    for genre, number in total_genre_dic.items():
        labels.append(genre)
        sizes.append(number)

    # Plot
    plt.pie(sizes, autopct='%1.1f%%')
    plt.title(f'Top Genres from {year_start} to {year_end}')
    plt.legend(labels,
          title="Genres",
          loc="center left",
          bbox_to_anchor=(0.8, 0, 1, 1.3))
    plt.axis('equal')
    plt.savefig(f'pi_chart{year_start}-{year_end}.png',bbox_inches='tight')
    plt.clf()

def generate_pies():

    create_pichart(1946,1949)
    create_pichart(1950,1969)
    create_pichart(1970,1989)
    create_pichart(1990,2009)
    create_pichart(2010, 2020)

generate_pies()