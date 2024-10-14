from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld

from .items import item_name_to_id
from .locations import location_name_to_id, location_name_groups
from .options import RogueLegacyOptions, rl_option_groups


class RogueLegacyWebWorld(WebWorld):
    theme = "ocean"
    bug_report_page = "https://github.com/ThePhar/RogueLegacyRandomizerRedux/issues"
    rich_text_options_doc = True
    option_groups = rl_option_groups
    tutorials = [
        Tutorial(
            "Multiworld Setup Tutorial",
            "A guide to installing and setting up the Rogue Legacy Randomizer on your computer and connecting to a "
            "multiworld session.",
            "English",
            "rogue_legacy_en.md",
            "rogue_legacy/en",
            ["Phar"],
        )
    ]


class RogueLegacyWorld(World):
    """Rogue Legacy is a genealogical rogue-"lite", where anyone can be a hero. Each time you die, your child will
    succeed you. Every child is unique. One child might be colorblind, another might have vertigo-- they could even be a
    dwarf. But that's OK, because no one is perfect, and you don't have to be to succeed.
    """

    game = "Rogue Legacy"
    required_client_version = (0, 5, 1)
    location_name_to_id = location_name_to_id
    item_name_to_id = item_name_to_id
    web = RogueLegacyWebWorld()

    location_name_groups = location_name_groups

    options_dataclass = RogueLegacyOptions
    options: RogueLegacyOptions
