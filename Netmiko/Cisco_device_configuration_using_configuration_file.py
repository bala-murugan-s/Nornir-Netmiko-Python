#------------------------------[Cisco_device_configuration_using_configuration_file]-------------------------------#
"""
:DESCRIPTION:
	Configure switch / router one  by one using the configuration file

:REQUIREMENTS:
	Python3
	Netmiko

:INPUTS:
	input_file.txt >>> enter the IP address of the Cisco Router/Switch
	sample input_file.txt
	
	10.10.10.1
	10.10.20.1
	10.10.30.1
	
	configfile.txt >> enter your configuration and save the file in same location where script file executes
	
	no ip http
	no ip http secure server

:OUTPUT:
	Cisco_Switch#
	config_term
	config term
	Enter configuration commands, one per line.  End with CNTL/Z.
	Cisco_Switch(config)#no ip http server
	Cisco_Switch(config)#no ip http secure-server
	Cisco_Switch(config)#
	Cisco_Switch(config)#end
	Cisco_Switch#

:DRAWBACKS:
	banner commands have some issues
	single line commands works
	

:NOTES:
  Version:        1.0
  Author:         bala-murugan-s
  Creation Date:  Jun-2020
  Purpose/Change: Initial script development	

"""
#---------------------------------------------[Code Starts]------------------------------------------------------#
from netmiko import Netmiko
import time

with open('input_file.txt', 'r') as in_file:
    inp_file = in_file.readlines()

for ip in inp_file:
        
    Devices = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': 'sivarab',
            'password': 'Zebra*123',
            'port' : 22,          # optional, defaults to 22
            'secret': '',        # optional, defaults to ''
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
	
#---------------------------------------------[Code Ends]------------------------------------------------------#
