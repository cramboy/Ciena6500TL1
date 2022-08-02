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

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
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

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def otsInfo(nodeName):
    """ Method used to retrieve OTS information from the TID """

    telnetServer.write(("RTRV-OTS::ALL:PYTHON;").encode())
    commandResponse = telnetServer.read_until(b";\r\n<").decode()
    commandResponse = commandResponse.splitlines()

    # remove garbage from string
    commandResponse = [item for item in commandResponse if "PYTHON COMPLD" not in item]
    commandResponse = [item for item in commandResponse if ">" not in item]
    commandResponse = [item for item in commandResponse if nodeName not in item]
    commandResponse = [item for item in commandResponse if len(item) > 2]

   # get the OTM4 name which starts with OTM4 and ends before "::"
    OTSList = []
    for index, item in enumerate(commandResponse):
        if item.find("OTS-") > 0:
            start = item.find("OTS-")
            end = item.find("::")
            OTSentity = item[start:end]
            OTSList.append(OTSentity)

    # remove the OTS name from the list including "::"
    for index, item in enumerate(commandResponse):
        newStartIndex = item.find("::") + 2
        item = item.replace(item[:newStartIndex], "")
        commandResponse.pop(index)
        commandResponse.insert(index, item)

    for index, item in enumerate(commandResponse):
        item = item.replace("\\", "")  # remove back-slashes
        commandResponse.pop(index)
        commandResponse.insert(index, item)

    OTSdictList = []
    for index, item in enumerate(commandResponse):
            dictionary = dict(subString.split("=") for subString in item.split(","))
            if dictionary["SUBTYPE"] == "ROADM":
                if "DSCM1" not in dictionary: dictionary["DSCM1"] = "None"
            OTSdictList.append(dictionary)

    # create the final interface list
    OTSinfoList = []
    for index, item in enumerate(OTSList):
        OTSinstance = item
        OTSinstDict = OTSdictList[index]
        OTSinfoList.append([OTSinstance, OTSinstDict])

    return(OTSinfoList)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def tidComms(nodeName):
    """ Returns all provisioned IP addresses on the TID """

    # Get the shelf numbers in each TID
    RTRVSHELFlist = []
    shelfNumbers = shelfNumbs(nodeName)
    for index, item in enumerate(shelfNumbers):
        RTRVSHELFlist.append(item[0])

    # Get the static routes provisioned in the TID
    telnetServer.write(("RTRV-IPSTATICRT:::PYTHON;").encode())
    commandResponse = telnetServer.read_until(b";\r\n<").decode()
    commandResponse = commandResponse.splitlines()

    # remove garbage from string
    commandResponse = [item for item in commandResponse if "PYTHON COMPLD" not in item]
    commandResponse = [item for item in commandResponse if ">" not in item]
    commandResponse = [item for item in commandResponse if nodeName not in item]
    commandResponse = [item for item in commandResponse if len(item) > 2]

    # Find each instance of "SHELF-"
    RTRVIPSTATICRTSHELFlist = []
    for index, item in enumerate(commandResponse):
        if item.find("SHELF-") > 0:
            start = item.find("SHELF-")
            end = item.find("::")
            shelfName = item[start:end]
            RTRVIPSTATICRTSHELFlist.append(shelfName)
    RTRVIPSTATICRTSHELFlist = sorted(RTRVIPSTATICRTSHELFlist)

    # remove the SHELF- name from the list including "::"
    for index, item in enumerate(commandResponse):
        newStartIndex = item.find("::") + 2
        item = item.replace(item[:newStartIndex], "")
        item = item.replace("\\", "")  # remove back-slashes
        item = item.replace('"""', " ")  # remove triple quotes
        commandResponse.pop(index)
        commandResponse.insert(index, item)

    # convert commandResponse to dictionary and add to list
    StaticRouteDictList = []
    for index, item in enumerate(commandResponse):
        dictionary = dict(subString.split("=") for subString in item.split(","))
        dictionary["TYPE"] = "STATICROUTE"
        StaticRouteDictList.append(dictionary)

    # Add shelf and static route dictionary together
    ShelfStaticRouteList = []
    for index, item in enumerate(RTRVIPSTATICRTSHELFlist):
        ShelfStaticRouteList.append([item, StaticRouteDictList[index]])

    # Find which shelves are in RTRVSHELFlist but not in RTRVIPSTATICRTSHELFlist 
    RemainingShelvesList = [ element for element in RTRVSHELFlist if element not in RTRVIPSTATICRTSHELFlist]

    for index, item in enumerate(RemainingShelvesList):
        emptyDictionary = {"IPADDR": "","NETMASK":"","NEXTHOP":"" ,"CIRCUIT":"","COST":"","CARRIER":"","STATUS":"","DESCRIPTION":"", "TYPE":"STATICROUTE"}
        ShelfStaticRouteList.append([item, emptyDictionary])

    # Get the IP provisioning in the TID
    telnetServer.write(("RTRV-IP:::PYTHON:::;").encode())
    commandResponse = telnetServer.read_until(b";\r\n<").decode()
    commandResponse = commandResponse.splitlines()

    # Remove garbage from string
    commandResponse = [item for item in commandResponse if "PYTHON COMPLD" not in item]
    commandResponse = [item for item in commandResponse if ">" not in item]
    commandResponse = [item for item in commandResponse if nodeName not in item]
    commandResponse = [item for item in commandResponse if len(item) > 2]
    commandResponse = [item for item in commandResponse if "ILAN-" not in item]

    # Find any entries with the string "COLAN-"
    CommsList = []
    COLANXlist = []
    LAN15list = []
    SHELFIPlist = []
    for index, item in enumerate(commandResponse):
        if item.find("COLAN-") > 0:
            start = item.find("COLAN-")
            end = item.find(":")
            colanX = item[start:end]
            COLANXline = item
            newStartIndex = COLANXline.find("::") + 2
            COLANXline = COLANXline.replace(COLANXline[:newStartIndex], "")
            COLANXdictionary = dict(subString.split("=") for subString in COLANXline.split(","))
            COLANXdictionary["TYPE"] = colanX
            shelfNumber = COLANXdictionary["TYPE"][6:-2]
            COLANXdictionary["SHELF"] = ("SHELF-" + shelfNumber)
            COLANXlist.append(COLANXdictionary)
    commandResponse = [item for item in commandResponse if "COLAN-" not in item]

    for index, item in enumerate(commandResponse):
        if item.find("LAN-") > 0:
            start = item.find("LAN-")
            end = item.find(":")
            lan = item[start:end]
            LANline = item
            newStartIndex = LANline.find("::") + 2
            LANline = LANline.replace(LANline[:newStartIndex], "")
            LANdictionary = dict(subString.split("=") for subString in LANline.split(","))
            LANdictionary["TYPE"] = lan
            shelfNumber = LANdictionary["TYPE"][4:-3]
            LANdictionary["SHELF"] = ("SHELF-" + shelfNumber)
            LAN15list.append(LANdictionary)
    commandResponse = [item for item in commandResponse if "LAN-" not in item]

    for index, item in enumerate(commandResponse):
        if item.find("SHELF-") > 0:
            start = item.find("SHELF-")
            end = item.find(":")
            shelf = item[start:end]
            SHELFline = item
            newStartIndex = SHELFline.find("::") + 2
            SHELFline = SHELFline.replace(SHELFline[:newStartIndex], "")
            SHELFdictionary = dict(subString.split("=") for subString in SHELFline.split(","))
            SHELFdictionary["TYPE"] = shelf
            shelfNumber = SHELFdictionary["TYPE"][6:]
            SHELFdictionary["SHELF"] = ("SHELF-" + shelfNumber)
            SHELFIPlist.append(SHELFdictionary)
    commandResponse = [item for item in commandResponse if "SHELF-" not in item]

    for index, item in enumerate(RTRVSHELFlist):
        shelfCommsList = []
        shelfCommsList.append(item) 
        for eachItem in COLANXlist:
            if eachItem["SHELF"] == item: 
                shelfCommsList.append(eachItem)
        for eachItem in LAN15list: 
            if eachItem["SHELF"] == item: 
                shelfCommsList.append(eachItem)
        for eachItem in SHELFIPlist:
            if eachItem["SHELF"] == item: 
                shelfCommsList.append(eachItem)  
        CommsList.append(shelfCommsList)  
    return(CommsList)
