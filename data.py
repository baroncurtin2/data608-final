from nba_api.stats.endpoints.leaguedashplayershotlocations import LeagueDashPlayerShotLocations
import pandas as pd


class NBAData:
    def __init__(self):
        self.__data = self.__get_data()
        self.__player_names = self.__data['PLAYER_NAME'].unique()

    def __get_data(self):
        # custom headers
        custom_headers = {
            'Host': 'stats.nba.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Basic Request
        shot_locations = LeagueDashPlayerShotLocations(distance_range='5ft Range', headers=custom_headers, timeout=15000)
        nba_data = shot_locations.data_sets[0].data['data']

        # fix headers
        distances = shot_locations.data_sets[0].data['headers'][0]['columnNames']
        self.__distances = distances  # easy referencing later

        headers = shot_locations.data_sets[0].data['headers'][1]['columnNames']
        distances = [f'{h}: {d}'
                     for d in distances
                     for h in headers[5:8]]
        headers = [*headers[:5], *distances]

        # create dataframe
        nba_data = pd.DataFrame(nba_data, columns=headers)

        # drop unneeded columns
        nba_data.drop(['PLAYER_ID', 'TEAM_ID'], inplace=True, axis=1)

        # create expected points per 10 shots
        for d in self.distances:
            nba_data[f'PP10: {d}'] = nba_data[f'FG_PCT: {d}'] * 10

        return nba_data

    @property
    def player_names(self):
        return self.__player_names

    @property
    def data(self):
        return self.__data

    @property
    def distances(self):
        return self.__distances

    @property
    def mid_range_distances(self):
        return self.distances[2:5]

    def __set_index(self, col_name):
        return self.data.set_index([col_name])

    def __find_cols(self, col_part):
        return [c for c in self.data.columns if col_part in c]

    @property
    def mid_range_data(self):
        ds = self.distances[2:5]
        my_data = self.__set_index('PLAYER_NAME')
        cols = [c for c in my_data.columns
                for d in ds
                if d in c]
        return my_data[cols].reset_index()

    @property
    def field_goal_percentages(self):
        cols = self.__find_cols('FG_PCT')
        my_data = self.__set_index('PLAYER_NAME')
        return my_data[cols]

    @property
    def points_per_ten_shots(self):
        cols = self.__find_cols('PP10')
        my_data = self.__set_index('PLAYER_NAME')
        return my_data[cols]

    @property
    def field_goal_attempts(self):
        cols = self.__find_cols('FGA')
        my_data = self.__set_index('PLAYER_NAME')
        return my_data[cols]


if __name__ == '__main__':
    nba = NBAData()
    print(nba.mid_range_distances)
