from BaseClasses import Location, Region

from .data import BASE_ID
from .options import Buttonsanity


class CliqueLocation(Location):
    game = "Clique"
    fake: bool = False


class CliqueRegion(Region):
    dual_region: bool = False


# fmt: off
location_table: dict[str, int] = {
    "The Button":                BASE_ID,
    "The Tempter's Gift":        BASE_ID + 1,
    **{f"Extra Button {i + 1}": (BASE_ID + 100) + i for i in range(Buttonsanity.range_end * 2)},
}

location_groups: dict[str, list[str]] = {
    "Extra Buttons": [f"Extra Button {i + 1}" for i in range(Buttonsanity.range_end * 2)],
}
