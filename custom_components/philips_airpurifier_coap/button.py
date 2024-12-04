from __future__ import annotations

from collections.abc import Callable
import logging

from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory

from .config_entry_data import ConfigEntryData
from .const import DOMAIN, FILTER_TYPES, FanAttributes
from .philips import PhilipsEntity, model_to_class

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[list[ButtonEntity], bool], None],
) -> None:
    """Set up the button platform for filters."""
    config_entry_data: ConfigEntryData = hass.data[DOMAIN][entry.entry_id]
    status = config_entry_data.latest_status
    model = config_entry_data.device_information.model

    model_class = model_to_class.get(model)
    if not model_class:
        _LOGGER.error("Unsupported model: %s", model)
        return

    unavailable_filters = []
    for cls in reversed(model_class.__mro__):
        cls_unavailable_filters = getattr(cls, "UNAVAILABLE_FILTERS", [])
        unavailable_filters.extend(cls_unavailable_filters)

    buttons = [
        PhilipsFilterResetButton(hass, entry, config_entry_data, _filter)
        for _filter in FILTER_TYPES
        if _filter in status and _filter not in unavailable_filters
    ]

    async_add_entities(buttons, update_before_add=False)


class PhilipsFilterResetButton(PhilipsEntity, ButtonEntity):
    """Define a Philips AirPurifier filter reset button."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: ConfigEntry,
        config_entry_data: ConfigEntryData,
        filter_type: str,
    ) -> None:
        """Initialize the filter reset button."""
        super().__init__(hass, config, config_entry_data)

        self._filter_type = filter_type
        self._description = FILTER_TYPES[filter_type]
        self._attr_name = (
            f"{config_entry_data.device_information.name} "
            f"{self._description[FanAttributes.LABEL].replace('_', ' ').title()} Reset"
        )
        self._attr_unique_id = (
            f"{config_entry_data.device_information.model}-"
            f"{config_entry_data.device_information.device_id}-{filter_type}-reset"
        )
        self._attr_device_class = ButtonDeviceClass.RESTART
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        """Handle the button press action to reset the filter."""
        try:
            total_value = self._device_status.get(self._description[FanAttributes.TOTAL])

            await self.coordinator.client.set_control_value(self._filter_type, total_value)
            self._handle_coordinator_update()

            _LOGGER.info("Filter %s successfully reset to %s", self._filter_type, total_value)
        except Exception as error:
            _LOGGER.error("Failed to reset filter %s: %s", self._filter_type, error)
