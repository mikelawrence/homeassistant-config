"""
Support for Haiku with SenseME ceiling fan and lights.

For more details about this platform, please refer to the documentation
?????
"""
import asyncio

import logging
import voluptuous as vol

from homeassistant.const import (CONF_INCLUDE, CONF_EXCLUDE)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import load_platform

# SenseMe Python library by Tom Faulkner
REQUIREMENTS = ['SenseMe==0.1.1']

# delay between status updates (in seconds)
UPDATE_DELAY = 30.0

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



@asyncio.coroutine
def async_setup(hass, config):
    """Set up the Haiku SenseME platform."""
    from senseme import discover
    from senseme import SenseMe
    # discover Haiku with SenseME fans
    devices = discover(config[DOMAIN][CONF_MAX_NUMBER_FANS], 8)
    hubs = []
    include_list = config[DOMAIN].get(CONF_INCLUDE)
    exclude_list = config[DOMAIN].get(CONF_EXCLUDE)
    if len(include_list) > 0:
        # add only included
        for device in devices:
            if device.name in include_list:
                hubs.append(SenseMe(ip=device.ip, name=device.name,
                                    monitor_frequency=UPDATE_DELAY,
                                    monitor=True))
                # _LOGGER.debug("SenseMe: Added included fan '%s'." %
                #                 device.name)
    else:
        # add only included and not excluded fans unless all
        for device in devices:
            # add only if NOT excluded
            if device.name not in exclude_list:
                hubs.append(SenseMe(ip=device.ip, name=device.name,
                                    monitor_frequency=UPDATE_DELAY,
                                    monitor=True))
                # _LOGGER.debug("SenseMe: Added discovered fan '%s'." %
                #                 repr(device.name))

    # make sure included fans exist
    if len(include_list) > 0:
        for hub in hubs:
            if hub.name not in include_list:
                _LOGGER.warning("SenseMe: Included fan '%s' not found." %
                                hub.name)

    # start the first update of all parameters
    for hub in hubs:
        # this will take upwards of 10 seconds
        hub._get_all()

    # SenseME fan and light platforms use hub to communicate with the fan
    hass.data[DATA_HUBS] = hubs

    # Add fan and light platform
    load_platform(hass, 'fan', DOMAIN)
    load_platform(hass, 'light', DOMAIN)

    return True
