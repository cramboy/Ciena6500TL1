# CienaTL1.py
''' Module runs TL1 commands on Ciena 6500 devices and parses output'''

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
    RTRVSHLFResponse = telnetServer.read_until(b";\r\n<").decode()
    RTRVSHLFResponse = RTRVSHLFResponse.splitlines()

    # Remove garbage from string
    RTRVSHLFResponse = [item for item in RTRVSHLFResponse if "PYTHON COMPLD" not in item]
    RTRVSHLFResponse = [item for item in RTRVSHLFResponse if ">" not in item]
    RTRVSHLFResponse = [item for item in RTRVSHLFResponse if nodeName not in item]
    RTRVSHLFResponse = [item for item in RTRVSHLFResponse if len(item) > 2]
    RTRVSHLFResponse = sorted(RTRVSHLFResponse)

    # Get the shelf
    RTRVSHLFList = []
    for index, item in enumerate(RTRVSHLFResponse):
        if item.find("SHELF-") > 0:
            start = item.find("SHELF-")
            end = item.find("::")
            shelf = item[start:end]
            RTRVSHLFList.append(shelf)

    # remove the "SHELF" name from the list including "::"
    for index, item in enumerate(RTRVSHLFResponse):
        newStartIndex = item.find("::") + 2
        item = item.replace(item[:newStartIndex], "")
        RTRVSHLFResponse.pop(index)
        RTRVSHLFResponse.insert(index, item)

    # remove remaining garbage characters from string
    for index, item in enumerate(RTRVSHLFResponse):
        item = item.replace('\\', '')
        RTRVSHLFResponse.pop(index)
        RTRVSHLFResponse.insert(index, item)

    # convert RTRVSHLFResponse to dictionary and add to list
    RTRVShelfDictList = []
    for index, item in enumerate(RTRVSHLFResponse):
        dictionary = dict(subString.split("=") for subString in item.split(","))
        RTRVShelfDictList.append(dictionary)

    # create the final interface list
    FinalShelfList = []
    for index, item in enumerate(RTRVSHLFList):
        shelfDictionary = RTRVShelfDictList[index]
        FinalShelfList.append([item, shelfDictionary])
    return(FinalShelfList)
