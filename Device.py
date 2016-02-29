# Class definitions for devices
# Device is the primary class, and it has some pretty basic functions,
# mostly an snmpwalk for relevant data, and a weather check.
# APs and Clients descend from Device, and do geometry with one another to
# determine their relative angle. 

# OpenWeatherMap
import pyowm
# Configuration parsing
from configobj import ConfigObj
# SNMP
from easysnmp import Session
# Geocoordinate lookups
from pygeocoder import Geocoder
import os.path

# Load a configuration file, and return it as a dict-like.
whereAmI = os.path.dirname(os.path.abspath(__file__)) + '/'
config = ConfigObj(whereAmI + 'ClearSkies.conf')

APIKey = config['auth']['APIKey']
owm = pyowm.OWM(APIKey)

class Device:
    def __init__(self, name, IP):
        # The base class just takes a name, location, and IP address
        self.name = name
        self.IP = IP
    def checkWeather(self):
        # We can check the OpenWeatherMap servers for the nearest conditions
        self.station = owm.weather_around_coords(self.coords[0], self.coords[1], limit=1)[0]
        self.weather = self.station.get_weather().get_status()
    def getSNMP(self):
        # Get data from the host via SNMP
        session = Session(hostname=self.IP, community=config['auth']['SNMPCommunity'], version=1)
        location = session.get('sysLocation.0') 

        # Converts the address string into a coordinate pair
        self.coords = Geocoder.geocode(location)[0].coordinates

class Tower(Device):
    pass    

if __name__ == '__main__':
    a = Device('test', '172.24.53.42') #'62336 Deer Trl Lane Bend  OR 97701')
    #a = Device('test', '172.24.3.130')
    a.getSNMP()
    a.checkWeather()
    print(a.weather)
