from dataclasses import dataclass
from enum import IntEnum
from typing import Literal

from BaseClasses import Location
from .utils import int_to_roman

MAX_BROWN_CHESTS = 300
MIN_BROWN_CHESTS = 100
MAX_SILVER_CHESTS = 75
MIN_SILVER_CHESTS = 25
MAX_GOLD_CHESTS = 50
MIN_GOLD_CHESTS = 10
MAX_FAIRY_CHESTS = 25
MIN_FAIRY_CHESTS = 0
MIN_DIARIES = 2
MAX_DIARIES = 75


class FairyChestCondition(IntEnum):
    none = 0
    kill_all_enemies = 1
    do_not_look = 2
    no_jumping = 3
    no_attacking = 5
    timelimit = 8
    no_damage = 9
    invisible = 10

    def __str__(self):
        if self.none:
            return "No Requirement"
        if self.kill_all_enemies:
            return "Kill All Enemies"
        if self.do_not_look:
            return "Do Not Look"
        if self.no_jumping:
            return "No Jumping"
        if self.no_attacking:
            return "No Attacking"
        if self.timelimit:
            return "Reach in Time"
        if self.no_damage:
            return "No Damage"
        if self.invisible:
            return "Invisible"


@dataclass
class LocationData:
    name: str
    event: bool = False
    id: int | None = None

    __index: int = 1

    def __post_init__(self):
        if self.id is None and not self.event:
            self.id = self.__index
            self.__index += 1


class RogueLegacyLocation(Location):
    game = "Rogue Legacy"
    access_requirements: set[Literal["DASH", "FLIGHT", "DOUBLE_JUMP"]] = []
    fairy_requirement: FairyChestCondition = None


