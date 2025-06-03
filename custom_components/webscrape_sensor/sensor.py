import logging
import aiohttp
import asyncio
import voluptuous as vol

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, CONF_UNIT_OF_MEASUREMENT
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import HomeAssistantType, ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

DOMAIN = "webscrape_sensor"

CONF_URL = "url"
CONF_START = "start_string"
CONF_END = "end_string"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_URL): cv.url,
    vol.Required(CONF_START): cv.string,
    vol.Required(CONF_END): cv.string,
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
})

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities: AddEntitiesCallback, discovery_info: DiscoveryInfoType = None):
    url = config[CONF_URL]
    start = config[CONF_START]
    end = config[CONF_END]
    name = config[CONF_NAME]
    unit = config.get(CONF_UNIT_OF_MEASUREMENT)

    async_add_entities([WebScrapeSensor(name, url, start, end, unit)], True)

class WebScrapeSensor(SensorEntity):
    def __init__(self, name, url, start_string, end_string, unit):
        self._name = name
        self._url = url
        self._start = start_string
        self._end = end_string
        self._unit = unit
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit

    async def async_update(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url) as response:
                    text = await response.text()

                    start_idx = text.find(self._start)
                    end_idx = text.find(self._end, start_idx + len(self._start))

                    if start_idx == -1 or end_idx == -1:
                        _LOGGER.warning("Start/End strings not found in response")
                        self._state = None
                        return

                    value_str = text[start_idx + len(self._start):end_idx].strip()
                    self._state = float(value_str.replace(',', '.'))

        except Exception as e:
            _LOGGER.error("Error updating web scrape sensor: %s", e)
            self._state = None
