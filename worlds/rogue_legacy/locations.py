from dataclasses import dataclass
from typing import NamedTuple

from BaseClasses import Location


MAX_BROWN_CHESTS = 50
MAX_SILVER_CHESTS = 20
MAX_GOLD_CHESTS = 5
MAX_FAIRY_CHESTS = 15


class RogueLegacyLocation(Location):
    game = "Rogue Legacy"


class LocationData(NamedTuple):
    name: str
    event: bool = False


# fmt: off
@dataclass
class RogueLegacyLocations:
    # Manor - Main
    manor_ground_road =        LocationData("Manor - Ground Road")
    manor_main_base =          LocationData("Manor - Main Building")
    manor_main_window_bottom = LocationData("Manor - Main Bottom Window")
    manor_main_window_top =    LocationData("Manor - Main Top Window")
    manor_main_rooftop =       LocationData("Manor - Main Rooftop")
    manor_left_tree1 =         LocationData("Manor - Outdoors Left Tree 1")
    manor_left_tree2 =         LocationData("Manor - Outdoors Left Tree 2")
    manor_right_tree =         LocationData("Manor - Outdoors Right Tree")

    # Manor - Left
    manor_left_base =          LocationData("Manor - Left Wing Building")
    manor_left_window =        LocationData("Manor - Left Wing Window")
    manor_left_rooftop =       LocationData("Manor - Left Wing Rooftop")
    manor_left_big_base =      LocationData("Manor - Rear Left Wing First Floor")
    manor_left_big_upper1 =    LocationData("Manor - Rear Left Wing Second Floor")
    manor_left_big_upper2 =    LocationData("Manor - Rear Left Wing Third Floor")
    manor_left_big_window =    LocationData("Manor - Rear Left Wing Windows")
    manor_left_big_rooftop =   LocationData("Manor - Rear Left Wing Rooftop")
    manor_left_far_base =      LocationData("Manor - Far Left Wing Building")
    manor_left_far_rooftop =   LocationData("Manor - Far Left Wing Rooftop")
    manor_left_extension =     LocationData("Manor - Far Left Wing Extension")

    # Manor - Right
    manor_right_base =         LocationData("Manor - Right Wing Building")
    manor_right_window =       LocationData("Manor - Right Wing Window")
    manor_right_rooftop =      LocationData("Manor - Right Wing Rooftop")
    manor_right_extension =    LocationData("Manor - Right Wing Extension")
    manor_right_big_base =     LocationData("Manor - Far Right Wing First Floor")
    manor_right_big_upper =    LocationData("Manor - Far Right Wing Second Floor")
    manor_right_big_rooftop =  LocationData("Manor - Far Right Wing Rooftop")
    manor_right_tower_base =   LocationData("Manor - Right Tower Base Level")
    manor_right_tower_middle = LocationData("Manor - Right Tower Middle Level")
    manor_right_tower_top =    LocationData("Manor - Right Tower Top Level")
    manor_observatory_base =   LocationData("Manor - Observatory Building")
    manor_observatory_scope =  LocationData("Manor - Observatory Telescope")

    # One-offs
    melophobia =               LocationData("Melophobia")    # Jukebox
    coulrophilia =             LocationData("Coulrophilia")  # Carnival
    zoophobia =                LocationData("Zoophobia")     # Defeat All Mini-bosses

    # Diaries
    diaries =                  [LocationData(f"Diary Entry #{i + 1}") for i in range(25)]

    # Chests
    castle_chests_brown =      [LocationData(f"Castle Hamson Brown Chest #{i + 1}")  for i in range(MAX_BROWN_CHESTS)]
    castle_chests_silver =     [LocationData(f"Castle Hamson Silver Chest #{i + 1}") for i in range(MAX_SILVER_CHESTS)]
    castle_chests_gold =       [LocationData(f"Castle Hamson Gold Chest #{i + 1}")   for i in range(MAX_GOLD_CHESTS)]
    castle_chests_fairy =      [LocationData(f"Castle Hamson Fairy Chest #{i + 1}")  for i in range(MAX_FAIRY_CHESTS)]
    castle_chest_boss =        LocationData("Castle Hamson Boss Chest")
    castle_chest_boss_neo =    LocationData("Castle Hamson Neo Boss Chest")

    forest_chests_brown =      [LocationData(f"Forest Abkhazia Brown Chest #{i + 1}")  for i in range(MAX_BROWN_CHESTS)]
    forest_chests_silver =     [LocationData(f"Forest Abkhazia Silver Chest #{i + 1}") for i in range(MAX_SILVER_CHESTS)]
    forest_chests_gold =       [LocationData(f"Forest Abkhazia Gold Chest #{i + 1}")   for i in range(MAX_GOLD_CHESTS)]
    forest_chests_fairy =      [LocationData(f"Forest Abkhazia Fairy Chest #{i + 1}")  for i in range(MAX_FAIRY_CHESTS)]
    forest_chest_boss =        LocationData("Forest Abkhazia Boss Chest")
    forest_chest_boss_neo =    LocationData("Forest Abkhazia Neo Boss Chest")

    tower_chests_brown =       [LocationData(f"The Maya Brown Chest #{i + 1}")  for i in range(MAX_BROWN_CHESTS)]
    tower_chests_silver =      [LocationData(f"The Maya Silver Chest #{i + 1}") for i in range(MAX_SILVER_CHESTS)]
    tower_chests_gold =        [LocationData(f"The Maya Gold Chest #{i + 1}")   for i in range(MAX_GOLD_CHESTS)]
    tower_chests_fairy =       [LocationData(f"The Maya Fairy Chest #{i + 1}")  for i in range(MAX_FAIRY_CHESTS)]
    tower_chest_boss =         LocationData("The Maya Boss Chest")
    tower_chest_boss_neo =     LocationData("The Maya Neo Boss Chest")

    dungeon_chests_brown =     [LocationData(f"Land of Darkness Brown Chest #{i + 1}")  for i in range(MAX_BROWN_CHESTS)]
    dungeon_chests_silver =    [LocationData(f"Land of Darkness Silver Chest #{i + 1}") for i in range(MAX_SILVER_CHESTS)]
    dungeon_chests_gold =      [LocationData(f"Land of Darkness Gold Chest #{i + 1}")   for i in range(MAX_GOLD_CHESTS)]
    dungeon_chests_fairy =     [LocationData(f"Land of Darkness Fairy Chest #{i + 1}")  for i in range(MAX_FAIRY_CHESTS)]
    dungeon_chest_boss =       LocationData("Land of Darkness Boss Chest")
    dungeon_chest_boss_neo =   LocationData("Land of Darkness Neo Boss Chest")
