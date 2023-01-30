#IMPORTS
import sys
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body
import astropy.units as u
import time, threading
import socket


#FUNCTIONS

def separationattime(t): #gets the current distance from the earth to mars in KM
    converttime = Time(t)
    loc = EarthLocation.of_site('greenwich') 
    with solar_system_ephemeris.set('de440'):
        mars = get_body('mars', converttime, loc) 
        earth = get_body('earth', converttime, loc)
    sep = [mars.separation_3d(earth).to_value(u.km), mars.separation_3d(earth).to_value(u.au)]
    return sep

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    data = client.recv(1024)
    response = separationattime(data)
    listToStr = ' '.join(map(str, response))
    client.send(listToStr.encode())
