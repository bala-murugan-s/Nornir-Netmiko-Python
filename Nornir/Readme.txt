This folder consists of scripts based on Nornir/Netmiko

Inventory folder - Consists of regular nornir inventory files 

    hosts.yaml - Devices Information
    groups.yaml - Devices group based on vendor/device type
    defaults.yaml - Login credentials
    
    Credentials can be placed in any of the file. But Hosts.yaml takes the highest precedence over Groups.yaml which takes precedence over defaults.yaml.
    
 TextFSM folder - Consists of custom templates created to parse using TextFSM module
 
 #1 - nornir_cisco_wlc_show_ap_summary_using_textfsm
      To get the output of "show ap summary" from cisco wlc >>> parse the output using textfsm >>> write the output in CSV file
      nornir cisco wlc show ap summary using textfsm
 
