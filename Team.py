from Database import create_connection, create_table, database
from Player import skills, create_player


class Team:
    """This class defines the attributes of a team"""

    def __init__(self, city, name="", short="", abbrev=""):
        """Initialises the team
        city    the location of the team (e.g. Leicester, Madrid)
        name    the full of the team (e.g. Leicester Riders, Real Madrid Baloncesto)
        short   the short name of the team (e.g. Riders, Real Madrid)
        abbrev  the abbreviation of the team (e.g. LEI, RMB)"""
        self.city = city

        # If no full name given, make it the name of the city
        if name == "":
            self.name = city
        else:
            self.name = name

        # If no short name is given, make it the name of the city
        if short == "":
            self.short = city

        # If no abbreviation is given, make it the first three letters of the city, uppercase
        if abbrev == "":
            self.abbrev = self.city[0:3].upper()
        else:
            # The maximum length of the abbreviation is four letters
            self.abbrev = abbrev[0:4].upper()

        # The roster starts off as empty
        self.players = []

    def add_player(self, player):
        """Adds a player to the roster"""
        self.players.append(player)

    def print_players(self):
        """Prints the players on the team"""
        for i in range(len(self.players)):
            print(self.players[i])

    def __str__(self):
        """the string of the team returns the full name of the team"""
        if self.name != self.city:
            return self.name
        else:
            return self.city


def create_team(conn, city, name="", short="", abbrev=""):
    """
    :param conn:    the database connection
    :param city:    the location of the team (e.g. Leicester, Madrid)
    :param name:    the full of the team (e.g. Leicester Riders, Real Madrid Baloncesto)
    :param short:   the short name of the team (e.g. Riders, Real Madrid)
    :param abbrev:  the abbreviation of the team (e.g. LEI, RMB)"""

    # If no full name given, make it the name of the city
    if name == "":
        name = city

    # If no short name is given, make it the name of the city
    if short == "":
        short = city

    # If no abbreviation is given, make it the first three letters of the city, uppercase
    if abbrev == "":
        abbrev = city[0:3].upper()
    else:
        # The maximum length of the abbreviation is four letters
        abbrev = abbrev[0:4]

    sql = """INSERT INTO teams (name, location, nickname, abbreviation)
            VALUES (?, ?, ?, ?);"""
    cur = conn.cursor()
    cur.execute(sql, (name, city, short, abbrev))


def add_location(conn, location):
    """
    Create a new location into the locations table
    :param location: a tuple location in the form (town, country)
    :param conn:     the database connection
    """
    sql = ''' INSERT INTO locations (place, country)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, location)
    return cur.lastrowid

