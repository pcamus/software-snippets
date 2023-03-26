# File: ntp_access.py
# Get time from NTP server
# See https://docs.micropython.org/en/latest/library/network.WLAN.html for WiFi connection
# See https://docs.micropython.org/en/latest/library/socket.html for socket usage
# See https://docs.python.org/3/library/struct.html for structure management
# info@pcamus.be
# 26/3/2023

import network, socket
import struct
from secrets import *
import utime

# Offset = shift from UTC time in sec 7200 = 2h (UTC + 1 + DST)
# DTS = 1 hour whenthis program was written.
# To be correct Daylight Saving Time (DST) should be taken into account automatically

# delta is the seconds difference between 1.1.1970 and 1.1.1900
# It is related to the way datetime is coded in NTP and
# the way the UNIX date used in Python is coded
def get_time(offset=7200, delta=2208988800, host="pool.ntp.org"):
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B # version 3 mode 3
    
    # Server name resolution
    addr = socket.getaddrinfo(host, 123)[0][-1] # 123 is the port number for NTP
    # the getaddrinfo() returns the IP address of the host and other info
    # in the form of a list of 5 tuples, the last tuple [-1] containing
    # a tuple with IP address as a string and port number as an integer
    
    # Creates a socket (= a connection to a service) on the NTP server
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP/IP
    
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr) # Sends query to FTP server (an empty packet
                                        # with field LI, VN & MODE specifications
        msg = s.recv(48) # Gets answer
    finally:
        s.close() # Closes the socket connection
    
    val = struct.unpack("!I", msg[40:44])[0] # extracts integer data, big endian coded
    # msg[40:44] contains the integer part of the transmit time stamp.
    # for details see https://labs.apnic.net/index.php/2014/03/10/protocol-basics-the-network-time-protocol/
    t = val - delta # converts from NTP time format to Python (Unix) type   
    tm = utime.gmtime(t+offset) # adds offset according your timezone
    return tm  # year month, day, hour, minute, second, weekday (0-6), yearday)


#WiFi connection
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

# Now we can use the connection to access Internet.

t_now=get_time() # Uses NTP protocol to gate date and time
print("Time is: {:2d}:{:02d}:{:02d}".format(t_now[3],t_now[4],t_now[5]))
# To initialize Pico RTC :
# machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

# Close connection
wlan.disconnect()