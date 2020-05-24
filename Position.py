from Constants import pos, skills, avg_height, height_sd


class Position:
    """This class defines the five basketball positions and also determines what position
    a given player should play"""
    
    # Constructor
    def __init__(self, height, skill_dict):

        # Count a 'score' for how well the player suits a given position. Initialise the count to 0
        # In the end, the highest score is what position the player should play.
        # For example, if the highest score is at index 1, the player should be an SG
        self.count = [0 for i in range(5)]

        self.position = ""
        self.second_position = ""

        # Diff is the difference between a player's rating in a given skill relative
        # to their average rating
        diff = {}
        for i in skills:
            diff[i] = skill_dict[i] / skill_dict["avg"]

        # Update count with the weights for each position
        # SF 6'5"/6'8"/6'11"
        # SG 6'2"/6'5"/6'8"
        # Position.tally(self, 25-((reach-avg_reach+1*(r_sd))/(0.17*(r_sd)))**2, 25-((reach-avg_reach+0.25*(r_sd))/
        # (0.15*(r_sd)))**2, 25-((reach-avg_reach-0.5*(r_sd))/(0.15*(r_sd)))**2, 25-((reach-avg_reach-0.75*(r_sd))/
        # (0.15*(r_sd)))**2, 25-((reach-avg_reach-1.2*(r_sd))/(0.15*(r_sd)))**2)
        avg_lh = avg_height + 3.77
        Position.tally(self, 25 - ((height - avg_lh + 1.3 * height_sd) / (0.17 * height_sd)) ** 2,
                       25 - ((height - avg_lh + 0.25 * height_sd) / (0.15 * height_sd)) ** 2,
                       25 - ((height - avg_lh - 0.42 * height_sd) / (0.15 * height_sd)) ** 2,
                       25 - ((height - avg_lh - 0.9 * height_sd) / (0.15 * height_sd)) ** 2,
                       25 - ((height - avg_lh - 1.6 * height_sd) / (0.15 * height_sd)) ** 2)
        Position.tally(self, 10 * diff["3pt"], 25 * diff["3pt"], 10 * diff["3pt"], 0, -15 * diff["3pt"])
        Position.tally(self, 35 * diff["pass"], 15 * diff["pass"], 10 * diff["pass"], 0, -5 * diff["pass"])
        Position.tally(self, 35 * diff["dribble"], 15 * diff["dribble"], 10 * diff["dribble"], 0, -15 * diff["dribble"])
        Position.tally(self, -10 * diff["post"], 0, 5 * diff["post"], 15 * diff["post"], 25 * diff["post"])
        Position.tally(self, -10 * diff["post_d"], 0, 5 * diff["post_d"], 15 * diff["post_d"], 30 * diff["post_d"])
        Position.tally(self, 20 * diff["per_d"], 20 * diff["per_d"], 15 * diff["per_d"], 5 * diff["per_d"],
                       -15 * diff["per_d"])
        Position.tally(self, 5 * diff["mid"], 10 * diff["mid"], 10 * diff["mid"], 5 * diff["mid"], 0)
        Position.tally(self, 17.5 * diff["speed"], 10 * diff["speed"], 7.5 * diff["speed"], 0, 0)
        Position.tally(self, 0, 0, 10 * diff["dreb"], 25 * diff["dreb"], 35 * diff["dreb"])
        Position.tally(self, -10 * diff["oreb"], 0, 10 * diff["oreb"], 25 * diff["oreb"], 35 * diff["oreb"])
        Position.tally(self, 0, 0, 5 * diff["strength"], 10 * diff["strength"], 30 * diff["strength"])
        Position.tally(self, -10 * diff["blk"], 0, 5 * diff["blk"], 15 * diff["blk"], 25 * diff["blk"])
        Position.tally(self, 25 * diff["drive"], 15 * diff["drive"], 20 * diff["drive"], 0, 0)

        # Using the final count, choose a position for the player
        self.position = Position.choose(self)
        self.second_position = Position.choose_second(self)

    def choose(self):
        """Finds which position has the greatest count, and returns that position"""

        current_max = self.count[0]
        current_pos = 0

        # Goes through each position one-by-one to determine which has the greatest count
        for i in range(5):
            if self.count[i] > current_max:
                current_max = self.count[i]
                current_pos = i

        return pos[current_pos]

    def choose_second(self):
        """Finds which position has the second-greatest count, and returns that position"""
        current_max = self.count[0]
        current_pos = 0
        current_second = self.count[1]
        current_second_pos = 1

        # Goes through each position one-by-one to determine which has the second-greatest count
        # We still keep track of which count has the maximum number, otherwise we can't know which is second-greatest
        for i in range(5):

            # If there is a new maximum, update current and secondary
            if self.count[i] > current_max:

                # The previous maximum must be assigned as the secondary position before we update the maximum
                current_second = current_max
                current_second_pos = current_pos

                # Update the maximum
                current_max = self.count[i]
                current_pos = i

            # If there is a position with a count greater than the secondary, but not the maximum
            # (AND isn't the maximum), update just the secondary
            elif self.count[i] > current_second and i != current_pos:
                current_second = self.count[i]
                current_second_pos = i
        if current_second * 1.1 >= current_max:
            return pos[current_second_pos]
        else:
            return ""

    def tally(self, pg, sg, sf, pf, c):
        """Updates the count for each position, using a given weight for each position."""
        self.count[0] += pg
        self.count[1] += sg
        self.count[2] += sf
        self.count[3] += pf
        self.count[4] += c

    def str_second(self):
        return self.second_position

    def __str__(self):
        return self.position
