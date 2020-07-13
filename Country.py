class Country:

    def __init__(self, country, nameset, cities, countries_list):
        self.country = country
        self.nameset = nameset
        self.cities = cities
        countries_list.add_country(self)

    def get_cities_quantity(self):
        return len(self.cities.cities["id"])

    def get_country(self):
        return self.country
