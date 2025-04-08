from typing import NamedTuple

from BaseClasses import Item, ItemClassification
from .data import BASE_ID
from .locations import CliqueRegion


class CliqueItem(Item):
    game = "Clique"
    unlocking_region: CliqueRegion | None = None


class CliqueItemData(NamedTuple):
    code: int
    classification: ItemClassification


# fmt: off
item_data: dict[str, CliqueItemData] = {
    "Feeling of Satisfaction":       CliqueItemData(BASE_ID + 0, ItemClassification.progression),
    "Feeling of Dissatisfaction":    CliqueItemData(BASE_ID + 1, ItemClassification.trap),
    "Clique Lore":                   CliqueItemData(BASE_ID + 2, ItemClassification.filler),
    "Extra Button":                  CliqueItemData(BASE_ID + 3, ItemClassification.progression),
    "Extra Two Buttons":             CliqueItemData(BASE_ID + 4, ItemClassification.progression),
    "Nothing":                       CliqueItemData(BASE_ID + 5, ItemClassification.filler),
}

item_table = {name: data.code for name, data in item_data.items() if data.code}
