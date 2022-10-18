# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 18:55:17 2022

@author: as292
"""
transIP = 2
import subprocess, re
# import module
import os


AP_name = "TEdata3CCB39"
AP_pass = "29902026"


# function to establish a new connection
def createNewConnection(name, SSID, password):
    print ("Creating Access Point Connection", name, SSID, password, sep="\t")
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+AP_name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+AP_name+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+AP_pass+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
    with open(name+".xml", 'w') as file:
        file.write(config)
    os.system(command)
    print (command)
 
# function to connect to a network   
def connect(name, SSID):
    command = "netsh wlan connect name=\""+AP_name+"\" ssid=\""+AP_name+"\" interface=Wi-Fi"
    os.system(command)
    print (command)
 
    
createNewConnection(AP_name,AP_name,AP_pass)

connect(AP_name,AP_pass)

def Get_Host (x):
    Dot_counter = 0
    Pos_counter = 0
    
    for i in x:
        if i == '.':
            Dot_counter+= 1
            
        if Dot_counter == 3:
            return (x[0:Pos_counter+1], x[Pos_counter+1:])
            break
        Pos_counter+=1
        
Network, First_Host = Get_Host("192.168.1.2")
Network, Last_Host = Get_Host("192.168.1.6")


empty_string = ""
counter = 0

for i in range( int(First_Host), int(Last_Host )+1):
    process = subprocess.getoutput("ping -n 1 "+Network+str(i))
    empty_string += process
    string_needed = re.compile(r"TTL=")
    mo = string_needed.search(empty_string)
    
    try :
        if mo.group()== "TTL=":
            print(str(Network+str(i))+"\tHost found")
    except :
            print("\t\t\tHost not found")
        
    empty_string=""

print ("Done")
            