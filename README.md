# volkszaehler

volkszaehler.org   

https://wiki.volkszaehler.org/howto/datenmengen   
https://wiki.volkszaehler.org/howto/node-red   


## hardware

| # |  | link |
|---|---|---|
| energy meter     | Apator Lepus | http://www.apator.com/de/produkte/strommessung/stromzaehler/neuheiten/lepus |
| IR Lesekopf      | bitShake SmartMeterReader - UART | IR Lesekopf ||
| Raspberry PI 3B+ |  |  |
| case             | italtronic | https://www.pollin.de/p/italtronic-hutschienengehaeuse-10-0012225-rmb-fuer-raspberry-pi-b-460517?utm_source=google&utm_medium=fshopping&gclid=EAIaIQobChMIpofNxumE-wIVj613Ch0MdQGqEAQYAiABEgJhRPD_BwE |

## installation
https://wiki.volkszaehler.org/howto/raspberry_pi_image  

## configuration
https://wiki.volkszaehler.org/software/controller/vzlogger/vzlogger_conf_parameter
https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm

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

## crontab
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


