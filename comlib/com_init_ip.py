"""
Created on Tue Oct 18 18:55:17 2022
Updated on Tue Dec 2   1:00:00 2022
"""
""" Import all Essintial Packages   """
import subprocess, re, os

"""  Create class named scanIP  """
class scanIP:
    """ Class Constructor with arguments nameAP, SSID, Password """
    def __init__(self, nameAP='Almosalamy', ssid='Almosalamy', password='Alm0salamy2000'):
        
        print("scanIP object is created...")
        
        """ run the feature """
        self.__call__(nameAP, ssid, password)
        
    
    """ Function to establish a new connection  """
    def create_new_connection(self,nameAP='Almosalamy', ssid='Almosalamy', password='Alm0salamy2000'):
        print ("Creating Access Point Connection", nameAP, ssid, password, sep="\t")
        config = """
        <?xml version=\"1.0\"?>
            <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                <name>"""+nameAP+"""</name>
                <SSIDConfig>
                    <SSID>
                        <name>"""+nameAP+"""</name>
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
        command = "netsh wlan add profile filename=\""+nameAP+".xml\""+" interface=Wi-Fi"
        with open(nameAP+".xml", 'w') as file:
            file.write(config)
        os.system(command)
        print (command)

    """ Function to connect to a network   """
    def connect(self,name, ssid):
        command = "netsh wlan connect name=\""+name+"\" ssid=\""+ssid+"\" interface=Wi-Fi"
        os.system(command)
        print (command)
     
    """ Dunder function to enable object to be callable """
    def __call__(self,nameAP, ssid, password):
        self.create_new_connection(nameAP, ssid, password)
        print ("Connection Created Succssfully...")
        self.connect(nameAP, ssid)
        print ("Connection Established...")
        print ("Done")
    
    """ Function to get the IP, Network """
    def get_host (self,x):
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
    def check_ips(self,start_ip,end_ip):
        empty_string = ""
        counter = 0
        Network, First_Host = self.get_host(start_ip)
        Network, Last_Host = self.get_host(end_ip)
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
s = scanIP("Almosalamy","Almosalamy","Alm0salamy2000")
found = s.check_ips(start_ip="192.168.1.9",end_ip="192.168.1.13")
print ("available IPs:",found)
