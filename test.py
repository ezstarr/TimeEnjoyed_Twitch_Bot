import pytz
import datetime

tzs = pytz.all_timezones

countries = pytz.country_timezones

for t in tzs:
    print(t)

print("===")

