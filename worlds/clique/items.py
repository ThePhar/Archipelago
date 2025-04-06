from typing import NamedTuple

from BaseClasses import Item, ItemClassification, Region
from .data import BASE_ID


class CliqueItem(Item):
    game = "Clique"
    unlock: Region | None = None


class CliqueItemData(NamedTuple):
    code: int | None
    type: ItemClassification = ItemClassification.filler


item_data: dict[str, CliqueItemData] = {
    "Feeling of Satisfaction": CliqueItemData(BASE_ID, ItemClassification.progression),
    "Feeling of Dissatisfaction": CliqueItemData(BASE_ID + 1, ItemClassification.trap),
    "Filler Item That Does Nothing": CliqueItemData(BASE_ID + 2),  # Used for random filler.
    "Button Activation": CliqueItemData(BASE_ID + 3, ItemClassification.progression),
    "Extra Button": CliqueItemData(BASE_ID + 4, ItemClassification.progression),
    "Extra Two Buttons": CliqueItemData(BASE_ID + 5, ItemClassification.progression),

    # Events
    "Cliqued": CliqueItemData(None, ItemClassification.progression)
}

item_table = {name: data.code for name, data in item_data.items() if data.code is not None}
