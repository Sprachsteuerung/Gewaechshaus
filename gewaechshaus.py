import time, os, sys
import board
import adafruit_dht
import Adafruit_ADS1x15
from gpiozero import LED, Button
from time import sleep
import pigpio
import busio 
import adafruit_ads1x15.ads1115 as ADS 
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import datetime
from influxdb import InfluxDBClient



#DHT22
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)

# Relais
Luefter = LED(23)
Bewaesserungspumpe1 = LED(24)
Bewaesserungspumpe2 = LED(27)
Heizmatte = LED(25)

# ~ Luefter.off()
# ~ Heizmatte.off()
# ~ Bewaesserungspumpe1.off()
# ~ Bewaesserungspumpe2.off()
# ~ time.sleep(2.0)
Luefter.on()
Heizmatte.on()
Bewaesserungspumpe1.on()
Bewaesserungspumpe2.on()

#Datenbank
# Configure InfluxDB connection variables
host = "localhost" # My Ubuntu NUC
port = 8086 # default port
user = "pi" # the user/password created for the pi, with write access
password = "raspberry" 
dbname = "gewaechshaus" # the database we created earlier
interval = 5 # Sample period in seconds

# ~ # Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)
measurement = "messung"
location = "office"

#Beginn

print("\033[0;32m...::: initialized :::...\033[0m")

def aktuelleTemperatur1():	
      
    # 1-wire Slave Datei lesen
    file = open('/sys/bus/w1/devices/28-01204fd35bbe/w1_slave')
    filecontent = file.read()
    file.close()
 
    # Temperaturwerte auslesen und konvertieren
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
 
    # Temperatur ausgeben
    rueckgabewert = '%6.2f' % temperature 
    #print(type(int(rueckgabewert))
    #return(rueckgabewert)
    return(round(float(rueckgabewert),1))
 
def aktuelleTemperatur2():	
      
    # 1-wire Slave Datei lesen
    file = open('/sys/bus/w1/devices/28-01204fc85c90/w1_slave')
    filecontent = file.read()
    file.close()
 
    # Temperaturwerte auslesen und konvertieren
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
 
    # Temperatur ausgeben
    rueckgabewert = '%6.2f' % temperature 
    #print(type(int(rueckgabewert))
    #return(rueckgabewert)
    return(round(float(rueckgabewert),1))   

def Luftfeuchtigkeit():
	humidity = dhtDevice.humidity
	return(humidity)
  
def Lufttemperatur():
	temperature_c = dhtDevice.temperature
	return(temperature_c)

def Erdfeuchtigkeit1():
	chan = AnalogIn(ads, ADS.P0)
	Erdfeuchtigkeit = (round(100-(chan.value-29040)/((30592-29040)/100),1))
	#Erdfeuchtigkeit = (round((100-(chan.value-29000)/((30750-29000)/100))))
	#return(Erdfeuchtigkeit)
	
	if Erdfeuchtigkeit < 1:
		return (1.0)
	else:	
		return(Erdfeuchtigkeit)
    
def Erdfeuchtigkeit2():
	chan = AnalogIn(ads, ADS.P2)
	Erdfeuchtigkeit = (round(100-(chan.value-29040)/((30592-29040)/100),1))
	#Erdfeuchtigkeit = (round((100-(chan.value-29000)/((30750-29000)/100))))
	#return(Erdfeuchtigkeit)
	
	if Erdfeuchtigkeit < 1:
		return (1.0)
	else:	
		return(Erdfeuchtigkeit)


while True:
    try:
  
        # ~ print("hallo")
        # ~ print(type(Luftfeuchtigkeit()))
        # ~ print(type(Lufttemperatur()))
        # ~ print(type(Erdfeuchtigkeit()))
        # ~ print(type(aktuelleTemperatur()))
        
        
        print("Lufttemperatur:         ",Lufttemperatur(),"°C")
        print("Erdtemperatur:          ",  aktuelleTemperatur1(),"°C")
        print("Erdtemperatur2:         ",  aktuelleTemperatur2(),"°C")
        print("Luftfeuchtigkeit:	",Luftfeuchtigkeit()," %")  
        print("Erdfeuchtigkeit:        ", Erdfeuchtigkeit1(), " %")
        print("Erdfeuchtigkeit2:       ", Erdfeuchtigkeit2(), " %")
        
        # ~ if float(aktuelleTemperatur1()) < 10:
            # ~ Heizmatte.off()
            # ~ print("Heizmatte an")
        # ~ if float(aktuelleTemperatur1()) > 13:
            # ~ Heizmatte.on()
            # ~ print("Heizmatte aus")
        # ~ if float(Erdfeuchtigkeit1()) < 50:
            # ~ Bewaesserungspumpe1.off()
            # ~ print("Bewässerung Pumpe1")
            # ~ time.sleep(5.0)
            # ~ Bewaesserungspumpe1.on()
        # ~ if float(Erdfeuchtigkeit2()) < 50:
            # ~ Bewaesserungspumpe2.off()
            # ~ print("Bewässerung Pumpe2")
            # ~ time.sleep(5.0)
            # ~ Bewaesserungspumpe2.on()
        # ~ if float(Lufttemperatur()) > 15:
            # ~ Luefter.on()
        # ~ if float(Lufttemperatur()) > 12:
            # ~ Luefter.off()         
        # ~ if float(Erdfeuchtigkeit1()) > 60:
            # ~ Bewaesserungspumpe1.off()
        # ~ if float(Erdfeuchtigkeit2()) > 60:
            # ~ Bewaesserungspumpe2.off()
        # Read the sensor using the configured driver and gpio
        
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
        # Send the JSON data to InfluxDB
        client.write_points(data)
        # Wait until it's time to query again...
        time.sleep(interval)
		
             
                  
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(5.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
        
        

    time.sleep(3.0)

