import random
import BasketballAverages
import math as maths
import Imperial
import Position
from Database import create_connection

from Constants import database, max_rating, min_rating, avg_height, height_sd, avg_weight, skills, tendencies


class Player:
    # This class defines all of the attributes of a player

    def __init__(self, country):

        # Give each player a unique ID
        # self.id = len(players)

        # Generate a name
        self.forename = country["names"].gen_forename()
        self.surname = country["names"].gen_surname()
        self.country = country["names"].get_country

        # Give our player a height, 'listed height', armspan, and standing reach
        # Height uses our predefined average and standard deviation
        self.height = round(random.normalvariate(avg_height, height_sd), 1)
        # NBA average "ape index" is 1.06, with a minimum of roughly 1.0 and a maximum of roughly 1.12
        self.armspan = round(random.normalvariate(self.height * 1.06, (self.height * 0.06) / 3), 1)
        # Standing reach in the NBA has an average of (height+armspan)/1.5477.
        # The divisor of 1.5477 has a sd of 0.02251, due to some of players' heights being above their shoulders.
        self.reach = round((self.height + self.armspan) / random.normalvariate(1.5477, 0.02251), 1)
        # Listed height in basketball is the height in shoes, usually (somewhat randomly) rounded up.
        if self.height < 183:
            short_syndrome = random.random() * 0.4 * (183 - self.height) + 0.1
        else:
            short_syndrome = 0
        self.l_height = Imperial.from_metric_round(self.height + (random.random() * 5) + 1.27 + short_syndrome, 0)

        # Generate empty dictionaries for the player's skills and tendencies
        self.skills = {}
        self.tendencies = {}
        # For each attribute, generate random number between the minimum and maximum rating
        # The constants 'skills' and 'tendencies' are defined at the beginning of the code.
        for i in skills:
            self.skills[i] = random.randint(min_rating, max_rating)
        for i in tendencies:
            self.tendencies[i] = random.randint(min_rating, max_rating)

        # A player's 'height' (actually based on standing reach) will be one of our strongest indicators of position.
        self.skills["ht"] = int(
            (self.reach - ((avg_height * 2.06) / 1.5477 - 4 * height_sd) / 8 * height_sd) * 100)

        # If ht is outside the range 0-100, set ht to 0 or 100
        if self.skills["ht"] < 0:
            self.skills["ht"] = 0
        elif self.skills["ht"] > 100:
            self.skills["ht"] = 100

        # Give each player an average value of their ratings
        self.avg = int(BasketballAverages.average(self.skills) + 0.5)

        # Give each player a random pot that is greater than their avg
        self.pot = maths.ceil((random.random() * random.random() * (max_rating - self.avg)) + self.avg)

        # Create an empty list that will contain the players' game stats
        self.game_stats = []

        # Determine the position of the player
        self.pos = Position(self)

        # Assign the player to first available team with an open spot
        valid_team = False
        i = 1
        while not valid_team:
            # If there are less than 5 players on the team, assign the player
            if len(teams[i].players) < 5:
                teams[i].addplayer(self)
                self.team = i
                valid_team = True
            elif i == len(teams) - 1:
                teams[0].addplayer(self)
                self.team = 0
                valid_team = True
            else:
                i += 1

    def __str__(self):
        """the string of a player returns their full name"""
        return self.forename + " " + self.surname

    def print(self, info="vitals"):
        """returns the name, position, physical attributes, and overall ratings of a player"""
        if info == "vitals":
            return str(self.pos) + " " + str(self.pos.second_position) + "\t" + str(self)[0:15] + "\t" + str(
                self.l_height) + "\t" + str(Imperial.from_metric_round(self.height, 1)) + ", " + str(
                Imperial.from_metric_round(self.armspan, 1)) + ", " + str(Imperial.from_metric_round(self.reach, 1)) +\
                   ", " + str(self.avg) + ", " + str(self.pot)


