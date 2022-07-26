# File : test_openweather.py
# API : https://openweathermap.org/current
# info@pcamus.be
# 16/2/2022

# importing the required libraries
import requests # HTTP library
import datetime as dt # to convert UNIX time into something readable

def round_time (h,m,s):
    # round time to minute
    if s>29 : 
        m=m+1
        if m>59:
            h=h+1
            m=0
    return h,m


# My api key for openweathermap 
api_key = "-- your API key --"
# Base url for the open map api
root_url = "http://api.openweathermap.org/data/2.5/weather?"
# My location :
lat="50.3813"
lon="5.7324"

url=root_url+"lat="+lat+"&lon="+lon+"&appid="+api_key
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

print("Température actuelle : ",round(temp-273.15,1),"°C")
print("Température minimum : ",round(temp_min-273.15,1),"°C")
print("Température maximum : ",round(temp_max-273.15,1),"°C")
print("Humidité relative : ",round(humidity),"%")
print("Pression atmosphérique : ",round(pressure),"hPa")
print()

hr,mr=round_time(dt_rise.hour,dt_rise.minute,dt_rise.second)
print("Lever du soleil :",hr,"h",mr)

hr,mr=round_time(dt_set.hour,dt_set.minute,dt_set.second)
print("Coucher du soleil :",hr,"h",mr)


