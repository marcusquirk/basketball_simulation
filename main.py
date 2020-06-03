from Database import define_tables
import Player
from Player import add_random_players, read_players, create_player
from Team import add_teams
import Nameset
import Cities


def main():
    england = {"names": Nameset.Nameset("England", "England_First.json", "England_Last.json"),
               "cities": Cities.Cities("England.json", "England", "ENG")}
    scotland = {"names": Nameset.Nameset("Scotland", "Scotland_First.json", "Scotland_Last.json"),
                "cities": Cities.Cities("Scotland.json", "Scotland", "SCO")}

    startup = input("'new', 'read' or 'add'?")
    if startup.lower() == 'new':
        define_tables()
        add_random_players(250, england)
        add_random_players(50, scotland)
        add_teams()
    elif startup.lower() == 'add':
        add_random_players(13, england)
    elif startup.lower() == 'read':
        which_player = input("Which player?")
        read_players(which_player)
    england["cities"].to_database()
    scotland["cities"].to_database()


if __name__ == "__main__":
    main()
