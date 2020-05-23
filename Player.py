import random
import BasketballAverages
import math as maths
import Imperial

# The minimum and maximum rating for skills
min_rating = 10
max_rating = 99

# The average height and standard deviation in cm
# Player heights will be determined with a normal distribution
avg_height = 196.5
height_sd = 8

# Define what the skills and tendencies are
skills = ["3pt", "mid", "fin", "dunk",  "ft", "post", "pass", "drive", "dribble", "per_d", "post_d", "blk", "speed",
          "jump", "strength", "o_reb", "d_reb"]
tendencies = ["3pt", "mid", "pass", "drive", "post", "layup", "dunk", "foul", "stl", "blk"]


class Player:
    # This class defines all of the attributes of a player

    def __init__(self, country):

        # Give each player a unique ID
        # self.id = len(players)

        # Generate a name
        self.forename = country.gen_forename()
        self.surname = country.gen_surname()
        self.country = country.get_country

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
        validteam = False
        i = 1
        while validteam == False:
            # If there are less than 5 players on the team, assign the player
            if len(teams[i].players) < 5:
                teams[i].addplayer(self)
                self.team = i
                validteam = True
            elif i == len(teams) - 1:
                teams[0].addplayer(self)
                self.team = 0
                validteam = True
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
