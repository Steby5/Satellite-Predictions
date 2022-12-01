from shapely.geometry import LineString, Point
import os.path, datetime, ephem, pandas, requests, os, fastkml

OUTPUT_DIR=os.path.dirname(os.path.realpath(__file__))  #lokacija sat-predict.py datoteke (to je ta datoteka)


tle_txt=os.path.join(OUTPUT_DIR,'tle.txt')  #path to tle.txt file
file1 = open(tle_txt, 'r')
Lines = file1.readlines()

count = 0
text = []
for line in Lines:
    count += 1
    #print("Line{}: {}".format(count, line.strip()))
    #print(line.strip())
    text.append(line.strip())
    
#print(text)

sateliti = {}
tmparr = [0,0]
len = len(text)
for i in range(0, len, 3):
    tmparr[0] = text[i+1]
    tmparr[1] = text[i+2]
    sateliti[text[i]] = tmparr

print(sateliti.get('TEMPSAT 1')) #dobi cell arraz podatkov
print(sateliti.get('TEMPSAT 1')[0])
    
