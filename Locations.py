import os
import json
import random
import bisect


class Locations:

    def __init__(self, locations_file):
        json_file = open(os.getcwd() + "/Locations/" + locations_file)
        self.locations = json.load(json_file)
        print(self.locations)

    """Chooses a name from a given nameset, with a probability (prob) of a double-barrelled name being generated.
    prob is automatically set to 2.5%.
    The names in the nameset should be ordered according to a cumulative distribution function (cdf).
    The get_names function should have already sorted out the cdf."""
    def gen_forename(self):
        # Generate a random number between 0 and the total cumulative frequency of names
        randnum = random.random() * self.forenames["cdf"][-1]
        # Choose a name
        name_num = bisect.bisect(self.forenames["cdf"], randnum)

        # Small chance of a double-barrelled name
        compound = random.random()
        if compound < self.forename_prob:
            name_num2 = name_num
            # Makes sure the two names aren't the same
            while name_num2 == name_num:
                randnum2 = random.random() * self.forenames["cdf"][-1]
                name_num2 = bisect.bisect(self.forenames["cdf"], randnum2)
            # Return the double-barrelled name with a hyphen in between
            return self.forenames["name"][name_num] + "-" + self.forenames["name"][name_num2]
        # If no double-barrelled name is generated, return the single name
        else:
            return self.forenames["name"][name_num]

    def gen_surname(self):
        # Generate a random number between 0 and the total cumulative frequency of names
        randnum = random.random() * self.surnames["cdf"][-1]
        # Choose a name
        name_num = bisect.bisect(self.surnames["cdf"], randnum)

        # Small chance of a double-barrelled name
        compound = random.random()
        if compound < self.surname_prob:
            name_num2 = name_num
            # Makes sure the two names aren't the same
            while name_num2 == name_num:
                randnum2 = random.random() * self.surnames["cdf"][-1]
                name_num2 = bisect.bisect(self.surnames["cdf"], randnum2)
            # Return the double-barrelled name with a hyphen in between
            return self.surnames["name"][name_num] + "-" + self.surnames["name"][name_num2]
        # If no double-barrelled name is generated, return the single name
        else:
            return self.surnames["name"][name_num]

    def get_country(self):
        return self.country