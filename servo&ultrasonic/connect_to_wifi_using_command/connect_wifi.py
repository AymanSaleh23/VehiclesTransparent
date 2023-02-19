import os 


#connect to wifi using CLI write data on configuration file and reconfigure wifi
essid = "Engineering"
password =  "AaSsDdFf2022@#"
def connect_wifi(essid = "Engineering", password ="AaSsDdFf2022@#"):
	#os.system("sudo rfkill block wifi")
	#open wifi
	os.system("sudo rfkill unblock wifi")
	#write in cofigration data on temp file
	os.system('''sudo echo 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=EG\n
network={
\tssid='''+'"'+essid+'"'+'''
\tpsk='''+'"'+password+'"'+'''
\tkey_mgmt=WPA-PSK
}' > wpa_supplicant.conf ''')
	#copy temp file to correct path
	os.system("sudo cp wpa_supplicant.conf /etc/wpa_supplicant/")
	#reconfigure wifi to read new configuration
	os.system("wpa_cli -i wlan0 reconfigure")

	
connect_wifi(essid,password)
