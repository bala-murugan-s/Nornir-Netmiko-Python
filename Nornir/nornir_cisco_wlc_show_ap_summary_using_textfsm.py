#------------------------------[nornir_cisco_wlc_show_ap_summary_using_textfsm]-------------------------------#
"""
:DESCRIPTION:
	To get the output of "show ap summary" from cisco wlc >>> parse the output using textfsm >>> write the output in CSV file
:REQUIREMENTS:
	Python3
	Netmiko
    Nornir
    TextFSM
    CSV
    
:INPUTS:
	Regular Nornir files hosts.yaml / groups.yaml / defaults.yaml
	
	10.10.10.10
	10.10.10.11
	
    After executing command via netmiko, output as like below
    AP Name              Ethernet MAC       AP Up Time               Association Up Time
    ------------------   -----------------  -----------------------  -----------------------
    Cisco_AP01     f4:db:e6:11:11:11  10 days, 00 h 27 m 12 s   10 days, 00 h 24 m 39 s
    Cisco_AP02     f4:db:e6:22:22:22  10 days, 00 h 27 m 14 s   10 days, 00 h 24 m 27 s
    Cisco_AP03     f4:db:e6:24:24:24  10 days, 00 h 27 m 10 s   10 days, 00 h 24 m 27 s
    Cisco_AP04     f4:db:e6:44:44:44  10 days, 00 h 27 m 08 s   10 days, 00 h 24 m 32 s
	
    Parse this output with the custom template created in sh_ap_uptime.txt (TextFSM format)
    
       
	
:OUTPUT:
    Following output is the sample output of csv file 
	['AP_NAME', 'ETH_MAC', 'AP_UP_TIME', 'ASSO_UP_TIME']
    ['Cisco_AP01', 'f4:db:e6:11:11:11', '10 days, 00 h 27 m 12 s', '10 days, 00 h 24 m 39 s']
    ['Cisco_AP02', 'f4:db:e6:22:22:22', '10 days, 00 h 27 m 14 s', '10 days, 00 h 24 m 27 s']
    ['Cisco_AP03', 'f4:db:e6:24:24:24', '10 days, 00 h 27 m 10 s', '10 days, 00 h 24 m 27 s']
    ['Cisco_AP04', 'f4:db:e6:44:44:44', '10 days, 00 h 27 m 08 s', '10 days, 00 h 24 m 32 s']

:DRAWBACKS:
	- maybe sometime require to make modification in output csv file.
    - anyother let me know
	
:NOTES:
  Version:        1.0
  Author:         wol-verine
  Creation Date:  SEP-2020
  Purpose/Change: Initial script development

:INSPIRATION:  
    Henry Ölsner - https://github.com/hoelsner
"""
#---------------------------------------------[Code Starts]------------------------------------------------------#

from nornir import InitNornir
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config
from nornir.plugins.tasks import commands
from nornir.plugins.tasks import networking
import time
import csv
import textfsm

def ap_sum_test(ap_task_1):
   # Using Netmiko execute the show ap uptime in cisco wlc
   wlc_ap_sum = ap_task_1.run(task=netmiko_send_command, command_string = "show ap uptime")
   # Assign the output to input_to_parse
   input_to_parse = wlc_ap_sum.result
   # Remove the first 3 lines in the output which shows no. of AP counts.
   data_to_parse = input_to_parse.split("\n",3)[3];
   
   # Open the TextFSM formatted custom template saved under sh_ap_uptime.txt
   
   with open("sh_ap_uptime.txt", 'r') as f:
        template = textfsm.TextFSM(f)
   
   # Parse the command output (data_to_parse) with the custom template
   fsm_results = template.ParseText(data_to_parse)
        
   # Create a CSV file
   outfile_name = open("ap_outfile.csv", "w+")
   
   # Map the CSV file to outfile
   outfile = outfile_name

   # Display result as CSV and write it to the output file
   # First the column headers...
   print(template.header)
   for s in template.header:
       outfile.write("%s;" % s)
   outfile.write("\n")

    # ...now all row's which were parsed by TextFSM
   counter = 0
   for row in fsm_results:
       print(row)
       for s in row:
           outfile.write("%s;" % s)
       outfile.write("\n")
       counter += 1
   print("Write %d records" % counter)
  
      

def main():
    # initialize The Norn
    nr = InitNornir(config_file="config.yaml")
    # filter The required device from the nornir input file
    single_host = nr.filter(hostname='10.10.10.10')
    # Execute the tasks in single host
    results = single_host.run(task=ap_sum_test)
    

if __name__ == "__main__":
    main()
    
#---------------------------------------------[Code Ends]------------------------------------------------------#    
