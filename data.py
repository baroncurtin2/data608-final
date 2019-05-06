from nba_api.stats.endpoints.leaguedashplayershotlocations import LeagueDashPlayerShotLocations
import pandas as pd


class NBAData:
    def __init__(self):
        self.__data = self.__get_data()
        self.__player_names = self.__data['PLAYER_NAME'].unique()

    def __get_data(self):
        # Basic Request
        shot_locations = LeagueDashPlayerShotLocations(distance_range='5ft Range')
        data = shot_locations.data_sets[0].data['data']

        # fix headers
        distances = shot_locations.data_sets[0].data['headers'][0]['columnNames']
        self.__distances = distances  # easy referencing later

        headers = shot_locations.data_sets[0].data['headers'][1]['columnNames']
        distances = [f'{h}: {d}'
                     for d in distances
                     for h in headers[5:8]]
        headers = [*headers[:5], *distances]

        # create dataframe
        data = pd.DataFrame(data, columns=headers)

        # drop unneeded columns
        data.drop(['PLAYER_ID', 'TEAM_ID'], inplace=True, axis=1)
        return data

    @property
    def player_names(self):
        return self.__player_names

    @property
    def data(self):
        return self.__data

    @property
    def distances(self):
        return self.__distances

    def attempts_check(self, player, distance):
        to_check = self.data[self.data[f'FGA: {distance}'] > 25]
        players_list = ('\n'.join(to_check['PLAYER_NAME'].str.lower().to_list()))
        return player.lower() in players_list

    def player_lookup(self, player):
        to_check = self.data[self.data['PLAYER_NAME'].str.contains(player, case=False)]
        return to_check


if __name__ == '__main__':
    nba = NBAData()
    data = nba.data.set_index('PLAYER_NAME')
