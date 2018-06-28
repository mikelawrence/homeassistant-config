"""
Support for Haiku with SenseME ceiling fan.

For more details about this platform, please refer to the documentation
?????
"""
import logging
import socket

from homeassistant.components.light import (Light, ATTR_BRIGHTNESS,
                                            SUPPORT_BRIGHTNESS)

from custom_components.senseme import (DATA_HUBS)

_LOGGER = logging.getLogger(__name__)

SENSEME_LIGHT_BRIGHTNESS = 'LIGHT;LEVEL;ACTUAL'
SENSEME_LIGHT_POWER  = 'LIGHT;PWR'
SENSEME_LIGHT_PRESENT = 'DEVICE;LIGHT'



def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the Haiku with SenseME ceiling fan light platform."""
    lights = []
    for hub in hass.data[DATA_HUBS]:
        # add the light only if one is installed in the fan
        if hub._query('<%s;DEVICE;LIGHT;GET>' % hub.name) == 'PRESENT':
            lights.append(HaikuSenseMeLight(hass, hub))
    add_devices_callback(lights)


class HaikuSenseMeLight(Light):
    """Representation of a Haiku with SenseME ceiling fan light."""
    def __init__(self, hass, hub):
        """Initialize the entity."""
        self.hass = hass
        self._hub = hub
        self._name = hub.name + " Light"
        self._last_brightness = None
        self._supported_features = SUPPORT_BRIGHTNESS
        _LOGGER.debug("%s: Created HaikuSenseMeLight" % self.name)


    @property
    def name(self):
        """Get light name."""
        return self._name


    @property
    def should_poll(self) -> bool:
        """Polling needed for this light."""
        return True


    @property
    def brightness(self) -> str:
        """Return the brightness of the light."""
        try:
            fan_brightness = int(self._hub.get_attribute(SENSEME_LIGHT_BRIGHTNESS))
            brightness = fan_brightness * 16
        except KeyError:
            brightness = None
        return str(brightness)


    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        try:
            state = self._hub.get_attribute(SENSEME_LIGHT_POWER) == 'ON'
        except KeyError:
            state = None
        return state


    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._supported_features


    def turn_on(self, **kwargs) -> None:
        """Turn on the light."""
        brightness = kwargs.get(ATTR_BRIGHTNESS)
        if brightness == None:
            # brightness undefined, use last brightness if available
            if self._last_brightness:
                brightness = self._last_brightness
            else:
                brightness = 16
        else:
            brightness = int(brightness / 16)
        retryCount = 2
        while retryCount != 0:
            try:
                self._hub.brightness = brightness
                break
            except socket.error as e:
                retryCount -= 1
                if retryCount == 0:
                    raise
        _LOGGER.debug("%s: Turn light on. Brightness: %d" %
            (self._name, brightness))


    def turn_off(self, **kwargs) -> None:
        """Turn off the light."""
        # use to default brightness when turning on again
        self._last_brightness = self.brightness
        retryCount = 2
        while retryCount != 0:
            try:
                self._hub.light_powered_on = False
                break
            except socket.error as e:
                retryCount -= 1
                if retryCount == 0:
                    raise
        _LOGGER.debug("%s: Turn light off." % self._name)
