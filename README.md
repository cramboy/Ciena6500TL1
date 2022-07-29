# Ciena6500TL1
 '' Module runs TL1 RTRV commands on Ciena 6500 devices and parses output'''

# This module is intended to be used as an import to a 'Main' module, used to 
# execute TL1 RTRV commands (specifically) on Ciena 6500 DWDM devices 
# configured in a ROADM or FOADM network. At this time, this module is ONLY
# to retrieve information - no SET, DLT, ED, ENT, or other system editing 
# commands are used.

# TL1 RTRV commands are executed, the output is cleaned-up, parsed and returned
# to Main as either a list, a dictionary, or a list of dictionaries (depending
# on the command).

# This module itself imports:
# - telnetlib
# - re
# - pprint (but only for troubleshooting)
