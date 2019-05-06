from itertools import repeat
from nba_api.stats.endpoints.leaguedashplayershotlocations import LeagueDashPlayerShotLocations
import pandas as pd

# Basic Request
shot_locations = LeagueDashPlayerShotLocations(distance_range='5ft Range')
data = shot_locations.data_sets[0].data['data']
distances = shot_locations.data_sets[0].data['headers'][0]['columnNames']
headers = shot_locations.data_sets[0].data['headers'][1]['columnNames']

distances = [f'{h}: {d}'
             for d in distances
             for h in headers[5:8]]

headers = [*headers[:5], *distances]
print(headers)

data = pd.DataFrame(data, columns=headers)
print(data.columns)
