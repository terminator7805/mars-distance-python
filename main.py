#IMPORTS
from re import T
from tkinter import *
from tkcalendar import Calendar, DateEntry
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

def separationattime(t): #gets the current distance from the earth to mars in KM
    converttime = Time(t)
    loc = EarthLocation.of_site('greenwich') 
    with solar_system_ephemeris.set('builtin'):
        solar_system_ephemeris.set('de440') 
        mars = get_body('mars', converttime, loc) 
        earth = get_body('earth', converttime, loc)
    sep = mars.separation_3d(earth).to(u.km)
    return sep

def distancebutton(): #Triggers the loop of the distance text, function for dbutton
    if timeget.get() == 'now': 
        utc = Time.now()
        timenow = utc + datetime.timedelta(hours=2)
        time = datetime.datetime.strptime(str(timenow), '%Y-%m-%d %H:%M:%S.%f')
        msg_display.config(text=time.strftime('%d/%m/%Y %H:%M:%S'))
    else: 
        time = datetime.datetime.strptime(timeget.get(), '%Y/%m/%d %H:%M:%S.%f')
        msg_display.config(text=time.strftime('%d/%m/%Y %H:%M:%S'))
    distance = StringVar()
    distance.set(separationattime(time))
    def update():
        if timeget.get() == 'now': 
            utc = Time.now()
            timenow = utc + datetime.timedelta(hours=2)
            time = datetime.datetime.strptime(str(timenow), '%Y-%m-%d %H:%M:%S.%f')
            msg_display.config(text=time.strftime('%d/%m/%Y %H:%M:%S'))
        else: 
            time = datetime.datetime.strptime(timeget.get(), '%Y/%m/%d %H:%M:%S.%f')
            msg_display.config(text=time.strftime('%d/%m/%Y %H:%M:%S'))
    prueba = Label(textvariable=distance)
    prueba.pack()
    set_interval(update, 1)

#TKINTER
# Add Calendar

 
window = Tk() 
#window.overrideredirect(True)
window.title('Mars')
global timeget
timeget = StringVar()
timeget.set('now')


window.iconphoto(False, PhotoImage(file='resources/3D_Mars.png'))
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
    year=2021, 
    month=2,
    day=3
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
def display_msg():
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



actionBtn =Button(
    window,
    text="Establecer fecha",
    padx=10,
    pady=10,
    command=display_msg
)
actionBtn.pack(pady=10)

actionBtn2 =Button(
    window,
    text="Tiempo real",
    padx=10,
    pady=10,
    command=lambda: timeget.set('now')
)
actionBtn2.pack(pady=10)

msg_display = Label(
    window,
    text=""
)
msg_display.pack(pady=10)



date = Label(window, text = "")
date.pack(pady = 20)
text1 = Label(text='Distancia Tierra-Marte')
text1.pack()
distancebutton()
window.mainloop()