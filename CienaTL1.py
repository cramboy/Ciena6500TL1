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

    # Run command and split into lines
    telnetServer.write(("RTRV-SHELF::ALL:PYTHON;").encode())
    RTRVSHLFResponse = telnetServer.read_until(b";\r\n<").decode()
    RTRVSHLFResponse = RTRVSHLFResponse.splitlines()

    # Remove garbage from string
    RTRVSHLFResponse = [item for item in RTRVSHLFResponse if "PYTHON COMPLD" not in item]
    RTRVSHLFResponse = [item for item in RTRVSHLFResponse if ">" not in item]
    RTRVSHLFResponse = [item for item in RTRVSHLFResponse if nodeName not in item]
    RTRVSHLFResponse = [item for item in RTRVSHLFResponse if len(item) > 2]

    # Sort outputaccording to shelf number (first part of string)
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
        item = item.replace('"', '')
        RTRVSHLFResponse.pop(index)
        RTRVSHLFResponse.insert(index, item)

    ShelfList = []
    ShelfDict = {}
    # Search RTRVSHLFResponse for strings
    for index, item in enumerate(RTRVSHLFResponse):
        ACTFLTRTIMER = item.find("ACTFLTRTIMER")
        BAYNUM = item.find("BAYNUM")
        CLUSTERING = item.find("CLUSTERING")
        DBSYNCSTATE = item.find("DBSYNCSTATE")
        EXTENDEDSHELF = item.find("EXTENDEDSHELF")
        FIC = item.find("FIC")
        FLTRTIMER = item.find(",FLTRTIMER")
        LOCATION = item.find("LOCATION")
        OM5000_NE_ID = item.find("OM5000_NE_ID")
        OM5000_PRIMARY_IP = item.find("OM5000_PRIMARY_IP")
        PHYSSHELF = item.find("PHYSSHELF")
        PRIMARY = item.find("PRIMARY")
        SHELFSYNC  = item.find("SHELFSYNC")
        SITEGROUP = item.find("SITEGROUP")
        if SITEGROUP == -1: SITEGROUP = len(item)-10
        SITEID = item.find("SITEID")
        SITENAME = item.find("SITENAME")
        SUBNETNAME = item.find("SUBNETNAME")
        TIDC = item.find("TIDC")

        # Parse output
        ACTFLTRTIMERval = item[ACTFLTRTIMER+13:FLTRTIMER]
        BAYNUMval = i = item[BAYNUM+7:FIC-1]
        CLUSTERINGval = item[CLUSTERING+10:SITEGROUP-1]
        if len(CLUSTERINGval) > 7: CLUSTERINGval = ""
        DBSYNCSTATEval = item[DBSYNCSTATE+12:SHELFSYNC-1]
        EXTENDEDSHELFval = item[EXTENDEDSHELF+14:ACTFLTRTIMER-1]
        FICval = item[FIC+4:SUBNETNAME-1]
        FLTRTIMERval = item[FLTRTIMER+11:DBSYNCSTATE-1]
        LOCATIONval = item[LOCATION+10:EXTENDEDSHELF-1]
        OM5000_NE_IDval = item[OM5000_NE_ID+13:BAYNUM-1]
        OM5000_PRIMARY_IPval = item[OM5000_PRIMARY_IP+18:OM5000_NE_ID-1]
        PHYSSHELFval = item[PHYSSHELF+10:LOCATION-1]
        PRIMARYval = item[PRIMARY+8:TIDC-1]
        SHELFSYNCval = item[PRIMARY+8:TIDC-1]
        SITEGROUPval = item[SITEGROUP+10:]
        SITEIDval = item[SITEID+7:SITENAME-1]
        SITENAMEval = item[SITENAME+9:PRIMARY-1]
        SUBNETNAMEval = item[SITENAME+9:PRIMARY-1]
        TIDCval = item[SITENAME+9:PRIMARY-1]

        # Assign values to dictionary
        ShelfDict["ACTFLTRTIMER"] = ACTFLTRTIMERval
        ShelfDict["BAYNUM"] = BAYNUMval
        ShelfDict["CLUSTERING"] = CLUSTERINGval
        ShelfDict["DBSYNCSTATE"] = DBSYNCSTATEval
        ShelfDict["EXTENDEDSHELF"] = EXTENDEDSHELFval
        ShelfDict["FIC"] = FICval
        ShelfDict["FLTRTIMER"] = FLTRTIMERval
        ShelfDict["LOCATION"] = LOCATIONval
        ShelfDict["OM5000_NE_ID"] = OM5000_NE_IDval
        ShelfDict["OM5000_PRIMARY_IP"] = OM5000_PRIMARY_IPval
        ShelfDict["PHYSSHELF"] = PHYSSHELFval
        ShelfDict["SHELFSYNC"] = SHELFSYNCval
        ShelfDict["SITEGROUP"] = SITEGROUPval
        ShelfDict["SITEID"] = SITEIDval
        ShelfDict["SITENAME"] = SITENAMEval
        ShelfDict["SUBNETNAME"] = SUBNETNAMEval
        ShelfDict["TIDC"] = TIDCval
        ShelfDict["ACTFLTRTIMER"] = ACTFLTRTIMERval

        ShelfList.append([RTRVSHLFList[index], ShelfDict])
    
    # Final output has the form:
    # [[Shelf-n, {shelf dictionary}], [Shelf-n, {shelf dictionary}], ...]
    return(ShelfList)
