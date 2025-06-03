import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class WebScrapeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Hier kannst du evtl. Validierung der URL machen
            return self.async_create_entry(title=user_input["name"], data=user_input)

        data_schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("url"): str,
            vol.Required("start_string"): str,
            vol.Required("end_string"): str,
            vol.Optional("unit_of_measurement", default=""): str,
            vol.Optional("update_interval", default=5): int,  # Minuten
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
