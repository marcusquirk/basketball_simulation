import math as maths
import random

import BasketballAverages
import Imperial
import Position
from Constants import database, max_rating, min_rating, avg_height, height_sd, avg_weight, skills, tendencies
from Database import create_connection


class Player:
    # This class defines all of the attributes of a player

    def __init__(self, country):
        # Give each player a unique ID
        # self.id = len(players)

        # Generate a name
        self.forename = country.nameset.gen_forename()
        self.surname = country.nameset.gen_surname()
        self.country = country.nameset.get_country

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

        # A player's 'height' (actually based on standing reach) will be one of our strongest indicators of position
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
                Imperial.from_metric_round(self.armspan, 1)) + ", " + str(Imperial.from_metric_round(self.reach, 1)) + \
                   ", " + str(self.avg) + ", " + str(self.pot)


def read_team(id):
    conn = create_connection(database)
    cur = conn.cursor()
    sql = "SELECT p.id, p.forename, p.surname, h.reach, s.ovr, s.'3pt', s.mid, s.fin,  s.ft, s.post, s.pass, s.drive, " \
          "s.dribble, s.per_d, s.post_d, s.blk, s.speed," \
          "s.jump, s.strength, s.oreb, s.dreb FROM skills AS s INNER JOIN players AS p ON s.id = p.id INNER JOIN teams " \
          "AS t ON p.team_id = t.id INNER JOIN physicals AS h ON p.id=h.id WHERE t.id = " + str(id)
    cur.execute(sql)
    result = [i for i in cur.fetchall()]
    return result


def read_player(id):
    conn = create_connection(database)
    cur = conn.cursor()
    sql = "SELECT * FROM skills WHERE id = " + str(id)
    cur.execute(sql)
    result = [i for i in cur.fetchall()[0]]
    return result


def create_player(conn, country, team_id=0):
    forename = country.nameset.gen_forename()
    surname = country.nameset.gen_surname()

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

    # # Assign the player to first available team with an open spot
    # valid_team = False
    # i = 1
    # while not valid_team:
    #     # If there are less than 5 players on the team, assign the player
    #     if len(teams[i].players) < 5:
    #         teams[i].addplayer(self)
    #         self.team = i
    #         valid_team = True
    #     elif i == len(teams) - 1:
    #         teams[0].addplayer(self)
    #         self.team = 0
    #         valid_team = True
    #     else:
    #         i += 1

    sql = """INSERT INTO players (forename, surname, team_id)
            VALUES(?, ?, ?)"""
    cur = conn.cursor()
    cur.execute(sql, (forename, surname, team_id))
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

    sql += ", avg, ovr, pot, grade)\n"

    skill_dict["avg"] = int(BasketballAverages.average_dict(skill_dict))

    # Overall rating, roughly scaled like 2K
    skill_dict["ovr"] = (int(((skill_dict["avg"] - 55) * 1) + 75.5))

    # Give each player a random pot that is greater than their ovr
    skill_dict["pot"] = (
        maths.ceil((random.random() * random.random() * (max_rating - skill_dict["ovr"])) + skill_dict["ovr"]))

    # Give each player a grade based on their ovr and pot
    temp_grade = (skill_dict["pot"] + skill_dict["ovr"]) / 2

    if temp_grade > 90:
        skill_dict["grade"] = "A+"
    elif temp_grade > 87:
        skill_dict["grade"] = "A"
    elif temp_grade > 84:
        skill_dict["grade"] = "A-"
    elif temp_grade > 81:
        skill_dict["grade"] = "B+"
    elif temp_grade > 78:
        skill_dict["grade"] = "B"
    elif temp_grade > 75:
        skill_dict["grade"] = "B-"
    elif temp_grade > 72:
        skill_dict["grade"] = "C+"
    elif temp_grade > 69:
        skill_dict["grade"] = "C"
    elif temp_grade > 66:
        skill_dict["grade"] = "C-"
    elif temp_grade > 63:
        skill_dict["grade"] = "D"
    else:
        skill_dict["grade"] = "F"

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

    sql += ", ?, ?, ?, ?);"

    data = [current_id]
    skill_list = skill_dict.values()
    data.extend(skill_list)
    data = tuple(data)
    cur.execute(sql, data)

    position = (Position.Position(l_height, skill_dict))
    sql = """INSERT INTO positions (id, position)
            VALUES(?, ?)"""
    cur.execute(sql, (current_id, str(position)))

    sql = """INSERT INTO hometowns (player_id, hometown_id)
            VALUES(?, ?)"""
    cur.execute(sql, (current_id, country.cities.gen_hometown()))
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


def add_random_players(quantity, country, team_id=0):
    # create a database connection
    conn = create_connection(database)
    with conn:
        for i in range(quantity):
            create_player(conn, country, team_id)


def read_players(player_id):
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = """SELECT p.surname, po.position, ph.height, s.ovr, c.city FROM players p INNER JOIN positions po ON
        p.id = po.id INNER JOIN physicals ph ON p.id = ph.id INNER JOIN skills s ON p.id = s.id INNER JOIN hometowns h
        ON p.id = h.player_id INNER JOIN cities c ON h.hometown_id = c.id WHERE p.id >= 0 AND p.id <= """
        # sql = """SELECT p.surname, h.hometown FROM players p INNER JOIN hometowns h ON p.id = h.id WHERE p.id = """
        sql += str(player_id)
        cur = conn.cursor()
        cur.execute(sql)
        print(cur.fetchall())
