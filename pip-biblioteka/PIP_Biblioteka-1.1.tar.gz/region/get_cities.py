# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests


class City:

    def get_all(self, country, region):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/" + country + "/regions/" + region + "/cities"

        headers = {
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            "X-RapidAPI-Key": "518d945c7cmsh3f642083888a0b3p1a57e2jsn1512eef47ab2"
        }

        response = requests.request("GET", url, headers=headers)
        return response

    def get_info(self, id):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/" + id

        headers = {
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            "X-RapidAPI-Key": "518d945c7cmsh3f642083888a0b3p1a57e2jsn1512eef47ab2"
        }

        response = requests.request("GET", url, headers=headers)

        return response

    def get_time(self, id):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/" + id + "/time"

        headers = {
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            "X-RapidAPI-Key": "518d945c7cmsh3f642083888a0b3p1a57e2jsn1512eef47ab2"
        }

        response = requests.request("GET", url, headers=headers)

        return response

    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(City.get_info("Q60").json())

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
