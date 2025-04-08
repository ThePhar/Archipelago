from dataclasses import dataclass

from BaseClasses import Item, ItemClassification
from .data import BASE_ID
from .locations import CliqueRegion


class CliqueItem(Item):
    game = "Clique"
    unlocking_region: CliqueRegion | None = None


@dataclass
class CliqueItemData:
    code: int | None
    classification: ItemClassification
    __counter = 0

    def __init__(self, classification: ItemClassification):
        self.code = BASE_ID + self.__counter
        self.classification = classification
        self.__counter += 1


# fmt: off
item_data: dict[str, CliqueItemData] = {
    "Feeling of Satisfaction":       CliqueItemData(ItemClassification.progression),
    "Feeling of Dissatisfaction":    CliqueItemData(ItemClassification.trap),
    "Clique Lore":                   CliqueItemData(ItemClassification.filler),
    "Extra Button":                  CliqueItemData(ItemClassification.progression),
    "Extra Two Buttons":             CliqueItemData(ItemClassification.progression),
    "Nothing":                       CliqueItemData(ItemClassification.filler),
}

item_table = {name: data.code for name, data in item_data.items() if data.code}
