# File : ow_pico_ESP8266.py
# API : https://openweathermap.org/current
# Add a try... except to overcome the problem of incorrect http answer
# info@pcamus.be
# 5/4/2022

from machine import UART, Pin
from esp8266 import ESP8266
import time, sys,json

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("RPi-Pico MicroPython Ver:", sys.version)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

## Create On-board Led objects
ledN=Pin(12,Pin.OUT)
ledE=Pin(13,Pin.OUT)
ledS=Pin(14,Pin.OUT)
ledW=Pin(15,Pin.OUT)
for led in [ledN, ledE, ledS, ledW]:
        led.low()

def set_wind_led(wd):
    for led in [ledN, ledE, ledS, ledW]:
        led.low()
    if wd>=315 or wd<45 :
        ledN.high()
    elif wd>=45 and wd<135 :
        ledE.high()
    elif wd>=135 and wd<225 :
        ledS.high()
    elif wd>=225 and wd<315 :
        ledW.high()

# Create an ESP8266 Object
esp01 = ESP8266(uartPort=1 ,baudRate=115200, txPin=(4), rxPin=(5))
esp8266_at_ver = None

print("StartUP",esp01.startUP())
print("Echo-Off",esp01.echoING())
print("")


#Print ESP8266 AT comand version and SDK details
esp8266_at_ver = esp01.getVersion()
if(esp8266_at_ver != None):
    print(esp8266_at_ver)
print()
# set the current WiFi in SoftAP+STA
esp01.setCurrentWiFiMode()

#Connect with the WiFi
print("Try to connect with the WiFi..")
while (1):
    if "WIFI CONNECTED" in esp01.connectWiFi("-- your WiFi SSID --","-- your WiFi password--"):
        print("ESP8266 connected with the WiFi..")
        break;
    else:
        print(".")
        time.sleep(2)

print()
print("HTTP Get Operation.......\r\n")

# My api key for openweathermap 
api_key = "-- your API key --"
# Base url for the open map api
host = "api.openweathermap.org"
# My location (Chevron Belgium):
lat="50.3813"
lon="5.7324"

url_path="/data/2.5/weather?"+"lat="+lat+"&lon="+lon+"&appid="+api_key

#Test server
#host="www.httpbin.org"
#url_path="/anything"

http_success=False

while http_success==False:
    try:
        #HTTP Get Operation with host, path on host = url_path 
        httpCode, httpRes = esp01.doHttpGet(host,url_path,"RaspberryPi-Pico", port=80)
        print("-------------  Get Result -----------------------")
        print("HTTP Code:",httpCode) # 200 = success
        print("HTTP Response:",httpRes)
        print("-------------------------------------------------\r\n\r\n")

        owdict=json.loads(httpRes[:len(httpRes)-2]) # skip some unwanted char
        winddir=((owdict["wind"]["deg"]))

        print("Direction du vent : ",winddir,"°")
        set_wind_led(winddir)
        http_success=True
    except:
        pass

    
