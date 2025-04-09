from math import ceil

from BaseClasses import Location, Region
from .data import BASE_ID
from .options import Buttonsanity, Dissatisfaction


class CliqueLocation(Location):
    game = "Clique"
    fake: bool = False


class CliqueRegion(Region):
    dual_region: bool = False


button_maximum = ceil(Buttonsanity.range_end * (Dissatisfaction.range_end / 100 + 1))

# fmt: off
location_table: dict[str, int] = {
    "The Button":                BASE_ID,
    "The Tempter's Gift":        BASE_ID + 1,
    **{f"Extra Button {i + 1}": (BASE_ID + 100) + i for i in range(button_maximum)},
}

location_groups: dict[str, list[str]] = {
    "Extra Buttons": [f"Extra Button {i + 1}" for i in range(button_maximum)],
}
