# music-genres-over-time
In this project we analyzed how music genres have changed in the United States over the years. Specifically, we looked at the Billboard Hot 100 charts to look at the top songs from 1946 to 2020, and found the genres of each of these songs through the discogs database. We then created three visualizations- a pie chart, an area chart, and a bar chart race- to summarize and analyze how genres have change

## Required Libraries/Packages
To obtain data, first install the wikipedia package and discogs client. The [wikipedia package](https://pypi.org/project/wikipedia/) is used to get articles from Wikipedia. To install it, use the following command: `$ pip install wikipedia`. The [discogs client](https://github.com/discogs/discogs_client) is used to access Discog's API. We used it to query the Discogs database for information on the genre of songs. To install it, use the following command: `$ pip install discogs_client`.

To process data, install [pandas](https://pandas.pydata.org/docs/getting_started/install.html), which allows the user to make dataframes that are nice to work with. To install pandas use the command `$pip install pandas`.

To visualize the plots, matplotlib is needed. Installation instruction as well as more information on the pacakge can be found [here](https://matplotlib.org/stable/users/installing.html). To install it using pip use the following commands `$python -m pip install -U pip`, `$python -m pip install -U matplotlib`.

Information on the bar chart race can be found [here](https://www.dexplo.org/bar_chart_race/). To install it use the command `$pip install bar_chart_race`.
 To save the file to disk, [ffmpeg](https://www.dexplo.org/bar_chart_race/installation/#installing-ffmpeg) is needed. To download ffmpeg, go to the [ffmpeg](https://www.ffmpeg.org/download.html) site and click one of the green download buttons.
 
 ## Instructions for Obtaining and Visualizing data
 
 * To obtain the genre data, run collect_genre_data.py. This will create a csv called "genre_year_data.csv" that holds all of the top genres per year. Note that due to rate limits in how many requests can be made in a minute, this may take more than 8 hours
 * To see the plots and the computational essay simply go to music-genres-over-time.ipynb and run the notebook
 * If you would like to save all of the plots, uncomment all of the lines in visualizations.py that are below the comment that says "uncomment this line to save the [type of plot]," comment the line that says "comment this line if saving the bar plot race," and run visualizations.py. This will save all of the plots to a folder in your repository called "visualizations"