# Home Assistant Configuration
Here's my [Home Assistant](https://home-assistant.io/) configuration. I am using the easy to install [Hass.io](https://www.home-assistant.io/hassio/) running on a [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/).

## Some of the devices and services that I use with HA
* [ISY-994i](https://www.home-assistant.io/components/isy994/) for Insteon control.
* Lots of SmartHome [Insteon](https://www.smarthome.com/insteon.html) devices controlled through ISY-994i.
* Presence detection.
  * [Unifi Controller](https://home-assistant.io/components/device_tracker.unifi/) for network device tracking.
  * [iOS app](https://itunes.apple.com/us/app/home-assistant-companion/id1099568401?mt=8) for location tracking and notifications.
* Climate
  * Three [Nest](https://www.home-assistant.io/components/nest/) thermostats.
  * [Davis Vantage Pro2](https://www.davisnet.com/solution/vantage-pro2/) connected to [weeWX](http://www.weewx.com/) which publishes to [Wunderground](https://www.wunderground.com/weather/us/tx/elgin/KTXELGIN7) and local MQTT server so HA can pick up current conditions.
* Cameras
  * Multiple [Unifi Video Cameras](https://www.home-assistant.io/components/camera.uvc/).
* Custom MQTT devices
  * WiFi Gate Controller for controlling my [US Automatic](https://www.usautomatic.com/) gate opener.
    * KiCAD board design and software is available on [GitHub](https://github.com/mikelawrence/WiFi-Gate-Controller).
  * WiFi Septic Controller for controlling and monitoring my Aerobic Septic System.
    * KiCAD board design and software is available on [GitHub](https://github.com/mikelawrence/WiFi-Septic-Controller).
  * Raspberry Pi RGBW LED Controller HAT for controlling a high power RGB LED Floodlight.
    * KiCAD board design and software is available on [GitHub](https://github.com/mikelawrence/RPi-HAT-RGBW-LED-Controller).
* Custom Haiku with SenseME fan component

## Custom Haiku with SenseME fan components
The Haiku with SenseME fan is a WiFi connected fan and installable light. This custom component uses TomFaulkner's [SenseMe](https://github.com/TomFaulkner/SenseMe) Python Library to communicate with the fan.

### Installation
There are three senseme.py files that must be installed in the config/custom_components directory. Note the location of the three senseme.py files in their respective folders (fan/ and light/) is important.

### Configuration
The Haiku with SenseME fan component will automatically discover and create a fan and light (if installed) for each discovered fan. Setting ```max_number_fans``` to the number of Haiku fans on your network will speed up the discovery process but is not required. If ```include:``` is specified, only those fans listed will be added. If the fans does not exist it will not be added. If ```exclude``` is specified, discovered fans with a matching name will not be added. If both ```include:``` and ```exclude``` are specified, only ```include:``` will by honored.
```yaml
# enable Haiku with SenseMe ceiling fans
senseme:
  max_number_fans: 2
  include:
    - "Studio Vault Fan"
    - "Studio Beam Fan"
  exclude:
    - "Studio Beam Fan"
```

### Problems
* TomFaulkner's SenseMe library has a bug that periodically causes exceptions when getting the status of common attributes like fan speed or light brightness.
* TomFaulkner's SenseMe library doesn't immediately update attributes when they are set by the same library. This means when you turn the fan on it may take upwards of 30 seconds before the correct status is shown in Home Assistant.
* I have modified TomFaulkner's library to work with HA and have opened [two issues](https://github.com/TomFaulkner/SenseMe/issues) and offered a pull request to see if TomFaulkner will pick them and update his library. Until this happens you can replace the senseme file installed in your configuration folder under deps/lib/python?.?/site-packages/senseme with this [senseme.py](https://github.com/mikelawrence/SenseMe/blob/master/senseme/senseme.py) file.
