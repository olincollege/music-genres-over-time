# music-genres-over-time
In this project we analyzed how music genres have changed in the United States over the years. Specifically, we looked at the billboard hot 100 charts to look at the top songs from 1946 to 2020, and found the genres of each of these songs through the discogs database. We then created three visualizations, a pie chart, an area chart, and a bar chart race to summarize and analyze how genres have changed.

## Required Libraries/Packages
To obtain data, first install the wikipedia package and discogs client. The [wikipedia package](https://pypi.org/project/wikipedia/) is used to get articles from Wikipedia. To install it, use the following command: `$ pip install wikipedia`. The [discogs client](https://github.com/discogs/discogs_client) is used to access Discog's API Python. We used it to query the Discogs database for information on the genre of songs. To install it, use the following command: `$ pip install discogs_client`.

To process data, install [pandas](https://pandas.pydata.org/docs/getting_started/install.html), which allows the user to make dataframes that are nice to work with. To install pandas use the command `$pip install pandas`.

To visualize the plots, matplotlib is needed. Installation instruction as well as more information on the pacakge can be found [here](https://matplotlib.org/stable/users/installing.html). To install it using pip use the following commands `$python -m pip install -U pip`, `$python -m pip install -U matplotlib`. Next for the bar chart race, you.

Information on the bar chart race can be found [here](https://www.dexplo.org/bar_chart_race/). To install it use the command `$pip install bar_chart_race`.
 To see the bar chart race, [ffmpeg](https://www.dexplo.org/bar_chart_race/installation/#installing-ffmpeg) is needed. To download it, go to the [ffmpeg](https://www.ffmpeg.org/download.html) site. After downloading it
 
 ## Instructions for Obtaining and Visualizing data
 
 * In order to use the Discogs API, you need to first obtain a token. Register for an account on https://www.discogs.com/my. Then go to the following link and click "Generate new token": https://www.discogs.com/settings/developers. Copy this token. In your local repository, create a new folder named "keys" and create a new python file named "api_keys.py." Set the variable name "token" to the token you copied earlier.
 * To obtain the data run collect_genre_data.py. This will create a csv called "genre_year_data.csv" that holds all of the top genres per year. Note that due to rate limits in how many requests can be made in a minute, this may take more than 8 hours
 * To see the visualizations, simply run music-genres-over-time.ipynb
 * If you would like to save all of the visualizations, uncomment all of the lines in visualizations.py that say "uncomment this line to save the [type of plot]," and run visualizations.py
 
## Unit Tests

In order to run the unit tests first comment the line that says "comment this line for unit tests," which is in the file 'collect_genre_data.py.' Then run `$pytest test_cases.py'.

