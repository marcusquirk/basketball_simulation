import os
import json
import random
import bisect

from Database import create_connection
from Constants import database


class Cities:

    def __init__(self, cities_file, country):
        self.country = country

        json_file = open(os.getcwd() + "/cities/" + cities_file)
        self.cities = json.load(json_file)

        # Create a cumulative distribution function based on the probability density function.
        self.cities["cdf"] = self.cities["pdf"]
        self.cities["id"] = 1
        for i in range(1, len(self.cities["pdf"])):
            self.cities["cdf"][i] = self.cities["cdf"][i-1]+self.cities["cdf"][i]
            self.cities["id"] = i

    def gen_location(self):
        # Generate a random number between 0 and the total cumulative frequency of names
        randnum = random.random() * self.cities["cdf"][-1]
        # Choose a name
        city_num = bisect.bisect(self.cities["cdf"], randnum)
        return self.cities["city"][city_num]

    def gen_hometown(self):
        # Generate a random number between 0 and the total cumulative frequency of names
        randnum = random.random() * self.cities["cdf"][-1]
        # Choose a name
        city_num = bisect.bisect(self.cities["cdf"], randnum)
        return city_num+1

    def to_database(self):
        conn = create_connection(database)
        with conn:
            cur = conn.cursor()
            current_id = cur.lastrowid
            for i in range(len(self.cities["pdf"])):
                data = [current_id, self.cities["city"][i], self.country, self.cities["pdf"][i]]
                sql = """INSERT INTO cities (id, city, country, cdf)
                        VALUES(?, ?, ?, ?)"""
                cur.execute(sql, data)

    def get_country(self):
        return self.country