def create_player(conn, country):
    forename = country["names"].gen_forename()
    surname = country["names"].gen_surname()

    # Give our player a height (listed), weight, barefoot height, armspan, and standing reach
    # Height uses our predefined average and standard deviation
    height = round(random.normalvariate(avg_height, height_sd), 1)

    # NBA average "ape index" is 1.06, with a minimum of roughly 1.0 and a maximum of roughly 1.12
    armspan = round(random.normalvariate(height * 1.06, (height * 0.06) / 3), 1)

    # Standing reach in the NBA has an average of (height+armspan)/1.5477.
    # The divisor of 1.5477 has a sd of 0.02251, due to some of a player's height being above their shoulders.
    reach = round((height + armspan) / random.normalvariate(1.5477, 0.02251), 1)

    l_height = maths.floor(height + (random.random() * 5) + 1.27)
    l_height_feet = Imperial.from_metric_round(l_height, 0)

    # NBA average BMI is 24.88 with a sd of 1.6633
    weight = round(random.normalvariate(24.9, 1.6633) * ((height / 100) ** 2), 1)

    sql = """INSERT INTO players (forename, surname)
            VALUES(?, ?)"""
    cur = conn.cursor()
    cur.execute(sql, (forename, surname))
    current_id = cur.lastrowid

    data = [current_id, str(l_height_feet), weight, l_height, height, armspan, reach]

    sql = """INSERT INTO physicals (id, height, weight, 'metric height', barefoot, armspan, reach)
            VALUES(?, ?, ?, ?, ?, ?, ?)"""
    cur.execute(sql, data)

    skill_dict = {}

    for i in skills:
        if i == "3pt":
            sql = "INSERT INTO skills (id, '3pt'"
            skill_dict[i] = (random.randint(min_rating, max_rating))
        elif i == "speed":
            # Speed is related to weight (see Google Sheet)
            sql += ", " + i
            temp_rating = random.randint(min_rating, max_rating)
            if weight >= avg_weight:
                factor = (weight - avg_weight) / 17
                skill_dict[i] = int(factor * random.random() * temp_rating + (1 - factor) * temp_rating)
            else:
                factor = (avg_weight - weight) / 17
                rxn = random.random()
                skill_dict[i] = int(
                    factor * (max_rating - (rxn * temp_rating)) + (1 - factor) * (max_rating - temp_rating))
        elif i == "strength":
            # Strength is related to weight
            sql += ", " + i
            temp_rating = random.randint(min_rating, max_rating)
            if weight < avg_weight:
                factor = (avg_weight - weight) / 17
                skill_dict[i] = int(factor * random.random() * temp_rating + (1 - factor) * temp_rating)
            else:
                factor = (weight - avg_weight) / 17
                rxn = random.random()
                skill_dict[i] = int(
                    factor * (max_rating - (rxn * temp_rating)) + (1 - factor) * (max_rating - temp_rating))
        else:
            sql += ", " + i
            skill_dict[i] = (random.randint(min_rating, max_rating))

    sql += ", avg, ovr, pot)\n"

    skill_dict["avg"] = int(BasketballAverages.average_dict(skill_dict))

    # Overall rating, roughly scaled like 2K
    skill_dict["ovr"] = (int(((skill_dict["avg"] - 55) * 1) + 75.5))

    # Give each player a random pot that is greater than their avg
    skill_dict["pot"] = (
        maths.ceil((random.random() * random.random() * (max_rating - skill_dict["avg"])) + skill_dict["avg"]))

    # If overall rating outside 1-99, fix that
    for i in "speed", "strength", "avg", "ovr", "pot":
        if skill_dict[i] >= 100:
            skill_dict[i] = 99
        elif skill_dict[i] <= 0:
            skill_dict[i] = 1

    for i in skills:
        if i == "3pt":
            sql += "VALUES(?, ?"
        else:
            sql += ", ?"

    sql += ", ?, ?, ?);"

    data = [current_id]
    skill_list = skill_dict.values()
    data.extend(skill_list)
    data = tuple(data)
    cur.execute(sql, data)

    position = (Position.Position(l_height, skill_dict))
    sql = """INSERT INTO positions (id, position)
            VALUES(?, ?)"""
    cur.execute(sql, (current_id, str(position)))

    sql = """INSERT INTO hometowns (id, hometown)
            VALUES(?, ?)"""
    cur.execute(sql, (current_id, country["locations"].gen_hometown()))
    return cur.lastrowid


def add_player(conn, player):
    """
    Add a player to the players table
    :param conn:   the database connection
    :param player: the player's name, in the form (forename, surname)"""

    sql = ''' INSERT INTO players (forename, surname)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, player)
    return cur.lastrowid


def add_random_players(quantity, country):
    # create a database connection
    conn = create_connection(database)
    with conn:
        for i in range(quantity):
            create_player(conn, country)


def read_players(player_id):
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = """SELECT p.surname, po.position, ph.height, s.ovr, l.place FROM players p INNER JOIN positions po ON
        p.id = po.id INNER JOIN physicals ph ON p.id = ph.id INNER JOIN skills s ON p.id = s.id INNER JOIN hometowns h
        ON p.id = h.id INNER JOIN locations l ON h.hometown = l.id WHERE p.id >= 0 AND p.id <= """
        # sql = """SELECT p.surname, h.hometown FROM players p INNER JOIN hometowns h ON p.id = h.id WHERE p.id = """
        sql += str(player_id)
        cur = conn.cursor()
        cur.execute(sql)
        print(cur.fetchall())
