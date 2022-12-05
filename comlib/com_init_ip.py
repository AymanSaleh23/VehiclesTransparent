
"""
Created on Tue Oct 18 18:55:17 2022
Updated on Tue Dec 2   1:00:00 2022
"""
""" Import all Essintial Packages   """
import subprocess, re, os

"""  Create class named scanIP  """
class init_com:
    """ Class Constructor with arguments nameAP, SSID, Password """
    
    
    """ Function to establish a new connection  """
    @staticmethod
    def create_new_connection(ssid='Almosalamy', password='Alm0salamy2000', machine= 'windows'):
        if machine == 'windows':
            command = "netsh wlan connect name=\""+ssid+"\" ssid=\""+ssid+"\" interface=Wi-Fi"
            os.system(command)
            print (command)
            print ("Creating Access Point Connection", ssid, password, sep="\t")
            config = """
            <?xml version=\"1.0\"?>
                <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                    <name>"""+ssid+"""</name>
                    <SSIDConfig>
                        <SSID>
                            <name>"""+ssid+"""</name>
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
                                <keyMaterial>"""+password+"""</keyMaterial>
                            </sharedKey>
                        </security>
                    </MSM>
                    </WLANProfile>"""
            command = "netsh wlan add profile filename=\""+ssid+".xml\""+" interface=Wi-Fi"
            os.system(command)
            print (command)
        elif machine == 'linux':
        	#os.system("sudo rfkill block wifi")
        	#open wifi
        	os.system("sudo rfkill unblock wifi")
        	#write in cofigration data on temp file
        	os.system('''sudo echo 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        country=EG\n
        network={
        \tssid='''+'"'+ssid+'"'+'''
        \tpsk='''+'"'+password+'"'+'''
        \tkey_mgmt=WPA-PSK
        }' > wpa_supplicant.conf ''')
        	#copy temp file to correct path
        	os.system("sudo cp wpa_supplicant.conf /etc/wpa_supplicant/")
        	#reconfigure wifi to read new configuration
        	os.system("wpa_cli -i wlan0 reconfigure")



     
    """ Dunder function to enable object to be callable """
    @staticmethod
    def __call__( ssid, password, machine = "linux"):
        init_com.create_new_connection(ssid, password, machine )
        
    
    """ Function to get the IP, Network """
    @staticmethod
    def get_host(x):
        Dot_counter = 0
        Pos_counter = 0
        
        for i in x:
            if i == '.':
                Dot_counter+= 1
                
            if Dot_counter == 3:
                return (x[0:Pos_counter+1], x[Pos_counter+1:])
                break
            Pos_counter+=1
 
    """ Function to get all available Hosts in the LAN  """
    @staticmethod
    def check_ips(start_ip,end_ip):
        empty_string = ""
        counter = 0
        Network, First_Host = init_com.get_host(start_ip)
        Network, Last_Host = init_com.get_host(end_ip)
        found = []
        for i in range( int(First_Host), int(Last_Host )+1):
            process = subprocess.getoutput("ping -n 1 "+Network+str(i))
            empty_string += process
            string_needed = re.compile(r"TTL=")
            mo = string_needed.search(empty_string)
            
            try :
                if mo.group()== "TTL=":
                    print(str(Network+str(i))+"\tHost found")
                    found.append(str(Network+str(i)))
            except :
                    print(str(Network+str(i))+"\t\tHost not found")
                
            empty_string=""
        return found

""" Only for test using windows """

init_com.create_new_connection(machine='windows')
init_com.check_ips('192.168.1.3', '192.168.1.21')
found = init_com.check_ips(start_ip="192.168.1.9",end_ip="192.168.1.13")
print ("available IPs:",found)

