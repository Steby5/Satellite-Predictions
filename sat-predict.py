from shapely.geometry import LineString, Point
import os.path, datetime, ephem, pandas, requests, os, fastkml

OUTPUT_DIR=os.path.dirname(os.path.realpath(__file__))  #lokacija sat-predict.py datoteke (to je ta datoteka)

trenutni_cas = datetime.datetime.now()    #nastavi trenutni cas, kot zacetni cas
interval = datetime.timedelta(minutes=1)   #nastavimo interval racunanja pozicije opazovanega satelita
noaa_txt=os.path.join(OUTPUT_DIR,"noaa.txt")    #lokacija noaa.txt datoteke
noaa_kml=os.path.join(OUTPUT_DIR,"noaa.kml")    #lokacija noaa.kml datoteke
modified=0  #<---- izbrisi (temp spremenljivka)

#========================= izracun razlike med trenutnim in casom sprememb datoteke noaa.txt ==============================#

cas_spremembe=os.path.getmtime(noaa_txt)    #cas spremembe datoteke noaa.txt (omejeno stevilo povprasevanj za streznik)
cas_spremembe_dt = datetime.datetime.fromtimestamp(cas_spremembe)   #pretvori cas spremembe v datetime format
razlika=trenutni_cas-cas_spremembe_dt   #izracuna razliko med trenutnim casom in casom zadnje spremembe
razlika_s = razlika.total_seconds() #cas zapise v sekundah za kasnejse pretvarjanje
razlika_ure = divmod(razlika_s, 3600)[0]    #iz sekund pretvori v ure

#================================= preverimo ali je datoteka starejsa od 2 ur =============================================#

if (razlika_ure<=2):    #preveri ali je od zadnje spremembe ze preteklo vec kot 2 uri
    response = requests.get("https://celestrak.com/NORAD/elements/gp.php?CATNR=33591")  #poslje zahtevek za opazovani satelit (v tem primeru je to NOAA 19)
    with open(noaa_txt, "w") as datoteka:
        datoteka.write(response.text)   #dobljene podatke zapise v noaa.txt datoteko na disku (ce se ne obstaja jo ustvari)
else:
    print("Se je OK!")

lista=pandas.read_csv(os.path.join(OUTPUT_DIR,"noaa.txt"),sep='\t',header=None)[0].tolist()  #iz noaa.txt naredi tabelo, iz katere nato izpise vsak element v svojo spremenljivko

name=lista[0]
line1=lista[1]
line2=lista[2]

tle_rec = ephem.readtle(name, line1, line2);    #prebere TLE podatke
#tle_rec.compute();

timelist = []   #seznam casovnih tock zamaknjenih za interval (1 minuta)
cas=int(input("Vnesi zeljeni opazovani cas (v minutah):")) #za koliko minut naj program predvide lokacijo opazovanega staelita
if cas<2:
    print('Minimalni opazovan interval mora imeti vsaj 2 razlicni vrednosti!')
    cas=2

for i in range(cas):
    timelist.append(trenutni_cas + i*interval)

pozicija = []   #seznam lokacij satelita ob dolocenem casu iz seznama "timelist"
for t in timelist:
    tle_rec.compute(t)
    pozicija.append(((tle_rec.sublong / ephem.degree),(tle_rec.sublat / ephem.degree),tle_rec.elevation))
#print(pozicija)
k = fastkml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
center= fastkml.Placemark(ns,"FE",'noaa')
#center.geometry=Point("46.044562,14.489438")
center.geometry =  LineString(pozicija)
k.append(center)
with open(noaa_kml, 'w') as kmlfile:
    kmlfile.write(k.to_string())
os.startfile(os.path.join(OUTPUT_DIR,"noaa.kml"))