# fmt: off
rl_locations_data: dict[str, LocationData | list[LocationData]] = {
    # Manor - Main
    "manor_ground_road":        LocationData("Manor - Ground Road"),
    "manor_main_base":          LocationData("Manor - Main Building"),
    "manor_main_window_bottom": LocationData("Manor - Main Bottom Window"),
    "manor_main_window_top":    LocationData("Manor - Main Top Window"),
    "manor_main_rooftop":       LocationData("Manor - Main Rooftop"),
    "manor_left_tree1":         LocationData("Manor - Outdoors Left Tree 1"),
    "manor_left_tree2":         LocationData("Manor - Outdoors Left Tree 2"),
    "manor_right_tree":         LocationData("Manor - Outdoors Right Tree"),

    # Manor - Left
    "manor_left_base":          LocationData("Manor - Left Wing Building"),
    "manor_left_window":        LocationData("Manor - Left Wing Window"),
    "manor_left_rooftop":       LocationData("Manor - Left Wing Rooftop"),
    "manor_left_big_base":      LocationData("Manor - Rear Left Wing First Floor"),
    "manor_left_big_upper1":    LocationData("Manor - Rear Left Wing Second Floor"),
    "manor_left_big_upper2":    LocationData("Manor - Rear Left Wing Third Floor"),
    "manor_left_big_window":    LocationData("Manor - Rear Left Wing Windows"),
    "manor_left_big_rooftop":   LocationData("Manor - Rear Left Wing Rooftop"),
    "manor_left_far_base":      LocationData("Manor - Far Left Wing Building"),
    "manor_left_far_rooftop":   LocationData("Manor - Far Left Wing Rooftop"),
    "manor_left_extension":     LocationData("Manor - Far Left Wing Extension"),

    # Manor - Right
    "manor_right_base":         LocationData("Manor - Right Wing Building"),
    "manor_right_window":       LocationData("Manor - Right Wing Window"),
    "manor_right_rooftop":      LocationData("Manor - Right Wing Rooftop"),
    "manor_right_extension":    LocationData("Manor - Right Wing Extension"),
    "manor_right_big_base":     LocationData("Manor - Far Right Wing First Floor"),
    "manor_right_big_upper":    LocationData("Manor - Far Right Wing Second Floor"),
    "manor_right_big_rooftop":  LocationData("Manor - Far Right Wing Rooftop"),
    "manor_right_tower_base":   LocationData("Manor - Right Tower Base Level"),
    "manor_right_tower_middle": LocationData("Manor - Right Tower Middle Level"),
    "manor_right_tower_top":    LocationData("Manor - Right Tower Top Level"),
    "manor_observatory_base":   LocationData("Manor - Observatory Building"),
    "manor_observatory_scope":  LocationData("Manor - Observatory Telescope"),

    # One-off Challenges
    "melophobia":               LocationData("Melophobia"),       # Interact with Jukebox
    "coulrophobia":             LocationData("Coulrophobia"),     # Beat a Carnival
    "zoophobia":                LocationData("Zoophobia"),        # Defeat all Mini-bosses
    "artphobia":                LocationData("Artphobia"),        # Read all Paintings
    "theophobia":               LocationData("Theophobia"),       # Interact with Shrine
    "eutychemaphobia":          LocationData("Eutychemaphobia"),  # Cheapskate Elf Reward

    # Diaries
    "diaries":                  [LocationData(f"Diary Entry #{i + 1}") for i in range(MAX_DIARIES)],

    # Chests
    "chests_brown":             [LocationData(f"Brown Chest {int_to_roman(i+1)}") for i in range(MAX_BROWN_CHESTS)],
    "chests_silver":            [LocationData(f"Silver Chest {int_to_roman(i+1)}") for i in range(MAX_SILVER_CHESTS)],
    "chests_gold":              [LocationData(f"Gold Chest {int_to_roman(i+1)}")   for i in range(MAX_GOLD_CHESTS)],
    "chests_fairy":             [LocationData(f"Fairy Chest {int_to_roman(i+1)}")  for i in range(MAX_FAIRY_CHESTS)],

    "castle_chest_boss":        LocationData("Castle Hamson Boss Chest"),
    "castle_chest_boss_neo":    LocationData("Castle Hamson Neo Boss Chest"),
    "forest_chest_boss":        LocationData("Forest Abkhazia Boss Chest"),
    "forest_chest_boss_neo":    LocationData("Forest Abkhazia Neo Boss Chest"),
    "tower_chest_boss":         LocationData("The Maya Boss Chest"),
    "tower_chest_boss_neo":     LocationData("The Maya Neo Boss Chest"),
    "dungeon_chest_boss":       LocationData("The Land of Darkness Boss Chest"),
    "dungeon_chest_boss_neo":   LocationData("The Land of Darkness Neo Boss Chest"),

    # Boss Events
    "evt_castle":               LocationData("Castle Hamson Boss Chamber",            event=True),
    "evt_forest":               LocationData("Forest Abkhazia Boss Chamber",          event=True),
    "evt_tower":                LocationData("The Maya Boss Chamber",                 event=True),
    "evt_dungeon":              LocationData("The Land of Darkness Boss Chamber",     event=True),
    "evt_castle_ex":            LocationData("Castle Hamson Neo Boss Chamber",        event=True),
    "evt_forest_ex":            LocationData("Forest Abkhazia Neo Boss Chamber",      event=True),
    "evt_tower_ex":             LocationData("The Maya Neo Boss Chamber",             event=True),
    "evt_dungeon_ex":           LocationData("The Land of Darkness Neo Boss Chamber", event=True),
    "evt_fountain":             LocationData("The Fountain Room",                     event=True),
    "evt_fountain_ex":          LocationData("The Brothers Boss Chamber",             event=True),
}

# fmt:on

location_name_to_id: dict[str, int] = {}
for value in rl_locations_data.values():
    if isinstance(value, list):
        for data in value:
            location_name_to_id[data.name] = data.id
    elif not value.event:
        location_name_to_id[value.name] = value.id

location_name_groups: dict[str, set[str]] = {
    "Manor": {data.name for key, data in rl_locations_data.items() if key.startswith("manor_")},
    "Brown Chests": {data.name for data in rl_locations_data["chests_brown"]},
    "Silver Chests": {data.name for data in rl_locations_data["chests_silver"]},
    "Gold Chests": {data.name for data in rl_locations_data["chests_gold"]},
    "Fairy Chests": {data.name for data in rl_locations_data["chests_fairy"]},
    "Diaries": {data.name for data in rl_locations_data["diaries"]},
}
