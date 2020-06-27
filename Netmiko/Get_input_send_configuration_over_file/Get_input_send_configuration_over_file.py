import pandas as pd
from netmiko import ConnectHandler
from netmiko import Netmiko
import time

get_input = input("Please provide ip_address or hostname: ")

if (get_input == ""):
    print("Empty input. Please enter again.")
found = False

user_input = str(get_input)

print ("This is the IP/hostname you have entered - ", user_input)
input_db = read_db.parse(0)
search_ip = input_db.loc[(input_db["Host_Name"] == user_input) | (input_db["Mgt_IP_Address"] == user_input), "Mgt_IP_Address"]
out_ip = search_ip.to_string(index=False)
ip = out_ip

Devices = {
    	'device_type': 'cisco_ios',
    	'host': ip,             
    	'username': 'cisco',
    	'password': 'cisco',
    	'port' : 22,          
    	'secret': '',        
        'auth_timeout' : 20
}

net_connect = Netmiko(**Devices)
time.sleep(20)
cfg_file = "configfile.txt"
print()
print(net_connect.find_prompt())
output = net_connect.enable()
output = net_connect.send_config_from_file(cfg_file) 
print(output)
print()

net_connect.save_config()
net_connect.disconnect() 
