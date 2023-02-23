# File : test_openweather.py
# API : https://openweathermap.org/current
# info@pcamus.be
# 16/2/2022
# Updated 23/02/2023

# importing the required libraries
import requests # HTTP library
import datetime as dt # to convert UNIX time into something readable
from secrets import *

def round_time (h,m,s):
    # round time to minute
    if s>29 : 
        m=m+1
        if m>59:
            h=h+1
            m=0
    return h,m


# My api key for openweathermap 
api_key = my_secrets["OWM_API_key"]
# Base url for the open map api
root_url = "http://api.openweathermap.org/data/2.5/weather?"
# My location :
lat=my_secrets["lat"]
lon=my_secrets["lon"]

url=root_url+"lat="+lat+"&lon="+lon+"&units=metric"+"&appid="+api_key
r = requests.get(url) # Query openweather in http

# displaying the json weather data returned by the api
dict=r.json()

temp=float((dict["main"]["temp"]))
temp_min=float((dict["main"]["temp_min"]))
temp_max=float((dict["main"]["temp_max"]))
humidity=float((dict["main"]["humidity"]))
pressure=float((dict["main"]["pressure"]))

sun_rise=float((dict["sys"]["sunrise"])) # epoch time  (= Unix notation)
dt_rise=dt.datetime.fromtimestamp(sun_rise) # return datetime object

sun_set=float((dict["sys"]["sunset"])) # epoch time (= Unix notation)
dt_set=dt.datetime.fromtimestamp(sun_set) # return datetime object

print("Current temperature: ",round(temp,1),"°C")
print("Minimum temperature today: ",round(temp_min,1),"°C")
print("Maximum temperature today: ",round(temp_max,1),"°C")
print("Relative humidity: ",round(humidity),"%")
print("Atmospheric pressure:",round(pressure),"hPa")
print()

hr,mr=round_time(dt_rise.hour,dt_rise.minute,dt_rise.second)
print("Sunrise: {:d}h{:02d}".format(hr,mr))

hr,mr=round_time(dt_set.hour,dt_set.minute,dt_set.second)
print("Sunset: {:d}h{:02d}".format(hr,mr))

