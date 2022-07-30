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
    """ 
    Login to Ciena 6500 and return node name 
    """

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

    
def shelfNumbs(nodeName):
    """
    Returns a list of the shelves in the TID using the form:
    [[SHELF-n, {shelfInfo}], [SHELF-n, {shelfInfo}], ...]

    Where "n" is the shelf number

    Each {shelfInfo} is a dictionary containing shelf attributes. The exact 
    contents of the shelf dictionary may vary depending on software load.

    """
    telnetServer.write(("RTRV-SHELF::ALL:PYTHON;").encode())
    commandResponse = telnetServer.read_until(b";\r\n<").decode()
    commandResponse = commandResponse.splitlines()

    # Remove garbage from string
    commandResponse = [item for item in commandResponse if "PYTHON COMPLD" not in item]
    commandResponse = [item for item in commandResponse if ">" not in item]
    commandResponse = [item for item in commandResponse if nodeName not in item]
    commandResponse = [item for item in commandResponse if len(item) > 2]

    shelfList = []
    for index, item in enumerate(commandResponse):
        if item.find("SHELF-") > 0:
            start = item.find("SHELF-")
            end = item.find("::")
            shelf = item[start:end]
            shelfList.append(shelf)
    # print(shelfList)

    # remove the "SHELF" name from the list including "::"
    for index, item in enumerate(commandResponse):
        newStartIndex = item.find("::") + 2
        item = item.replace(item[:newStartIndex], "")
        commandResponse.pop(index)
        commandResponse.insert(index, item)
    # print(commandResponse)

    # remove remaining garbage characters from string
    for index, item in enumerate(commandResponse):
        item = item.replace('\\', '')
        commandResponse.pop(index)
        commandResponse.insert(index, item)
    # print(commandResponse)

    # convert commandResponse to dictionary and add to list
    shelfDictionaryList = []
    for index, item in enumerate(commandResponse):
            dictionary = dict(subString.split("=") for subString in item.split(","))
            shelfDictionaryList.append(dictionary)
    # pprint.pprint(shelfDictionaryList)

    # create the final interface list
    FinalShelfList = []
    for index, item in enumerate(shelfList):
        shelfDictionary = shelfDictionaryList[index]
        FinalShelfList.append([item, shelfDictionary])
    # pprint.pprint(FinalShelfList)

    return(FinalShelfList)
