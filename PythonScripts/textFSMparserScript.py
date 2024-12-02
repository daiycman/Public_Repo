##########################################################################################################################
# Script Name: FSM parser
# Author: Joe Smith
# Date: 2022-07-06
# Description: This script utilizes the text FSM parser to parse various information from a template and a data file
#              This script is showing parsing a startup config file from an ASA and using the Template to parse for the ASA
#              Tunnel groups.
##########################################################################################################################

import csv
import textfsm 

"""
Link out to directory full of TextFSM templates for a variety of platforms:
https://github.com/networktocode/ntc-templates/tree/master/ntc_templates/templates
"""
 
template = r"cisco_asa_show_running-config_tunnel-group.textfsm"
datafile = r"startup-config.txt"
outputfile = r"tunnelgroup-output.csv"
 
# Parse output from show command
with open(template, 'r') as template_file, open(datafile, 'r') as data_file:
    re_table = textfsm.TextFSM(template_file)
    header = re_table.header
    result = re_table.ParseText(data_file.read())

# Display result as CSV
with open(outputfile, 'w', newline='\n') as file_out:
    writer = csv.writer(file_out)
    headerline = [",".join(header)]
    resultlines = [",".join(str(line)) for line in result]
    data_out = [header] + result
    writer.writerows(data_out)