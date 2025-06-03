from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = config_entry.data
    sensor = WebScrapeSensor(
        name=data["name"],
        url=data["url"],
        start_string=data["start_string"],
        end_string=data["end_string"],
        unit=data.get("unit_of_measurement", "")
    )
    async_add_entities([sensor], True)

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
                        _LOGGER.warning("Start/End strings not found")
                        self._state = None
                        return
                    value = text[start_idx + len(self._start):end_idx].strip()
                    self._state = float(value.replace(",", "."))
        except Exception as e:
            _LOGGER.error("Error scraping data: %s", e)
            self._state = None
