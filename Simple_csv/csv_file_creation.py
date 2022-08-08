# File : csv_file_creation.py
# write numerical data in csv formatted file
# and check remaining space in flash.
# uos doc : https://makeblock-micropython-api.readthedocs.io/en/latest/library/uos.html
# info@pcamus.be
# 6/8/2022

import uos

test_val=[[25.2,1010],[25.5, 1010],[25.1, 1011],[25.3,1010],[25.5, 1010]]

filename = "csv_test.csv"

f = open(filename, "w") # "w" overwrire file, "a" append to file

f.write("Temperature;Pressure\r\n") # header

for row in test_val :
    buffer="%2.1f;%4d\r\n"%(row[0],row[1])
    f.write(buffer)

f.close()

fsys_info = uos.statvfs('/')
freeSize=fsys_info[3] # number of remaining free blocks after adding data
                        # for Raspberry Pi Pico a block is 4096 bytes
print("Number of free blocks", freeSize)

