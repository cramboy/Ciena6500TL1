# Ciena6500TL1
 '' Module runs TL1 RTRV commands on Ciena 6500 devices and parses output'''

# TL1 (Transaction Language 1)
# TL1 (Transaction Language 1) is an ancient and mysterious command line syntax
# used to speak directly to telecom devices in "the old tongue". Possibly alien
# in origin, this language is believed to have been used in shadowy druid cults
# attempting to gain favor with the dark telco underlord. Don't stare at it for
# too long. Cramboy 2022
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

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

# All functions are tested on Ciena 6500 REL10.00, REL11.20, and REL12.60
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# PROJECT GOAL
# This project is being designed to have 3 phases
# 1) Create a module with prebuilt functions to expedite the creation of 
#    customized scripts/programs. 
# 2) Create a number of programs that utlize combinations of these functions
#    to pull network wide information not easily obtainable from Site
#    Manager or MPC.
# 3) Create a number of Excel Workbooks to be used for output where data can
#    be further scrutinized through pivot tables, filtering, or output for 
#    reports.
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
P.S. Excuse me if my format is poor, this is my first experience with GIT
