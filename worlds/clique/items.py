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

filler_items: list[str] = [
    "Feeling of Acceptance",
    "Feeling of Anticipation",
    "Feeling of Apprehension",
    "Feeling of Awe",
    "Feeling of Bewilderment",
    "Feeling of Confusion",
    "Feeling of Contemplation",
    "Feeling of Curiosity",
    "Feeling of Disbelief",
    "Feeling of Empathy",
    "Feeling of Exasperation",
    "Feeling of Feeling",
    "Feeling of Forgiveness",
    "Feeling of Humiliation",
    "Feeling of Humility",
    "Feeling of Indifference",
    "Feeling of Innocence",
    "Feeling of Nostalgia",
    "Feeling of Phar",
    "Feeling of Pride",
    "Feeling of Sarcasm",
    "Feeling of Surprise",
    "Feeling of Sympathy",
    "Feeling of Trust",
    "Feeling of Wistfulness",
    "Feeling of Yearning",
]

# fmt: off
item_data: dict[str, CliqueItemData] = {
    "Feeling of Satisfaction":       CliqueItemData(BASE_ID + 0, ItemClassification.useful),
    "Clique Lore":                   CliqueItemData(BASE_ID + 1, ItemClassification.useful),
    "Feeling of Dissatisfaction":    CliqueItemData(BASE_ID + 2, ItemClassification.trap),
    "Extra Button":                  CliqueItemData(BASE_ID + 3, ItemClassification.progression),
    "Extra Two Buttons":             CliqueItemData(BASE_ID + 4, ItemClassification.progression),

    # Joke filler items that don't really do anything.
    **{item: CliqueItemData(BASE_ID + 100 + i, ItemClassification.filler) for i, item in enumerate(filler_items)},
}

item_groups: dict[str, list[str]] = {
    "Buttons": ["Extra Button", "Extra Two Buttons"]
}

item_table = {name: data.code for name, data in item_data.items() if data.code}
