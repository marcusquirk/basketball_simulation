from Database import define_tables
from Player import add_random_players, read_players, create_player
from Team import add_teams
import Nameset


def main():
    england = Nameset.Nameset("England", "England_First.json", "England_Last.json")
    startup = input("'new', 'read' or 'add'?")
    if startup.lower() == 'new':
        define_tables()
        add_random_players(5000, england)
        add_teams()
    elif startup.lower() == 'add':
        add_random_players(13, england)
    elif startup.lower() == 'read':
        which_player = input("Which player?")
        read_players(which_player)


if __name__ == "__main__":
    main()
