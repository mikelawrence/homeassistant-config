"""
Support for Haiku with SenseME ceiling fan.

For more details about this platform, please refer to the documentation
?????
"""
import logging
import socket

from homeassistant.components.fan import (FanEntity, DOMAIN, SPEED_OFF,
                                          SUPPORT_SET_SPEED, SUPPORT_OSCILLATE)
from custom_components.senseme import (DATA_HUBS)

_LOGGER = logging.getLogger(__name__)



# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the Haiku with SenseME ceiling fan platform."""
    fans = []
    for hub in hass.data[DATA_HUBS]:
        fans.append(HaikuSenseMeFan(hass, hub))
    add_devices_callback(fans)


class HaikuSenseMeFan(FanEntity):
    """Representation of a Haiku with SenseME ceiling fan."""
    def __init__(self, hass, hub) -> None:
        """Initialize the entity."""
        self.hass = hass
        self._hub = hub
        self._name = hub.name
        self._supported_features = SUPPORT_SET_SPEED | SUPPORT_OSCILLATE
        _LOGGER.debug("%s: Created HaikuSenseMeFan" % self.name)


    @property
    def name(self) -> str:
        """Get fan name."""
        return self._name


    @property
    def should_poll(self) -> bool:
        """Polling is needed for this fan."""
        return True


    @property
    def speed(self) -> str:
        return self._hub.fan_speed


    @property
    def speed_list(self) -> list:
        """Get the list of available speeds."""
        return ['0', '1', '2', '3', '4', '5', '6', '7']


    @property
    def is_on(self) -> bool:
        """Return true if the fan is on."""
        return self._hub.fan_on


    @property
    def oscillating(self):
        """Return the oscillation state."""
        return self._hub.whoosh_on


    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._supported_features


    def turn_on(self, speed: str = None, **kwargs) -> None:
        """Turn on the fan."""
        retryCount = 2
        while retryCount != 0:
            try:
                self._hub.fan_speed = speed
                break
            except socket.error as e:
                retryCount -= 1
                if retryCount == 0:
                    raise
        _LOGGER.debug("%s: Turn fan on, speed: %s" % (self._name, speed))


    def turn_off(self, **kwargs) -> None:
        """Turn off the fan."""
        retryCount = 2
        while retryCount != 0:
            try:
                self._hub.fan_on = False
                break
            except socket.error as e:
                retryCount -= 1
                if retryCount == 0:
                    raise
        _LOGGER.debug("%s: Turn fan off" % self._name)


    def set_speed(self, speed: str) -> None:
        """Set the speed of the fan."""
        retryCount = 2
        while retryCount != 0:
            try:
                self._hub.fan_speed = speed
                break
            except socket.error as e:
                retryCount -= 1
                if retryCount == 0:
                    raise
        _LOGGER.debug("%s: Set fan speed: %s" % (self._name, speed))


    def oscillate(self, oscillating: bool) -> None:
        """Set oscillation."""
        retryCount = 2
        while retryCount != 0:
            try:
                self._hub.whoosh_on = oscillating
                break
            except socket.error as e:
                retryCount -= 1
                if retryCount == 0:
                    raise
        _LOGGER.debug("%s: Turn Whoosh On:%s" % (self._name, oscillating))


    def update(self) -> None:
        """Update current fan values."""
        self._hub.update()
