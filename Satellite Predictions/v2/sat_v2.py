import datetime as dt
import os
import requests
import pandas

OUTPUT_DIR=os.path.dirname(os.path.realpath(__file__))  #curent directory of python file
tle_txt=os.path.join(OUTPUT_DIR,'tle.txt')  #path to tle.txt file
temp=os.path.join(OUTPUT_DIR,"temp.txt")
now = dt.datetime.now() #read system date/time

modifyed=os.path.getmtime(tle_txt)    #get the time since the last update of tle.txt file
#print(modifyed)
modifyed_dt = dt.datetime.fromtimestamp(modifyed)   #convert into datetime format
#print(modifyed_dt)
diff=now-modifyed_dt   #calculate the difference between now and last modification
#print(diff)
diff_sec = diff.total_seconds() #convert the time in seconds
#print(diff_sec)
diff_hours = divmod(diff_sec, 3600)[0]    #convert seconds to hours
#print(diff_hours)

if (diff_hours>=2):    #check if time since last update is less than 2 hours
    response = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle")  #send request to celestrak.com to get current TLE data
    with open(temp,'w') as file:
        file.write(response.text)   #write data from request function into text file
    with open(temp, 'r') as r, open(tle_txt, 'w') as o:
        for line in r:
            if line.strip():    #remove all empty lines in the file
                o.write(line)
    os.remove(temp) #delete temp file
else:
    print("File is stil relavant. No update necessary.")
tle=pandas.read_csv(tle_txt,sep='\t',header=None)[0].tolist()  #create an array from tle.txt file

#x = slice(0, len(tle), 3)   #first value -> satellitre name
#y = slice(1, len(tle), 3)   #second value -> TLE line 1
#z = slice(2, len(tle), 3)   #third value -> TLE line 2

#a=tle[x]
#d = dict.fromkeys(a)
#print(d)

for i in tle:
    d=dict.fromkeys(tle[slice(0, len(tle), 3)])
#    
#print(d)

def add_values_in_dict(sample_dict, key, list_of_values):
    ''' Append multiple values to a key in 
        the given dictionary '''
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict

word_freq = {'is'   : [1, 3, 4, 8, 10],
             'at'   : [3, 10, 15, 7, 9],
             'test' : [5, 3, 7, 8, 1],
             'this' : [2, 3, 5, 6, 11],
             'why'  : [10, 3, 9, 8, 12] }
# Append multiple values for existing key 'at'
word_freq = add_values_in_dict(d, , [20, 21, 22])
print('Contents of the dictionary: ')
print(word_freq)