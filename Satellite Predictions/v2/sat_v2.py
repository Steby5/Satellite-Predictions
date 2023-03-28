import datetime as dt
from datetime import timedelta
import os
import requests
import skyfield
from skyfield.api import wgs84,load,EarthSatellite
from termcolor import colored

print(colored('                                                                                                                                                                                ','cyan'))
print(colored('                                                                                                                                                                                ','cyan'))
print(colored('  /$$$$$$              /$$               /$$ /$$ /$$   /$$                     /$$$$$$$                            /$$ /$$             /$$     /$$                              ','cyan'))
print(colored(' /$$__  $$            | $$              | $$| $$|__/  | $$                    | $$__  $$                          | $$|__/            | $$    |__/                              ','cyan'))
print(colored('| $$  \__/  /$$$$$$  /$$$$$$    /$$$$$$ | $$| $$ /$$ /$$$$$$    /$$$$$$       | $$  \ $$  /$$$$$$   /$$$$$$   /$$$$$$$ /$$  /$$$$$$$ /$$$$$$   /$$  /$$$$$$  /$$$$$$$   /$$$$$$$','cyan'))
print(colored('|  $$$$$$  |____  $$|_  $$_/   /$$__  $$| $$| $$| $$|_  $$_/   /$$__  $$      | $$$$$$$/ /$$__  $$ /$$__  $$ /$$__  $$| $$ /$$_____/|_  $$_/  | $$ /$$__  $$| $$__  $$ /$$_____/','cyan'))
print(colored(' \____  $$  /$$$$$$$  | $$    | $$$$$$$$| $$| $$| $$  | $$    | $$$$$$$$      | $$____/ | $$  \__/| $$$$$$$$| $$  | $$| $$| $$        | $$    | $$| $$  \ $$| $$  \ $$|  $$$$$$ ','cyan'))
print(colored(' /$$  \ $$ /$$__  $$  | $$ /$$| $$_____/| $$| $$| $$  | $$ /$$| $$_____/      | $$      | $$      | $$_____/| $$  | $$| $$| $$        | $$ /$$| $$| $$  | $$| $$  | $$ \____  $$','cyan'))
print(colored('|  $$$$$$/|  $$$$$$$  |  $$$$/|  $$$$$$$| $$| $$| $$  |  $$$$/|  $$$$$$$      | $$      | $$      |  $$$$$$$|  $$$$$$$| $$|  $$$$$$$  |  $$$$/| $$|  $$$$$$/| $$  | $$ /$$$$$$$/','cyan'))
print(colored(' \______/  \_______/   \___/   \_______/|__/|__/|__/   \___/   \_______/      |__/      |__/       \_______/ \_______/|__/ \_______/   \___/  |__/ \______/ |__/  |__/|_______/ ','cyan'))
print(colored('                                                                                                                                                                                ','cyan'))
print(colored('                                                                                                                                                                                ','cyan'))
print(colored('                                                                                                                                                                                ','cyan'))

OUTPUT_DIR=os.path.dirname(os.path.realpath(__file__))  #curent directory of python file
temp=os.path.join(OUTPUT_DIR,"temp.txt")    #path to temp.txt file
tle_txt=os.path.join(OUTPUT_DIR,'tle.txt')  #path to tle.txt file
now = dt.datetime.now() #read system date/time

count=0
tle=[]
sateliti = {}
check=0

if os.path.isfile(tle_txt):
    modifyed=os.path.getmtime(tle_txt)    #get the time since the last update of tle.txt file
    modifyed_dt = dt.datetime.fromtimestamp(modifyed)   #convert into datetime format
    diff=now-modifyed_dt   #calculate the difference between now and last modification
    diff_sec = diff.total_seconds() #convert the time in seconds
    diff_hours = divmod(diff_sec, 3600)[0]    #convert seconds to hours
else:   #if file does not exists set latest modification time to 0
    diff = 0
    diff_sec = 0
    diff_hours = 0

