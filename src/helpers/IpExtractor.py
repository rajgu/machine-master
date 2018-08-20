import os
import ElementTree.ElementTree as ET
from src import Config
from src.db import DBStps


class IpExtractor:


    localizations = {
        'Ki': ['ki', 'ki10'],
        'Li': ['li'],
    }


    paths = [
        './ethernetLink/ip',
        './node/ethernetLink/ip',
        '{http://www.springframework.org/schema/beans}bean[@class="G2RbsResource"]/{http://www.springframework.org/schema/beans}property[@name="host"]',
        '{http://www.springframework.org/schema/beans}bean[@class="BasebandProcessingUnitResource"]/{http://www.springframework.org/schema/beans}property[@name="host"]',
        '{http://www.springframework.org/schema/beans}bean[@class="ColiResource"]/{http://www.springframework.org/schema/beans}property[@name="host"]',
        '{http://www.springframework.org/schema/beans}bean[@class="TemporaryG2RbsAndBasebandProcessingUnitResource"]/{http://www.springframework.org/schema/beans}property[@name="host"]',
    ]


    def __init__(self, db, stpCfgLocation):
        self.stpCfgLocation = stpCfgLocation
        self.config         = Config.Config()
        self.DBStps         = DBStps.DBStps(db)


    def extract(self, stpData):

        if not stpData or not 'name' in stpData:
            return ''

        stpName = stpData['name']

        for directory in self.localizations[stpData['site']]:
            configFileLocations = [
                "{0}{1}/{2}/rcm/{2}.xml".format(self.stpCfgLocation, directory, stpName),
                "{0}{1}/{2}/rcm/{3}.xml".format(self.stpCfgLocation, directory, stpName, stpName.replace('tstp', 'trbs')),
                "{0}{1}/{2}/{2}.xml".format(self.stpCfgLocation, directory, stpName),
                "{0}{1}/{2}/beans/{2}.xml".format(self.stpCfgLocation, directory, stpName),
                "{0}{1}/{2}/beans/{3}.xml".format(self.stpCfgLocation, directory, stpName, stpName.lower()),
            ]

            for configFileLoc in configFileLocations:
                if os.path.exists(configFileLoc):
                    root = ET.parse(configFileLoc).getroot()
                    for xpath in self.paths:
                        for tag in root.findall(xpath):
                            if 'value' in tag.attrib:
                                return str(tag.attrib['value'])
                            return str(tag.text)

        return ''