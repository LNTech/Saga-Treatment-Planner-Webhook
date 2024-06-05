# main.py
"""Gets Civil Twilight time from coordinates"""
import json
import requests
from requests.auth import HTTPBasicAuth
from geopy.geocoders import Nominatim
from astral import CivilTwilight
from webhook import Embed

civil_twilight = CivilTwilight()
geolactor = Nominatim(user_agent = "Civil Twilight Locator")


def read_config():
    """ Reads JSON file for various config values """
    with open("config.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    return data['username'], data['password'], data['webhooks'], data['url']

def get_country(latittude : str, longitude : str):
    """ Gets country from coordinates """
    location = geolactor.reverse(latittude + "," + longitude, language='en')#
    return location.raw['address']['country']


def read_json(username : str, password : str, url : str):
    """ Read JSON from URL """
    auth = HTTPBasicAuth(username, password)
    response = requests.get(url + "/start-time/data" , auth=auth)
    data = response.json()
    return data


def parse_json(data : list):
    """ Parses JSON file and gets start time"""
    location_data = {}
    for location in data:
        lattitude = str(location['lat'])
        longitude = str(location['lng'])

        country = get_country(lattitude, longitude)
        times = civil_twilight.calculate(lattitude, longitude)

        if country not in location_data:
            location_data[country] = {}
        if location['site'] not in location_data[country]:
            location_data[country][location['site']] = []

        location_data[country][location['site']].append({
            "times": times
        })

    return location_data


def main():
    """ Main function handler """
    print("Fetching configuration data")
    username, password, webhooks, url = read_config()

    print("Fetching location data (this might take a minute)")
    data = read_json(username, password, url)
    location_data = parse_json(data)

    print("Initializing webhooks")
    webhook = Embed(
        treatment=webhooks['treatment_start_time'],
        companion=webhooks['companion_start_time']
    )

    print("Sending information to Discord")
    for country in location_data:
        webhook.send_times(location_data[country], country) # Send the embed object


if __name__ == "__main__":
    main()