if (diff_hours>=2 or diff==0):    #check if time since last update is more than 2 hours or 0 (-> create file)
    response = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle")  #send request to celestrak.com to get updated TLE data
    with open(temp,'w+') as file:
        file.write(response.text)   #write new data from request function into text file
    with open(temp, 'r') as r, open(tle_txt, 'w') as o: #remove all empty lines in the file
        for line in r:
            if line.strip():
                o.write(line)
    os.remove(temp) #delete temp file
with open(tle_txt, 'r') as file1:
    Lines = file1.readlines()
for line in Lines:
    count += 1
    tle.append(line.strip())    #write content from tle.txt to list 'TLE'

tmparr = [0,0]  #create temp array
for i in range(0, len(tle), 3):
    tmparr[0] = tle[i+1]    #set TLE line 1 as first element in tmparr
    tmparr[1] = tle[i+2]    #set TLE line 2 as second element in tmparr
    sateliti[tle[i]] = tmparr   #set the satellite name as dict key and other two TLE lines as values for this key
    tmparr=[0,0]    #clears temp array for new value
class Error(Exception):
    """Base class for other exceptions"""
    pass
class Quit(Error):
    pass
class Exists(Error):
    pass
class NotSat(Error):
    pass

while True:
    try:
        usr_input=input("Input Satellite name (or type 'quit' to end the program): ").upper()   #get user input for satellite name and convert it to uppercase letters
        if usr_input in sateliti:   #check if user input matches satellite name from dict
            raise Exists    #Raised if user input is a valid satellite name
        elif usr_input == 'QUIT':   #check if user entered 'quit'
            raise Quit  #Raised when user input equals to 'QUIT'
        elif usr_input not in sateliti: #check if user made a mistake or the specified satellite name is not in the dict
            raise NotSat   #Raised if user input is NOT a valid satellite name
        break
    except Quit:
        print('')
        print("Goodbye!     (｡◕‿◕｡)'ﾉ''")
        break
    except Exists:
        observatory = wgs84.latlon(46.044562, -14.489438, 295)   #lon, lat, ele(m)
        line1=sateliti.get(usr_input)[0]    #reads the first TLE line
        line2=sateliti.get(usr_input)[1]    #reads the second TLE line
        ts = load.timescale()
        satellite = EarthSatellite(line1, line2, usr_input, ts)
        while check==0:
            try:
                days=int(input("Enter how many days in advance would you like to see the predictions: "))   #get number of days for prediction
                check=1
            except ValueError:
                print("Please enter a valid int number")
                continue
        t0 = ts.now()   #set start time to current time
        t1 = ts.utc(t0.utc_datetime() + timedelta(days))  #set end time to now + x days
        altitude_degrees = 8.0  #set default value to 8.0 degrees
        check=0
        while check==0:
            try:
                print(colored('                                   ','white'))
                print(colored('---___                       ___---','white'))
                print('   '+colored('/  ','red')+colored('¯¯¯---___     ___---¯¯¯  ','white')+colored('\   ','red'))
                print('___'+colored('\_','red')+colored('__________\ '+colored('X','yellow')+colored(' /__________','white')+colored('_/','red')+'___'))
                print('')
                altitude_degrees = float(input("Enter min. elevation angle for observation: ").upper())    #get user input for altitude limit
                check=1
            except ValueError:
                print("Please enter a valid floating-point number")
                continue
        else:
            t, events = satellite.find_events(observatory, t0, t1, altitude_degrees)    #get all events above our location, for our time window and that are above altitude limit
            for ti, event in zip(t, events):
                name = (f'Above {altitude_degrees} degrees -> ','Highest point above -> ',f'Bellow {altitude_degrees} degrees -> ')[event]
                print(name, ti.utc_strftime('%Y %b %d %H:%M:%S'))
                if event==2:
                    print('----------------------------------------')
    except NotSat:
        print("This is not a valid satellite name.")    #return error message and allow user to enter different satellite name