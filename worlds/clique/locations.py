from BaseClasses import Location, Region

from .data import BASE_ID
from .options import ExtraButtons


class CliqueLocation(Location):
    game = "Clique"


class CliqueRegion(Region):
    button_requirement: int = 0


location_table: dict[str, int] = {
    "The Button": BASE_ID,
    "The Tempter's Gift": BASE_ID + 1,
    **{f"Extra Button {i}": (BASE_ID + 100) + i for i in range(1, ExtraButtons.range_end)},
}

location_groups: dict[str, list[str]] = {
    "Freebie": ["The Tempter's Gift"],
    "Final Button": ["The Button", "The Final Button"],
    "Extra Buttons": [f"Extra Button {i}" for i in range(1, ExtraButtons.range_end)],
}
