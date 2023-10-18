import pytz
from geopy.geocoders import Nominatim
from datetime import datetime


print(type(datetime.today()))
#
# def get_time(location_input=""):
#     # Use geopy to get the latitude and longitude of the location
#
#     tzfinder = TimezoneFinder()
#     geolocator = Nominatim(user_agent=tzfinder)
#     location = geolocator.geocode(location_input)
#     latitude = location.latitude
#     longitude = location.longitude
#
#     # Use geopy to get the location information (including country code) based on the latitude and longitude
#     location_info = geolocator.reverse((latitude, longitude), exactly_one=True, zoom=12)
#
#     # Use pytz to get the timezone for the location
#     country_code = location_info.raw['address']['country_code']
#     timezone = pytz.timezone(pytz.country_timezones.get(country_code, [])[0])
#
#     # Get the current time in the timezone of the location
#     now = datetime.now(timezone)
#
#     print("Current time in {}: {}".format(location.address, now.strftime("%I:%M %p, %m-%d-%Y")))
#
# get_time("germany")
# print(type(*args))