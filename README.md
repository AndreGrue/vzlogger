# volkszaehler
Configuration and settings of a Raspberry PI installation of a Volkszaehler.

volkszaehler.org   


## hardware

| Device           | Type                             | Link                                                                                                                                                                                                  |
|------------------|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| energy meter     | Apator Lepus                     | http://www.apator.com/de/produkte/strommessung/stromzaehler/neuheiten/lepus                                                                                                                           |
| IR Lesekopf      | bitShake SmartMeterReader - UART | IR Lesekopf                                                                                                                                                                                           ||
| Raspberry PI 3B+ |                                  |                                                                                                                                                                                                       |
| case             | italtronic                       | https://www.pollin.de/p/italtronic-hutschienengehaeuse-10-0012225-rmb-fuer-raspberry-pi-b-460517?utm_source=google&utm_medium=fshopping&gclid=EAIaIQobChMIpofNxumE-wIVj613Ch0MdQGqEAQYAiABEgJhRPD_BwE |

## installation
https://wiki.volkszaehler.org/howto/raspberry_pi_image  

## configuration
https://wiki.volkszaehler.org/software/controller/vzlogger/vzlogger_conf_parameter
http://volkszaehler.github.io/vzlogger/

[OBIS codes](https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm)


## services
relevant services:  
~~~
sudo systemctl status vzlogger.service
sudo systemctl status middleware.service
sudo systemctl status mariadb.service
sudo systemctl status apache2.service 
sudo systemctl status push-server.service 
~~~

### disable services
 - middleware.service
 - mariadb.service
 - apache2.service 
 - push-server.service 

~~~
sudo systemctl stop *
sudo systemctl disable *
~~~

## crontab - automatic daily reboot
~~~
sudo crontab -e
~~~

enter the following line 
~~~
00 3 * * * /sbin/shutdown -r now
~~~

## logrotate
Change log file path in /etc/logrotate/vzlogger to /var/log/vzlogger/vzlogger.log

## overlay file system
~~~
sudo raspi-config
~~~
goto -> Performance Options -> Enable Overlay File System



## Energy meter
Python scripts to simulate an energy meter (Carlo Gavazzi EM24 Ethernet).   
Type: EM24DINAV23XE1PFB    

[Manufacturer](https://gavazziautomation.com)   
[Modbus TCP Protocol description](https://www.enika.eu/data/files/produkty/energy%20m/CP/em24%20ethernet%20cp.pdf)


### configuration
Configuration:  [em24_config.csv](./push2modbus/data/em24_config.csv)


### setup python venv

copy folder push2modbus to /hom/pi/push2modbus.

create python virtual environment:   
~~~commandline
sudo apt-get install python3 python3-pip python3-venv
WORKDIR=/home/pi/push2modbus
VENV=.venv
cd ${WORKDIR}
python3 -m venv ${VENV}
source ${VENV}/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
~~~


### systemd service

copy service:    
~~~commandline
cp ./push2modbus.service /etc/systemd/system
~~~

enable and restart service:   
~~~commandline
sudo systemctl enable push2modbus.service
sudo systemctl restart push2modbus.service
~~~

check status of service:   
~~~commandline
sudo systemctl status push2modbus.service
~~~

