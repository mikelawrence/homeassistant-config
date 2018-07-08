"""
Support for Haiku with SenseME ceiling fan and lights.

For more details about this platform, please refer to the documentation
?????
"""
import logging
import voluptuous as vol
from datetime import timedelta

from homeassistant.const import (CONF_INCLUDE, CONF_EXCLUDE)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.event import track_time_interval
from homeassistant.util import Throttle

# SenseMe Python library by Tom Faulkner
REQUIREMENTS = ['SenseMe==0.1.2']

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

DOMAIN = 'senseme'

DATA_HUBS = 'fans'

CONF_MAX_NUMBER_FANS = 'max_number_fans'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_MAX_NUMBER_FANS, default=5):
                     vol.All(vol.Coerce(int), vol.Range(min=1, max=25)),
        vol.Optional(CONF_INCLUDE, default=[]):
                     vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_EXCLUDE, default=[]):
                     vol.All(cv.ensure_list, [cv.string]),
    })
}, extra=vol.ALLOW_EXTRA)

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Set up the Haiku SenseME platform."""
    from senseme import discover
    from senseme import SenseMe
    # discover Haiku with SenseME fans
    devices = discover(config[DOMAIN][CONF_MAX_NUMBER_FANS], 8)
    hubs = []
    include_list = config[DOMAIN].get(CONF_INCLUDE)
    exclude_list = config[DOMAIN].get(CONF_EXCLUDE)
    if len(include_list) > 0:
        # add only included fans
        for device in devices:
            if device.name in include_list:
                hubs.append(SenseMeDevice(device))
                _LOGGER.debug("Added included fan '%s'." % device.name)
        # make sure all included fans exist
        for hub in hubs:
            if hub.name not in include_list:
                _LOGGER.warning("Included fan '%s' not found." % hub.name)
    else:
        # add only not excluded fans
        for device in devices:
            # add only if NOT excluded
            if device.name not in exclude_list:
                hubs.append(SenseMeHub(device))
                _LOGGER.debug("Added discovered fan '%s'." % device.name)

    # SenseME fan and light platforms use hub to communicate with the fan
    hass.data[DATA_HUBS] = hubs

    # Add fan and light platform
    load_platform(hass, 'fan', DOMAIN)
    load_platform(hass, 'light', DOMAIN)

    return True


def conv_bright_ha_to_lib(brightness) -> int:
    """Convert HA brightness scale 0-255 to library scale 0-16."""
    if brightness == 255:   # this will end up as 16 which is max
        brightness = 256
    return int(brightness / 16)


def conv_bright_lib_to_ha(brightness) -> int:
    """Convert library brightness scale 0-16 to HA scale 0-255."""
    brightness = int(brightness) * 16
    if brightness > 255:    # force big numbers into 8-bit int range
        brightness = 255
    return brightness


class SenseMeHub(object):
    """Data object and access to Haiku with SenseME fan."""

    def __init__(self, device):
        """Initialize the data object."""
        self._device = device
        self._fan_on = None
        self._fan_speed = None
        self._last_speed = None
        self._whoosh_on = None
        self._light_on = None
        self._light_brightness = None
        # need to know if fan has a light early, before first update()
        if device._query('<%s;DEVICE;LIGHT;GET>' % device.name) == 'PRESENT':
            self._light_exists = True
        else:
            self._light_exists = False


    @property
    def name(self) -> str:
        """Gets name of fan."""
        return self._device.name

    @property
    def ip(self) -> str:
        """Gets IP address of fan."""
        return self._device.ip


    @property
    def fan_on(self) -> bool:
        """Gets fan on state."""
        return self._fan_on


    @fan_on.setter
    def fan_on(self, fan_on):
        """Sets fan on state."""
        if not fan_on:      # used to continue fan speed when turning back on
            if self._fan_speed != '0':  # don't save fan speed that is off
                self._last_speed = self._fan_speed
        self._device.fan_powered_on = fan_on
        self._fan_on = fan_on
        # changing fan on state also affects fan speed and whoosh state
        if not fan_on:
            self._fan_speed = '0'
            self._whoosh_on = False


    @property
    def fan_speed(self) -> str:
        """Gets fan speed."""
        return self._fan_speed


    @fan_speed.setter
    def fan_speed(self, fan_speed):
        """Sets fan speed."""
        if fan_speed == None:
            if self._last_speed:    # use last speed
                fan_speed = self._last_speed
            else:                   # use default speed
                fan_speed = '4'
        self._device.speed = int(fan_speed)
        self._fan_speed = fan_speed
        # changing fan speed also affects fan on and whoosh states
        if fan_speed == '0':
            self._fan_on = False
            self._whoosh_on = False
        else:
            self._fan_on = True


    @property
    def whoosh_on(self) -> bool:
        """Gets whoosh on state."""
        return self._whoosh_on


    @whoosh_on.setter
    def whoosh_on(self, whoosh_on):
        """Sets whoosh on state."""
        self._device.whoosh = whoosh_on
        self._whoosh_on = whoosh_on


    @property
    def light_exists(self) -> bool:
        """Gets light exists state."""
        return self._light_exists


    @property
    def light_on(self) -> bool:
        """Gets current light state."""
        return self._light_on


    @light_on.setter
    def light_on(self, light_on):
        """Sets light state."""
        self._device.light_powered_on = light_on
        self._light_on = light_on
        # changing light on state also affects light brightness
        if not light_on:
            self._light_brightness = 0


    @property
    def light_brightness(self) -> int:
        """Gets light brightness."""
        return self._light_brightness


    @light_brightness.setter
    def light_brightness(self, light_brightness):
        """Sets light brightness."""
        self._device.brightness = conv_bright_ha_to_lib(light_brightness)
        self._light_brightness = light_brightness
        # changing brightness also affects light on state
        if light_brightness == 0:
            self.light_on = False
        else:
            self.light_on = True


    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self) -> None:
        """Get the latest status from fan."""
        data = self._device._get_all()
        if data['FAN;PWR']:
            self._fan_on = data['FAN;PWR']
        if data['FAN;SPD;ACTUAL']:
            self._fan_speed = data['FAN;SPD;ACTUAL']
        if data['FAN;WHOOSH;STATUS']:
            self._whoosh_on = data['FAN;WHOOSH;STATUS'] == 'ON'
        if data['LIGHT;PWR']:
            self._light_on = data['LIGHT;PWR'] == 'ON'
        if data['LIGHT;LEVEL;ACTUAL']:
            self._light_brightness = conv_bright_lib_to_ha(
                data['LIGHT;LEVEL;ACTUAL'])
        _LOGGER.debug("SenseMe: Updated fan '%s'." % self._device.name)
        return True
