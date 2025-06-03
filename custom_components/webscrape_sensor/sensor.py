import logging
import aiohttp
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    data = entry.data
    update_interval = timedelta(minutes=data.get("update_interval", 5))

    coordinator = WebScrapeCoordinator(
        hass,
        name=data["name"],
        url=data["url"],
        start_string=data["start_string"],
        end_string=data["end_string"],
        update_interval=update_interval,
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([WebScrapeSensor(coordinator, data.get("unit_of_measurement", ""))], True)

class WebScrapeCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, name, url, start_string, end_string, update_interval):
        super().__init__(
            hass,
            _LOGGER,
            name=f"{name} Coordinator",
            update_interval=update_interval,
        )
        self.url = url
        self.start_string = start_string
        self.end_string = end_string

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    text = await response.text()
                    start_idx = text.find(self.start_string)
                    if start_idx == -1:
                        raise UpdateFailed(f"Start string '{self.start_string}' not found")
                    end_idx = text.find(self.end_string, start_idx + len(self.start_string))
                    if end_idx == -1:
                        raise UpdateFailed(f"End string '{self.end_string}' not found")

                    value = text[start_idx + len(self.start_string):end_idx].strip()
                    return float(value.replace(",", "."))
        except Exception as e:
            raise UpdateFailed(f"Error fetching data: {e}")

class WebScrapeSensor(SensorEntity):
    def __init__(self, coordinator: WebScrapeCoordinator, unit_of_measurement: str):
        self.coordinator = coordinator
        self._unit = unit_of_measurement
        self._attr_name = coordinator.name.replace(" Coordinator", "")
        self._attr_unique_id = f"webscrape_sensor_{self._attr_name.lower().replace(' ', '_')}"

    @property
    def state(self):
        return self.coordinator.data

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        return self._attr_unique_id

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))
