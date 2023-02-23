# File: owm_picow.py
# Demo program to connect to openweathermap.org using a WiFi connection
# on Raspberry Pi Pico W and to retreive and parse data using the openweather API.
# API : https://openweathermap.org/current
# info@pcamus.be
# 23/11/2022

import urequests, network
from secrets import *
import utime

wlan = network.WLAN(network.STA_IF) # Creates a WLAN object and initializes it
wlan.active(True)
wlan.connect(my_secrets["ssid"],my_secrets["WiFi_pass"])

print("Connection to WiFi network.")
print("---------------------------")
print("Trying to connect to WiFi...")
print()

# Waits for connection or exit with error code if it fails
retry = 10
while (retry > 0):
    wlan_stat=wlan.status()
    if wlan_stat==3:
        print("Got IP")
        break
    if wlan_stat==-1:
        raise RuntimeError('WiFi connection failed')
    if wlan_stat==-2:
        raise RuntimeError('No AP found')    
    if wlan_stat==-3:
        raise RuntimeError('Wrong WiFi password')
    
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    retry = retry-1
    utime.sleep(1)

if wlan_stat!=3:
    raise RuntimeError('WiFi connection failed')


print()
print('Connected to WiFi network: ',end="")
print(wlan.config("ssid"))
print()
ip=wlan.ifconfig()
print("IP info (IP address, mask, gateway, DNS):")
print(ip)
print()

# Now we can use the connection to access openweathermap.

# Base url for the openweathermap API
root_url = "http://api.openweathermap.org/data/2.5/weather?"

url=root_url+"lat="+my_secrets["lat"]+"&lon="+my_secrets["lon"]+"&appid="+my_secrets["OWM_API_key"]
r = urequests.get(url) # Query openweather in http

# Parsing and displaying some weather data returned by the API (in json format)
dict=r.json() # convert json data into a dictionnary

temp=float((dict["main"]["temp"]))
temp_min=float((dict["main"]["temp_min"]))
temp_max=float((dict["main"]["temp_max"]))
humidity=float((dict["main"]["humidity"]))
pressure=float((dict["main"]["pressure"]))

print("Weather forecast from openweathermap.org")
print("----------------------------------------")
print("Location:",dict["name"])
print("Type of weather: ",dict["weather"][0]["main"])
print("Current temperature: ",round(temp-273.15,1),"°C")
print("Minimum temperature today: ",round(temp_min-273.15,1),"°C")
print("Miaximum temperature today: ",round(temp_max-273.15,1),"°C")
print("Relative humidity: ",round(humidity),"%")
print("Atmospheric pressure: ",round(pressure),"hPa")

