import requests,os

OUTPUT_DIR=os.path.dirname(os.path.realpath(__file__))  #curent directory of python file
temp=os.path.join(OUTPUT_DIR,"temp.txt")
tle_txt=os.path.join(OUTPUT_DIR,'tle.txt')

response = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle")  #request for TLE file from WEB
with open(temp,'w') as file:
    file.write(response.text)   #write data from request function into text file

with open(temp, 'r') as r, open(tle_txt, 'w') as o: #remove all empty lines in the file
    for line in r:
        if line.strip():
            o.write(line)
os.remove(temp) #delete temp file