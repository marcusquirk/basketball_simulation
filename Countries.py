class Countries:

    def __init__(self):
        self.dictionary = {}

    def add_country(self, country):
        self.dictionary[country.get_country] = country

    def count_cities(self):
        counter = 0
        for i in self.dictionary:
            counter = counter + self.dictionary[i].cities.get_quantity()
        return counter
