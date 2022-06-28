#IMPORTS
from tkinter import *
from tkcalendar import Calendar, DateEntry
import datetime;
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body, get_moon
import astropy.units as u
import time, threading

inter = None
StartTime=time.time()

class setInterval : #set interval requirements
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

#FUNCTIONS

def separationattime(t): #gets the current distance from the earth to mars in KM
    converttime = Time(t)
    loc = EarthLocation.of_site('greenwich') 
    with solar_system_ephemeris.set('builtin'):
        solar_system_ephemeris.set('de440') 
        mars = get_body('mars', converttime, loc) 
        earth = get_body('earth', converttime, loc)
    sep = mars.separation_3d(earth).to(u.km)
    return sep

def distancebutton(): #Changes the distance text, function for date buttons
    global inter
    if timeget.get() == 'now': 
        utc = Time.now()
        timenow = utc + datetime.timedelta(hours=2)
        timed = datetime.datetime.strptime(str(timenow), '%Y-%m-%d %H:%M:%S.%f')
        clock_display.config(text=timed.strftime('%d/%m/%Y %H:%M:%S'))
    else: 
        timed = datetime.datetime.strptime(timeget.get(), '%Y/%m/%d %H:%M:%S.%f')
        clock_display.config(text=timed.strftime('%d/%m/%Y %H:%M:%S'))
    distance = StringVar()
    distance.set(separationattime(timed))
    distance_display.config(text=distance.get())
    def update(): #Updates the realtime distance when needed
        global inter
        if timeget.get() != 'now': 
            inter.cancel()
            inter = None
            return
        utc = Time.now()
        timenow = utc + datetime.timedelta(hours=2)
        timed = datetime.datetime.strptime(str(timenow), '%Y-%m-%d %H:%M:%S.%f')
        clock_display.config(text=timed.strftime('%d/%m/%Y %H:%M:%S'))
        distance.set(separationattime(timed))
        distance_display.config(text=distance.get())
    if timeget.get() == 'now' and inter == None:  inter=setInterval(1,update) #Triggers the loop of update funct without stacking intervals

#TKINTER
#Window's settings
window = Tk() 
#window.overrideredirect(True)
window.title('Mars')
window.iconphoto(False, PhotoImage(file='resources/3D_Mars.png'))

#Date select
global timeget
timeget = StringVar()
timeget.set('now')
today = datetime.date.today().strftime("%d/%m/%Y").split('/')
hour_string=StringVar()
min_string=StringVar()
last_value_sec = ""
last_value = ""        
f = ('Times', 20)
fone = Frame(window)
ftwo = Frame(window)

fone.pack(pady=10)
ftwo.pack(pady=10)
cal = Calendar(
    fone, 
    selectmode="day", 
    year=int(today[2]), 
    month=int(today[1]),
    day=int(today[0])
    )
cal.pack()

sec_hour = Spinbox(
    ftwo,
    from_=0,
    to=23,
    wrap=True,
    textvariable=hour_string,
    width=2,
    state="readonly",
    font=f,
    justify=CENTER
    )
min_sb = Spinbox(
    ftwo,
    from_=0,
    to=59,
    wrap=True,
    textvariable=min_string,
    font=f,
    width=2,
    justify=CENTER
    )

sec = Spinbox(
    ftwo,
    from_=0,
    to=59,
    wrap=True,
    textvariable=sec_hour,
    width=2,
    font=f,
    justify=CENTER
    )


if last_value == "59" and min_string.get() == "0":
    hour_string.set(int(hour_string.get())+1 if hour_string.get() !="23" else 0)   
    last_value = min_string.get()

if last_value_sec == "59" and sec_hour.get() == "0":
    min_string.set(int(min_string.get())+1 if min_string.get() !="59" else 0)
if last_value == "59":
    hour_string.set(int(hour_string.get())+1 if hour_string.get() !="23" else 0)            
    last_value_sec = sec_hour.get()


sec_hour.pack(side=LEFT, fill=X, expand=True)
min_sb.pack(side=LEFT, fill=X, expand=True)
sec.pack(side=LEFT, fill=X, expand=True)

def setdatefromcal(): #Gets the info from the calendar and sends it to process and get the distance
    date = cal.get_date()
    m = min_sb.get()
    h = sec_hour.get()
    s = sec.get()
    if len(h) == 1:
        h = '0' + h
    if len(m) == 1:
        m = '0' + m
    if len(s) == 1:
        s = '0' + s
    timeget.set(f"{datetime.datetime.strptime(date, '%d/%m/%y').strftime('%Y/%m/%d')} {h}:{m}:{s}.0")
       


#Buttons that correspond to setting time
actionBtn =Button(
    window,
    text="Establecer fecha",
    padx=10,
    pady=10,
    command=lambda: (setdatefromcal(), distancebutton())
)
actionBtn.pack(pady=10)

actionBtn2 =Button(
    window,
    text="Tiempo real",
    padx=10,
    pady=10,
    command=lambda: (timeget.set('now'), distancebutton())
)
actionBtn2.pack(pady=10)

text1 = Label(text='Distancia Tierra-Marte')
text1.pack()
#Clock shown
clock_display = Label(
    window,
    text=""
)
clock_display.pack(pady=10)

#Distance shown
distance_display = Label(
    window,
    text=""
)
distance_display.pack(pady=10)


#Run processes
distancebutton()
window.mainloop()