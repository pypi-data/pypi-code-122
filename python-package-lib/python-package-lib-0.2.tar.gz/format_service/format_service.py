import json
from request_service.city_requests import CityRequests
from request_service.country_requests import CountryRequests


class FormatService:
    def __init__(self):
        self.city = CityRequests()
        self.country = CountryRequests()

    def get_all_cities(self):
        json_cities = self.city.get_city()
        json_object = json.loads(json_cities)
        print(json.dumps(json_object, ident=1))

    def get_all_countries(self):
        json_countries = self.country.get_country()
        json_object = json.loads(json_countries)
        print(json.dumps(json_object, ident=1))

