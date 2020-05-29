import os
import json
import random
import bisect

from Database import create_connection
from Constants import database


class Locations:

    def __init__(self, locations_file, country):
        self.country = country

        json_file = open(os.getcwd() + "/Locations/" + locations_file)
        self.locations = json.load(json_file)

        # Create a cumulative distribution function based on the probability density function.
        self.locations["cdf"] = self.locations["pdf"]
        for i in range(1, len(self.locations["pdf"])):
            self.locations["cdf"][i] = self.locations["cdf"][i-1]+self.locations["cdf"][i]

    def gen_location(self):
        # Generate a random number between 0 and the total cumulative frequency of names
        randnum = random.random() * self.locations["cdf"][-1]
        # Choose a name
        name_num = bisect.bisect(self.locations["cdf"], randnum)
        return self.locations["city"][name_num]

    def to_database(self):
        conn = create_connection(database)
        with conn:
            cur = conn.cursor()
            current_id = cur.lastrowid
            for i in range(len(self.locations["pdf"])):
                data = [current_id, self.locations["city"][i], self.country, self.locations["pdf"][i]]
                sql = """INSERT INTO locations (id, place, country, cdf)
                        VALUES(?, ?, ?, ?)"""
                cur.execute(sql, data)

    def get_country(self):
        return self.country
