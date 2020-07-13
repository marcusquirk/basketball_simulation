from Database import define_tables
import Player
from Player import add_random_players, read_players, create_player
from Team import add_teams
import Nameset
import Cities
import Country
import Countries


def main():
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
        add_random_players(2500, england)
        add_random_players(500, scotland)
        add_teams()
    elif startup.lower() == 'add':
        add_random_players(13, england)
    elif startup.lower() == 'read':
        which_player = input("Which player?")
        read_players(which_player)
    england.cities.to_database()
    scotland.cities.to_database()


if __name__ == "__main__":
    main()
