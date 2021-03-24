# Test file for Discogs API

import discogs_client


ds = discogs_client.Client('DiscogsClient/1.0', user_token='sWUMMBbXLhNtVbXxeXyimGXfkRAgYcZXUXtwvpkB')

result = ds.search('Let it go',artist='Menzel',year='2013')

print(result.page(1))