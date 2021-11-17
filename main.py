from Database import define_tables
import Player
from Player import add_random_players, read_players, read_team
from Team import add_teams, create_team
from Constants import skills
import Nameset
import Cities
import Country
import Countries
import Game


def main():
    print('here')
    countries_list = Countries.Countries()

    england = Country.Country("England", Nameset.Nameset("England_First.json", "England_Last.json"),
                              Cities.Cities("England.json", "England", "ENG", countries_list.count_cities()),
                              countries_list)
    scotland = Country.Country("Scotland", Nameset.Nameset("Scotland_First.json", "Scotland_Last.json"),
                               Cities.Cities("Scotland.json", "Scotland", "SCO", countries_list.count_cities()),
                               countries_list)

    startup = input("'new', 'read' or 'add'?")
    if startup.lower() == 'new':
        define_tables()
        add_random_players(12, england, 1)
        add_random_players(12, scotland, 2)
        add_teams()
        england.cities.to_database()
        scotland.cities.to_database()
    elif startup.lower() == 'add':
        add_random_players(12, england)
    elif startup.lower() == 'read':
        which_player = input("Which player?")
        read_players(which_player)

    teams = []
    for i in range(1,3):
        teams.append(read_team(i))

    dict_keys = ["id", "forename", "surname", "reach", "ovr"] + skills + ["index"]
    def list_to_dict(a, b):
        return dict(zip(a, b))
    list_of_teams = []
    for i in range(len(teams)):
        list_of_teams.append([])
        for dict_values in teams[i]:
            list_of_teams[i].append(list_to_dict(dict_keys, dict_values))
    test_game = Game.Game(list_of_teams[0], list_of_teams[1])
    starters = test_game.generate_starters()


if __name__ == "__main__":
    main()
