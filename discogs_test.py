# Test file for Discogs API

import discogs_client

# Start a client to Discogs servers
ds = discogs_client.Client('DiscogsClient/1.0', user_token='sWUMMBbXLhNtVbXxeXyimGXfkRAgYcZXUXtwvpkB')
""" ds = discogs_client.Client('DiscogsClient/1.0 +https://www.olin.edu/', consumer_key='QqUitVracYCVMioDAoEl', consumer_secret='PpENGJAkGURkAUkwRdpqisppTIkpVQLD')
ds.get_authorize_url()
d.get_access_token('verifier-here') """
# Search for song
result = ds.search(title='Let it go')

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






