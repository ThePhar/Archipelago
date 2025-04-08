from BaseClasses import Location

from .data import BASE_ID
from .options import Buttonsanity


class CliqueLocation(Location):
    game = "Clique"


# fmt: off
location_table: dict[str, int] = {
    "The Button":              BASE_ID,
    "The Tempter's Gift":      BASE_ID + 1,
    **{f"Button {i} Pressed": (BASE_ID + 100) + i for i in range(Buttonsanity.range_end)},
}

location_groups: dict[str, list[str]] = {
    "Intermediate Buttons": [f"Button {i} Pressed" for i in range(Buttonsanity.range_end)],
}
