Python script to add or remove public port mappings to Vodafone WiFi Hub

Selenium Webdriver is used to connect and login to the routers web admin panel. The base URL of the router and the admin password should be provided as arguments. 

See [raspberry-pi-chromium-webdriver](https://github.com/ekinsokmen/raspberry-pi-chromium-webdriver) for Raspberry Pi Chrome Driver docker image.


## Running using `raspberry-pi-chromium-webdriver` Docker Image
The script can be executed using Docker. Clone the code and run following command in the project directory:
```
docker run --rm -w /usr/workspace -v $(pwd):/usr/workspace raspberry-pi-chromium-webdriver python -u hub_addport.py -p *** --url http://192.168.0.1 add webmin 192.168.0.45 10000 10000
```

Run following command to get help on the arguments:
```
docker run --rm -w /usr/workspace -v $(pwd):/usr/workspace raspberry-pi-chromium-webdriver python hub_addport.py -h
```
