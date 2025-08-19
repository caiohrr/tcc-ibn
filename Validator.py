import json
from os import path
from copy import copy

class MNHost:
    ID = ""
    IP = "127.0.0.1"
    ELEM = None

    def __init__(self, ID, IP):
        self.ID = ID
        self.IP = IP

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class MNSwitch:
    ID = ""
    ELEM = None

    def __init__(self, ID):
        self.ID = ID

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class MNController:
    ID = ""
    ELEM = None

    def __init__(self, ID):
        self.ID = ID

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class MNOVSSwitch:
    ID = ""
    CONTROLLER = None
    ELEM = None

    def __init__(self, ID, CONTROLLER):
        self.ID = ID
        self.CONTROLLER = CONTROLLER

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class Validator:
    JSON = None
    STATUS = None
    ID = None
    MNHOSTS = []
    MNSWITCHES = []
    MNCONTROLLER = []
    MNOVSES = []
    CONNECTIONS = []

    def __init__(self, jsonFilePath):

        if path.isfile(jsonFilePath):
            with open(jsonFilePath) as data:
                self.JSON = json.load(data)
        else:
            self.STATUS = -1
            return

        if 'ID' not in self.JSON:
            self.STATUS = -2
            return
        else:
            if isinstance(self.JSON["ID"], str):
                self.ID = self.JSON["ID"]
            else:
                self.STATUS = -2
                return
        if 'COMPONENTS' not in self.JSON:
            self.STATUS = -2
            return
        if 'CONNECTIONS' not in self.JSON:
            self.STATUS = -2
            return

        if self.componentsValidate() == 0:
            if self.connectionsCheck() == 0:
               self.STATUS = 0

#------------------------------------------------------------------

    def isint(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

#------------------------------------------------------------------

    def componentsValidate(self):

        if isinstance(self.JSON['COMPONENTS'], dict):
            componentsList = self.JSON['COMPONENTS']
        else:
            self.STATUS = -3
            return -3

        IDLIST = []
        CONTROLLERLIST = []
        if "HOSTS" in componentsList:
            if isinstance(componentsList["HOSTS"], list):
                for HOST in componentsList["HOSTS"]:
                    if "ID" in HOST and "IP" in HOST:
                        if HOST["ID"] in IDLIST:
                            self.STATUS = -4
                            return -4
                        else:
                            IDLIST.append(HOST["ID"])
                    else:
                        self.STATUS = -4
                        return -4

                    self.MNHOSTS.append(MNHost(HOST["ID"], HOST["IP"]))
            else:
                self.STATUS = -4
                return -4

        if "SWITCHES" in componentsList:
            if isinstance(componentsList["SWITCHES"], list):
                for SWITCH in componentsList["SWITCHES"]:
                    if SWITCH in IDLIST:
                        self.STATUS = -5
                        return -5
                    else:
                        IDLIST.append(SWITCH)

                    self.MNSWITCHES.append(MNSwitch(SWITCH))

        if "CONTROLLERS" in componentsList:
            if isinstance(componentsList["CONTROLLERS"], list):
                for CONTROLLER in componentsList["CONTROLLERS"]:
                    if CONTROLLER in IDLIST:
                        self.STATUS = -6
                        return -6
                    else:
                        CONTROLLERLIST.append(CONTROLLER)

                    self.MNCONTROLLER.append(MNController(CONTROLLER))

        if "OVSSWITCHES" in componentsList:
            if isinstance(componentsList["OVSSWITCHES"], list):
                for OVSSWITCH in componentsList["OVSSWITCHES"]:
                    if "ID" in OVSSWITCH and "CONTROLLER" in OVSSWITCH:
                        if OVSSWITCH["ID"] in IDLIST or OVSSWITCH["ID"] in CONTROLLERLIST:
                            self.STATUS = -7
                            return -7
                        else:
                            if OVSSWITCH["CONTROLLER"] in CONTROLLERLIST:
                                IDLIST.append(OVSSWITCH["ID"])
                            else:
                                self.STATUS = -7
                                return -7
                    else:
                        self.STATUS = -7
                        return -7

                    self.MNOVSES.append(MNOVSSwitch(OVSSWITCH["ID"], OVSSWITCH["CONTROLLER"]))

                return 0

# ------------------------------------------------------------------

    def connectionsCheck(self):

        HOSTSIDS = [HOST.ID for HOST in self.MNHOSTS]
        SWITCHESIDS = [SWITCH.ID for SWITCH in self.MNSWITCHES]
        OVSSWITCHESIDS = [OVS.ID for OVS in self.MNOVSES]

        if isinstance(self.JSON['CONNECTIONS'], list):
            connectionsList = self.JSON['CONNECTIONS']
        else:
            self.STATUS = -8
            return -8

        revisedConnection = []
        for CONNECTION in connectionsList:
            if "IN/OUT" in CONNECTION and "OUT/IN" in CONNECTION:
                if CONNECTION["IN/OUT"] in HOSTSIDS or CONNECTION["IN/OUT"] in SWITCHESIDS or CONNECTION["IN/OUT"] in OVSSWITCHESIDS:
                    if CONNECTION["OUT/IN"] in HOSTSIDS or CONNECTION["OUT/IN"] in SWITCHESIDS or CONNECTION["OUT/IN"] in OVSSWITCHESIDS:
                        if CONNECTION["OUT/IN"] != CONNECTION["IN/OUT"] and CONNECTION not in revisedConnection:
                            revisedConnection.append(CONNECTION)
                        else:
                            self.STATUS = -9
                            return -9
                    else:
                        self.STATUS = -9
                        return -9
                else:
                    self.STATUS = -9
                    return -9
            else:
                self.STATUS = -9
                return -9

        self.CONNECTIONS = copy(connectionsList)
        return 0
