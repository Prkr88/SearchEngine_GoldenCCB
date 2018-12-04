import json
import requests
import pickle
import ijson
MILLION = 1000000
THOUSAND = 1000

class API:
    hash_cities = {}

    # constructor #

    def __init__(self):
        self.hash_cities = {}

    # function retrieves API data from server #

    def get_api_info(self):
        str_state = ""
        str_population = ""
        str_currency = ""
        cities_data = {}
        url = "https://raw.githubusercontent.com/apilayer/restcountries/master/src/main/resources/countriesV2.json"
        response = requests.get(url)
        if response.ok:
            json_obj = json.loads(response.content)
            for entry in json_obj:
                if entry['capital'].upper() not in cities_data and entry['capital']!= '' :
                    population = entry['population']
                    if population>MILLION:
                        population = float(population) / MILLION
                        population = str(round(population, 2)) + 'M'
                    else:
                        population = float(population) / THOUSAND
                        population = str(round(population, 2)) + 'K'
                    cities_data[entry['capital'].upper()] = {'Country_Name': entry['name'],
                                                        'Currency': entry['currencies'][0]['code'],
                                                        'Population': population}
        self.hash_cities = cities_data
        with open('cities_data.pkl', 'wb') as output:
            pickle.dump(cities_data, output, pickle.HIGHEST_PROTOCOL)

    def create_world_cities_hash(self):
        cities_of_the_world = {}
        with open('C:\\Users\\Prkr_Xps\\Desktop\\citiesCopy.json') as f:
            json_obj = json.load(f)
        for entry in json_obj:
            cities_of_the_world[entry['name']] = ''
        with open('cities_of_the_world.pkl', 'wb') as output:
            pickle.dump(cities_of_the_world, output, pickle.HIGHEST_PROTOCOL)

    def parse_json(self):
        cities_of_the_world = {}
        with open('C:\\Users\\Prkr_Xps\\Desktop\\cities.json', 'rb') as input_file:
            # load json iteratively
            parser = ijson.parse(input_file)
            for prefix, event, value in parser:
                #print('prefix={}, event={}, value={}'.format(prefix, event, value))
                if prefix == 'item.name':
                    cities_of_the_world[value.upper()] = ''
        with open('cities_of_the_world.pkl', 'wb') as output:
            pickle.dump(cities_of_the_world, output, pickle.HIGHEST_PROTOCOL)

# a ={}
# api = API()
# api.get_api_info()
#api.create_world_cities_hash()
# api.parse_json()