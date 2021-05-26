sudo apt-get update
sudo apt-get upgrade

#ADS115 installieren

sudo apt-get install build-essential python-dev python-smbus git
cd
git clone https://github.com/adafruit/Adafruit_Python_ADS1x15
cd Adafruit_Python_ADS1x15
sudo python3 setup.py install
cd
sudo pip3 install adafruit-circuitpython-ads1x15

#DHT22 mit pigpio 

pip3 install adafruit-circuitpython-dht RPi.GPIO
sudo apt-get install pigpio
sudo pigpiod

#influxdb

echo "deb https://repos.influxdata.com/ubuntu bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
sudo apt-get install influxdb -y
sudo systemctl start influxd
sudo systemctl enable influxd

#grafana (localhost:3000)

wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get install -y grafana
sudo /bin/systemctl enable grafana-server
sudo /bin/systemctl start grafana-server
