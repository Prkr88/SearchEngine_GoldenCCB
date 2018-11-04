import json
import urllib
import urllib.parse
import requests
import optparse
import sys
from flask import Response, json, request


class CityObject:

    # static counter for the pointers to the IF

    def s_count(self):  # pointer to the inverted file
        global count
        self.count += 1
        return self.count

    count = 0

    # constructor #

    def __init__(self, doc_id, city_name):
        self.get_api_info(city_name)
        self.list_docs = [doc_id]
        self.doc_pos = ""
        self.pIF = self.s_count()

    # function retrieves API data from server #

    def get_api_info(self, city_name):
        str_state = ""
        str_population = ""
        str_currency = ""
        url = "http://getcitydetails.geobytes.com/GetCityDetails?fqcn=%s" % city_name
        response = requests.get(url)
        if response.ok:
            json_obj = json.loads(response.content)
            str_state = json_obj['geobytescountry']
            str_population = json_obj['geobytespopulation']
            str_currency = json_obj['geobytescurrency']
        self.city_name = city_name
        self.state_name = str_state
        self.population = str_population
        self.currency = str_currency

    def __hash__(self):
        return hash(self.city_name)

    def __eq__(self, other):
        return other == self.city_name

    def __ne__(self, other):
        return other != self.city_name

    def get_doc(self, doc_id):
        self.list_docs.__contains__(doc_id)

    def get_city_name(self):
        return self.city_name

    def get_state_name(self):
        return self.state_name
