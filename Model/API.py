import json
import requests
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
                if entry['capital'] not in cities_data and entry['capital']!= '' :
                    population = entry['population']
                    if population>MILLION:
                        population = float(population) / MILLION
                        population = str(round(population, 2)) + 'M'
                    else:
                        population = float(population) / THOUSAND
                        population = str(round(population, 2)) + 'K'
                    cities_data[entry['capital']] = {'Country_Name': entry['name'],
                                                        'Currency': entry['currencies'][0]['code'],
                                                        'Population': population}
        self.hash_cities = cities_data
        # with open('cities_data.pkl', 'wb') as output:
        #     pickle.dump(cities_data,output ,pickle.HIGHEST_PROTOCOL)

# a ={}
# api = API()
# api.get_api_info()