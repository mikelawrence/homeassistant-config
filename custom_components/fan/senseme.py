"""
Support for Haiku with SenseME ceiling fan.

For more details about this platform, please refer to the documentation
?????
"""
from datetime import timedelta
import logging

from homeassistant.components.fan import (FanEntity, DOMAIN, SPEED_OFF,
                                          SUPPORT_SET_SPEED, SUPPORT_OSCILLATE)

from custom_components.senseme import (DATA_HUBS)

_LOGGER = logging.getLogger(__name__)

SENSEME_FAN_SPEED  = 'FAN;SPD;ACTUAL'
SENSEME_FAN_POWER  = 'FAN;PWR'
SENSEME_FAN_WHOOSH = 'FAN;WHOOSH;STATUS'



# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the Haiku with SenseME ceiling fan platform."""
    hubs = []
    for hub in hass.data[DATA_HUBS]:
        hubs.append(HaikuSenseMeFan(hass, hub))
    add_devices_callback(hubs)


class HaikuSenseMeFan(FanEntity):
    """Representation of a Haiku with SenseME ceiling fan."""
    def __init__(self, hass, hub) -> None:
        """Initialize the entity."""
        self.hass = hass
        self._hub = hub
        self._name = hub.name
        self._supported_features = SUPPORT_SET_SPEED | SUPPORT_OSCILLATE
        # _LOGGER.warning("SenseME Fan: Added fan '%s'." % self._name)


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
        speed = str(self._hub.get_attribute(SENSEME_FAN_SPEED))
        # _LOGGER.warning("%s: Speed:%s" % (self._name, speed))
        return speed


    @property
    def speed_list(self) -> list:
        """Get the list of available speeds."""
        return ['0', '1', '2', '3', '4', '5', '6', '7']


    @property
    def is_on(self) -> bool:
        """Return true if the fan is on."""
        state = self._hub.get_attribute(SENSEME_FAN_POWER) == 'ON'
        # _LOGGER.warning("%s: Is on:%s" % (self._name, state))
        return state


    @property
    def oscillating(self):
        """Return the oscillation state."""
        state = self._hub.get_attribute(SENSEME_FAN_WHOOSH) == 'ON'
        # _LOGGER.warning("%s: Oscillating:%s" % (self._name, state))
        return state


    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._supported_features


    def turn_on(self, speed: str = None, **kwargs) -> None:
        """Turn on the fan."""
        self.set_speed(speed)
        # _LOGGER.debug("%s: Turn fan on, speed:%s" % (self._name, speed))


    def turn_off(self, **kwargs) -> None:
        """Turn off the fan."""
        self._hub.fan_powered_on = False
        # _LOGGER.debug("%s: Turn fan off" % self._name)


    def set_speed(self, speed: str) -> None:
        """Set the speed of the fan."""
        if speed == None:
            # do nothing for no speed selected
            return
        else:
            speed = int(speed)
        self._hub.speed = speed
        #_LOGGER.debug("%s: Set fan speed: %d" % (self._name, speed))


    def oscillate(self, oscillating: bool) -> None:
        """Set oscillation."""
        self._hub.whoosh = oscillating
