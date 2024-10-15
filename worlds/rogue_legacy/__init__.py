from typing import Any

from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld

from .items import item_name_to_id
from .locations import location_name_to_id, location_name_groups
from .options import RogueLegacyOptions, rl_option_groups

WORLD_VERSION = 3  # If you're going to copy from this world, just know you probably don't need this line.


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
    location_name_groups = location_name_groups
    options_dataclass = RogueLegacyOptions
    options: RogueLegacyOptions
    web = RogueLegacyWebWorld()

    boss_order: list[str]

    def generate_early(self) -> None:
        # Compute boss order.
        self.boss_order = self.options.boss_shuffle.generate_boss_order(self)

    def fill_slot_data(self) -> dict[str, Any]:
        # In theory, I could use self.options.as_dict, but I want more control over the value types.
        slot_data: dict[str, Any] = {
            # fmt: off

            # Easy flag to check for updates.
            "world_version": WORLD_VERSION,

            # Game options relevant to client.
            "children": self.options.children.value,
            "level_limit": bool(self.options.level_limit.value),
            "shuffle_blacksmith": bool(self.options.shuffle_blacksmith.value),
            "shuffle_enchantress": bool(self.options.shuffle_enchantress.value),
            "chests_brown": self.options.chests_brown.value,
            "chests_silver": self.options.chests_silver.value,
            "chests_gold": self.options.chests_gold.value,
            "chests_fairy": self.options.chests_fairy.value,
            "diary_entries": self.options.diary_entries.value,
            "neo_bosses": self.options.neo_bosses.current_key,
            "additional_challenges": bool(self.options.additional_challenges.value),
            "enemy_scaling": self.options.enemy_scaling.value / 100.0,
            "castle_scaling": self.options.castle_scaling.value / 100.0,
            "ngplus_requirement": self.options.ngplus_requirement.value,
            "gold_gain": self.options.gold_gain.value / 100.0,
            "charon": bool(self.options.charon.value),
            "fountain_hunt": bool(self.options.fountain_hunt.value),
            "fountain_pieces_available": self.options.fountain_pieces_available.value,
            "fountain_pieces_required": self.options.fountain_pieces_required.value / 100.0,
            "character_names_sir": self.options.character_names_sir.value,
            "character_names_lady": self.options.character_names_lady.value,
            "max_health": self.options.max_health.value,
            "max_mana": self.options.max_mana.value,
            "max_attack": self.options.max_attack.value,
            "max_magic_damage": self.options.max_magic_damage.value,
            "death_link": self.options.death_link.current_key,

            # Computed data.
            "boss_order": self.boss_order,
        }

        # fmt: on
        return slot_data
