#!/usr/bin/env python3
import time, os, sys                                                    #Importierte Betriebssystem, Sys und Zeit                                        
import board                                                            #Importiere Board Modul notwendig für adafriut
import adafruit_dht                                                     #Adafruit Bibiliothek für den DHT Sensor
import Adafruit_ADS1x15                                                 #Adafruit Bibiliothek für den AD-Wandler
from gpiozero import LED, Button                                        #Von dem Modul GPIOZERO lade die Funktion LED und Button   
from time import sleep                                                  #Von dem Modul Time lade die Funktion sleep  
import pigpio                                                           #Bibiliothek zum gezielten steuern der GPIOs präzises Timing und PWM  
import busio                                                            #Benötigt Adafruit zum benutzung verschiedener Protokolle
import adafruit_ads1x15.ads1115 as ADS                                  #Von dem Modul adafruit_ads1x15.ads1115 lade die Funktion ADS
from adafruit_ads1x15.analog_in import AnalogIn                         #Funktion AnalogIn um die Analogen Werte des AD-Wanlders zu erfassen
import RPi.GPIO as GPIO                                                 #Bibiliothek zum steuern der GPIOS                      
from influxdb import InfluxDBClient                                     #Importiere das Modul InfluxDatenbank
from datetime import datetime                                           #Importiere das Datum

#DHT22       Definieren
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)

# Relais    Definieren  
Luefter = LED(23)
Bewaesserungspumpe1 = LED(24)
Bewaesserungspumpe2 = LED(27)
Heizmatte = LED(25)

#Relais     abschalten LowLeveltrigger
Luefter.on()
Heizmatte.on()
Bewaesserungspumpe1.on()
Bewaesserungspumpe2.on()

#Datenbank Influx DB Login Konfigurieren
host = "localhost"                                                      #Host ip
port = 8086                                                             #Host port
user = "pi"                                                             #user mit Berechtigung
password = "raspberry"                                                  #Userpassword
dbname = "gewaechshaus"                                                 #Datenbank die gefüttert wird
interval = 5                                                            #Intervall wie oft

#Datenbak Client Definieren
client = InfluxDBClient(host, port, user, password, dbname)
measurement = "messung"                                                 #Datenbank
location = "office"                                                     #Ort

#Beginn
print("\033[0;32m...::: initialized :::...\033[0m")

def aktuelleTemperatur1():	                                        #Definieren des Erdtemperatursensors1

    #1-wire Slave Datei lesen
    file = open('/sys/bus/w1/devices/28-01204fd35bbe/w1_slave')         #Textdatei Ordner aus dem die daten ausgelesen werden
    filecontent = file.read()
    file.close()
 
    #Temperaturwerte auslesen und konvertieren
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
 
    #Temperatur ausgeben
    rueckgabewert = '%6.2f' % temperature 
    return(round(float(rueckgabewert),1))                               #Runden der Werte und Ausgabe als Float
 
def aktuelleTemperatur2():	                                        #Definieren der Erdtemperatursensors1
      
    #1-wire Slave Datei lesen
    file = open('/sys/bus/w1/devices/28-01204fc85c90/w1_slave')         #Textdatei Ordner aus dem die daten ausgelesen werden
    filecontent = file.read()
    file.close()
 
    #Temperaturwerte auslesen und konvertieren
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
 
    #Temperatur ausgeben
    rueckgabewert = '%6.2f' % temperature 
    return(round(float(rueckgabewert),1))                               #Runden der Werte und Ausgabe als Float

def Luftfeuchtigkeit():                                                 #Definieren der Luftfeuchtigkeit DHT22
	humidity = dhtDevice.humidity
	return(humidity)
  
def Lufttemperatur():                                                   #Definieren der Lufttemperatur DHT22
	temperature_c = dhtDevice.temperature
	return(temperature_c)

def Erdfeuchtigkeit1():                                                 #Definieren der Erdfeuchtigkeit1
	chan = AnalogIn(ads, ADS.P0)                                    #ADS.P0 Analogwerte des Pins 0 am AD-Wandler auslesen
	Erdfeuchtigkeit = (round(100-(chan.value-29040)/((30592-29040)/100),1))#Umrechnung der Bits Min/Max in % mit der Funktion Round gerundet
	
	if Erdfeuchtigkeit < 1:                                         #Wenn durch Spannungsschwankungen Wert unter 1 ist trotzdem 1 anzeigen
		return (1.0)
	if Erdfeuchtigkeit > 100:                                       #Wenn durch Spannungsschwankungen Wert unter 1 ist trotzdem 1 anzeigen
		return (100.0)
	else:	
		return(Erdfeuchtigkeit)
            
