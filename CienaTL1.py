# CienaTL1.py
''' Module runs TL1 commands on Ciena 6500 devices and parses output'''

# TL1 (Transaction Language 1) is an ancient and mysterious command line syntax
# used to speak directly to telecom devices in "the old tongue". Possibly alien
# in origin, this language is believed to have been used in shadowy druid cults 
# attempting to gain favor with the dark telco underlord. Don't stare at it for
# too long. Weltin 2022.06

# Imported libraries
import telnetlib
import pprint
import re

def login(mgmtIP, username, password):
    """ Login to Ciena 6500 and return node name """

    global telnetServer
    telnetServer = telnetlib.Telnet(mgmtIP, 23, timeout=10)
    telnetServer.write(("ACT-USER::" + username + ":PYTHON::\"" + password + "\";").encode())
    actUserResponse = telnetServer.read_until(b";\r\n<").decode()

    if "PYTHON COMPLD" in actUserResponse:
        print(f"\nConnection successful to {mgmtIP}")
        if actUserResponse.find("ACT-USER:") != -1:
            ACTUSERindex = actUserResponse.find("ACT-USER:")
            usernameIndex = actUserResponse.find(username)
            nodeName = actUserResponse[(ACTUSERindex + 14):usernameIndex - 2]
            print(f"TID identified as {nodeName}")
            return(nodeName)
        else: return("Node name not found")
    else: return("TL1 DENY")
