import sqlite3
from sqlite3 import Error
import os

database = r"Test"


def create_file(db_file, iteration=0):
    """ create a database file to a SQLite database """
    if iteration != 0:
        db_filename = db_file + str(iteration)
    else:
        db_filename = db_file
    conn = None
    try:
        if not os.path.exists(db_filename + ".db"):
            conn = sqlite3.connect(db_filename + ".db")
        else:
            create_file(db_file,iteration+1)
    except Error as e:
        print(e)
    return conn


def create_connection(db_file):
    """create a database connection to SQLite"""
    db_filename = db_file + ".db"
    conn = None
    try:
        if os.path.exists(db_filename):
            conn = sqlite3.connect(db_filename)
            print('opened!')
        else:
            conn = create_file(db_file)
            print("File not found, creating file...")
    except Error as e:
        print(e)
    return conn


def create_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def define_tables():

    sql_drop_player = """DROP TABLE IF EXISTS players"""
    sql_drop_location = """DROP TABLE IF EXISTS locations"""

    sql_player_table = """
                                CREATE TABLE IF NOT EXISTS players (
                                        id integer PRIMARY KEY,
                                        forename text NOT NULL,
                                        surname text NOT NULL
                                );"""
    sql_location_table = """
                                    CREATE TABLE IF NOT EXISTS locations (
                                    id integer PRIMARY KEY,
                                    place text NOT NULL,
                                    country text NOT NULL
                                );"""

    # create a database connection
    conn = create_connection(database)

    with conn:

        # create projects table
        create_table(conn, sql_drop_player)
        create_table(conn, sql_player_table)

        # create tasks table
        create_table(conn, sql_drop_location)
        create_table(conn, sql_location_table)

        # create table for physicals
        sql = """DROP TABLE IF EXISTS physicals"""
        create_table(conn, sql)
        sql = """
                CREATE TABLE IF NOT EXISTS physicals (
                id integer NOT NULL,
                height text NOT NULL,
                weight integer NOT NULL,
                'metric height' integer NOT NULL,
                barefoot real NOT NULL,
                armspan integer NOT NULL,
                reach integer NOT NULL,
                FOREIGN KEY(id) REFERENCES player(id)
                );"""
        create_table(conn, sql)

        # create table for skills
        sql = """DROP TABLE IF EXISTS skills"""
        create_table(conn, sql)
        sql = """
                CREATE TABLE IF NOT EXISTS skills (
                id integer NOT NULL,
                ovr integer NOT NULL"""
        for i in skills:
            sql += """,
            '""" + i + """' integer NOT NULL"""
        sql += ", avg integer NOT NULL, pot integer NOT NULL);"
        create_table(conn, sql)

        # create table for position
        sql = """DROP TABLE IF EXISTS positions"""
        create_table(conn, sql)
        sql = """
                CREATE TABLE IF NOT EXISTS positions (
                id integer NOT NULL,
                position text NOT NULL,
                FOREIGN KEY(id) REFERENCES player(id)
                );"""
        create_table(conn, sql)

        # create table for teams
        sql = """DROP TABLE IF EXISTS teams"""
        create_table(conn, sql)
        sql = """
                CREATE TABLE IF NOT EXISTS teams (
                id integer PRIMARY KEY,
                name text NOT NULL,
                location text NOT NULL,
                nickname text NOT NULL,
                abbreviation text NOT NULL 
                );"""
        create_table(conn, sql)

        # create a new location
        location = ("Aberdeen", "Scotland");
        add_location(conn, location)
        location = ("London", "England");
        add_location(conn, location)

        for i in range(50000):
            create_player(conn)

        create_team(conn, 'Leicester', 'Leicester Riders', 'Riders', 'LEI')
        create_team(conn, 'Edinburgh', 'City of Edinburgh', 'Kings', 'CoE')
        create_team(conn, 'Glasgow', 'Radisson Red Glasgow Rocks', 'Rocks')
        create_team(conn, 'Manchester', 'Manchester Magic', 'Magic', 'MAN')
        create_team(conn, 'Worthing', 'Worthing Thunder', 'Thunder', 'WTH')
        create_team(conn, 'Worcester', 'Worcester Wolves', 'Wolves', 'WCS')
        create_team(conn, 'Newcastle upon Tyne', 'Newcastle Eagles', 'Eagles')
        create_team(conn, 'London', 'London City Royals', 'Royals', 'LCR')
        create_team(conn, 'London', 'London Lions', 'Lions', 'LON')
        create_team(conn, 'Dublin', 'Dublin Giants', 'Giants', 'DUB')
        create_team(conn, 'Liverpool')
        create_team(conn, 'Cardiff', 'Cardiff Cougars', 'Cougars', 'CAR')
        create_team(conn, 'Bristol', 'Bristol Flyers', 'Flyers', )


