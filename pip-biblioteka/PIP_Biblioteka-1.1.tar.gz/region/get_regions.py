# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests


class Region:

    def get_all(self, id):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/" + id + "/regions"

        headers = {
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            "X-RapidAPI-Key": "518d945c7cmsh3f642083888a0b3p1a57e2jsn1512eef47ab2"
        }

        response = requests.request("GET", url, headers=headers)
        return response

    def get_info(self, country, id):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/" + country + "/regions/" + id

        headers = {
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            "X-RapidAPI-Key": "518d945c7cmsh3f642083888a0b3p1a57e2jsn1512eef47ab2"
        }

        response = requests.request("GET", url, headers=headers)

        return response

    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(Region.get_info("PL", "WP").json())

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
