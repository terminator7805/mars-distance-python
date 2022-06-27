#IMPORTS
from tkinter import *
import datetime;
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body, get_moon
import astropy.units as u
import threading

#FUNCTIONS
def set_interval(func, sec): #basic interval function
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def separationnow(): #gets the current distance from the earth to mars in KM
    utc = Time.now()
    t = utc + datetime.timedelta(hours=2)
    loc = EarthLocation.of_site('greenwich') 
    with solar_system_ephemeris.set('builtin'):
        solar_system_ephemeris.set('de440s') 
        mars = get_body('sun', t, loc) 
        earth = get_body('earth', t, loc)
    sep = mars.separation_3d(earth).to(u.km)
    return sep

def distancebutton(): #Triggers the loop of the distance text, function for dbutton
    distance = StringVar()
    distance.set(separationnow())
    def update():
        distance.set(separationnow())
        print(distance.get())
    prueba = Label(textvariable=distance)
    prueba.pack()
    dbutton.destroy()
    set_interval(update, 1)

#TKINTER
window = Tk()
#window.overrideredirect(True)
window.title('Mars')
window.iconphoto(False, PhotoImage(file='resources/3D_Mars.png'))
text1 = Label(text='Prueba')
text1.pack()
dbutton = Button(text="Conseguir distancia actual", command=distancebutton)
dbutton.pack()
window.mainloop()