def Erdfeuchtigkeit2():                                                 #Definieren der Erdfeuchtigkeit1
	chan = AnalogIn(ads, ADS.P2)                                    #ADS.P2 Analogwerte des Pins 2 am AD-Wandler auslesen
	Erdfeuchtigkeit = (round(100-(chan.value-29040)/((30592-29040)/100),1))#Umrechnung der Bits Min/Max in % mit der Funktion Round gerundet
		
	if Erdfeuchtigkeit < 1:                                         #Wenn durch Spannungsschwankungen Wert unter 1 ist trotzdem 1 anzeigen
		return (1.0)
	if Erdfeuchtigkeit > 100:                                       #Wenn durch Spannungsschwankungen Wert unter 1 ist trotzdem 1 anzeigen
		return (100.0)
	else:	
		return(Erdfeuchtigkeit)
        
#Beginn der Schleife
while True:
    try:
	
       
        now = datetime.now()						 #Aktuele Uhrzeit
        current_time = now.strftime("%H:%M:%S")				 #Formatiere die aktuelle Uhrzeit
	#Anzeigen der Werte
        print("Aktuelle Uhrzeit:", current_time)
        print("Lufttemperatur:         ",Lufttemperatur(),"°C")
        print("Luftfeuchtigkeit:	",Luftfeuchtigkeit()," %")  
        print("Erdtemperatur1:         ",  aktuelleTemperatur1(),"°C")
        print("Erdtemperatur2:         ",  aktuelleTemperatur2(),"°C")
        print("Erdfeuchtigkeit1:       ", Erdfeuchtigkeit1(), " %")
        print("Erdfeuchtigkeit2:       ", Erdfeuchtigkeit2(), " %")
        
        #Regelung des Gewächshauses
        if float(aktuelleTemperatur1()) < 18.2:                         #Wenn Temperatur1 unter 10°C Dann Heize
            Heizmatte.off()
            print("Heizmatte an")
        if float(aktuelleTemperatur1()) > 20:                           #Wenn Temperatur1 über 13°C Dann Heize nicht
            Heizmatte.on()
            print("Heizmatte aus")
        if float(Erdfeuchtigkeit1()) < 50:                              #Wenn Erdfeuchtigkeit1 unter 50% dann gieße 5 sekundden
            Bewaesserungspumpe1.off()
            print("Bewässerung Pumpe1")
            time.sleep(5.0)
            Bewaesserungspumpe1.on()
        if float(Erdfeuchtigkeit2()) < 50:                              #Wenn Erdfeuchtigkeit2 unter 50% dann gieße 5 sekundden
            Bewaesserungspumpe2.off()
            print("Bewässerung Pumpe2")
            time.sleep(5.0)
            Bewaesserungspumpe2.on()
        if float(Lufttemperatur()) > 21:                                #Wenn Lufttemperatur über 19°C dann Lüfte das Gewächshaus
            Luefter.off()	    
        if float(Lufttemperatur()) > 17:                                #Wenn Lufttemperatur unter 17°C dann Lüfte das Gewächshaus nicht
            Luefter.on()  

        iso = time.ctime()
        data = [
        {
          "measurement": measurement,
              "tags": {
                  "location": location,
              },
              "time": iso,
              "fields": {
                  "Lufttemperatur" : Lufttemperatur(),
                  "Luftfeuchtigkeit" : Luftfeuchtigkeit(),
                  "Erdtemperatur1" : aktuelleTemperatur1(),
                  "Erdtemperatur2" : aktuelleTemperatur2(),
                  "Erdfeuchtigkeit1" : Erdfeuchtigkeit1(),
                  "Erdfeuchtigkeit2" : Erdfeuchtigkeit2()
					
              }
          }
        ]
        client.write_points(data)                                      #senden der JSON daten an die InfluxDX 
        time.sleep(interval)                                           #pause bis zum nächsten schleifen durchlauf
             
                  
    except RuntimeError as error:
        print(error.args[0])                                           #Fehler treten ziemlich oft auf, DHTs sind schwer zu lesen, einfach lauffen lassen
        time.sleep(5.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
        
        

 

