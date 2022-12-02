import datetime as dt
import os

OUTPUT_DIR=os.path.dirname(os.path.realpath(__file__))  #curent directory of python file
tle_txt=os.path.join(OUTPUT_DIR,'tle.txt')  #path to tle.txt file

now = dt.datetime.now()

modifyed=os.path.getmtime(tle_txt)    #time of last modification of tle.txt file
modifyed_dt = dt.datetime.fromtimestamp(modifyed)   #convert into datetime format
diff=now-modifyed_dt   #calculate the difference between now and last modification
diff_sec = diff.total_seconds() #convert the time in seconds
diff_hours = divmod(diff_sec, 3600)[0]    #convert seconds to hours