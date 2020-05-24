from Database import define_tables
from Player import add_random_players, read_players
import Nameset


def main():
    england_names = Nameset("England_First.json", "England_Last.json")

    startup = input("'new', 'read' or 'add'?")
    if startup.lower() == 'new':
        define_tables()
    elif startup.lower() == 'add':
        add_random_players(13)
    elif startup.lower() == 'read':
        which_player = input("Which player?")
        read_players(which_player)



if __name__ == "__main__":
    main()
