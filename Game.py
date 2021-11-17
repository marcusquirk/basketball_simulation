from Constants import stats, period_length, num_periods

class Game:
    def __init__(self, team0, team1):
        self.time_remaining = period_length*60
        self.period = 0
        self.score = [0,0]
        self.teams = (team0, team1)
        self.stats = [[0]*17]*len(self.teams[0]),[[0]*17]*len(self.teams[1])
        self.lineups = self.generate_starters()
        reach_index = self.find_best(1,"reach")
        print(reach_index)
        print(self.teams[1][reach_index])

    def generate_starters(self):
        starting_lineups = []
        for team in (self.teams[0], self.teams[1]):
            player_list = team[:]
            player_list.sort(key=lambda Player: Player['ovr'], reverse=True)
            current_lineup = []
            for i in range(len(team)):
                for player in player_list[0:5]:
                    if team[i]["id"] == player["id"]:
                        current_lineup.append(i)
                        break
            starting_lineups.append(current_lineup)
        return starting_lineups

    def find_best(self, team, category):
        best_player = 0
        best_rating = self.teams[team][self.lineups[team][0]][category]
        for i in range(len(self.lineups[team])):
            if self.teams[team][self.lineups[team][i]][category] > best_rating:
                print(self.teams[team][self.lineups[team][i]][category])
                print(best_rating)
                best_rating = self.teams[team][self.lineups[team][i]][category]
                best_player = self.lineups[team][i]
        return best_player


    def play_game(self, starters0=(0, 1, 2, 3, 4), starters1=(0, 1, 2, 3, 4)):
        self.lineups[0] = [self.team[0][starters0[i]] for i in starters0]
        self.lineups[1] = [self.team[0][starters1[i]] for i in starters1]

        if self.time_remaining > 0:
            self.score = self.play_possession()

    def play_possession(self, possession=None):
        if possession == None:
            possession = self.jumpball()

    def jumpball(self, player0, player1):
        print("foobar")