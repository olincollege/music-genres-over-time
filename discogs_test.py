# Test file for Discogs API

import discogs_client

# Start a client to Discogs servers
ds = discogs_client.Client('DiscogsClient/1.0', user_token='sWUMMBbXLhNtVbXxeXyimGXfkRAgYcZXUXtwvpkB')

# Search for song
result = ds.search(title='Prisoner of Love')#, artist='Como', year='1946')

# Search for first release object
# Only finds the first usable object, may cause unexpected behavior!
is_release = 0
count = 0
while is_release == 0:
    # Finds url for each object
    link = result[count].url
    # If url is a release object, find the genre
    if link.find('release') != -1:
        genres = result[count].genres
        is_release = 1
    count += 1

print(genres)






