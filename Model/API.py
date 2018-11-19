import json
import requests


class API:

    hash_cities = {}

    # constructor #

    def __init__(self, hash_cities):
        self.hash_cities = hash_cities

    # function retrieves API data from server #

    def get_api_info(self):
        str_state = ""
        str_population = ""
        str_currency = ""
        for this_city in self.hash_cities:
            obj_city = self.hash_cities[this_city]
            url = "http://getcitydetails.geobytes.com/GetCityDetails?fqcn=%s" % this_city
            response = requests.get(url)
            if response.ok:
                json_obj = json.loads(response.content)
                str_state = json_obj['geobytescountry']
                str_population = json_obj['geobytespopulation']
                str_currency = json_obj['geobytescurrency']
            obj_city.set_state_name(str_state)
            obj_city.set_state_population(str_population)
            obj_city.set_state_currency(str_currency)
