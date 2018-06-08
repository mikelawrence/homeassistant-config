# Home Assistant Configuration
Here's my [Home Assistant](https://home-assistant.io/) configuration. I am using the easy to install [Hass.io](https://www.home-assistant.io/hassio/) running on a [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/).

## Some of the devices and services that I use with HA
* [ISY-994i](https://www.universal-devices.com/residential/isy994i-series/) for Insteon control.
* Lots of SmartHome [Insteon](https://www.smarthome.com/insteon.html) devices
* Custom MQTT devices
  * WiFi Gate Controller for controlling my [US Automatic](https://www.usautomatic.com/) gate opener.
    * KiCAD board design and software is available on [GitHub](https://github.com/mikelawrence/WiFi-Gate-Controller).
  * WiFi Septic Controller for controlling and monitoring my Aerobic Septic System.
    * KiCAD board design and software is available on [GitHub](https://github.com/mikelawrence/WiFi-Septic-Controller).
  * Raspberry Pi RGBW LED Controller HAT for controlling a high power RGB LED Floodlight.
    * KiCAD board design and software is available on [GitHub](https://github.com/mikelawrence/RPi-HAT-RGBW-LED-Controller).
* Presence detection.
  * [Unifi Controller](https://home-assistant.io/components/device_tracker.unifi/) for network device tracking.
  * [iOS app](https://itunes.apple.com/us/app/home-assistant-companion/id1099568401?mt=8) for location tracking and notifications.
* Climate
  * Three [Nest](https://www.home-assistant.io/components/nest/) thermostats.
  * [Davis Vantage Pro2](https://www.davisnet.com/solution/vantage-pro2/) connected to [weeWX](http://www.weewx.com/) which publishes to [Wunderground](https://www.wunderground.com/weather/us/tx/elgin/KTXELGIN7) and local MQTT server so HA can pick up current conditions.
* Cameras
  * Multiple [Unifi Video Cameras](https://www.home-assistant.io/components/camera.uvc/).
