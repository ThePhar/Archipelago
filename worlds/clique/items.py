from dataclasses import dataclass

from BaseClasses import Item, ItemClassification, Region
from .data import BASE_ID


class CliqueItem(Item):
    game = "Clique"
    unlocking_region: Region | None = None


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
    "Filler Item That Does Nothing": CliqueItemData(ItemClassification.filler),
    "Extra Button":                  CliqueItemData(ItemClassification.progression),
    "Extra Two Buttons":             CliqueItemData(ItemClassification.progression),
}

item_table = {name: data.code for name, data in item_data.items() if data.code}
